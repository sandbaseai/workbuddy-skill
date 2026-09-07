#!/usr/bin/env python3
"""Fetch immutable skill texts and add conservative compatibility signals.

No downloaded content is executed or persisted. Identical blob SHAs are fetched
once, analyzed once, and then applied to every provenance record for that blob.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import InvalidURL
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DEFAULT_CATALOG = Path("catalog/skills.jsonl")
USER_AGENT = "sandbaseai-workbuddy-skill-analyzer/0.3"
ANALYSIS_VERSION = "0.5"
ANALYSIS_FIELDS = {
    "analysis_version", "analysis_status", "frontmatter_valid", "workbuddy_score",
    "workbuddy_status", "workbuddy_missing_fields", "license_declared", "compatibility", "security_status",
    "security_signals", "skill_lines",
}
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)
RISK_PATTERNS = {
    "prompt-injection": re.compile(
        r"(?:ignore|disregard|override)\s+(?:all\s+)?(?:previous|prior|above|earlier)\s+"
        r"instructions|(?:reveal|print|show|leak)\s+(?:the\s+)?(?:system|hidden)\s+prompt",
        re.I,
    ),
    "pipe-to-shell": re.compile(r"(?:curl|wget)[^\n|]{0,500}\|\s*(?:ba)?sh\b", re.I),
    "recursive-delete": re.compile(r"\brm\s+(?:-[a-zA-Z]*r[a-zA-Z]*f|-{1,2}recursive)[^\n]*", re.I),
    "privilege-escalation": re.compile(r"\bsudo\s+", re.I),
    "credential-path": re.compile(r"(?:\.ssh/|\.aws/credentials|\.env\b|keychain|credential store)", re.I),
    "sensitive-data-exfiltration": re.compile(
        r"(?:send|upload|post|transmit|exfiltrat)[^\n]{0,240}"
        r"(?:api\s*key|access\s*token|secret|password|credential|environment variable)",
        re.I,
    ),
    "dynamic-eval": re.compile(r"(?:\beval\s*\(|\bexec\s*\(|base64\s+(?:--decode|-d))", re.I),
}


def parse_frontmatter(text: str) -> tuple[bool, dict[str, str]]:
    match = FRONTMATTER.match(text)
    if not match:
        return False, {}
    fields: dict[str, str] = {}
    lines = match.group(1).splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line[0].isspace() or ":" not in line:
            index += 1
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value in {">", "|"}:
            chunks = []
            index += 1
            while index < len(lines) and (not lines[index] or lines[index][0].isspace()):
                chunks.append(lines[index].strip())
                index += 1
            value = (" " if value == ">" else "\n").join(chunks).strip()
            fields[key.strip()] = value
            continue
        fields[key.strip()] = value.strip('"\'')
        index += 1
    return True, fields


def analyze_text(text: str) -> dict:
    valid, fields = parse_frontmatter(text)
    name = fields.get("name", "")
    risks = sorted(label for label, pattern in RISK_PATTERNS.items() if pattern.search(text))
    required_workbuddy = (
        "name", "description", "description_zh", "description_en", "version", "author", "license"
    )
    missing = [field for field in required_workbuddy if not fields.get(field)]

    score = 20
    score += 20 if valid else 0
    score += 15 if fields.get("description") else 0
    score += 10 if name and NAME_PATTERN.fullmatch(name) else 0
    score += sum(5 for field in required_workbuddy[1:] if fields.get(field))
    score += 10 if text.count("\n") + 1 <= 500 else 0
    score += 5 if not risks else 0
    score = min(score, 100)

    if valid and not missing and not risks:
        status = "workbuddy-ready"
    elif valid and fields.get("description"):
        status = "adaptable"
    else:
        status = "needs-review"
    return {
        "analysis_version": ANALYSIS_VERSION,
        "analysis_status": "ok",
        "frontmatter_valid": valid,
        "workbuddy_score": score,
        "workbuddy_status": status,
        "workbuddy_missing_fields": missing,
        "license_declared": bool(fields.get("license")),
        "compatibility": fields.get("compatibility", ""),
        "security_status": "flagged" if risks else "no-static-flags",
        "security_signals": risks,
        "skill_lines": text.count("\n") + 1,
    }


def fetch_and_analyze(url: str, retries: int = 2) -> dict:
    request = Request(quote(url, safe=":/%"), headers={"User-Agent": USER_AGENT})
    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=20) as response:
                raw = response.read(512 * 1024 + 1)
            if len(raw) > 512 * 1024:
                return {"analysis_status": "oversize", "workbuddy_status": "needs-review", "security_status": "unscanned"}
            return analyze_text(raw.decode("utf-8", errors="replace"))
        except (HTTPError, URLError, TimeoutError, InvalidURL) as exc:
            if attempt >= retries or isinstance(exc, HTTPError) and exc.code in (401, 403, 404):
                return {
                    "analysis_status": f"fetch-error:{getattr(exc, 'code', exc.__class__.__name__)}",
                    "workbuddy_status": "needs-review",
                    "security_status": "unscanned",
                }
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def write_atomic(path: Path, rows: list[dict]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in sorted(rows, key=lambda item: item["id"].casefold()):
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="re-fetch and re-analyze every unique content SHA instead of reusing cached results",
    )
    args = parser.parse_args()
    if args.workers < 1 or (args.limit is not None and args.limit < 1):
        parser.error("workers and limit must be positive")

    rows = [json.loads(line) for line in args.path.read_text(encoding="utf-8").splitlines() if line]
    cached: dict[str, dict] = {}
    for row in rows:
        if (
            row.get("analysis_status")
            and row.get("analysis_version") == ANALYSIS_VERSION
            and not args.refresh
        ):
            cached_analysis = {key: row[key] for key in ANALYSIS_FIELDS if key in row}
            if "license_declared" not in cached_analysis:
                cached_analysis["license_declared"] = "license" not in row.get(
                    "workbuddy_missing_fields", []
                )
            cached.setdefault(row["sha"], cached_analysis)

    sha_sources: dict[str, str] = {}
    candidates = rows[: args.limit] if args.limit else rows
    for row in candidates:
        if row["sha"] not in cached:
            sha_sources.setdefault(row["sha"], row["raw_url"])

    analyses: dict[str, dict] = dict(cached)
    completed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch_and_analyze, url): sha for sha, url in sha_sources.items()}
        for future in as_completed(futures):
            analyses[futures[future]] = future.result()
            completed += 1
            if completed % 500 == 0 or completed == len(futures):
                print(f"analyzed {completed}/{len(futures)} new unique contents", flush=True)

    for row in rows:
        analysis = analyses.get(row["sha"])
        if analysis:
            row.update(analysis)
    write_atomic(args.path, rows)

    analyzed = [row for row in rows if "analysis_status" in row]
    summary = {
        "analyzed_paths": len(analyzed),
        "analyzed_unique_shas": len({row["sha"] for row in analyzed}),
        "analysis_ok": sum(row["analysis_status"] == "ok" for row in analyzed),
        "workbuddy_ready": sum(row["workbuddy_status"] == "workbuddy-ready" for row in analyzed),
        "adaptable": sum(row["workbuddy_status"] == "adaptable" for row in analyzed),
        "needs_review": sum(row["workbuddy_status"] == "needs-review" for row in analyzed),
        "security_flagged": sum(row["security_status"] == "flagged" for row in analyzed),
    }
    summary_path = args.path.with_name("analysis-stats.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
