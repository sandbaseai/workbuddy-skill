from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from catalog_signals import source_context, source_signals  # noqa: E402


class CatalogSignalTests(unittest.TestCase):
    def test_primary_looking_source_has_no_context_signals(self):
        row = {
            "repository": "owner/project",
            "path": "skills/research/SKILL.md",
            "repository_fork": False,
        }
        self.assertEqual(source_signals(row), [])
        self.assertEqual(source_context(row), "primary-looking")

    def test_fork_mirror_and_dormant_paths_are_reported(self):
        row = {
            "repository": "owner/skills-mirror",
            "path": "mirrors/vendor/_archive/research/SKILL.md",
            "repository_fork": True,
        }
        self.assertEqual(
            source_signals(row),
            ["repository-fork", "copy-or-mirror-path", "dormant-path"],
        )
        self.assertEqual(source_context(row), "review-source")

    def test_substrings_do_not_create_false_path_signals(self):
        row = {
            "repository": "owner/legacycraft",
            "path": "skills/backup-plan/SKILL.md",
            "repository_fork": False,
        }
        self.assertEqual(source_signals(row), [])


if __name__ == "__main__":
    unittest.main()
