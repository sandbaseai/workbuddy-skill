#!/usr/bin/env python3
"""Verify that a local frozen catalog matches published catalog metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(catalog: Path, metadata: Path) -> str:
    try:
        payload = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"unable to read metadata: {exc}") from exc
    if payload.get("snapshot_frozen") is not True:
        raise ValueError("metadata does not describe a frozen snapshot")
    expected = payload.get("catalog_sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        raise ValueError("metadata has no valid catalog_sha256 fingerprint")
    actual = sha256(catalog)
    if actual != expected.lower():
        raise ValueError(f"snapshot mismatch: expected {expected}, got {actual}")
    return actual


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a frozen skills.jsonl against catalog-meta.json"
    )
    parser.add_argument(
        "--catalog", type=Path, default=Path("catalog/skills.jsonl"),
        help="local catalog file (default: catalog/skills.jsonl)",
    )
    parser.add_argument(
        "--metadata", type=Path, default=Path("site/catalog-meta.json"),
        help="metadata file containing catalog_sha256 (default: site/catalog-meta.json)",
    )
    args = parser.parse_args()
    try:
        digest = verify(args.catalog, args.metadata)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Verified frozen catalog {args.catalog} ({digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
