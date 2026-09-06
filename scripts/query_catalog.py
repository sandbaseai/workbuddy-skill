#!/usr/bin/env python3
"""Search the provenance-only catalog without third-party dependencies."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

from catalog_signals import source_context


CHECKSUM_URL = "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/SHA256SUMS"
RELEASE_REPO = "sandbaseai/workbuddy-skill"


def catalog_id(row: dict) -> str:
    return str(row.get("id") or f"github:{row.get('repository', '')}:{row.get('path', '')}")


def package_download_command(asset: str) -> str:
    return (
        f"gh release download --repo {RELEASE_REPO} --pattern '{asset}' "
        "--pattern SHA256SUMS --dir workbuddy-download --clobber"
    )


def matches(row: dict, terms: list[str]) -> bool:
    haystack = " ".join(
        str(row.get(field, ""))
        for field in (
            "name_hint",
            "repository",
            "path",
            "workbuddy_status",
            "security_status",
            "workbuddy_missing_fields",
            "compatibility",
            "security_signals",
        )
    ).casefold()
    haystack = f"{haystack} {catalog_id(row).casefold()}"
    return all(term.casefold() in haystack for term in terms)


def query_rows(
    rows: list[dict],
    terms: list[str],
    *,
    status: str | None = None,
    security: str | None = None,
    source: str | None = None,
    min_score: int | None = None,
    package_status: str = "all",
    curated_ids: set[str] | None = None,
    unique: bool = False,
    order: str = "source",
    limit: int = 20,
) -> tuple[list[dict], Counter]:
    def score_of(row: dict) -> int:
        score = row.get("workbuddy_score")
        return score if isinstance(score, int) else -1

    copies = Counter(row.get("sha") for row in rows if row.get("sha"))
    results = [
        row for row in rows
        if matches(row, terms)
        and (status is None or row.get("workbuddy_status") == status)
        and (security is None or row.get("security_status") == security)
        and (source is None or source_context(row) == source)
        and (min_score is None or score_of(row) >= min_score)
        and (
            package_status == "all"
            or curated_ids is None
            or (catalog_id(row) in curated_ids) == (package_status == "reviewed")
        )
    ]

    def by_name(row: dict) -> tuple[str, str]:
        return (row.get("name_hint", "").casefold(), row.get("repository", "").casefold())

    def by_source(row: dict) -> tuple[str, str]:
        return (row.get("repository", "").casefold(), row.get("path", "").casefold())

    if unique:
        # Pick the best provenance representative before applying the display
        # order. This prevents a mirror or flagged duplicate from winning just
        # because it appears earlier in the JSONL snapshot.
        results.sort(
            key=lambda row: (
                source_context(row) != "primary-looking",
                row.get("security_status") == "flagged",
                -score_of(row),
                by_name(row),
            )
        )
        seen: set[str] = set()
        unique_results = []
        for row in results:
            sha = row.get("sha")
            if sha and sha in seen:
                continue
            if sha:
                seen.add(sha)
            unique_results.append(row)
        results = unique_results
    if order == "score":
        results.sort(key=lambda row: (-score_of(row), -copies[row.get("sha")], by_name(row)))
    elif order == "copies":
        results.sort(key=lambda row: (-copies[row.get("sha")], -score_of(row), by_name(row)))
    elif order == "name":
        results.sort(key=by_name)
    elif order == "source":
        results.sort(key=by_source)
    return results[:limit], copies


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search catalog/skills.jsonl by catalog ID, repository, path, or skill name."
    )
    parser.add_argument("terms", nargs="+", help="Words that must all match")
    parser.add_argument("--catalog", type=Path, default=Path("catalog/skills.jsonl"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--status",
        choices=("workbuddy-ready", "adaptable", "needs-review", "unreviewed"),
        help="Require an exact WorkBuddy review state",
    )
    parser.add_argument(
        "--security",
        choices=("no-static-flags", "flagged", "unscanned"),
        help="Require an exact static review state",
    )
    parser.add_argument("--min-score", type=int, help="Require a WorkBuddy score from 0 to 100")
    parser.add_argument(
        "--package-status",
        choices=("all", "reviewed", "catalog-only"),
        default="all",
        help="Require a reviewed WorkBuddy package or a catalog-only result",
    )
    parser.add_argument(
        "--curated",
        type=Path,
        default=Path("catalog/curated.json"),
        help="Curated package manifest used by --package-status",
    )
    parser.add_argument(
        "--source-context",
        choices=("primary-looking", "review-source"),
        help="Filter deterministic fork, mirror, and dormant-path context",
    )
    parser.add_argument("--unique", action="store_true", help="Return one path per unique blob SHA")
    parser.add_argument(
        "--sort",
        choices=("source", "score", "copies", "name"),
        default="source",
        help="Order matches before applying the limit",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    if args.min_score is not None and not 0 <= args.min_score <= 100:
        parser.error("--min-score must be between 0 and 100")
    if not args.catalog.exists():
        raise SystemExit(f"catalog not found: {args.catalog}")
    curated_ids = None
    curated_urls: dict[str, str] = {}
    if args.curated.exists():
        curated_entries = json.loads(args.curated.read_text(encoding="utf-8"))
        curated_urls = {
            entry["catalog_id"]: entry["download_url"]
            for entry in curated_entries
            if entry.get("download_url")
        }
        if args.package_status != "all":
            curated_ids = {entry["catalog_id"] for entry in curated_entries}
    elif args.package_status != "all":
        raise SystemExit(f"curated manifest not found: {args.curated}")

    rows: list[dict] = []
    with args.catalog.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"invalid JSONL at line {line_number}: {exc}") from exc
            rows.append(row)

    results, copies = query_rows(
        rows,
        args.terms,
        status=args.status,
        security=args.security,
        source=args.source_context,
        min_score=args.min_score,
        package_status=args.package_status,
        curated_ids=curated_ids,
        unique=args.unique,
        order=args.sort,
        limit=args.limit,
    )

    if args.as_json:
        output_rows = []
        for row in results:
            output = dict(row)
            package_url = curated_urls.get(catalog_id(row))
            if package_url:
                output["workbuddy_package_url"] = package_url
                asset = Path(urlparse(package_url).path).name
                output["workbuddy_package_asset"] = asset
                output["workbuddy_checksum_url"] = CHECKSUM_URL
                output["workbuddy_download_command"] = package_download_command(asset)
            output_rows.append(output)
        json.dump(output_rows, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    for row in results:
        print(f"{row['repository']}:{row['path']}")
        display_catalog_id = catalog_id(row)
        print(f"  catalog id: {display_catalog_id}")
        print(f"  source: {row['source_url']}")
        package_url = curated_urls.get(catalog_id(row))
        if package_url:
            print(f"  WorkBuddy package: {package_url}")
            asset = Path(urlparse(package_url).path).name
            print(f"  WorkBuddy asset: {asset}")
            print(f"  WorkBuddy checksum: {CHECKSUM_URL}")
            print(f"  WorkBuddy download: {package_download_command(asset)}")
        print(
            f"  review: {row['workbuddy_status']} ({row.get('workbuddy_score', '—')}/100); "
            f"security: {row['security_status']}; copies: {copies[row.get('sha')]}"
            f"; source: {source_context(row)}"
        )
    print(f"\n{len(results)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
