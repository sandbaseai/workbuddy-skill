import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from crawl_github_skills import (  # noqa: E402
    rate_limit_delay,
    repository_skill_rows,
    main,
    wait_for_rate_limit,
    write_stats,
)


class RateLimitTests(unittest.TestCase):
    def test_default_published_catalog_requires_explicit_opt_in(self):
        with patch("sys.argv", ["crawl_github_skills.py"]):
            with self.assertRaises(SystemExit) as raised:
                main()
        self.assertEqual(raised.exception.code, 2)

    @patch("crawl_github_skills.time.time", return_value=1_000)
    def test_delay_uses_largest_server_boundary(self, _time):
        self.assertEqual(
            rate_limit_delay({"Retry-After": "40", "X-RateLimit-Reset": "1030"}),
            40,
        )

    @patch("crawl_github_skills.time.time", return_value=1_000)
    def test_long_wait_pauses_instead_of_sleeping(self, _time):
        started = time.monotonic()
        with self.assertRaisesRegex(RuntimeError, "remaining 120s budget"):
            wait_for_rate_limit(
                {"X-RateLimit-Remaining": "0", "Retry-After": "734"},
                remaining_wait=120,
            )
        self.assertLess(time.monotonic() - started, 1)

    @patch("crawl_github_skills.time.sleep")
    @patch("crawl_github_skills.time.time", return_value=1_000)
    def test_wait_reports_budget_consumed(self, _time, sleep):
        consumed = wait_for_rate_limit(
            {"X-RateLimit-Remaining": "0", "Retry-After": "40"},
            remaining_wait=45,
        )
        self.assertEqual(consumed, 40)
        sleep.assert_called_once_with(40)

    def test_stats_are_replaced_atomically(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "skills.jsonl"
            rows = {"one": {"sha": "abc", "repository": "owner/repo"}}
            write_stats(output, rows, requests=2, capped_queries=1)
            stats = json.loads((Path(directory) / "stats.json").read_text(encoding="utf-8"))
            self.assertEqual(stats["records"], 1)
            self.assertFalse((Path(directory) / "stats.json.tmp").exists())

    @patch("crawl_github_skills.request_api")
    def test_repository_tree_scan_pins_default_branch_commit(self, request_api):
        request_api.side_effect = [
            ({"default_branch": "main", "html_url": "https://github.com/owner/repo", "fork": False}, {}),
            ({"object": {"sha": "commitsha"}}, {}),
            ({
                "truncated": False,
                "tree": [
                    {"type": "blob", "path": "skills/useful/SKILL.md", "sha": "blobsha"},
                    {"type": "tree", "path": "skills/useful"},
                ],
            }, {}),
        ]
        rows, requests = repository_skill_rows("owner/repo", "token")
        self.assertEqual(requests, 3)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["sha"], "blobsha")
        self.assertIn("/commitsha/skills/useful/SKILL.md", rows[0]["raw_url"])
        self.assertEqual(request_api.call_count, 3)


if __name__ == "__main__":
    unittest.main()
