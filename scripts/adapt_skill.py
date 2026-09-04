#!/usr/bin/env python3
"""Create a reviewable WorkBuddy package from one indexed public skill.

The command never executes source content. It requires an explicit license
declaration, preserves provenance, and refuses flagged or incomplete packages
unless the caller deliberately opts in.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import quote
from urllib.request import Request, urlopen
from zipfile import ZIP_DEFLATED, ZipFile

from analyze_catalog import FRONTMATTER, analyze_text, parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "catalog" / "skills.jsonl"
DEFAULT_OUTPUT = ROOT / "dist" / "adapted"
USER_AGENT = "sandbaseai-workbuddy-skill-adapter/0.4"
RESOURCE_REFERENCE = re.compile(r"(?:@|\]\()(?P<path>(?:references|scripts|assets|templates)/[^\s)]+)")


def catalog_record(path: Path, record_id: str) -> dict:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row["id"] == record_id:
                return row
    raise SystemExit(f"catalog id not found: {record_id}")


def fetch_text(url: str) -> str:
    request = Request(quote(url, safe=":/%"), headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        raw = response.read(512 * 1024 + 1)
    if len(raw) > 512 * 1024:
        raise SystemExit("source exceeds the 512 KiB review limit")
    return raw.decode("utf-8", errors="replace")


def portable_name(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")[:64].rstrip("-")
    if not value:
        raise SystemExit("could not derive a portable skill name")
    return value


def yaml_value(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def adapted_text(source: str, args: argparse.Namespace) -> tuple[str, str]:
    valid, fields = parse_frontmatter(source)
    match = FRONTMATTER.match(source)
    body = source[match.end():] if valid and match else source
    name = portable_name(fields.get("name") or args.name_hint)
    description = fields.get("description") or args.description_en
    frontmatter = {
        "name": name,
        "display_name": args.display_name_zh,
        "display_name_en": args.display_name_en,
        "description": description,
        "description_zh": args.description_zh,
        "description_en": args.description_en,
        "category": args.category,
        "version": args.version,
        "author": args.author,
    }
    for optional in ("allowed-tools", "disable-model-invocation", "user-invocable"):
        if fields.get(optional):
            frontmatter[optional] = fields[optional]
    rendered = "---\n" + "\n".join(
        f"{key}: {yaml_value(value)}" for key, value in frontmatter.items()
    ) + "\n---\n\n" + body.lstrip()
    return name, rendered


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--catalog-id")
    source.add_argument("--source-file", type=Path)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--display-name-zh", required=True)
    parser.add_argument("--display-name-en", required=True)
    parser.add_argument("--description-zh", required=True)
    parser.add_argument("--description-en", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--source-license", required=True)
    parser.add_argument("--category", default="productivity")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--allow-flagged", action="store_true")
    parser.add_argument("--allow-missing-resources", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.catalog_id:
        record = catalog_record(args.catalog, args.catalog_id)
        source_text = fetch_text(record["raw_url"])
        source_info = {
            "catalog_id": record["id"],
            "repository": record["repository"],
            "path": record["path"],
            "sha": record["sha"],
            "source_url": record["source_url"],
        }
        args.name_hint = record["name_hint"]
    else:
        source_text = args.source_file.read_text(encoding="utf-8")
        source_info = {"source_file": str(args.source_file)}
        args.name_hint = args.source_file.parent.name

    analysis = analyze_text(source_text)
    if analysis["security_signals"] and not args.allow_flagged:
        raise SystemExit(
            "source has static review signals; inspect before retrying with --allow-flagged: "
            + ", ".join(analysis["security_signals"])
        )
    missing_resources = sorted(set(match.group("path") for match in RESOURCE_REFERENCE.finditer(source_text)))
    if missing_resources and not args.allow_missing_resources:
        raise SystemExit(
            "source references bundled resources that were not fetched: "
            + ", ".join(missing_resources[:10])
        )

    name, skill_text = adapted_text(source_text, args)
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f"{name}-workbuddy.zip"
    if archive.exists() and not args.force:
        raise SystemExit(f"output exists; use --force to replace: {archive}")

    provenance = {
        **source_info,
        "declared_source_license": args.source_license,
        "adaptation": {
            "missing_resources": missing_resources,
            "security_signals": analysis["security_signals"],
            "tool": "scripts/adapt_skill.py",
        },
    }
    with tempfile.TemporaryDirectory(prefix="workbuddy-adapt-") as temporary:
        package = Path(temporary)
        (package / "SKILL.md").write_text(skill_text, encoding="utf-8")
        (package / "SOURCE.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary_archive = archive.with_suffix(".zip.tmp")
        with ZipFile(temporary_archive, "w", compression=ZIP_DEFLATED) as output:
            output.write(package / "SKILL.md", "SKILL.md")
            output.write(package / "SOURCE.json", "SOURCE.json")
        temporary_archive.replace(archive)
    print(f"OK: created {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
