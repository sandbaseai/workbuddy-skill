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
    ROOT / "docs/resources.md",
    ROOT / "docs/resources.zh-CN.md",
    ROOT / "docs/quickstart.md",
    ROOT / "docs/quickstart.zh-CN.md",
    ROOT / "docs/starter-packs.md",
    ROOT / "docs/starter-packs.zh-CN.md",
    ROOT / "site/llms.txt",
)
URL_PATTERN = re.compile(r"https?://[^\s)<>`]+")
DOWNLOAD_PATTERN = re.compile(r"/releases/latest/download/")
SITE_URL_PREFIX = "https://sandbaseai.github.io/workbuddy-skill/"


def extract_urls(paths: tuple[Path, ...] = SOURCE_FILES) -> list[str]:
    """Return stable, externally hosted URLs from the public resource files."""

    urls = set()
    for path in paths:
        for url in URL_PATTERN.findall(path.read_text(encoding="utf-8")):
            url = url.rstrip(".,;。")
            if not DOWNLOAD_PATTERN.search(url) and not url.startswith(SITE_URL_PREFIX):
                urls.add(url)
    return sorted(urls)


def check_url(url: str, timeout: float = 20.0, attempts: int = 2) -> tuple[str, int | None, str | None]:
    """Fetch one URL without downloading its response body."""

    request = Request(url, headers={"User-Agent": "workbuddy-skill-resource-check/1.0"})
    last_error = None
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=timeout) as response:
                response.read(1)
                return url, response.status, None
        except HTTPError as error:
            last_error = f"HTTP {error.code}"
        except (URLError, TimeoutError, OSError) as error:
            last_error = str(error.reason if isinstance(error, URLError) else error)
        if attempt + 1 < attempts:
            time.sleep(0.5)
    return url, None, last_error or "unknown error"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    urls = extract_urls()
    failures = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(check_url, url, args.timeout) for url in urls]
        for future in as_completed(futures):
            url, status, error = future.result()
            if status is None or status >= 400:
                failures.append((url, status, error))
    print(f"Checked {len(urls)} public resource links")
    for url, status, error in sorted(failures):
        print(f"FAIL {status or error}: {url}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
