from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RefreshWorkflowTests(unittest.TestCase):
    def test_release_action_uses_node24_generation(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("softprops/action-gh-release@v3.0.3", workflow)
        self.assertNotIn("softprops/action-gh-release@v2", workflow)

    def test_daily_incremental_refresh_is_serial_and_non_interrupting(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertIn('cron: "17 3 * * *"', workflow)
        self.assertIn("group: refresh-skill-catalog", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertIn("target=$((current + 100))", workflow)
        self.assertIn("--max-rate-wait 120", workflow)
        self.assertIn('"$crawl_status" -ne 2', workflow)
        self.assertIn('echo "changed=false" >> "$GITHUB_OUTPUT"', workflow)
        self.assertEqual(
            workflow.count("if: steps.crawl.outputs.changed == 'true'"),
            3,
        )

    def test_public_freshness_metadata_matches_daily_schedule(self):
        catalog_docs = (ROOT / "catalog/README.md").read_text(encoding="utf-8")
        sitemap = (ROOT / "site/sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("Daily refreshes", catalog_docs)
        self.assertIn("rebuilds this index daily", catalog_docs)
        self.assertEqual(sitemap.count("<changefreq>daily</changefreq>"), 2)


if __name__ == "__main__":
    unittest.main()
