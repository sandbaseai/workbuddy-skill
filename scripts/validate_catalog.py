#!/usr/bin/env python3
"""Validate catalog integrity without third-party dependencies."""

from pathlib import Path
import argparse
import json
import re

REQUIRED = {
    "id", "name_hint", "repository", "path", "sha", "source_url",
    "raw_url", "repository_url", "repository_fork", "github_query",
    "workbuddy_status", "security_status",
}
SHA = re.compile(r"[0-9a-f]{40,64}")
ANALYSIS_STATUSES = {"ok", "oversize"}
WORKBUDDY_STATUSES = {"unreviewed", "workbuddy-ready", "adaptable", "needs-review"}
SECURITY_STATUSES = {"unscanned", "no-static-flags", "flagged"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=Path("catalog/skills.jsonl"))
    parser.add_argument("--minimum", type=int, default=10_000)
    parser.add_argument("--require-analysis", action="store_true")
    parser.add_argument(
        "--check-stats",
        action="store_true",
        help="verify catalog/stats.json matches the records in the selected catalog",
    )
    args = parser.parse_args()
    seen_ids, rows, items = set(), 0, []
    with args.path.open(encoding="utf-8") as handle:
        for rows, line in enumerate(handle, 1):
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"line {rows}: invalid JSON ({exc.msg})") from exc
            if not isinstance(item, dict):
                raise SystemExit(f"line {rows}: record must be a JSON object")
            missing = REQUIRED - item.keys()
            if missing:
                raise SystemExit(f"line {rows}: missing {sorted(missing)}")
            if not all(isinstance(item[field], str) and item[field] for field in (
                "id", "repository", "path", "source_url", "raw_url",
                "repository_url", "github_query", "workbuddy_status", "security_status",
            )):
                raise SystemExit(f"line {rows}: string fields must be non-empty")
            if not isinstance(item["name_hint"], str):
                raise SystemExit(f"line {rows}: name_hint must be a string")
            if item["path"].casefold() != "skill.md" and not item["name_hint"]:
                raise SystemExit(f"line {rows}: name_hint is required for nested paths")
            if not isinstance(item["repository_fork"], bool):
                raise SystemExit(f"line {rows}: repository_fork must be boolean")
            if item["id"] in seen_ids:
                raise SystemExit(f"line {rows}: duplicate id {item['id']}")
            seen_ids.add(item["id"])
            expected_id = f"github:{item['repository']}:{item['path']}"
            if item["id"] != expected_id:
                raise SystemExit(f"line {rows}: id does not match repository/path")
            if not SHA.fullmatch(item["sha"]):
                raise SystemExit(f"line {rows}: invalid SHA")
            if Path(item["path"]).name.casefold() != "skill.md":
                raise SystemExit(f"line {rows}: unexpected path {item['path']}")
            repo_url = f"https://github.com/{item['repository']}"
            if not item["repository_url"].rstrip("/") == repo_url:
                raise SystemExit(f"line {rows}: repository_url does not match repository")
            source_match = re.fullmatch(
                rf"{re.escape(repo_url)}/blob/([0-9a-f]{{40}})/{re.escape(item['path'])}",
                item["source_url"],
            )
            if not source_match:
                raise SystemExit(
                    f"line {rows}: source_url must pin the repository path to a full commit"
                )
            raw_prefix = f"https://raw.githubusercontent.com/{item['repository']}/"
            expected_raw = f"{raw_prefix}{source_match.group(1)}/{item['path']}"
            if item["raw_url"] != expected_raw:
                raise SystemExit(f"line {rows}: raw_url does not match immutable source")
            if item["workbuddy_status"] not in WORKBUDDY_STATUSES:
                raise SystemExit(f"line {rows}: invalid WorkBuddy status")
            if item["security_status"] not in SECURITY_STATUSES:
                raise SystemExit(f"line {rows}: invalid security status")
            if "analysis_status" in item:
                status = item["analysis_status"]
                if status not in ANALYSIS_STATUSES and not status.startswith("fetch-error:"):
                    raise SystemExit(f"line {rows}: invalid analysis status")
                if status == "ok":
                    if not isinstance(item.get("frontmatter_valid"), bool):
                        raise SystemExit(f"line {rows}: frontmatter_valid must be boolean")
                    score = item.get("workbuddy_score")
                    if not isinstance(score, int) or not 0 <= score <= 100:
                        raise SystemExit(f"line {rows}: invalid WorkBuddy score")
                    if not isinstance(item.get("security_signals"), list):
                        raise SystemExit(f"line {rows}: security_signals must be a list")
            elif args.require_analysis:
                raise SystemExit(f"line {rows}: analysis is required")
            items.append(item)
    if rows < args.minimum:
        raise SystemExit(f"catalog has {rows} records; minimum is {args.minimum}")
    if args.check_stats:
        stats_path = Path("catalog/stats.json")
        try:
            stats = json.loads(stats_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SystemExit(f"unable to read {stats_path}: {exc}") from exc
        expected = {
            "records": len(items),
            "unique_content_shas": len({item["sha"] for item in items}),
            "repositories": len({item["repository"] for item in items}),
        }
        actual = {key: stats.get(key) for key in expected}
        if actual != expected:
            raise SystemExit(f"catalog stats mismatch: expected {expected}, found {actual}")
    print(f"OK: {rows} catalog records are structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
