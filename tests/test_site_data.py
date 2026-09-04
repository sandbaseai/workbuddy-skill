import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SiteDataTests(unittest.TestCase):
    def test_curated_adaptation_is_installable_and_workbuddy_ready(self):
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_site_data.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        records = json.loads((ROOT / "site" / "catalog.json").read_text(encoding="utf-8"))
        record = next(
            item
            for item in records
            if item["r"] == "GuicedEE/ai-rules"
            and item["p"] == "skills/.curated/systematic-debugging/SKILL.md"
        )
        self.assertEqual(record["w"], "workbuddy-ready")
        self.assertEqual(
            record["a"],
            "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/"
            "systematic-debugging-workbuddy-skill.zip",
        )
        metadata = json.loads(
            (ROOT / "site" / "catalog-meta.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["curated_adaptations"], 1)


if __name__ == "__main__":
    unittest.main()
