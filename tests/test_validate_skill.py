from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_skill.py"


class ValidateSkillTests(unittest.TestCase):
    def run_validator(self, skill_text: str):
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            skill_dir = skills_root / "demo"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), "--skills-root", str(skills_root)],
                capture_output=True,
                text=True,
            )

    def test_requires_standard_metadata_and_body(self):
        result = self.run_validator("---\ndescription: Demo\n---\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing frontmatter: author, description_en, description_zh, name, version", result.stderr)

    def test_accepts_a_complete_skill(self):
        result = self.run_validator(
            "---\nname: demo\ndescription: Demo\n"
            "description_zh: 演示\ndescription_en: Demo\n"
            "version: 1.0.0\nauthor: Test\n---\n\n# Demo\n"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_requires_name_to_match_directory(self):
        result = self.run_validator(
            "---\nname: another-skill\ndescription: Demo\n"
            "description_zh: 演示\ndescription_en: Demo\n"
            "version: 1.0.0\nauthor: Test\n---\n\n# Demo\n"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("name must match its directory", result.stderr)

    def test_rejects_array_allowed_tools(self):
        result = self.run_validator(
            "---\nname: demo\ndescription: Demo\n"
            "description_zh: 演示\ndescription_en: Demo\n"
            "version: 1.0.0\nauthor: Test\nallowed-tools: [Read, Write]\n"
            "---\n\n# Demo\n"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("allowed-tools must be", result.stderr)


if __name__ == "__main__":
    unittest.main()
