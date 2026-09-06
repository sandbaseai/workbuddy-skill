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

    def test_quickstarts_link_reference_resources_without_endorsing_them(self):
        for name in ("docs/quickstart.md", "docs/quickstart.zh-CN.md"):
            quickstart = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("https://github.com/AlephAITech/WorkBuddyGuide", quickstart)
            self.assertIn("https://github.com/Tencent/workbuddy-bench", quickstart)
            self.assertTrue(
                "trust endorsements" in quickstart or "不构成信任背书" in quickstart
            )

    def test_resource_maps_cover_both_languages_and_the_main_paths(self):
        for name in ("docs/resources.md", "docs/resources.zh-CN.md"):
            resources = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("workbuddy.ai/docs", resources)
            self.assertIn("WorkBuddyGuide", resources)
            self.assertIn("AI-Coding-Guide-Zh", resources)
            self.assertIn("learn-workbuddy", resources)
            self.assertIn("workbuddy-bench", resources)
            self.assertIn("Skill Atlas", resources)
            self.assertIn("use-cases.md", resources)

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

    def test_contributing_docs_describe_safe_auto_merge_settings(self):
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("GitHub auto-merge is enabled", contributing)
        self.assertIn("merged branches are deleted", contributing)
        self.assertIn("does not bypass validation", contributing)

    def test_unreleased_changelog_covers_current_public_improvements(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        unreleased = changelog.split("## [", 1)[0]
        for phrase in (
            "bilingual WorkBuddy resource maps",
            "current count of reviewed WorkBuddy packages",
            "full `catalog id`",
            "`SHA256SUMS` verification",
            "Chinese official Automation",
            "GitHub auto-merge governance",
        ):
            self.assertIn(phrase, unreleased)

    def test_feedback_templates_match_the_frozen_catalog_scope(self):
        feature = (ROOT / ".github/ISSUE_TEMPLATE/feature.yml").read_text(encoding="utf-8")
        showcase = (ROOT / ".github/ISSUE_TEMPLATE/showcase.yml").read_text(encoding="utf-8")
        self.assertIn("Existing reviewed package or workflow", feature)
        self.assertIn("Documentation or usability", feature)
        self.assertIn("Skill, connector, or external capability", showcase)
        self.assertIn("frozen snapshot", feature)

    def test_pull_request_template_preserves_frozen_catalog_and_validation_gates(self):
        template = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("did not add catalog records", template)
        self.assertIn("source commit, license, compatibility notes", template)
        self.assertIn("python3 scripts/validate_catalog.py --minimum 10000", template)
        self.assertIn("python3 -m unittest discover -s tests -q", template)
        self.assertIn("human review", template)

    def test_contributing_docs_describe_required_main_branch_checks(self):
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("main` branch requires the `validate` status check", contributing)
        self.assertIn("conversation resolution", contributing)
        self.assertIn("admin enforcement remains off", contributing)

    def test_support_points_to_resource_and_use_case_guides(self):
        support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("docs/resources.md", support)
        self.assertIn("docs/use-cases.md", support)
        self.assertIn("docs/resources.zh-CN.md", support)
        self.assertIn("docs/quickstart.zh-CN.md", support)

    def test_support_has_separate_showcase_and_discussion_paths(self):
        support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("template=showcase.yml", support)
        self.assertIn("github.com/sandbaseai/workbuddy-skill/discussions", support)

    def test_starter_packs_reference_existing_curated_packages(self):
        curated = (ROOT / "catalog/curated.json").read_text(encoding="utf-8")
        for path in ("docs/starter-packs.md", "docs/starter-packs.zh-CN.md"):
            content = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("latest/download/", content)
            for skill in ("code-review-excellence", "debugging-strategies", "mcp-security-audit"):
                self.assertIn(f'"skill": "{skill}"', curated)
                self.assertIn(f"{skill}-workbuddy-skill.zip", content)

    def test_resource_maps_label_external_references_and_rights_boundaries(self):
        for path in ("docs/resources.md", "docs/resources.zh-CN.md", "site/llms.txt"):
            content = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("zjp1997720/zhijian-ai-bluebook-workbuddy-harness", content)
            self.assertIn("staruhub/awesome-workbuddy", content)
            self.assertIn("infometa/workbuddyskills", content)
        english = (ROOT / "docs/resources.md").read_text(encoding="utf-8")
        chinese = (ROOT / "docs/resources.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("not as a trust or license decision", english)
        self.assertIn("不替代信任或许可证判断", chinese)
        self.assertIn("https://workbuddy.homes", english)
        self.assertIn("https://zjp1997720.github.io/zhijian-ai-bluebook-workbuddy-harness/", chinese)


if __name__ == "__main__":
    unittest.main()
