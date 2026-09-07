from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RefreshWorkflowTests(unittest.TestCase):
    def test_refresh_workflow_probes_upstream_sources_without_publishing(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertIn("upstream-discovery-probe:", workflow)
        self.assertIn("--dry-run", workflow)
        self.assertIn("--repository-only", workflow)
        for repository in (
            "github/awesome-copilot",
            "aiworkskills/wechat-article-skills",
            "anthropics/skills",
            "mattpocock/skills",
            "addyosmani/agent-skills",
            "vercel-labs/agent-skills",
            "vercel-labs/skills",
            "google/skills",
            "ComposioHQ/awesome-claude-skills",
            "alirezarezvani/claude-skills",
            "wshobson/agents",
            "K-Dense-AI/scientific-agent-skills",
            "phuryn/pm-skills",
            "JimLiu/baoyu-skills",
            "nexu-io/open-design",
            "googleworkspace/cli",
        ):
            self.assertIn(f"--repository {repository}", workflow)
        self.assertIn("--target 10000", workflow)
        self.assertIn("--output /tmp/upstream-skill-probe.jsonl", workflow)
        self.assertIn("--dry-run-output /tmp/upstream-skill-probe-report.jsonl", workflow)
        self.assertIn("scripts/report_new_discoveries.py", workflow)
        self.assertIn("--output /tmp/upstream-skill-new-candidates.jsonl", workflow)
        self.assertIn("scripts/analyze_discovery.py", workflow)
        self.assertIn("/tmp/upstream-skill-new-candidates-reviewed.jsonl", workflow)
        self.assertIn("--summary-output /tmp/upstream-skill-discovery-summary.json", workflow)
        self.assertIn("GITHUB_STEP_SUMMARY", workflow)
        self.assertIn("/tmp/upstream-skill-discovery-summary.json", workflow)
        self.assertIn("actions/upload-artifact@v7", workflow)
        self.assertIn("retention-days: 7", workflow)
        self.assertNotIn("--allow-frozen-catalog", workflow)

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
        self.assertIn("scripts/build_site_data.py", workflow)
        self.assertIn("scripts/validate_site_data.py", workflow)
        self.assertIn("scripts/verify_catalog_snapshot.py", workflow)

    def test_release_publishes_sha256_checksums(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("sha256sum *-workbuddy-skill.zip > SHA256SUMS", workflow)
        self.assertIn('gh release upload "$GITHUB_REF_NAME" dist/SHA256SUMS', workflow)
        self.assertIn("Verify uploaded assets", workflow)
        self.assertIn("Missing uploaded release asset", workflow)
        self.assertIn("Verify downloaded release checksums", workflow)
        self.assertIn('gh release download "$GITHUB_REF_NAME"', workflow)
        self.assertIn("python3 scripts/verify_release.py release-download", workflow)

    def test_packaging_rejects_symlinks(self):
        script = (ROOT / "scripts/package_skill.sh").read_text(encoding="utf-8")
        self.assertIn("path.is_symlink()", script)
        self.assertIn("symlink is not allowed", script)

    def test_quickstarts_document_exact_release_download_and_verification(self):
        for name in ("docs/quickstart.md", "docs/quickstart.zh-CN.md"):
            quickstart = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("gh release download \\\n", quickstart)
            self.assertIn("--clobber", quickstart)
            self.assertIn("--repo sandbaseai/workbuddy-skill", quickstart)
            self.assertIn("--pattern SHA256SUMS", quickstart)
            self.assertIn("sha256sum --check SHA256SUMS --ignore-missing", quickstart)
            self.assertIn("scripts/verify_release.py", quickstart)
            self.assertIn("no-static-flags", quickstart)
            if name.endswith("zh-CN.md"):
                self.assertIn("额外 WorkBuddy ZIP", quickstart)
            else:
                self.assertIn("rejects an extra WorkBuddy ZIP", quickstart)
            self.assertIn("open.workbuddy.cn", quickstart)
            self.assertIn("Permission-Modes", quickstart)
            self.assertIn("Ask", quickstart)
            self.assertIn("Plan", quickstart)
            self.assertIn("Craft", quickstart)
            self.assertIn("Function-Description/Model", quickstart)
            self.assertIn("Function-Description/Skills-Market", quickstart)
            self.assertIn("Skill Marketplace", quickstart)
            expected_connector = (
                "open.workbuddy.cn/docs/connector"
                if name.endswith("zh-CN.md")
                else "open.workbuddy.cn/en/docs/connector"
            )
            self.assertIn(expected_connector, quickstart)
            if name.endswith("zh-CN.md"):
                self.assertIn("只读", quickstart)
                self.assertIn("API Key", quickstart)
            else:
                self.assertIn("read-only", quickstart.lower())
                self.assertIn("API keys", quickstart)
            self.assertIn("cli.github.com/manual/gh_skill", quickstart)
            if name.endswith("zh-CN.md"):
                self.assertIn("open.workbuddy.cn/docs/what-is-open-platform", quickstart)
                self.assertIn("open.workbuddy.cn/docs/onboarding", quickstart)
            else:
                self.assertIn("open.workbuddy.cn/en/docs/what-is-open-platform", quickstart)
                self.assertIn("open.workbuddy.cn/en/docs/onboarding", quickstart)

    def test_quickstarts_document_host_scope_and_version_pinning(self):
        for name in ("docs/quickstart.md", "docs/quickstart.zh-CN.md"):
            quickstart = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("--agent codex", quickstart)
            self.assertIn("--scope project", quickstart)
            self.assertIn('gh release view --repo sandbaseai/workbuddy-skill --json tagName --jq .tagName', quickstart)
            self.assertIn('--pin "$release_tag"', quickstart)
            self.assertIn("cli.github.com/manual/gh_skill_install", quickstart)

    def test_quickstarts_distinguish_gh_skill_from_workbuddy_zip_import(self):
        english = (ROOT / "docs/quickstart.md").read_text(encoding="utf-8")
        chinese = (ROOT / "docs/quickstart.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("not WorkBuddy desktop's ZIP importer", english)
        self.assertIn("不是 WorkBuddy 桌面端的 ZIP 导入功能", chinese)

    def test_quickstarts_use_catalog_metadata_for_current_size(self):
        for name in ("docs/quickstart.md", "docs/quickstart.zh-CN.md"):
            quickstart = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("catalog-meta.json", quickstart)
            self.assertIn("records", quickstart)
            self.assertNotIn("21,818", quickstart)

    def test_quickstarts_explain_reviewed_package_filter(self):
        english = (ROOT / "docs/quickstart.md").read_text(encoding="utf-8")
        chinese = (ROOT / "docs/quickstart.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("WorkBuddy package → Reviewed package available", english)
        self.assertIn("WorkBuddy 包状态 → 有精选包可用", chinese)

    def test_quickstarts_link_reference_resources_without_endorsing_them(self):
        for name in ("docs/quickstart.md", "docs/quickstart.zh-CN.md"):
            quickstart = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("https://github.com/AlephAITech/WorkBuddyGuide", quickstart)
            self.assertIn("https://github.com/Tencent/workbuddy-bench", quickstart)
            self.assertTrue(
                "exact source and license" in quickstart
                or "具体来源和许可证" in quickstart
            )

    def test_chinese_quickstart_routes_to_chinese_support(self):
        quickstart = (ROOT / "docs/quickstart.zh-CN.md").read_text(encoding="utf-8")
        support = (ROOT / "SUPPORT.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("SUPPORT.zh-CN.md", quickstart)
        self.assertIn("中文支持说明", quickstart)
        self.assertIn("不会新增 Skill 记录", support)

    def test_resource_maps_cover_both_languages_and_the_main_paths(self):
        for name in ("docs/resources.md", "docs/resources.zh-CN.md"):
            resources = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("workbuddy.ai/docs", resources)
            expected_open_platform = (
                "open.workbuddy.cn/zh/docs/skill"
                if name.endswith("zh-CN.md")
                else "open.workbuddy.cn/en/docs/skill"
            )
            self.assertIn(expected_open_platform, resources)
            expected_onboarding = (
                "open.workbuddy.cn/docs/onboarding"
                if name.endswith("zh-CN.md")
                else "open.workbuddy.cn/en/docs/onboarding"
            )
            self.assertIn(expected_onboarding, resources)
            self.assertIn("WorkBuddyGuide", resources)
            self.assertIn("workbuddy-account-migrate", resources)
            self.assertIn("self-media-compliance-review", resources)
            self.assertIn("gks-QianLV-uiSkill", resources)
            self.assertIn("CodeDrobe/skills", resources)
            self.assertIn("CodeDrobe/core", resources)
            self.assertIn("ontology-driven-dev", resources)
            self.assertIn("WorkBuddy-AppBuilderSkill", resources)
            self.assertIn("image-story-video-wizard", resources)
            self.assertIn("nuwa-skill", resources)
            self.assertIn("qa-testing-guide", resources)
            self.assertIn("wechat-article-skills", resources)
            self.assertIn("agentic-awesome-skills", resources)
            self.assertIn("awesome-agent-skills", resources)
            self.assertIn("vanillagreencom/kendex", resources)
            self.assertIn("Hisn00w/ASu-skills", resources)
            self.assertIn("TencentDB-Agent-Memory", resources)
            self.assertIn("AI-Coding-Guide-Zh", resources)
            self.assertIn("ecommerce-visual-copywriting-skill", resources)
            self.assertIn("agency-agents-zh", resources)
            if name.endswith("zh-CN.md"):
                self.assertIn("MIT 许可、覆盖工程、设计、营销、金融等工作流", resources)
                self.assertIn("MIT 许可、明确兼容 WorkBuddy 的电商视觉文案工作流", resources)
                self.assertNotIn("仓库当前未声明许可证", resources)
            else:
                self.assertIn("MIT-licensed Chinese collection", resources)
                self.assertIn("an MIT-licensed WorkBuddy-compatible e-commerce visual-copy workflow", resources)
                self.assertNotIn("no repository license is currently declared", resources)
            self.assertIn("workbuddy-usage-status", resources)
            self.assertIn("markitdown-skill", resources)
            self.assertIn("learn-workbuddy", resources)
            self.assertIn("workbuddy-harness", resources)
            self.assertIn("yinqd3/workbuddy-skills", resources)
            self.assertIn("oh-my-workbuddy", resources)
            self.assertIn("open.workbuddy.cn", resources)
            self.assertIn("cli.github.com/manual/gh_skill", resources)
            self.assertIn("agentskills.io/specification", resources)
            self.assertIn("what-is-open-platform", resources)
            self.assertIn("Efficient-Tips", resources)
            self.assertIn("/FQA", resources)
            self.assertIn("workbuddy-bench", resources)
            self.assertIn("2602.12670", resources)
            self.assertIn("2606.11435", resources)
            self.assertIn("workbuddy-skill-groups", resources)
            self.assertIn("Skill Atlas", resources)
            self.assertIn("use-cases.md", resources)

        self.assertIn(
            "Search current GitHub Skill files",
            (ROOT / "docs/catalog-guide.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "在 GitHub 搜索当前 Skill 文件",
            (ROOT / "docs/catalog-guide.zh-CN.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "GitHub's current `SKILL.md` code search",
            (ROOT / "site/llms.txt").read_text(encoding="utf-8"),
        )

    def test_catalog_refresh_is_frozen_without_automatic_additions(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertIn('cron: "17 5 * * *"', workflow)
        self.assertNotIn("--allow-frozen-catalog", workflow)
        self.assertNotIn("git push", workflow)
        self.assertIn("Verify frozen catalog", workflow)
        self.assertIn("--check-stats", workflow)
        self.assertIn("scripts/update_readme_stats.py --catalog-only", workflow)
        self.assertIn("git diff --exit-code -- catalog/README.md", workflow)
        self.assertIn("scripts/build_site_data.py", workflow)
        self.assertIn("scripts/validate_site_data.py", workflow)
        self.assertIn("scripts/verify_catalog_snapshot.py", workflow)
        self.assertIn("scripts/check_release_assets.py", workflow)
        self.assertIn("GH_TOKEN: ${{ github.token }}", workflow)
        self.assertIn("scripts/check_resource_links.py", workflow)

    def test_resource_link_check_is_read_only_and_scheduled(self):
        workflow = (ROOT / ".github/workflows/check-resource-links.yml").read_text(encoding="utf-8")
        self.assertIn("schedule:", workflow)
        self.assertIn("pull_request:", workflow)
        self.assertIn('"README.md"', workflow)
        self.assertIn('"scripts/build_site_data.py"', workflow)
        self.assertIn("workflow_dispatch", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("scripts/check_resource_links.py", workflow)

    def test_readme_keeps_internal_catalog_governance_out_of_the_user_entrypoint(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("21,818", readme)
        self.assertIn("冻结的公开快照", readme)
        self.assertIn("frozen public snapshot", readme)
        self.assertIn("For English readers", readme)
        self.assertIn("English quickstart", readme)
        self.assertIn("给项目加一个 Star](https://github.com/sandbaseai/workbuddy-skill)", readme)
        self.assertIn("[Star the project](https://github.com/sandbaseai/workbuddy-skill)", readme)
        self.assertIn("actions/workflows/validate.yml/badge.svg", readme)
        self.assertIn("actions/workflows/pages.yml/badge.svg", readme)
        self.assertIn("actions/workflows/check-resource-links.yml/badge.svg", readme)
        self.assertNotIn("admin enforcement", readme.lower())
        self.assertNotIn("re-enable the crawler", readme.lower())
        self.assertNotIn("future maintenance focuses", readme.lower())

    def test_readme_exposes_a_three_step_user_path_in_both_languages(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("### 最短路径", readme)
        self.assertIn("### Three-step start", readme)
        self.assertIn("SHA256SUMS", readme)
        self.assertIn("Reviewed package available", readme)

    def test_readme_public_counts_match_catalog_and_curated_data(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        stats = json.loads((ROOT / "catalog/stats.json").read_text(encoding="utf-8"))
        curated = json.loads((ROOT / "catalog/curated.json").read_text(encoding="utf-8"))
        records = f"{stats['records']:,}"
        packages = f"{len(curated):,}"
        self.assertIn(f"当前公开目录包含 **{records} 条", readme)
        self.assertIn(f"另有 **{packages} 个经过审阅", readme)
        self.assertIn(f"contains **{records} indexed", readme)
        self.assertIn(f"alongside **{packages} reviewed", readme)

    def test_external_sandbase_migration_pointer_is_not_a_skill(self):
        pointer = (ROOT / "skills/sandbase/README.md").read_text(encoding="utf-8")
        self.assertIn("awesome-workbuddy/tree/main/skills/sandbase", pointer)
        self.assertIn("contains no\n`SKILL.md`", pointer)
        self.assertFalse((ROOT / "skills/sandbase/SKILL.md").exists())

    def test_catalog_guides_document_catalog_id_roundtrip(self):
        for path in ("docs/catalog-guide.md", "docs/catalog-guide.zh-CN.md"):
            guide = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("scripts/query_catalog.py 'github:owner/repository:path/to/SKILL.md'", guide)

    def test_catalog_guides_document_reviewed_package_cli_filter(self):
        for path in ("docs/catalog-guide.md", "docs/catalog-guide.zh-CN.md"):
            guide = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("--package-status reviewed", guide)

    def test_catalog_guides_document_chinese_category_alias(self):
        self.assertIn("Chinese labels such as `研究`", (ROOT / "docs/catalog-guide.md").read_text(encoding="utf-8"))
        self.assertIn("直接写 `研究`", (ROOT / "docs/catalog-guide.zh-CN.md").read_text(encoding="utf-8"))

    def test_catalog_guides_distinguish_compatibility_and_package_signals(self):
        english = (ROOT / "docs/catalog-guide.md").read_text(encoding="utf-8")
        chinese = (ROOT / "docs/catalog-guide.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("Reviewed package availability", english)
        self.assertIn("精选包是否可用", chinese)

    def test_catalog_readme_stays_user_facing_and_site_schedule_is_published(self):
        catalog_docs = (ROOT / "catalog/README.md").read_text(encoding="utf-8")
        sitemap = (ROOT / "site/sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("Search locally", catalog_docs)
        self.assertNotIn("Snapshot maintenance", catalog_docs)
        self.assertNotIn("The published snapshot is frozen", catalog_docs)
        self.assertNotIn("auto-merge", catalog_docs.lower())
        self.assertEqual(sitemap.count("<changefreq>daily</changefreq>"), 2)
        self.assertIn("https://sandbaseai.github.io/workbuddy-skill/catalog.json", sitemap)
        self.assertIn("https://sandbaseai.github.io/workbuddy-skill/packages.json", sitemap)
        self.assertIn("https://sandbaseai.github.io/workbuddy-skill/packages.html", sitemap)
        self.assertIn("https://sandbaseai.github.io/workbuddy-skill/categories.html", sitemap)
        self.assertIn("https://sandbaseai.github.io/workbuddy-skill/llms.txt", sitemap)

    def test_pages_actions_use_current_node_runtime_generations(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/configure-pages@v6", workflow)
        self.assertIn("actions/upload-pages-artifact@v5", workflow)
        self.assertIn("actions/deploy-pages@v5", workflow)
        self.assertNotIn("actions/configure-pages@v5", workflow)
        self.assertNotIn("actions/upload-pages-artifact@v4", workflow)
        self.assertNotIn("actions/deploy-pages@v4", workflow)

    def test_long_running_jobs_have_explicit_timeouts(self):
        expected = {
            ".github/workflows/validate.yml": "timeout-minutes: 15",
            ".github/workflows/release.yml": "timeout-minutes: 30",
            ".github/workflows/pages.yml": "timeout-minutes: 10",
            ".github/workflows/refresh-catalog.yml": "timeout-minutes: 10",
            ".github/workflows/cleanup-merged-branches.yml": "timeout-minutes: 10",
        }
        for path, marker in expected.items():
            with self.subTest(path=path):
                self.assertIn(marker, (ROOT / path).read_text(encoding="utf-8"))

    def test_dependabot_tracks_github_actions_without_runtime_dependencies(self):
        dependabot = (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8")
        self.assertIn("package-ecosystem: github-actions", dependabot)
        self.assertIn('directory: "/"', dependabot)
        self.assertIn("interval: weekly", dependabot)
        self.assertIn("open-pull-requests-limit: 5", dependabot)

    def test_codeql_scans_python_and_github_actions(self):
        workflow = (ROOT / ".github/workflows/codeql.yml").read_text(encoding="utf-8")
        self.assertIn("github/codeql-action/init@v4", workflow)
        self.assertIn("github/codeql-action/analyze@v4", workflow)
        self.assertIn("language: python", workflow)
        self.assertIn("language: actions", workflow)
        self.assertIn("security-events: write", workflow)
        self.assertIn("timeout-minutes: 20", workflow)

    def test_validate_workflow_checks_generated_site_data(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        self.assertIn("scripts/build_site_data.py", workflow)
        self.assertIn("node --check site/app.js", workflow)
        self.assertIn("scripts/validate_site_data.py", workflow)
        self.assertIn("scripts/verify_catalog_snapshot.py", workflow)

    def test_catalog_guides_keep_user_facing_installation_guidance(self):
        for path in ("docs/catalog-guide.md", "docs/catalog-guide.zh-CN.md"):
            content = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("query_catalog.py", content)
            self.assertIn("adapt", content.lower())
            self.assertNotIn("verify_catalog_snapshot.py", content)

    def test_readme_gh_skill_examples_resolve_and_pin_the_current_release(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(readme.count('gh release view --repo sandbaseai/workbuddy-skill --json tagName --jq .tagName'), 3)
        self.assertEqual(readme.count('--pin "$release_tag"'), 3)
        self.assertNotIn("--pin v4.66.0", readme)

    def test_readme_exposes_high_signal_catalog_search(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(readme.count("python3 scripts/query_catalog.py research --high-signal --limit 10"), 2)
        self.assertEqual(readme.count("python3 scripts/query_catalog.py --category research --package-status reviewed --sort score --limit 10"), 2)

    def test_frozen_check_does_not_publish_changes(self):
        workflow = (ROOT / ".github/workflows/refresh-catalog.yml").read_text(encoding="utf-8")
        self.assertNotIn("git commit", workflow)
        self.assertNotIn("git push", workflow)
        self.assertNotIn("gh pr", workflow)
        self.assertIn('cron: "17 5 * * *"', workflow)
        self.assertIn("validate_catalog.py --minimum 10000 --require-analysis --check-stats", workflow)

    def test_contributing_docs_describe_safe_auto_merge_settings(self):
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("GitHub auto-merge is enabled", contributing)
        self.assertIn("merged branches are deleted", contributing)
        self.assertIn("does not bypass validation", contributing)
        self.assertIn("Pull requests from forks remain manual", contributing)
        self.assertIn("Analyze (actions)", contributing)
        self.assertIn("Analyze (python)", contributing)

    def test_auto_merge_only_queues_trusted_same_repository_pull_requests(self):
        workflow = (ROOT / ".github/workflows/auto-merge.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request_target", workflow)
        self.assertIn("group: auto-merge-pr-${{ github.event.pull_request.number }}", workflow)
        self.assertIn("cancel-in-progress: true", workflow)
        self.assertIn("timeout-minutes: 15", workflow)
        self.assertIn("ready_for_review", workflow)
        self.assertIn("HEAD_REPOSITORY", workflow)
        self.assertIn('[[ \"$HEAD_REPOSITORY\" != \"$GITHUB_REPOSITORY\" ]]', workflow)
        self.assertIn('[[ \"$DRAFT\" == \"true\" ]]', workflow)
        self.assertIn("AUTHOR_ASSOCIATION", workflow)
        self.assertIn("*,CONTRIBUTOR,*)", workflow)
        self.assertIn("author_association", workflow)
        self.assertIn("--auto --squash", workflow)
        self.assertNotIn("--auto --squash --delete-branch", workflow)
        self.assertIn('gh api --method DELETE "repos/$GITHUB_REPOSITORY/git/refs/heads/$BRANCH"', workflow)
        self.assertIn("Merged branch already deleted", workflow)
        self.assertNotIn("actions/checkout", workflow)

    def test_merged_branch_cleanup_only_deletes_safe_same_repository_refs(self):
        workflow = (ROOT / ".github/workflows/cleanup-merged-branches.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request_target:", workflow)
        self.assertIn("types: [closed]", workflow)
        self.assertIn('[[ "$MERGED" != "true" ]]', workflow)
        self.assertIn('[[ "$HEAD_REPOSITORY" != "$GITHUB_REPOSITORY" ]]', workflow)
        self.assertIn('[[ -z "$BRANCH" || "$BRANCH" == "main" ]]', workflow)
        self.assertIn("gh api --method DELETE", workflow)
        self.assertIn("Merged branch already deleted", workflow)
        self.assertNotIn("actions/checkout", workflow)

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
        bug = (ROOT / ".github/ISSUE_TEMPLATE/bug.yml").read_text(encoding="utf-8")
        feature = (ROOT / ".github/ISSUE_TEMPLATE/feature.yml").read_text(encoding="utf-8")
        showcase = (ROOT / ".github/ISSUE_TEMPLATE/showcase.yml").read_text(encoding="utf-8")
        package_feedback = (ROOT / ".github/ISSUE_TEMPLATE/package-feedback.yml").read_text(encoding="utf-8")
        self.assertIn("Existing reviewed package or workflow", feature)
        self.assertIn("Operating system and host", bug)
        self.assertIn("Reproduction steps", bug)
        self.assertIn("smallest public or synthetic input", bug)
        self.assertIn("Documentation or usability", feature)
        self.assertIn("public catalog is currently frozen", feature)
        self.assertIn("does not add new Skill records", feature)
        self.assertIn("Validation or provenance", feature)
        self.assertIn("Skill, connector, or external capability", showcase)
        self.assertIn("reproducible example", feature)
        self.assertIn("Failure stage", package_feedback)
        self.assertIn("SHA256 verification", package_feedback)
        self.assertIn("reviewed-package", package_feedback)

    def test_issue_template_config_routes_public_questions(self):
        config = (ROOT / ".github/ISSUE_TEMPLATE/config.yml").read_text(encoding="utf-8")
        self.assertIn("blank_issues_enabled: false", config)
        self.assertIn("/discussions", config)
        self.assertIn("/security/advisories/new", config)
        self.assertIn("SUPPORT.zh-CN.md", config)
        self.assertNotIn("#english", config)

    def test_pull_request_template_preserves_frozen_catalog_and_validation_gates(self):
        template = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("did not add catalog records", template)
        self.assertIn("source commit, license, compatibility notes", template)
        self.assertIn("python3 scripts/validate_catalog.py --minimum 10000", template)
        self.assertIn("python3 -m unittest discover -s tests -q", template)
        self.assertIn("human review", template)

    def test_contributing_docs_describe_required_main_branch_checks(self):
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("main` branch requires the `validate`, `Analyze (actions)`, and", contributing)
        self.assertIn("Conversation resolution", contributing)
        self.assertIn("admin enforcement remains off", contributing)

    def test_support_points_to_resource_and_use_case_guides(self):
        support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("docs/resources.md", support)
        self.assertIn("docs/use-cases.md", support)
        self.assertIn("docs/resources.zh-CN.md", support)
        self.assertIn("docs/quickstart.zh-CN.md", support)
        self.assertIn("sandbaseai.github.io/workbuddy-skill/packages.html", support)

    def test_use_cases_include_local_first_content_review(self):
        use_cases = (ROOT / "docs/use-cases.md").read_text(encoding="utf-8")
        self.assertIn("self-media-compliance-review", use_cases)
        self.assertIn("Pre-publication content review", use_cases)
        self.assertIn("不要发布", use_cases)
        self.assertIn("实时平台接口", use_cases)

    def test_support_has_separate_showcase_and_discussion_paths(self):
        support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("template=showcase.yml", support)
        self.assertIn("github.com/sandbaseai/workbuddy-skill/discussions", support)
        self.assertIn("desired outcome", support)
        self.assertNotIn("do not add new catalog records", support)

    def test_starter_packs_reference_existing_curated_packages(self):
        curated = (ROOT / "catalog/curated.json").read_text(encoding="utf-8")
        for path in ("docs/starter-packs.md", "docs/starter-packs.zh-CN.md"):
            content = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("latest/download/", content)
            for skill in ("code-review-excellence", "debugging-strategies", "evidence-map-builder", "mcp-security-audit"):
                self.assertIn(f'"skill": "{skill}"', curated)
                self.assertIn(f"{skill}-workbuddy-skill.zip", content)

    def test_resource_maps_label_external_references_and_rights_boundaries(self):
        for path in ("docs/resources.md", "docs/resources.zh-CN.md", "site/llms.txt"):
            content = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("zjp1997720/zhijian-ai-bluebook-workbuddy-harness", content)
            self.assertIn("staruhub/awesome-workbuddy", content)
            self.assertIn("infometa/workbuddyskills", content)
            self.assertIn("bitcjm/workbuddy-skills", content)
            self.assertIn("semlinker/awesome-workbuddy", content)
            self.assertIn("sunyet-01/WorkBuddy-Starter", content)
            self.assertIn("chonpszhou/workbuddy-chatcut-mcp", content)
            self.assertIn("zhuang-HE/workbuddy-harness", content)
        english = (ROOT / "docs/resources.md").read_text(encoding="utf-8")
        chinese = (ROOT / "docs/resources.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("not as a trust or license decision", english)
        self.assertIn("不替代信任或许可证判断", chinese)
        self.assertIn("https://workbuddy.homes", english)
        self.assertIn("https://zjp1997720.github.io/zhijian-ai-bluebook-workbuddy-harness/", chinese)


if __name__ == "__main__":
    unittest.main()
