#!/usr/bin/env python3
"""Add conservative static compatibility signals to a discovery report."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path

from analyze_catalog import fetch_and_analyze


def load_rows(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
        if not isinstance(row, dict) or not isinstance(row.get("raw_url"), str):
            raise SystemExit(f"invalid discovery row at {path}:{line_number}: missing raw_url")
        rows.append(row)
    return rows


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in sorted(rows, key=lambda item: item["id"].casefold()):
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def analyze(rows: list[dict], workers: int) -> dict[str, int]:
    by_sha: dict[str, str] = {}
    for row in rows:
        by_sha.setdefault(str(row.get("sha", row["raw_url"])), row["raw_url"])
    analyses = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fetch_and_analyze, url): sha for sha, url in by_sha.items()}
        for future in as_completed(futures):
            analyses[futures[future]] = future.result()
    for row in rows:
        row.update(analyses[str(row.get("sha", row["raw_url"]))])
    summary = {
        "candidate_records": len(rows),
        "unique_contents": len(by_sha),
        "analysis_ok": sum(row.get("analysis_status") == "ok" for row in rows),
        "workbuddy_ready": sum(row.get("workbuddy_status") == "workbuddy-ready" for row in rows),
        "adaptable": sum(row.get("workbuddy_status") == "adaptable" for row in rows),
        "needs_review": sum(row.get("workbuddy_status") == "needs-review" for row in rows),
        "security_flagged": sum(row.get("security_status") == "flagged" for row in rows),
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be positive")
    rows = load_rows(args.input)
    summary = analyze(rows, args.workers)
    write_rows(args.output, rows)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
