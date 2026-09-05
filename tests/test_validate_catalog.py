import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_catalog.py"


def catalog_row(source_ref: str) -> dict:
    repository = "owner/repo"
    path = "skills/demo/SKILL.md"
    return {
        "id": f"github:{repository}:{path}",
        "name_hint": "demo",
        "repository": repository,
        "path": path,
        "sha": "b" * 40,
        "source_url": f"https://github.com/{repository}/blob/{source_ref}/{path}",
        "raw_url": f"https://raw.githubusercontent.com/{repository}/{source_ref}/{path}",
        "repository_url": f"https://github.com/{repository}",
        "repository_fork": False,
        "github_query": "filename:SKILL.md",
        "workbuddy_status": "unreviewed",
        "security_status": "unscanned",
    }


class ValidateCatalogTests(unittest.TestCase):
    def run_validator(self, row: dict, *extra_args: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skills.jsonl"
            path.write_text(json.dumps(row) + "\n", encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(path), "--minimum", "1", *extra_args],
                capture_output=True,
                text=True,
            )

    def test_requires_full_commit_in_both_source_urls(self):
        result = self.run_validator(catalog_row("main"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("full commit", result.stderr)

    def test_accepts_matching_immutable_urls(self):
        result = self.run_validator(catalog_row("a" * 40))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_check_stats_requires_matching_snapshot(self):
        result = self.run_validator(catalog_row("a" * 40), "--check-stats")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("catalog stats mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
