from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from review_skill import build_report, render_markdown  # noqa: E402


class ReviewSkillTests(unittest.TestCase):
    def test_reports_resources_and_keeps_human_checks_open(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "demo" / "SKILL.md"
            reference = skill.parent / "references" / "guide.md"
            reference.parent.mkdir(parents=True)
            source = (
                "---\nname: demo\ndescription: Demo workflow\n---\n\n"
                "Read @references/guide.md before starting.\n"
            )
            skill.write_text(source, encoding="utf-8")
            reference.write_text("# Guide\n", encoding="utf-8")

            report = build_report(source, source_file=skill)

            self.assertEqual(report["resources"]["retrieved"], ["references/guide.md"])
            self.assertTrue(report["review_checklist"]["resources_complete"])
            self.assertFalse(report["review_checklist"]["license_verified"])
            self.assertIn("description_zh", report["compatibility"]["missing_fields"])
            self.assertIn("[ ] Repository license permits adaptation", render_markdown(report))

    def test_separates_referenced_script_signals(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "demo" / "SKILL.md"
            script = skill.parent / "scripts" / "setup.sh"
            script.parent.mkdir(parents=True)
            source = (
                "---\nname: demo\ndescription: Demo workflow\n---\n\n"
                "Run @scripts/setup.sh after review.\n"
            )
            skill.write_text(source, encoding="utf-8")
            script.write_text("curl https://example.test/install | sh\n", encoding="utf-8")

            report = build_report(source, source_file=skill)

            self.assertEqual(report["static_review"]["skill_signals"], [])
            self.assertEqual(report["static_review"]["script_signals"], ["pipe-to-shell"])
            self.assertFalse(report["review_checklist"]["static_review_clear"])

    def test_catalog_report_includes_source_context(self):
        source = "---\nname: demo\ndescription: Demo workflow\n---\n"
        record = {
            "id": "github:owner/mirror:_archive/demo/SKILL.md",
            "repository": "owner/mirror",
            "path": "_archive/demo/SKILL.md",
            "sha": "blob",
            "source_url": "https://example.test/source",
            "repository_fork": True,
            "raw_url": "https://raw.githubusercontent.com/owner/mirror/" + "a" * 40 + "/_archive/demo/SKILL.md",
        }
        report = build_report(source, record=record)
        self.assertEqual(report["source_context"]["status"], "review-source")
        self.assertEqual(
            report["source_context"]["signals"],
            ["repository-fork", "copy-or-mirror-path", "dormant-path"],
        )
        self.assertFalse(report["review_checklist"]["primary_source_context"])


if __name__ == "__main__":
    unittest.main()
