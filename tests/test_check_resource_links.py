from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_resource_links import extract_urls


ROOT = Path(__file__).resolve().parents[1]


class ResourceLinkCheckTests(unittest.TestCase):
    def test_extracts_external_links_and_skips_release_archives(self):
        urls = extract_urls((ROOT / "docs/starter-packs.md", ROOT / "docs/quickstart.md"))
        self.assertIn("https://github.com/sandbaseai/workbuddy-skill/releases/latest", urls)
        self.assertNotIn("https://sandbaseai.github.io/workbuddy-skill/packages.html", urls)
        self.assertNotIn(
            "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/code-review-excellence-workbuddy-skill.zip",
            urls,
        )

    def test_default_sources_include_the_public_readme(self):
        source = (ROOT / "scripts/check_resource_links.py").read_text(encoding="utf-8")
        self.assertIn('ROOT / "README.md"', source)
        self.assertIn('ROOT / "CHANGELOG.md"', source)
        self.assertIn('ROOT / "SUPPORT.md"', source)
        self.assertIn('ROOT / "SECURITY.md"', source)
        self.assertIn('ROOT / "catalog/README.md"', source)

    def test_extracts_json_urls_without_quotes_or_following_markup(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "generated.html"
            path.write_text(
                '<script>{"url":"https://example.com/pinned/SKILL.md"}</script>',
                encoding="utf-8",
            )
            self.assertEqual(
                extract_urls((path,)),
                ["https://example.com/pinned/SKILL.md"],
            )

    def test_skips_pinned_skill_source_checks_from_generated_package_page(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "packages.html"
            path.write_text(
                '<a href="https://github.com/example/repo/blob/abc/skills/demo/SKILL.md">source</a>'
                '<a href="https://github.com/example/repo">repo</a>',
                encoding="utf-8",
            )
            self.assertEqual(extract_urls((path,)), ["https://github.com/example/repo"])

    def test_workflow_runs_read_only_scheduled_check(self):
        workflow = (ROOT / ".github/workflows/check-resource-links.yml").read_text(encoding="utf-8")
        self.assertIn('cron: "17 4 * * 1"', workflow)
        self.assertIn("timeout-minutes: 10", workflow)
        self.assertIn("pull_request:", workflow)
        self.assertIn('"docs/**"', workflow)
        self.assertIn("python3 scripts/build_site_data.py", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("scripts/check_resource_links.py", workflow)

    def test_rate_limited_links_are_warnings_not_hard_failures(self):
        source = (ROOT / "scripts/check_resource_links.py").read_text(encoding="utf-8")
        self.assertIn("if status == 429:", source)
        self.assertIn("rate_limited", source)


if __name__ == "__main__":
    unittest.main()
