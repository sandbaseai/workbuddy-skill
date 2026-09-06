#!/usr/bin/env python3
"""Check external links used by the public learning and resource guides."""

from __future__ import annotations

import argparse
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = (
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "SUPPORT.md",
    ROOT / "SUPPORT.zh-CN.md",
    ROOT / "SECURITY.md",
    ROOT / "catalog/README.md",
    ROOT / "docs/resources.md",
    ROOT / "docs/resources.zh-CN.md",
    ROOT / "docs/quickstart.md",
    ROOT / "docs/quickstart.zh-CN.md",
    ROOT / "docs/starter-packs.md",
    ROOT / "docs/starter-packs.zh-CN.md",
    ROOT / "docs/use-cases.md",
    ROOT / "site/llms.txt",
    ROOT / "site/packages.html",
    ROOT / "site/categories.html",
    ROOT / "site/categories.zh-CN.html",
)
URL_PATTERN = re.compile(r'''https?://[^\s)<>`"']+''')
DOWNLOAD_PATTERN = re.compile(r"/releases/latest/download/")
SITE_URL_PREFIX = "https://sandbaseai.github.io/workbuddy-skill/"
RETRYABLE_HTTP_STATUS = {408, 429, 500, 502, 503, 504}


def extract_urls(paths: tuple[Path, ...] = SOURCE_FILES) -> list[str]:
    """Return stable, externally hosted URLs from the public resource files."""

    urls = set()
    for path in paths:
        if not path.is_file():
            continue
        for url in URL_PATTERN.findall(path.read_text(encoding="utf-8")):
            url = url.rstrip(".,;。")
            if path.name == "packages.html" and "/blob/" in url and url.endswith("/SKILL.md"):
                continue
            if not DOWNLOAD_PATTERN.search(url) and not url.startswith(SITE_URL_PREFIX):
                urls.add(url)
    return sorted(urls)


def retry_delay(error: HTTPError, attempt: int) -> float:
    retry_after = error.headers.get("Retry-After")
    try:
        return min(8.0, max(0.5, float(retry_after))) if retry_after else min(8.0, 0.5 * 2**attempt)
    except (TypeError, ValueError):
        return min(8.0, 0.5 * 2**attempt)


def check_url(url: str, timeout: float = 20.0, attempts: int = 3) -> tuple[str, int | None, str | None]:
    """Fetch one URL without downloading its response body."""

    request = Request(url, headers={"User-Agent": "workbuddy-skill-resource-check/1.0"})
    last_error = None
    last_status = None
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=timeout) as response:
                response.read(1)
                return url, response.status, None
        except HTTPError as error:
            last_status = error.code
            last_error = f"HTTP {error.code}"
            if error.code not in RETRYABLE_HTTP_STATUS:
                break
            if attempt + 1 < attempts:
                time.sleep(retry_delay(error, attempt))
                continue
        except (URLError, TimeoutError, OSError) as error:
            last_error = str(error.reason if isinstance(error, URLError) else error)
        if attempt + 1 < attempts:
            time.sleep(0.5)
    return url, last_status, last_error or "unknown error"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    urls = extract_urls()
    failures = []
    rate_limited = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(check_url, url, args.timeout) for url in urls]
        for future in as_completed(futures):
            url, status, error = future.result()
            if status == 429:
                rate_limited.append((url, status, error))
            elif status is None or status >= 400:
                failures.append((url, status, error))
    print(f"Checked {len(urls)} public resource links")
    for url, status, error in sorted(rate_limited):
        print(f"WARN {status or error}: {url}", file=sys.stderr)
    for url, status, error in sorted(failures):
        print(f"FAIL {status or error}: {url}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
