from pathlib import Path
import tempfile
import unittest

from scripts.validate_source_manifest import read_repositories


ROOT = Path(__file__).resolve().parents[1]


class SourceManifestTests(unittest.TestCase):
    def test_repository_manifest_is_valid_and_unique(self):
        repositories = read_repositories(ROOT / "config/upstream-skill-sources.txt")
        self.assertGreaterEqual(len(repositories), 200)
        self.assertEqual(len(repositories), len(set(repositories)))

    def test_repository_manifest_rejects_duplicate_and_malformed_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "sources.txt"
            manifest.write_text("owner/repo\nowner/repo\nnot a repo\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate repository"):
                read_repositories(manifest)
