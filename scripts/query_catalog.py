#!/usr/bin/env python3
"""Search the provenance-only catalog without third-party dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def matches(row: dict, terms: list[str]) -> bool:
    haystack = " ".join(
        str(row.get(field, ""))
        for field in ("name_hint", "repository", "path")
    ).casefold()
    return all(term.casefold() in haystack for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search catalog/skills.jsonl by repository, path, or skill name."
    )
    parser.add_argument("terms", nargs="+", help="Words that must all match")
    parser.add_argument("--catalog", type=Path, default=Path("catalog/skills.jsonl"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    if not args.catalog.exists():
        raise SystemExit(f"catalog not found: {args.catalog}")

    results: list[dict] = []
    with args.catalog.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"invalid JSONL at line {line_number}: {exc}") from exc
            if matches(row, args.terms):
                results.append(row)
                if len(results) >= args.limit:
                    break

    if args.as_json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    for row in results:
        print(f"{row['repository']}:{row['path']}")
        print(f"  source: {row['source_url']}")
        print(f"  review: {row['workbuddy_status']}; security: {row['security_status']}")
    print(f"\n{len(results)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
