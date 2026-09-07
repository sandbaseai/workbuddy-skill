#!/usr/bin/env python3
"""Validate the repository manifest used by the read-only discovery probe."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def read_repositories(path: Path) -> list[str]:
    repositories: list[str] = []
    seen: set[str] = set()
    errors: list[str] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = raw_line.strip()
        if not value or value.startswith("#"):
            continue
        if not REPOSITORY.fullmatch(value):
            errors.append(f"line {line_number}: invalid repository {value!r}")
            continue
        if value in seen:
            errors.append(f"line {line_number}: duplicate repository {value!r}")
            continue
        seen.add(value)
        repositories.append(value)
    if errors:
        raise ValueError("\n".join(errors))
    if not repositories:
        raise ValueError("manifest does not contain any repositories")
    return repositories


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        default=Path("config/upstream-skill-sources.txt"),
    )
    args = parser.parse_args()
    repositories = read_repositories(args.manifest)
    print(f"OK: {len(repositories)} unique repository sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
