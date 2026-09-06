from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RefreshWorkflowTests(unittest.TestCase):
    def test_release_action_uses_node24_generation(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("softprops/action-gh-release@v3.0.3", workflow)
        self.assertNotIn("softprops/action-gh-release@v2", workflow)

    def test_release_validates_the_frozen_catalog_before_packaging(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn(
            "validate_catalog.py --minimum 10000 --require-analysis --check-stats",
            workflow,
        )

    def test_release_publishes_sha256_checksums(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("sha256sum *-workbuddy-skill.zip > SHA256SUMS", workflow)
        self.assertIn('gh release upload "$GITHUB_REF_NAME" dist/SHA256SUMS', workflow)

    def test_quickstarts_document_exact_release_download_and_verification(self):
        for name in ("docs/quickstart.md", "docs/quickstart.zh-CN.md"):
            quickstart = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("gh release download \\\n", quickstart)
            self.assertIn("--repo sandbaseai/workbuddy-skill", quickstart)
            self.assertIn("--pattern SHA256SUMS", quickstart)
            self.assertIn("sha256sum --check SHA256SUMS --ignore-missing", quickstart)

    def test_catalog_refresh_is_frozen_without_automatic_additions(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertNotIn("schedule:", workflow)
        self.assertNotIn("crawl_github_skills.py", workflow)
        self.assertNotIn("git push", workflow)
        self.assertIn("Verify frozen catalog", workflow)
        self.assertIn("--check-stats", workflow)

    def test_public_freshness_metadata_matches_site_schedule(self):
        catalog_docs = (ROOT / "catalog/README.md").read_text(encoding="utf-8")
        sitemap = (ROOT / "site/sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("The published snapshot is frozen", catalog_docs)
        self.assertIn("read-only frozen-catalog check", catalog_docs)
        self.assertEqual(sitemap.count("<changefreq>daily</changefreq>"), 2)

    def test_pages_actions_use_current_node_runtime_generations(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/configure-pages@v6", workflow)
        self.assertIn("actions/upload-pages-artifact@v5", workflow)
        self.assertIn("actions/deploy-pages@v5", workflow)
        self.assertNotIn("actions/configure-pages@v5", workflow)
        self.assertNotIn("actions/upload-pages-artifact@v4", workflow)
        self.assertNotIn("actions/deploy-pages@v4", workflow)

    def test_frozen_check_does_not_publish_changes(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertNotIn("git commit", workflow)
        self.assertNotIn("git push", workflow)
        self.assertNotIn("gh pr", workflow)
        self.assertIn("validate_catalog.py --minimum 10000 --require-analysis --check-stats", workflow)


if __name__ == "__main__":
    unittest.main()
