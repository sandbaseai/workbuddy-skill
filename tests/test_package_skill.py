from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/package_skill.sh"


class PackageSkillScriptTests(unittest.TestCase):
    def test_help_does_not_start_packaging(self):
        result = subprocess.run(
            ["sh", str(SCRIPT), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage: scripts/package_skill.sh", result.stdout)
        self.assertNotIn("Created ", result.stdout)

    def test_unexpected_argument_is_rejected(self):
        result = subprocess.run(
            ["sh", str(SCRIPT), "unexpected"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("takes no positional arguments", result.stderr)


if __name__ == "__main__":
    unittest.main()
