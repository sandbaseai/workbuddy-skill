#!/usr/bin/env python3
"""Validate the compact browser catalog against its published JSON Schema contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse


HEX_SHA = re.compile(r"^[0-9a-f]{40}$")
URI_FIELDS = {"u", "a"}


def validate_rows(rows: object, schema: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(rows, list):
        return ["catalog root must be an array"]
    definition = schema.get("$defs", {}).get("record", {})
    properties = definition.get("properties", {})
    required = set(definition.get("required", []))
    allowed = set(properties)
    enums = {
        field: set(spec.get("enum", []))
        for field, spec in properties.items()
        if spec.get("enum")
    }
    for index, row in enumerate(rows):
        prefix = f"record {index}"
        if not isinstance(row, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = required - row.keys()
        extra = row.keys() - allowed
        errors.extend(f"{prefix} missing {field}" for field in sorted(missing))
        errors.extend(f"{prefix} has unknown field {field}" for field in sorted(extra))
        for field in sorted(required & row.keys()):
            value = row[field]
            if field == "q" and value is None:
                continue
            if field in {"n", "r", "p", "s", "w", "k", "g", "o"} and not isinstance(value, str):
                errors.append(f"{prefix}.{field} must be a string")
            if field == "s" and (not isinstance(value, str) or not HEX_SHA.fullmatch(value)):
                errors.append(f"{prefix}.s must be a 40-character lowercase hex SHA")
            if field in enums and value not in enums[field]:
                errors.append(f"{prefix}.{field} has unsupported value {value!r}")
            if field == "q" and (isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100):
                errors.append(f"{prefix}.q must be an integer from 0 to 100 or null")
            if field == "c" and (isinstance(value, bool) or not isinstance(value, int) or value < 1):
                errors.append(f"{prefix}.c must be a positive integer")
            if field == "x" and (not isinstance(value, list) or any(not isinstance(item, str) for item in value)):
                errors.append(f"{prefix}.x must be an array of strings")
            if field in URI_FIELDS and (not isinstance(value, str) or urlparse(value).scheme not in {"http", "https"}):
                errors.append(f"{prefix}.{field} must be an HTTP(S) URL")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate site/catalog.json against catalog-schema.json")
    parser.add_argument("--catalog", type=Path, default=Path("site/catalog.json"))
    parser.add_argument("--schema", type=Path, default=Path("site/catalog-schema.json"))
    args = parser.parse_args()
    try:
        rows = json.loads(args.catalog.read_text(encoding="utf-8"))
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    errors = validate_rows(rows, schema)
    if errors:
        for error in errors[:20]:
            print(f"error: {error}", file=sys.stderr)
        if len(errors) > 20:
            print(f"error: {len(errors) - 20} more error(s)", file=sys.stderr)
        return 1
    print(f"OK: validated {len(rows)} compact catalog records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
