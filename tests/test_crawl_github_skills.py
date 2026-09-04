from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from crawl_github_skills import rate_limit_delay, wait_for_rate_limit  # noqa: E402


class RateLimitTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
