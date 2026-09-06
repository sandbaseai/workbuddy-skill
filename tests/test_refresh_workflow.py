from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RefreshWorkflowTests(unittest.TestCase):
    def test_release_action_uses_node24_generation(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("softprops/action-gh-release@v3.0.3", workflow)
        self.assertNotIn("softprops/action-gh-release@v2", workflow)

    def test_catalog_refresh_is_frozen_without_automatic_additions(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertNotIn('cron: "17 */6 * * *"', workflow)
        self.assertIn("if: ${{ false }}", workflow)
        self.assertIn("group: refresh-skill-catalog", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertIn("The public catalog is intentionally frozen", workflow)

    def test_public_freshness_metadata_matches_site_schedule(self):
        catalog_docs = (ROOT / "catalog/README.md").read_text(encoding="utf-8")
        sitemap = (ROOT / "site/sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("published snapshot is currently", catalog_docs)
        self.assertIn("refresh workflow is currently frozen", catalog_docs)
        self.assertEqual(sitemap.count("<changefreq>daily</changefreq>"), 2)

    def test_pages_actions_use_current_node_runtime_generations(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/configure-pages@v6", workflow)
        self.assertIn("actions/upload-pages-artifact@v5", workflow)
        self.assertIn("actions/deploy-pages@v5", workflow)
        self.assertNotIn("actions/configure-pages@v5", workflow)
        self.assertNotIn("actions/upload-pages-artifact@v4", workflow)
        self.assertNotIn("actions/deploy-pages@v4", workflow)

    def test_concurrent_publish_reconciles_snapshots_before_retrying(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertIn("git rebase --abort", workflow)
        self.assertIn("rows[row[\"id\"]] = row", workflow)
        self.assertIn("git reset --hard origin/main", workflow)
        self.assertIn("git show origin/main:catalog/stats.json > /tmp/current-stats.json", workflow)
        self.assertIn("--stats /tmp/merged-stats.json", workflow)
        self.assertIn('sort_keys=True) + "\\n"', workflow)
        self.assertIn("reconcile concurrent catalog refresh", workflow)
        self.assertIn("scripts/validate_catalog.py --minimum 10000 --require-analysis", workflow)


if __name__ == "__main__":
    unittest.main()
