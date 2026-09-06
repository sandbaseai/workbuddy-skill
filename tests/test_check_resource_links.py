from pathlib import Path
import unittest

from scripts.check_resource_links import extract_urls


ROOT = Path(__file__).resolve().parents[1]


class ResourceLinkCheckTests(unittest.TestCase):
    def test_extracts_external_links_and_skips_release_archives(self):
        urls = extract_urls((ROOT / "docs/starter-packs.md", ROOT / "docs/quickstart.md"))
        self.assertIn("https://github.com/sandbaseai/workbuddy-skill/releases/latest", urls)
        self.assertNotIn(
            "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/code-review-excellence-workbuddy-skill.zip",
            urls,
        )

    def test_workflow_runs_read_only_scheduled_check(self):
        workflow = (ROOT / ".github/workflows/check-resource-links.yml").read_text(encoding="utf-8")
        self.assertIn('cron: "17 4 * * 1"', workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("scripts/check_resource_links.py", workflow)


if __name__ == "__main__":
    unittest.main()
