#!/usr/bin/env python3
"""Validate catalog integrity without third-party dependencies."""

from pathlib import Path
import argparse
import json
import re

REQUIRED = {
    "id", "name_hint", "repository", "path", "sha", "source_url",
    "raw_url", "repository_url", "workbuddy_status", "security_status",
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
            item = json.loads(line)
            missing = REQUIRED - item.keys()
            if missing:
                raise SystemExit(f"line {rows}: missing {sorted(missing)}")
            if item["id"] in seen_ids:
                raise SystemExit(f"line {rows}: duplicate id {item['id']}")
            seen_ids.add(item["id"])
            if not SHA.fullmatch(item["sha"]):
                raise SystemExit(f"line {rows}: invalid SHA")
            if Path(item["path"]).name.casefold() != "skill.md":
                raise SystemExit(f"line {rows}: unexpected path {item['path']}")
            if not item["source_url"].startswith("https://github.com/"):
                raise SystemExit(f"line {rows}: non-GitHub source")
    if rows < args.minimum:
        raise SystemExit(f"catalog has {rows} records; minimum is {args.minimum}")
    print(f"OK: {rows} catalog records are structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
