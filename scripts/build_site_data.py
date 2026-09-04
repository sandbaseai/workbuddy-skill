#!/usr/bin/env python3
"""Build the compact browser index used by the static catalog site."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog" / "skills.jsonl"
OUTPUT = ROOT / "site" / "catalog.json"

records = []
repositories = set()
shas = set()
with SOURCE.open(encoding="utf-8") as handle:
    for line in handle:
        row = json.loads(line)
        repositories.add(row["repository"])
        shas.add(row["sha"])
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
meta = {
    "records": len(records),
    "repositories": len(repositories),
    "unique_content_shas": len(shas),
}
meta_output = ROOT / "site" / "catalog-meta.json"
meta_temporary = meta_output.with_suffix(".json.tmp")
meta_temporary.write_text(json.dumps(meta, separators=(",", ":")), encoding="utf-8")
meta_temporary.replace(meta_output)
print(f"OK: wrote {len(records)} searchable records to {OUTPUT.relative_to(ROOT)}")
