"""Shared category inference for the Atlas site and local catalog CLI."""

from __future__ import annotations

import re


CATEGORY_RULES = (
    ("security", ("security", "audit", "pentest", "vulnerability", "sast", "threat", "auth")),
    ("media", ("video", "audio", "podcast", "voice", "music", "subtitle", "animation")),
    ("design", ("design", "ui", "ux", "frontend", "css", "figma", "brand", "visual")),
    ("research", ("research", "search", "academic", "paper", "literature", "citation", "analysis")),
    ("data", ("data", "database", "sql", "spreadsheet", "excel", "csv", "etl", "analytics")),
    ("content", ("content", "writing", "writer", "copy", "blog", "document", "markdown", "seo")),
    ("business", ("sales", "marketing", "finance", "legal", "hr", "customer", "commerce", "product")),
    ("productivity", ("task", "calendar", "email", "meeting", "note", "workflow", "automation", "planning")),
    ("development", ("code", "coding", "test", "debug", "deploy", "api", "git", "python", "javascript", "typescript")),
)
CATEGORIES = tuple(category for category, _ in CATEGORY_RULES) + ("other",)
CATEGORY_LABELS_ZH = {
    "business": "商业",
    "content": "内容",
    "data": "数据",
    "design": "设计",
    "development": "开发",
    "media": "媒体",
    "productivity": "效率",
    "research": "研究",
    "security": "安全",
    "other": "其他",
}
CATEGORY_ALIASES = {
    **{category: category for category in CATEGORIES},
    **{label: category for category, label in CATEGORY_LABELS_ZH.items()},
}


def normalize_category(value: str) -> str:
    """Return the canonical category for an English or Chinese label."""

    normalized = value.strip().casefold()
    try:
        return CATEGORY_ALIASES[normalized]
    except KeyError as exc:
        raise ValueError(f"unknown category: {value}") from exc


def category_for(row: dict) -> str:
    """Infer the public Atlas category from a catalog row."""

    explicit = row.get("category")
    if explicit in CATEGORIES:
        return explicit
    haystack = f"{row.get('name_hint', '')} {row.get('path', '')}".casefold()
    tokens = set(re.findall(r"[a-z0-9]+", haystack))
    for category, keywords in CATEGORY_RULES:
        if any(keyword in tokens for keyword in keywords):
            return category
    return "other"
