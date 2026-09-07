#!/usr/bin/env python3
"""Report discovery rows not already represented by the frozen catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_rows(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise SystemExit(f"invalid discovery row at {path}:{line_number}: missing id")
        rows[row["id"]] = row
    return rows


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in sorted(rows, key=lambda item: item["id"].casefold()):
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def compare(catalog: Path, discovery: Path, output: Path) -> dict[str, int]:
    catalog_rows = load_rows(catalog)
    discovery_rows = load_rows(discovery)
    catalog_shas = {
        row.get("sha") for row in catalog_rows.values() if isinstance(row.get("sha"), str)
    }
    new_rows = [
        row
        for row in discovery_rows.values()
        if row["id"] not in catalog_rows and row.get("sha") not in catalog_shas
    ]
    write_rows(output, new_rows)
    stats = {
        "catalog_records": len(catalog_rows),
        "discovered_records": len(discovery_rows),
        "new_records": len(new_rows),
        "new_repositories": len({row.get("repository") for row in new_rows}),
    }
    print(json.dumps(stats, ensure_ascii=False, sort_keys=True))
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--discovery", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    compare(args.catalog, args.discovery, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
