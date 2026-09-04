import json
from pathlib import Path
import re
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

    def test_llms_file_points_to_catalog_and_safety_guidance(self):
        content = (SITE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("catalog.json", content)
        self.assertIn("scripts/adapt_skill.py", content)
        self.assertIn("not a security guarantee", content)


if __name__ == "__main__":
    unittest.main()
