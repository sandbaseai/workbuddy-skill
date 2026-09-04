#!/usr/bin/env python3
"""Build the compact browser index used by the static catalog site."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog" / "skills.jsonl"
OUTPUT = ROOT / "site" / "catalog.json"

records = []
with SOURCE.open(encoding="utf-8") as handle:
    for line in handle:
        row = json.loads(line)
        records.append(
            {
                "n": row["name_hint"],
                "r": row["repository"],
                "p": row["path"],
                "u": row["source_url"],
                "s": row["sha"],
            }
        )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
temporary = OUTPUT.with_suffix(".json.tmp")
temporary.write_text(
    json.dumps(records, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)
temporary.replace(OUTPUT)
print(f"OK: wrote {len(records)} searchable records to {OUTPUT.relative_to(ROOT)}")

