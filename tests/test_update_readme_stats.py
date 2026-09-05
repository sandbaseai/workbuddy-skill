import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeStatsTests(unittest.TestCase):
    def test_updates_root_and_catalog_readmes_from_same_stats(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            readme = temporary / "README.md"
            catalog_readme = temporary / "catalog.md"
            stats = temporary / "stats.json"
            analysis = temporary / "analysis.json"
            readme.write_text(
                "before\n<!-- CATALOG-METRICS:START -->\nold\n<!-- CATALOG-METRICS:END -->\n"
                "<!-- CATALOG-ANALYSIS:START -->\nold\n<!-- CATALOG-ANALYSIS:END -->\nafter\n",
                encoding="utf-8",
            )
            catalog_readme.write_text(
                "<!-- CATALOG-SNAPSHOT:START -->\nold\n<!-- CATALOG-SNAPSHOT:END -->\n",
                encoding="utf-8",
            )
            stats.write_text(
                json.dumps({"records": 10400, "unique_content_shas": 6700, "repositories": 5300}),
                encoding="utf-8",
            )
            analysis.write_text(
                json.dumps({
                    "adaptable": 9300,
                    "needs_review": 900,
                    "workbuddy_ready": 3,
                    "security_flagged": 270,
                }),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "update_readme_stats.py"),
                    "--readme", str(readme),
                    "--catalog-readme", str(catalog_readme),
                    "--stats", str(stats),
                    "--analysis", str(analysis),
                ],
                check=True,
            )
            root_content = readme.read_text(encoding="utf-8")
            catalog_content = catalog_readme.read_text(encoding="utf-8")
            self.assertIn("| Indexed GitHub paths | 10,400 |", root_content)
            self.assertIn("9,300 are structurally adaptable", root_content)
            self.assertIn("- 10,400 indexed GitHub paths", catalog_content)
            self.assertIn("- 6,700 unique Git blob SHAs", catalog_content)
            self.assertIn("- 5,300 source repositories", catalog_content)

    def test_catalog_only_does_not_require_or_modify_root_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            readme = temporary / "README.md"
            catalog_readme = temporary / "catalog.md"
            stats = temporary / "stats.json"
            analysis = temporary / "analysis.json"
            root_content = "public README without internal build markers\n"
            readme.write_text(root_content, encoding="utf-8")
            catalog_readme.write_text(
                "<!-- CATALOG-SNAPSHOT:START -->\nold\n<!-- CATALOG-SNAPSHOT:END -->\n",
                encoding="utf-8",
            )
            stats.write_text(
                json.dumps({"records": 12757, "unique_content_shas": 8130, "repositories": 6434}),
                encoding="utf-8",
            )
            analysis.write_text(
                json.dumps({"adaptable": 10069, "needs_review": 910, "workbuddy_ready": 0, "security_flagged": 431}),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "update_readme_stats.py"),
                    "--catalog-only",
                    "--readme", str(readme),
                    "--catalog-readme", str(catalog_readme),
                    "--stats", str(stats),
                    "--analysis", str(analysis),
                ],
                check=True,
            )
            self.assertEqual(readme.read_text(encoding="utf-8"), root_content)
            self.assertIn("- 12,757 indexed GitHub paths", catalog_readme.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
