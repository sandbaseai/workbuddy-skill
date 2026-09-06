#!/usr/bin/env python3
"""Verify that every reviewed package is present in the latest public release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


CHECKSUM_ASSET = "SHA256SUMS"


def expected_assets(path: Path) -> set[str]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {
        row["asset"]
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("asset"), str)
    }


def release_assets(repo: str, release: str = "latest") -> set[str]:
    command = ["gh", "release", "view", "--repo", repo]
    if release != "latest":
        command.insert(3, release)
    command.extend(["--json", "assets", "--jq", ".assets[].name"])
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def compare(expected: set[str], published: set[str]) -> list[str]:
    errors = []
    missing = sorted(expected - published)
    extra = sorted((published - expected) - {CHECKSUM_ASSET})
    if missing:
        errors.append(f"missing release assets: {', '.join(missing)}")
    if extra:
        errors.append(f"unindexed release assets: {', '.join(extra)}")
    if CHECKSUM_ASSET not in published:
        errors.append(f"missing release asset: {CHECKSUM_ASSET}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="sandbaseai/workbuddy-skill")
    parser.add_argument("--release", default="latest")
    parser.add_argument("--packages", type=Path, default=Path("site/packages.json"))
    args = parser.parse_args()
    errors = compare(expected_assets(args.packages), release_assets(args.repo, args.release))
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    print(f"Verified {len(expected_assets(args.packages))} reviewed package assets in {args.release} release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
