#!/usr/bin/env python3
"""Build the compact browser index used by the static catalog site."""

from pathlib import Path
from collections import Counter
import json
import re

from catalog_signals import source_context, source_signals

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog" / "skills.jsonl"
OUTPUT = ROOT / "site" / "catalog.json"

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


def category_for(row: dict) -> str:
    haystack = f"{row['name_hint']} {row['path']}".casefold()
    tokens = set(re.findall(r"[a-z0-9]+", haystack))
    for category, keywords in CATEGORY_RULES:
        if any(keyword in tokens for keyword in keywords):
            return category
    return "other"

source_rows = []
repositories = set()
shas = set()
with SOURCE.open(encoding="utf-8") as handle:
    for line in handle:
        row = json.loads(line)
        source_rows.append(row)
        repositories.add(row["repository"])
        shas.add(row["sha"])

sha_copies = Counter(row["sha"] for row in source_rows)
category_counts = Counter()
records = []
for row in source_rows:
    category = category_for(row)
    category_counts[category] += 1
    records.append(
        {
            "n": row["name_hint"],
            "r": row["repository"],
            "p": row["path"],
            "u": row["source_url"],
            "s": row["sha"],
            "w": row.get("workbuddy_status", "unreviewed"),
            "q": row.get("workbuddy_score"),
            "k": row.get("security_status", "unscanned"),
            "g": category,
            "c": sha_copies[row["sha"]],
            "o": source_context(row),
            "x": source_signals(row),
        }
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
temporary = OUTPUT.with_suffix(".json.tmp")
temporary.write_text(
    json.dumps(records, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)
temporary.replace(OUTPUT)
meta = {
    "categories": dict(sorted(category_counts.items())),
    "records": len(records),
    "repositories": len(repositories),
    "unique_content_shas": len(shas),
}
meta_output = ROOT / "site" / "catalog-meta.json"
meta_temporary = meta_output.with_suffix(".json.tmp")
meta_temporary.write_text(json.dumps(meta, separators=(",", ":")), encoding="utf-8")
meta_temporary.replace(meta_output)
print(f"OK: wrote {len(records)} searchable records to {OUTPUT.relative_to(ROOT)}")
