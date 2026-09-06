#!/usr/bin/env python3
"""Verify WorkBuddy release ZIPs against a SHA256SUMS file."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys


CHECKSUM_LINE = re.compile(r"^([0-9a-fA-F]{64})\s+[* ](.+?)\s*$")


def read_checksums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        match = CHECKSUM_LINE.match(line)
        if not match:
            raise ValueError(f"invalid checksum line {line_number}: {raw_line}")
        digest, name = match.groups()
        if not name or "/" in name or "\\" in name or name in {".", ".."}:
            raise ValueError(f"invalid release asset filename on line {line_number}: {name}")
        if name in checksums:
            raise ValueError(f"duplicate checksum entry: {name}")
        checksums[name] = digest.lower()
    if not checksums:
        raise ValueError(f"no checksum entries found in {path}")
    unexpected = sorted(
        name for name in checksums if not name.endswith("-workbuddy-skill.zip")
    )
    if unexpected:
        raise ValueError(
            "checksum manifest contains non-WorkBuddy assets: "
            + ", ".join(unexpected)
        )
    return checksums


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(directory: Path, checksum_name: str = "SHA256SUMS", selected: list[str] | None = None) -> list[str]:
    checksum_path = directory / checksum_name
    if checksum_path.is_symlink():
        raise ValueError(f"checksum file must not be a symlink: {checksum_path}")
    if not checksum_path.is_file():
        raise FileNotFoundError(f"checksum file not found: {checksum_path}")
    checksums = read_checksums(checksum_path)
    if not selected:
        unlisted = sorted(
            path.name
            for path in directory.glob("*-workbuddy-skill.zip")
            if path.name not in checksums
        )
        if unlisted:
            raise ValueError(
                "release assets without checksums: " + ", ".join(unlisted)
            )
    names = selected or sorted(checksums)
    missing_entries = [name for name in names if name not in checksums]
    if missing_entries:
        raise ValueError(f"no checksum entry for: {', '.join(missing_entries)}")

    verified = []
    for name in names:
        path = directory / name
        if path.is_symlink():
            raise ValueError(f"release asset must not be a symlink: {path}")
        if not path.is_file():
            raise FileNotFoundError(f"release asset not found: {path}")
        actual = sha256(path)
        expected = checksums[name]
        if actual != expected:
            raise ValueError(f"checksum mismatch for {name}: expected {expected}, got {actual}")
        verified.append(name)
    return verified


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify release assets against SHA256SUMS")
    parser.add_argument("directory", type=Path, help="Directory containing SHA256SUMS and release assets")
    parser.add_argument("--checksums", default="SHA256SUMS", help="Checksum filename (default: SHA256SUMS)")
    parser.add_argument("files", nargs="*", help="Specific asset names; default verifies every manifest entry")
    args = parser.parse_args()
    try:
        verified = verify(args.directory, args.checksums, args.files)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Verified {len(verified)} release asset(s) in {args.directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
