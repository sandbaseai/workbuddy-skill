import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_discovery import analyze  # noqa: E402


class DiscoveryAnalysisTests(unittest.TestCase):
    @patch("analyze_discovery.fetch_and_analyze")
    def test_analyzes_each_unique_sha_and_adds_triage_fields(self, fetch):
        fetch.return_value = {
            "analysis_status": "ok",
            "workbuddy_status": "adaptable",
            "security_status": "flagged",
            "security_signals": ["credential-path"],
        }
        rows = [
            {"id": "one", "sha": "a" * 40, "raw_url": "https://example.test/a"},
            {"id": "two", "sha": "a" * 40, "raw_url": "https://example.test/a"},
        ]
        summary = analyze(rows, workers=1)
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual(summary["candidate_records"], 2)
        self.assertEqual(summary["unique_contents"], 1)
        self.assertEqual(summary["security_flagged"], 2)
        self.assertEqual(rows[0]["security_signals"], ["credential-path"])


if __name__ == "__main__":
    unittest.main()
