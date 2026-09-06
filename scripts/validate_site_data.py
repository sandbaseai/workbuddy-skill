#!/usr/bin/env python3
"""Validate generated browser data against its published JSON Schema contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse


HEX_SHA = re.compile(r"^[0-9a-f]{40}$")


def validate_unique_fields(rows: object, fields: tuple[str, ...], label: str) -> list[str]:
    if not isinstance(rows, list):
        return []
    errors: list[str] = []
    for field in fields:
        seen: dict[object, int] = {}
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or field not in row:
                continue
            value = row[field]
            if value in seen:
                errors.append(
                    f"{label} duplicate {field} {value!r} at records {seen[value]} and {index}"
                )
            else:
                seen[value] = index
    return errors


def validate_rows(rows: object, schema: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(rows, list):
        return ["catalog root must be an array"]
    definition = schema.get("$defs", {}).get("record", schema.get("items", {}))
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
        for field in sorted(row.keys() & allowed):
            value = row[field]
            spec = properties[field]
            types = spec.get("type", [])
            if isinstance(types, str):
                types = [types]
            valid_type = (
                ("null" in types and value is None)
                or ("string" in types and isinstance(value, str))
                or ("integer" in types and isinstance(value, int) and not isinstance(value, bool))
                or ("array" in types and isinstance(value, list))
                or ("object" in types and isinstance(value, dict))
            )
            if not valid_type:
                errors.append(f"{prefix}.{field} has an invalid type")
                continue
            if field in enums and value not in enums[field]:
                errors.append(f"{prefix}.{field} has unsupported value {value!r}")
            if isinstance(value, str) and spec.get("pattern") and not re.fullmatch(spec["pattern"], value):
                if field == "s":
                    errors.append(f"{prefix}.s must be a 40-character lowercase hex SHA")
                else:
                    errors.append(f"{prefix}.{field} does not match its schema pattern")
            if spec.get("format") == "uri" and (
                not isinstance(value, str) or urlparse(value).scheme not in {"http", "https"}
            ):
                errors.append(f"{prefix}.{field} must be an HTTP(S) URL")
            if isinstance(value, int) and not isinstance(value, bool):
                if "minimum" in spec and value < spec["minimum"]:
                    if field == "c":
                        errors.append(f"{prefix}.c must be a positive integer")
                    else:
                        errors.append(f"{prefix}.{field} is below its schema minimum")
                if "maximum" in spec and value > spec["maximum"]:
                    if field == "q":
                        errors.append(f"{prefix}.q must be an integer from 0 to 100 or null")
                    else:
                        errors.append(f"{prefix}.{field} exceeds its schema maximum")
            if isinstance(value, list) and spec.get("items", {}).get("type") == "string":
                if any(not isinstance(item, str) for item in value):
                    errors.append(f"{prefix}.{field} must be an array of strings")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated site data against its JSON Schema contracts")
    parser.add_argument("--catalog", type=Path, default=Path("site/catalog.json"))
    parser.add_argument("--schema", type=Path, default=Path("site/catalog-schema.json"))
    parser.add_argument("--packages", type=Path, default=Path("site/packages.json"))
    parser.add_argument("--packages-schema", type=Path, default=Path("site/packages-schema.json"))
    args = parser.parse_args()
    try:
        rows = json.loads(args.catalog.read_text(encoding="utf-8"))
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        packages = json.loads(args.packages.read_text(encoding="utf-8"))
        packages_schema = json.loads(args.packages_schema.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    errors = validate_rows(rows, schema)
    package_errors = validate_rows(packages, packages_schema)
    errors.extend(f"packages: {error}" for error in package_errors)
    errors.extend(validate_unique_fields(packages, ("id", "download_url"), "packages"))
    if errors:
        for error in errors[:20]:
            print(f"error: {error}", file=sys.stderr)
        if len(errors) > 20:
            print(f"error: {len(errors) - 20} more error(s)", file=sys.stderr)
        return 1
    print(f"OK: validated {len(rows)} compact catalog records and {len(packages)} reviewed packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
