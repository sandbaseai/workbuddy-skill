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
        dense_writing = next(
            item
            for item in records
            if item["r"] == "Bogyie/llm-reliability-skill"
            and item["p"] == "skills/dense-writing/SKILL.md"
        )
        self.assertEqual(dense_writing["w"], "workbuddy-ready")
        self.assertEqual(dense_writing["g"], "content")
        self.assertTrue(dense_writing["a"].endswith("/dense-writing-workbuddy-skill.zip"))
        accessibility = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/review-accessibility/SKILL.md"
        )
        self.assertEqual(accessibility["w"], "workbuddy-ready")
        self.assertEqual(accessibility["g"], "design")
        self.assertTrue(
            accessibility["a"].endswith("/review-accessibility-workbuddy-skill.zip")
        )
        test_strategy = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/design-test-strategy/SKILL.md"
        )
        self.assertEqual(test_strategy["w"], "workbuddy-ready")
        self.assertEqual(test_strategy["g"], "development")
        self.assertTrue(
            test_strategy["a"].endswith("/design-test-strategy-workbuddy-skill.zip")
        )
        handoff = next(
            item
            for item in records
            if item["r"] == "quarcs-lab/project20XXy"
            and item["p"] == ".claude/skills/handoff/SKILL.md"
        )
        self.assertEqual(handoff["w"], "workbuddy-ready")
        self.assertEqual(handoff["g"], "productivity")
        self.assertTrue(handoff["a"].endswith("/handoff-workbuddy-skill.zip"))
        performance = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/improve-performance/SKILL.md"
        )
        self.assertEqual(performance["w"], "workbuddy-ready")
        self.assertEqual(performance["g"], "development")
        self.assertTrue(
            performance["a"].endswith("/improve-performance-workbuddy-skill.zip")
        )
        cli = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/test-cli/SKILL.md"
        )
        self.assertEqual(cli["w"], "workbuddy-ready")
        self.assertEqual(cli["g"], "development")
        self.assertTrue(cli["a"].endswith("/test-cli-workbuddy-skill.zip"))
        meeting = next(
            item
            for item in records
            if item["r"] == "rainoff/skill-gauge"
            and item["p"]
            == "exercises/fixtures/meeting-notes/skill/meeting-notes/SKILL.md"
        )
        self.assertEqual(meeting["w"], "workbuddy-ready")
        self.assertEqual(meeting["g"], "productivity")
        self.assertTrue(meeting["a"].endswith("/meeting-notes-workbuddy-skill.zip"))
        release = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/release-software/SKILL.md"
        )
        self.assertEqual(release["w"], "workbuddy-ready")
        self.assertEqual(release["g"], "development")
        self.assertTrue(release["a"].endswith("/release-software-workbuddy-skill.zip"))
        metadata = json.loads(
            (ROOT / "site" / "catalog-meta.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            metadata["curated_adaptations"],
            len(json.loads((ROOT / "catalog/curated.json").read_text(encoding="utf-8"))),
        )


if __name__ == "__main__":
    unittest.main()
