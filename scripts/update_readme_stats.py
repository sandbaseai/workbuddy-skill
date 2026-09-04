#!/usr/bin/env python3
"""Keep README catalog metrics synchronized with generated catalog statistics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    start_index = text.index(start) + len(start)
    end_index = text.index(end, start_index)
    return text[:start_index] + "\n" + replacement.rstrip() + "\n" + text[end_index:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--catalog-readme", type=Path, default=Path("catalog/README.md"))
    parser.add_argument("--stats", type=Path, default=Path("catalog/stats.json"))
    parser.add_argument("--analysis", type=Path, default=Path("catalog/analysis-stats.json"))
    args = parser.parse_args()

    stats = json.loads(args.stats.read_text(encoding="utf-8"))
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    records = f"{stats['records']:,}"
    shas = f"{stats['unique_content_shas']:,}"
    repositories = f"{stats['repositories']:,}"
    adaptable = f"{analysis['adaptable']:,}"
    needs_review = f"{analysis['needs_review']:,}"
    ready = f"{analysis['workbuddy_ready']:,}"
    flagged = f"{analysis['security_flagged']:,}"
    metrics = "\n".join([
        "| Metric | Current snapshot |",
        "|---|---:|",
        f"| Indexed GitHub paths | {records} |",
        f"| Unique content SHAs | {shas} |",
        f"| Source repositories | {repositories} |",
    ])
    analysis_text = (
        f"The current static analysis successfully inspected {records} paths: "
        f"{adaptable} are structurally adaptable to WorkBuddy, {needs_review} "
        f"need manual review, {ready} are currently WorkBuddy-ready, and "
        f"{flagged} contain at least one conservative security signal."
    )
    text = args.readme.read_text(encoding="utf-8")
    text = replace_between(text, "<!-- CATALOG-METRICS:START -->", "<!-- CATALOG-METRICS:END -->", metrics)
    text = replace_between(text, "<!-- CATALOG-ANALYSIS:START -->", "<!-- CATALOG-ANALYSIS:END -->", analysis_text)
    args.readme.write_text(text, encoding="utf-8")
    catalog_metrics = "\n".join([
        f"- {records} indexed GitHub paths",
        f"- {shas} unique Git blob SHAs",
        f"- {repositories} source repositories",
    ])
    catalog_text = args.catalog_readme.read_text(encoding="utf-8")
    catalog_text = replace_between(
        catalog_text,
        "<!-- CATALOG-SNAPSHOT:START -->",
        "<!-- CATALOG-SNAPSHOT:END -->",
        catalog_metrics,
    )
    args.catalog_readme.write_text(catalog_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
