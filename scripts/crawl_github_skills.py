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
MAX_THROTTLE_RETRIES = 8


def rate_limit_delay(headers: dict) -> int:
    reset = int(headers.get("X-RateLimit-Reset", "0"))
    retry_after = int(headers.get("Retry-After", "0"))
    return max(5, retry_after, reset - int(time.time()) + 2)


def request_json(query: str, page: int, token: str, max_retries: int = 3) -> tuple[dict, dict]:
    # Relevance ordering repeatedly returns the same first page, which makes
    # incremental refreshes spend their budget rediscovering old records.
    # Indexed-descending order exposes newly indexed public skills first.
    params = urlencode({
        "q": query,
        "per_page": 100,
        "page": page,
        "sort": "indexed",
        "order": "desc",
    })
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{API}?{params}", headers=headers)
    for attempt in range(max_retries + 1):
        try:
            with urlopen(request, timeout=45) as response:
                return json.load(response), dict(response.headers)
        except HTTPError as exc:
            if exc.code not in (500, 502, 503, 504) or attempt >= max_retries:
                raise
            retry_after = int(exc.headers.get("Retry-After", "0"))
            delay = max(retry_after, 2**attempt)
            print(f"GitHub returned {exc.code}; retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
        except URLError:
            if attempt >= max_retries:
                raise
            delay = 2**attempt
            print(f"GitHub connection failed; retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)


def wait_for_rate_limit(headers: dict, remaining_wait: int) -> int:
    if int(headers.get("X-RateLimit-Remaining", "1")) > 0:
        return 0
    delay = rate_limit_delay(headers)
    if delay > remaining_wait:
        raise RuntimeError(
            f"GitHub rate-limit wait {delay}s exceeds this run's remaining "
            f"{remaining_wait}s budget; resume later"
        )
    print(f"GitHub code-search limit reached; waiting {delay}s", file=sys.stderr)
    time.sleep(delay)
    return delay


def search_shards(start_bytes: int, max_bytes: int) -> list[tuple[int, int]]:
    """Return non-overlapping size ranges that can be searched without the cap.

    GitHub truncates code-search results at 1,000 matches. Start with broad
    ranges, then split only ranges that are actually capped. This makes a
    refresh proportional to the distribution of files instead of issuing one
    request per possible byte size.
    """
    return [(start_bytes, max_bytes)]


def query_for_range(lower: int, upper: int) -> str:
    return f"filename:SKILL.md size:{lower}..{upper}"


def normalize(item: dict, query: str) -> dict:
    repo = item["repository"]
    path = item["path"]
    raw_url = item["html_url"].replace(
        "https://github.com/", "https://raw.githubusercontent.com/", 1
    ).replace("/blob/", "/", 1)
    return {
        "id": f"github:{repo['full_name']}:{path}",
        "name_hint": Path(path).parent.name,
        "repository": repo["full_name"],
        "path": path,
        "sha": item["sha"],
        "source_url": item["html_url"],
        "raw_url": raw_url,
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


def write_stats(path: Path, rows: dict[str, dict], requests: int, capped_queries: int) -> None:
    stats = {
        "records": len(rows),
        "unique_content_shas": len({row["sha"] for row in rows.values()}),
        "repositories": len({row["repository"] for row in rows.values()}),
        "requests": requests,
        "queries_over_github_cap": capped_queries,
    }
    stats_path = path.with_name("stats.json")
    stats_path.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(stats, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=10_000)
    parser.add_argument("--start-bytes", type=int, default=1)
    parser.add_argument("--max-bytes", type=int, default=20_000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--checkpoint-every", type=int, default=5)
    parser.add_argument(
        "--max-rate-wait",
        type=int,
        default=300,
        help="Pause resumably instead of sleeping longer than this many seconds",
    )
    parser.add_argument(
        "--max-requests",
        type=int,
        default=100,
        help="Bound Code Search requests for one resumable run",
    )
    args = parser.parse_args()
    if (
        args.target < 1
        or args.start_bytes < 1
        or args.max_bytes < args.start_bytes
        or args.max_requests < 1
        or args.max_rate_wait < 1
    ):
        parser.error(
            "require target > 0, max-requests > 0, max-rate-wait > 0, "
            "and 0 < start-bytes <= max-bytes"
        )

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN", "")
    rows = load_existing(args.output)
    requests = 0
    capped_queries = 0
    throttle_retries = 0
    rate_waited = 0

    try:
        pending = search_shards(args.start_bytes, args.max_bytes)
        while pending:
            lower, upper = pending.pop()
            query = query_for_range(lower, upper)
            if len(rows) >= args.target:
                break
            page = 1
            headers = {}
            while page <= 10 and len(rows) < args.target:
                try:
                    if requests >= args.max_requests:
                        raise RuntimeError(
                            f"request budget exhausted at {args.max_requests}; resume later"
                        )
                    payload, headers = request_json(query, page, token)
                except HTTPError as exc:
                    if exc.code in (403, 429):
                        throttle_retries += 1
                        if throttle_retries > MAX_THROTTLE_RETRIES:
                            raise RuntimeError(
                                "GitHub search API remained rate-limited after "
                                f"{MAX_THROTTLE_RETRIES} retries; resume later"
                            ) from exc
                        delay = rate_limit_delay(exc.headers)
                        remaining_wait = args.max_rate_wait - rate_waited
                        if delay > remaining_wait:
                            raise RuntimeError(
                                f"GitHub rate-limit wait {delay}s exceeds this run's "
                                f"remaining {remaining_wait}s budget; resume later"
                            ) from exc
                        print(f"GitHub returned {exc.code}; waiting {delay}s", file=sys.stderr)
                        time.sleep(delay)
                        rate_waited += delay
                        continue
                    raise
                throttle_retries = 0
                requests += 1
                total = int(payload.get("total_count", 0))
                if total > 1_000 and page == 1:
                    capped_queries += 1
                    if lower < upper:
                        middle = (lower + upper) // 2
                        pending.extend(((lower, middle), (middle + 1, upper)))
                        break
                items = payload.get("items", [])
                for item in items:
                    if Path(item["path"]).name.casefold() != "skill.md":
                        continue
                    row = normalize(item, query)
                    previous = rows.get(row["id"])
                    if previous and previous.get("sha") == row["sha"]:
                        row.update({
                            key: value for key, value in previous.items()
                            if key not in row
                        })
                    rows[row["id"]] = row
                    if len(rows) >= args.target:
                        break
                print(f"indexed={len(rows)} query={query!r} page={page}", file=sys.stderr)
                if not items or page * 100 >= min(total, 1_000):
                    break
                page += 1
                rate_waited += wait_for_rate_limit(
                    headers, args.max_rate_wait - rate_waited
                )
                if requests % args.checkpoint_every == 0:
                    write_atomic(args.output, rows)
            rate_waited += wait_for_rate_limit(
                headers, args.max_rate_wait - rate_waited
            )
            # Persist after every completed shard so a long refresh loses at
            # most one shard when interrupted.
            write_atomic(args.output, rows)
    except (KeyboardInterrupt, HTTPError, URLError, RuntimeError) as exc:
        write_atomic(args.output, rows)
        write_stats(args.output, rows, requests, capped_queries)
        print(f"crawl paused after {len(rows)} records: {exc}", file=sys.stderr)
        return 2

    write_atomic(args.output, rows)
    write_stats(args.output, rows, requests, capped_queries)
    return 0 if len(rows) >= args.target else 1


if __name__ == "__main__":
    raise SystemExit(main())
