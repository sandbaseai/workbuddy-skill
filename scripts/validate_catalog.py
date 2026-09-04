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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=Path("catalog/skills.jsonl"))
    parser.add_argument("--minimum", type=int, default=10_000)
    args = parser.parse_args()
    seen_ids, rows = set(), 0
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
            if not item["source_url"].startswith(repo_url + "/blob/"):
                raise SystemExit(f"line {rows}: non-GitHub source")
            if not item["source_url"].endswith("/" + item["path"]):
                raise SystemExit(f"line {rows}: source_url does not match path")
            raw_prefix = f"https://raw.githubusercontent.com/{item['repository']}/"
            if not item["raw_url"].startswith(raw_prefix) or not item["raw_url"].endswith("/" + item["path"]):
                raise SystemExit(f"line {rows}: raw_url does not match repository/path")
    if rows < args.minimum:
        raise SystemExit(f"catalog has {rows} records; minimum is {args.minimum}")
    print(f"OK: {rows} catalog records are structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
