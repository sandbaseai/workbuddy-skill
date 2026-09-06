import json
from pathlib import Path
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class SiteDiscoveryMetadataTests(unittest.TestCase):
    def test_opensearch_document_has_search_template(self):
        root = ET.parse(SITE / "opensearch.xml").getroot()
        namespace = {"os": "http://a9.com/-/spec/opensearch/1.1/"}
        search = root.find("os:Url", namespace)
        self.assertIsNotNone(search)
        self.assertEqual(search.attrib["type"], "text/html")
        self.assertIn("?q={searchTerms}", search.attrib["template"])

    def test_pages_expose_valid_dataset_json_ld_and_opensearch(self):
        for filename in ("index.html", "zh-CN.html"):
            with self.subTest(filename=filename):
                html = (SITE / filename).read_text(encoding="utf-8")
                self.assertIn('type="application/opensearchdescription+xml"', html)
                self.assertIn('rel="icon" href="favicon.svg"', html)
                self.assertIn('property="og:image"', html)
                self.assertIn('content="1280"', html)
                self.assertIn('content="640"', html)
                self.assertIn(
                    'name="twitter:card" content="summary_large_image"', html
                )
                match = re.search(
                    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                    html,
                    re.DOTALL,
                )
                self.assertIsNotNone(match)
                metadata = json.loads(match.group(1))
                self.assertEqual(metadata["@type"], "Dataset")
                self.assertEqual(
                    metadata["distribution"]["contentUrl"],
                    "https://sandbaseai.github.io/workbuddy-skill/catalog.json",
                )
                script_version = re.search(r'app\.js\?v=([0-9.]+)', html)
                style_version = re.search(r'styles\.css\?v=([0-9.]+)', html)
                self.assertIsNotNone(script_version)
                self.assertIsNotNone(style_version)
                self.assertEqual(script_version.group(1), style_version.group(1))

    def test_social_preview_is_expected_png_size(self):
        data = (SITE / "social-preview.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (1280, 640))

    def test_author_styles_preserve_hidden_state(self):
        styles = (SITE / "styles.css").read_text(encoding="utf-8")
        self.assertIn("[hidden] { display: none !important; }", styles)

    def test_llms_file_points_to_catalog_and_safety_guidance(self):
        content = (SITE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("catalog.json", content)
        self.assertIn("scripts/adapt_skill.py", content)
        self.assertIn("not a security guarantee", content)
        self.assertIn("21,818 indexed Skills", content)
        self.assertIn("new catalog records are not automatically added", content)
        self.assertIn("docs/catalog-guide.md", content)
        self.assertIn("docs/catalog-guide.zh-CN.md", content)


if __name__ == "__main__":
    unittest.main()
