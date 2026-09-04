#!/usr/bin/env python3
"""Generate a non-executing review report for one indexed or local Skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from adapt_skill import (
    DEFAULT_CATALOG,
    catalog_record,
    collect_resources,
    fetch_text,
    resource_paths,
)
from analyze_catalog import analyze_text, parse_frontmatter
from catalog_signals import source_context, source_signals

FRONTMATTER_FIELDS = (
    "name",
    "description",
    "description_zh",
    "description_en",
    "version",
    "author",
    "allowed-tools",
    "disable-model-invocation",
    "user-invocable",
)


def build_report(
    source_text: str, *, record: dict | None = None, source_file: Path | None = None
) -> dict:
    analysis = analyze_text(source_text)
    valid, fields = parse_frontmatter(source_text)
    requested = [str(path) for path in resource_paths(source_text)]
    resources, missing = collect_resources(
        source_text, record=record, source_file=source_file
    )
    script_signals = sorted({
        signal
        for resource_path, content in resources.items()
        if resource_path.startswith("scripts/")
        for signal in analyze_text(content.decode("utf-8", errors="replace"))["security_signals"]
    })
    all_signals = sorted(set(analysis["security_signals"] + script_signals))
    if record:
        source = {
            "catalog_id": record["id"],
            "repository": record["repository"],
            "path": record["path"],
            "blob_sha": record["sha"],
            "source_url": record["source_url"],
            "immutable": True,
        }
    else:
        source = {"source_file": str(source_file), "immutable": False}
    return {
        "source": source,
        "source_context": {
            "status": source_context(record) if record else "local-source",
            "signals": source_signals(record) if record else [],
            "note": "Source-context signals are deterministic triage hints, not authorship proof.",
        },
        "frontmatter": {
            "valid": valid,
            "fields": {key: fields[key] for key in FRONTMATTER_FIELDS if fields.get(key)},
        },
        "compatibility": {
            "status": analysis["workbuddy_status"],
            "score": analysis["workbuddy_score"],
            "missing_fields": analysis["workbuddy_missing_fields"],
        },
        "static_review": {
            "status": "flagged" if all_signals else "no-static-flags",
            "skill_signals": analysis["security_signals"],
            "script_signals": script_signals,
            "note": "A clean static review is not a security guarantee.",
        },
        "resources": {
            "requested": requested,
            "retrieved": sorted(resources),
            "missing": missing,
            "retrieved_bytes": sum(map(len, resources.values())),
        },
        "review_checklist": {
            "immutable_source": bool(record),
            "primary_source_context": bool(record) and not source_signals(record),
            "resources_complete": not missing,
            "static_review_clear": not all_signals,
            "license_verified": False,
            "instructions_reviewed": False,
            "network_behavior_reviewed": False,
            "permissions_reviewed": False,
        },
    }


def render_markdown(report: dict) -> str:
    source = report["source"]
    compatibility = report["compatibility"]
    static = report["static_review"]
    resources = report["resources"]
    checklist = report["review_checklist"]
    source_context_report = report["source_context"]
    lines = [
        "# WorkBuddy Skill review report",
        "",
        f"- Source: {source.get('source_url', source.get('source_file'))}",
        f"- Immutable source: {'yes' if source['immutable'] else 'no'}",
        f"- Source context: {source_context_report['status']}",
        f"- WorkBuddy compatibility: {compatibility['status']} ({compatibility['score']}/100)",
        f"- Static review: {static['status']}",
        f"- Referenced resources: {len(resources['requested'])}; missing: {len(resources['missing'])}",
        "",
        "## Frontmatter",
        "",
        "```json",
        json.dumps(report["frontmatter"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Review signals",
        "",
        f"- Skill signals: {', '.join(static['skill_signals']) or 'none detected'}",
        f"- Referenced-script signals: {', '.join(static['script_signals']) or 'none detected'}",
        f"- Missing WorkBuddy fields: {', '.join(compatibility['missing_fields']) or 'none'}",
        f"- Missing resources: {', '.join(resources['missing']) or 'none'}",
        f"- Source-context signals: {', '.join(source_context_report['signals']) or 'none'}",
        "",
        "## Human review checklist",
        "",
    ]
    labels = {
        "immutable_source": "Source is pinned to an immutable Git commit",
        "primary_source_context": "No fork, mirror, or dormant-path signal was detected",
        "resources_complete": "All referenced resources were retrieved",
        "static_review_clear": "No configured static signal was detected",
        "license_verified": "Repository license permits adaptation and redistribution",
        "instructions_reviewed": "Instructions and bundled files were manually reviewed",
        "network_behavior_reviewed": "Network destinations and data handling were reviewed",
        "permissions_reviewed": "Requested tools and permissions were reviewed",
    }
    lines.extend(
        f"- [{'x' if value else ' '}] {labels[key]}" for key, value in checklist.items()
    )
    lines.extend(["", f"> {static['note']}"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--catalog-id")
    source.add_argument("--source-file", type=Path)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.catalog_id:
        record = catalog_record(args.catalog, args.catalog_id)
        source_text = fetch_text(record["raw_url"])
        report = build_report(source_text, record=record)
    else:
        source_text = args.source_file.read_text(encoding="utf-8")
        report = build_report(source_text, source_file=args.source_file)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
