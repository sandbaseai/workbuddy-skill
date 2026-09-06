#!/usr/bin/env python3
"""Generate a non-executing review report for one indexed or local Skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from adapt_skill import (
    DEFAULT_CATALOG,
    catalog_record,
    collect_resources,
    fetch_text,
    immutable_github_source,
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
    "argument-hint",
    "compatibility",
    "disable-model-invocation",
    "license",
    "user-invocable",
)


def build_report(
    source_text: str, *, record: dict | None = None, source_file: Path | None = None
) -> dict:
    if record:
        immutable_github_source(record)
        if not isinstance(record.get("sha"), str) or not re.fullmatch(
            r"[0-9a-f]{40,64}", record["sha"]
        ):
            raise SystemExit("catalog record does not contain a valid blob SHA")
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


def render_markdown(report: dict, *, language: str = "en") -> str:
    source = report["source"]
    compatibility = report["compatibility"]
    static = report["static_review"]
    resources = report["resources"]
    checklist = report["review_checklist"]
    source_context_report = report["source_context"]
    zh = language == "zh-CN"
    labels = {
        "title": "WorkBuddy Skill 审阅报告" if zh else "WorkBuddy Skill review report",
        "source": "来源" if zh else "Source",
        "immutable": "不可变来源" if zh else "Immutable source",
        "yes": "是" if zh else "yes",
        "no": "否" if zh else "no",
        "source_context": "来源上下文" if zh else "Source context",
        "compatibility": "WorkBuddy 兼容性" if zh else "WorkBuddy compatibility",
        "static": "静态审阅" if zh else "Static review",
        "referenced": "引用资源" if zh else "Referenced resources",
        "missing": "缺失" if zh else "missing",
        "frontmatter": "Frontmatter 元数据" if zh else "Frontmatter",
        "signals": "审阅信号" if zh else "Review signals",
        "skill_signals": "Skill 信号" if zh else "Skill signals",
        "script_signals": "引用脚本信号" if zh else "Referenced-script signals",
        "missing_fields": "缺失的 WorkBuddy 字段" if zh else "Missing WorkBuddy fields",
        "missing_resources": "缺失资源" if zh else "Missing resources",
        "source_signals": "来源上下文信号" if zh else "Source-context signals",
        "checklist": "人工审阅清单" if zh else "Human review checklist",
        "none": "无" if zh else "none detected",
        "none_plain": "无" if zh else "none",
        "note": "静态审阅干净不代表安全保证。" if zh else static["note"],
    }
    checklist_labels = {
        "immutable_source": "来源已固定到不可变 Git 提交" if zh else "Source is pinned to an immutable Git commit",
        "primary_source_context": "未检测到 Fork、镜像或休眠路径信号" if zh else "No fork, mirror, or dormant-path signal was detected",
        "resources_complete": "所有引用资源均已获取" if zh else "All referenced resources were retrieved",
        "static_review_clear": "未检测到配置的静态信号" if zh else "No configured static signal was detected",
        "license_verified": "仓库许可证允许适配和再分发" if zh else "Repository license permits adaptation and redistribution",
        "instructions_reviewed": "指令和随附文件已人工审阅" if zh else "Instructions and bundled files were manually reviewed",
        "network_behavior_reviewed": "网络目标和数据处理方式已审阅" if zh else "Network destinations and data handling were reviewed",
        "permissions_reviewed": "请求的工具和权限已审阅" if zh else "Requested tools and permissions were reviewed",
    }
    lines = [
        f"# {labels['title']}",
        "",
        f"- {labels['source']}: {source.get('source_url', source.get('source_file'))}",
        f"- {labels['immutable']}: {labels['yes'] if source['immutable'] else labels['no']}",
        f"- {labels['source_context']}: {source_context_report['status']}",
        f"- {labels['compatibility']}: {compatibility['status']} ({compatibility['score']}/100)",
        f"- {labels['static']}: {static['status']}",
        f"- {labels['referenced']}: {len(resources['requested'])}; {labels['missing']}: {len(resources['missing'])}",
        "",
        f"## {labels['frontmatter']}",
        "",
        "```json",
        json.dumps(report["frontmatter"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        f"## {labels['signals']}",
        "",
        f"- {labels['skill_signals']}: {', '.join(static['skill_signals']) or labels['none']}",
        f"- {labels['script_signals']}: {', '.join(static['script_signals']) or labels['none']}",
        f"- {labels['missing_fields']}: {', '.join(compatibility['missing_fields']) or labels['none_plain']}",
        f"- {labels['missing_resources']}: {', '.join(resources['missing']) or labels['none_plain']}",
        f"- {labels['source_signals']}: {', '.join(source_context_report['signals']) or labels['none_plain']}",
        "",
        f"## {labels['checklist']}",
        "",
    ]
    lines.extend(
        f"- [{'x' if value else ' '}] {checklist_labels[key]}" for key, value in checklist.items()
    )
    lines.extend(["", f"> {labels['note']}"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--catalog-id")
    source.add_argument("--source-file", type=Path)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--language", choices=("en", "zh-CN"), default="en")
    parser.add_argument("--output", type=Path, help="write the rendered report to a file")
    args = parser.parse_args()

    if args.catalog_id:
        record = catalog_record(args.catalog, args.catalog_id)
        source_text = fetch_text(record["raw_url"])
        report = build_report(source_text, record=record)
    else:
        if args.source_file.is_symlink():
            raise SystemExit("source file must not be a symlink")
        if not args.source_file.is_file():
            raise SystemExit(f"source file is not a regular file: {args.source_file}")
        source_text = args.source_file.read_text(encoding="utf-8")
        report = build_report(source_text, source_file=args.source_file)
    if args.json:
        rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    else:
        rendered = render_markdown(report, language=args.language)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
