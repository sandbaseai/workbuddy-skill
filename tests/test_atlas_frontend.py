from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AtlasFrontendTests(unittest.TestCase):
    def setUp(self):
        self.app = (ROOT / "site/app.js").read_text(encoding="utf-8")
        self.styles = (ROOT / "site/styles.css").read_text(encoding="utf-8")
        self.english = (ROOT / "site/index.html").read_text(encoding="utf-8")
        self.chinese = (ROOT / "site/zh-CN.html").read_text(encoding="utf-8")

    def test_both_languages_expose_shareable_result_controls(self):
        for page in (self.english, self.chinese):
            self.assertIn('id="copy-link"', page)
            self.assertIn('id="language-link"', page)
            self.assertIn('id="snapshot-note"', page)
            self.assertIn('id="hero-count"', page)
            self.assertIn('aria-live="polite"', page)
            self.assertIn("/discussions", page)

    def test_url_state_supports_sharing_and_browser_history(self):
        self.assertIn("new URLSearchParams(location.search)", self.app)
        self.assertIn("copySearchLink", self.app)
        self.assertIn('window.addEventListener("popstate"', self.app)
        self.assertIn('history[`${historyMode}State`]', self.app)
        self.assertIn('search({ historyMode: "push" })', self.app)
        self.assertIn("syncLanguageLink", self.app)
        self.assertIn("control.value = control.options[0].value", self.app)
        self.assertIn("meta.records.toLocaleString()", self.app)
        self.assertIn("heroCount.textContent", self.app)
        self.assertIn('meta.snapshot_frozen !== true', self.app)

    def test_mobile_navigation_can_wrap(self):
        self.assertIn(".nav { height: auto;", self.styles)
        self.assertIn("flex-wrap: wrap", self.styles)
        self.assertIn("nav { flex: 1 1 100%;", self.styles)


if __name__ == "__main__":
    unittest.main()
