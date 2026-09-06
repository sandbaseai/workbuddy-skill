#!/usr/bin/env python3
"""Build the compact browser index used by the static catalog site."""

from pathlib import Path
from collections import Counter
import json
import re
from urllib.parse import urlparse

from catalog_signals import source_context, source_signals

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog" / "skills.jsonl"
CURATED = ROOT / "catalog" / "curated.json"
OUTPUT = ROOT / "site" / "catalog.json"
PACKAGES_OUTPUT = ROOT / "site" / "packages.json"
CHECKSUM_URL = "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/SHA256SUMS"

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
KNOWN_CATEGORIES = {category for category, _ in CATEGORY_RULES} | {"other"}


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

curated_entries = json.loads(CURATED.read_text(encoding="utf-8"))
curated = {entry["catalog_id"]: entry for entry in curated_entries}
if len(curated) != len(curated_entries):
    raise SystemExit("catalog/curated.json contains duplicate catalog IDs")
skill_paths = [entry["skill_path"] for entry in curated_entries]
if len(set(skill_paths)) != len(skill_paths):
    raise SystemExit("catalog/curated.json contains duplicate skill paths")
catalog_ids = {row["id"] for row in source_rows}
source_by_id = {row["id"]: row for row in source_rows}
for entry in curated_entries:
    if not (ROOT / entry["skill_path"] / "SKILL.md").is_file():
        raise SystemExit(f"curated Skill is missing: {entry['skill_path']}")
    if entry["catalog_id"] not in catalog_ids:
        raise SystemExit(f"curated source is missing from catalog: {entry['catalog_id']}")
    if not entry["download_url"].startswith(
        "https://github.com/sandbaseai/workbuddy-skill/releases/"
    ):
        raise SystemExit(f"unexpected curated download URL: {entry['download_url']}")
    if entry.get("category") not in KNOWN_CATEGORIES | {None}:
        raise SystemExit(f"unknown curated category: {entry['category']}")

sha_copies = Counter(row["sha"] for row in source_rows)
category_counts = Counter()
records = []
for row in source_rows:
    adaptation = curated.get(row["id"])
    category = adaptation.get("category", category_for(row)) if adaptation else category_for(row)
    category_counts[category] += 1
    record = {
        "n": row["name_hint"],
        "r": row["repository"],
        "p": row["path"],
        "u": row["source_url"],
        "s": row["sha"],
        "w": "workbuddy-ready" if adaptation else row.get("workbuddy_status", "unreviewed"),
        "q": row.get("workbuddy_score"),
        "k": row.get("security_status", "unscanned"),
        "g": category,
        "c": sha_copies[row["sha"]],
        "o": source_context(row),
        "x": source_signals(row),
    }
    if adaptation:
        record["a"] = adaptation["download_url"]
    records.append(record)

packages = []
for entry in sorted(curated_entries, key=lambda item: item["skill"]):
    source = source_by_id[entry["catalog_id"]]
    packages.append(
        {
            "id": entry["catalog_id"],
            "name": entry["skill"],
            "path": entry["skill_path"],
            "repository": source["repository"],
            "source_url": source["source_url"],
            "sha": source["sha"],
            "download_url": entry["download_url"],
            "asset": Path(urlparse(entry["download_url"]).path).name,
            "checksum_url": CHECKSUM_URL,
            "category": curated.get(entry["catalog_id"], {}).get(
                "category", category_for(source)
            ),
        }
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
temporary = OUTPUT.with_suffix(".json.tmp")
temporary.write_text(
    json.dumps(records, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)
temporary.replace(OUTPUT)
packages_temporary = PACKAGES_OUTPUT.with_suffix(".json.tmp")
packages_temporary.write_text(
    json.dumps(packages, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)
packages_temporary.replace(PACKAGES_OUTPUT)
meta = {
    "categories": dict(sorted(category_counts.items())),
    "snapshot_frozen": True,
    "records": len(records),
    "repositories": len(repositories),
    "unique_content_shas": len(shas),
    "curated_adaptations": len(curated),
    "release_checksum_url": CHECKSUM_URL,
}
meta_output = ROOT / "site" / "catalog-meta.json"
meta_temporary = meta_output.with_suffix(".json.tmp")
meta_temporary.write_text(json.dumps(meta, separators=(",", ":")), encoding="utf-8")
meta_temporary.replace(meta_output)
print(f"OK: wrote {len(records)} searchable records to {OUTPUT.relative_to(ROOT)}")
print(f"OK: wrote {len(packages)} installable packages to {PACKAGES_OUTPUT.relative_to(ROOT)}")
