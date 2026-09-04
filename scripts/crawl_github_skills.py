#!/usr/bin/env python3
"""Build a provenance-first index of public GitHub SKILL.md files.

The crawler stores metadata and source links, never executes downloaded code,
and checkpoints each page so interrupted runs can resume safely.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.github.com/search/code"
DEFAULT_OUT = Path("catalog/skills.jsonl")
USER_AGENT = "sandbaseai-workbuddy-skill-catalog/0.2"


def request_json(query: str, page: int, token: str) -> tuple[dict, dict]:
    params = urlencode({"q": query, "per_page": 100, "page": page})
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{API}?{params}", headers=headers)
    with urlopen(request, timeout=45) as response:
        return json.load(response), dict(response.headers)


def wait_for_rate_limit(headers: dict) -> None:
    if int(headers.get("X-RateLimit-Remaining", "1")) > 0:
        return
    reset = int(headers.get("X-RateLimit-Reset", "0"))
    delay = max(1, reset - int(time.time()) + 2)
    print(f"GitHub code-search limit reached; waiting {delay}s", file=sys.stderr)
    time.sleep(delay)


def search_shards(max_bytes: int) -> list[str]:
    # Exact sizes avoid GitHub's 1,000-result cap swallowing an entire range.
    # Common sizes can still exceed the cap; the catalog records this in stats.
    likely = list(range(1_000, max_bytes + 1))
    small = list(range(999, 0, -1))
    sizes = likely + small
    return [f"filename:SKILL.md size:{size}..{size}" for size in sizes]


def normalize(item: dict, query: str) -> dict:
    repo = item["repository"]
    branch = repo.get("default_branch") or "HEAD"
    path = item["path"]
    return {
        "id": f"github:{repo['full_name']}:{path}",
        "name_hint": Path(path).parent.name,
        "repository": repo["full_name"],
        "path": path,
        "sha": item["sha"],
        "source_url": item["html_url"],
        "raw_url": f"https://raw.githubusercontent.com/{repo['full_name']}/{branch}/{path}",
        "repository_url": repo["html_url"],
        "repository_fork": bool(repo.get("fork")),
        "github_query": query,
        "workbuddy_status": "unreviewed",
        "security_status": "unscanned",
    }


def load_existing(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    if not path.exists():
        return rows
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
        rows[row["id"]] = row
    return rows


def write_atomic(path: Path, rows: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    ordered = sorted(rows.values(), key=lambda row: row["id"].casefold())
    with temporary.open("w", encoding="utf-8") as handle:
        for row in ordered:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=10_000)
    parser.add_argument("--max-bytes", type=int, default=20_000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--checkpoint-every", type=int, default=5)
    args = parser.parse_args()
    if args.target < 1 or args.max_bytes < 1:
        parser.error("--target and --max-bytes must be positive")

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN", "")
    rows = load_existing(args.output)
    requests = 0
    capped_queries = 0

    try:
        for query in search_shards(args.max_bytes):
            if len(rows) >= args.target:
                break
            page = 1
            while page <= 10 and len(rows) < args.target:
                try:
                    payload, headers = request_json(query, page, token)
                except HTTPError as exc:
                    if exc.code in (403, 429):
                        reset = int(exc.headers.get("X-RateLimit-Reset", "0"))
                        delay = max(5, reset - int(time.time()) + 2)
                        print(f"GitHub returned {exc.code}; waiting {delay}s", file=sys.stderr)
                        time.sleep(delay)
                        continue
                    raise
                requests += 1
                total = int(payload.get("total_count", 0))
                capped_queries += int(total > 1_000 and page == 1)
                items = payload.get("items", [])
                for item in items:
                    row = normalize(item, query)
                    rows[row["id"]] = row
                    if len(rows) >= args.target:
                        break
                print(f"indexed={len(rows)} query={query!r} page={page}", file=sys.stderr)
                if not items or page * 100 >= min(total, 1_000):
                    break
                page += 1
                wait_for_rate_limit(headers)
                if requests % args.checkpoint_every == 0:
                    write_atomic(args.output, rows)
            wait_for_rate_limit(headers)
    except (KeyboardInterrupt, HTTPError, URLError) as exc:
        write_atomic(args.output, rows)
        print(f"crawl paused after {len(rows)} records: {exc}", file=sys.stderr)
        return 2

    write_atomic(args.output, rows)
    stats = {
        "records": len(rows),
        "unique_content_shas": len({row["sha"] for row in rows.values()}),
        "repositories": len({row["repository"] for row in rows.values()}),
        "requests": requests,
        "queries_over_github_cap": capped_queries,
    }
    stats_path = args.output.with_name("stats.json")
    stats_path.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(stats, sort_keys=True))
    return 0 if len(rows) >= args.target else 1


if __name__ == "__main__":
    raise SystemExit(main())
