import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SiteDataTests(unittest.TestCase):
    def test_curated_adaptations_are_installable_and_workbuddy_ready(self):
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_site_data.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        records = json.loads((ROOT / "site" / "catalog.json").read_text(encoding="utf-8"))
        debugging = next(
            item
            for item in records
            if item["r"] == "GuicedEE/ai-rules"
            and item["p"] == "skills/.curated/systematic-debugging/SKILL.md"
        )
        self.assertEqual(debugging["w"], "workbuddy-ready")
        self.assertEqual(
            debugging["a"],
            "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/"
            "systematic-debugging-workbuddy-skill.zip",
        )
        spreadsheet = next(
            item
            for item in records
            if item["r"] == "xuthreekid/clawchain"
            and item["p"] == "backend/data/skills/excel-ops/SKILL.md"
        )
        self.assertEqual(spreadsheet["w"], "workbuddy-ready")
        self.assertEqual(spreadsheet["g"], "data")
        self.assertTrue(spreadsheet["a"].endswith("/excel-ops-workbuddy-skill.zip"))
        metadata = json.loads(
            (ROOT / "site" / "catalog-meta.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["curated_adaptations"], 2)


if __name__ == "__main__":
    unittest.main()
