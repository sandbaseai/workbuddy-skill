import json
from pathlib import Path
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class SiteDiscoveryMetadataTests(unittest.TestCase):
    def test_catalog_metadata_exposes_frozen_snapshot_fingerprint(self):
        metadata = json.loads((SITE / "catalog-meta.json").read_text(encoding="utf-8"))
        self.assertTrue(metadata["snapshot_frozen"])
        self.assertRegex(metadata["catalog_sha256"], r"^[0-9a-f]{64}$")

    def test_catalog_schema_describes_the_compact_dataset(self):
        schema = json.loads((SITE / "catalog-schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["type"], "array")
        properties = schema["$defs"]["record"]["properties"]
        self.assertEqual(properties["u"]["format"], "uri")
        self.assertEqual(properties["a"]["description"], "Release ZIP URL for a reviewed package.")

    def test_catalog_metadata_schema_describes_the_snapshot_contract(self):
        schema = json.loads((SITE / "catalog-meta-schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["type"], "object")
        self.assertIn("catalog_sha256", schema["required"])
        self.assertEqual(schema["properties"]["snapshot_frozen"]["const"], True)

    def test_packages_schema_describes_installable_reviewed_packages(self):
        schema = json.loads((SITE / "packages-schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["type"], "array")
        properties = schema["items"]["properties"]
        self.assertEqual(properties["download_url"]["format"], "uri")
        self.assertEqual(properties["checksum_url"]["format"], "uri")
        self.assertEqual(properties["asset"]["type"], "string")
        self.assertEqual(properties["download_command"]["type"], "string")
        self.assertIn("sha", schema["items"]["required"])

    def test_citation_file_describes_the_public_atlas(self):
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn("cff-version: 1.2.0", citation)
        self.assertIn("title: WorkBuddy Skill Atlas", citation)
        self.assertIn("repository-code: https://github.com/sandbaseai/workbuddy-skill", citation)
        self.assertIn("license: MIT", citation)

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
                self.assertIn('href="packages.html"', html)
                self.assertIn('property="og:image"', html)
                self.assertIn('property="og:locale"', html)
                self.assertIn('property="og:locale:alternate"', html)
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
                self.assertIn(metadata["inLanguage"], ("en", "zh-CN"))
                self.assertEqual(
                    metadata["distribution"]["contentUrl"],
                    "https://sandbaseai.github.io/workbuddy-skill/catalog.json",
                )
                script_version = re.search(r'app\.js\?v=([0-9.]+)', html)
                style_version = re.search(r'styles\.css\?v=([0-9.]+)', html)
                self.assertIsNotNone(script_version)
                self.assertIsNotNone(style_version)
                self.assertEqual(script_version.group(1), style_version.group(1))
                self.assertEqual(script_version.group(1), "0.19.0")

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
        self.assertIn("packages.json", content)
        self.assertIn("packages.html", content)
        self.assertIn("packages-schema.json", content)
        self.assertIn("download_command", content)
        self.assertIn("sha256sum --check SHA256SUMS --ignore-missing", content)
        self.assertIn("rejects extra", content)
        self.assertIn("Experts · Skills · Connectors", content)
        self.assertIn("catalog-only", content)
        self.assertIn("https://agentskills.io/specification", content)
        self.assertIn("docs/quickstart.zh-CN.md", content)
        self.assertIn("scripts/adapt_skill.py", content)
        self.assertIn("CITATION.cff", content)
        self.assertIn("not a security guarantee", content)
        self.assertIn("https://github.com/AlephAITech/WorkBuddyGuide", content)
        self.assertIn("https://github.com/Neo5093/workbuddy-guide", content)
        self.assertIn("https://github.com/opcspace/WorkBuddy-Guide", content)
        self.assertIn("https://github.com/KimYx0207/AI-Coding-Guide-Zh", content)
        self.assertIn("https://github.com/adongwanai/learn-workbuddy", content)
        self.assertIn("https://github.com/yinqd3/workbuddy-skills", content)
        self.assertIn("https://github.com/huaweicloud/huaweicloud-devkit", content)
        self.assertIn("https://github.com/QwenLM/Qwen-MM-Plugins", content)
        self.assertIn("https://github.com/muzishuiji/mnemoport", content)
        self.assertIn("https://github.com/jamesting-eng/workbuddy-skills", content)
        self.assertIn("https://github.com/TencentCloudBase/CloudBase-AI-Toolkit", content)
        self.assertIn("Installation-Mac-Guide", content)
        self.assertIn("Installation-Win-Guide", content)
        self.assertIn("Function-Description/Model", content)
        self.assertIn("Function-Description/Assistant", content)
        self.assertIn("/docs/zh/ide/release-notes/release-notes", content)
        self.assertIn("Function-Description/Skills-Market", content)
        self.assertIn("https://www.workbuddy.ai/docs/zh/", content)
        self.assertIn("User-guide/Agent-Mode/Quickstart", content)
        self.assertIn("Function-Description/Memory", content)
        self.assertIn("https://github.com/crossoverJie/SkillDeck", content)
        self.assertIn("https://github.com/GrubbyLee/skill-manager", content)
        self.assertIn("https://github.com/qufei1993/skills-hub", content)
        self.assertIn("https://github.com/mrzhangguoguo/oh-my-workbuddy", content)
        self.assertIn("https://github.com/Tencent/workbuddy-bench", content)
        self.assertIn("arxiv.org/abs/2602.12670", content)
        self.assertIn("arxiv.org/abs/2606.11435", content)
        self.assertIn("darker2016/workbuddy-skill-groups", content)
        self.assertIn(
            "https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide",
            content,
        )
        self.assertIn("21,818 Skills", content)
        self.assertIn("inspect the linked source, license, and permissions", content)
        self.assertNotIn("new catalog records are not automatically added", content)
        self.assertNotIn("Future maintenance focuses", content)
        self.assertNotIn("分离内部建设约束", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("本 README 面向使用者", (ROOT / "README.md").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("https://www.workbuddy.ai/docs/zh/workbuddy/Quickstart", readme)
        self.assertIn("https://www.workbuddy.ai/docs/workbuddy/Quickstart", readme)
        self.assertIn("https://www.workbuddy.ai/docs/zh/ide/release-notes/release-notes", readme)
        self.assertIn("github.com/search?q=filename%3ASKILL.md&type=code", content)
        self.assertIn("docs/catalog-guide.md", content)
        self.assertIn("docs/catalog-guide.zh-CN.md", content)
        self.assertIn("docs/starter-packs.md", content)
        self.assertIn("docs/starter-packs.zh-CN.md", content)
        for path in ("docs/starter-packs.md", "docs/starter-packs.zh-CN.md"):
            starter_packs = (ROOT / path).read_text(encoding="utf-8")
            self.assertNotIn("does not add catalog records", starter_packs)
            self.assertNotIn("不会新增目录记录", starter_packs)
        self.assertIn("github.com/sandbaseai/workbuddy-skill/discussions", content)
        self.assertIn("github.com/sandbaseai/workbuddy-skill/issues/new?template=feature.yml", content)
        self.assertIn("github.com/sandbaseai/awesome-workbuddy", content)
        self.assertIn("www.workbuddy.ai/docs/zh/workbuddy/Quickstart", content)
        self.assertIn("Create-Skills", content)
        self.assertIn("MCP-Guide", content)
        self.assertIn("Automation-Guide", content)
        self.assertIn("large-codebases", content)
        self.assertIn("Dingtalk-Guide", content)
        self.assertIn("YuanBaoPai-Guide", content)
        self.assertIn("open.workbuddy.cn/en/docs/expert", content)
        self.assertIn("open.workbuddy.cn/docs/expert", content)
        self.assertIn("First check", (ROOT / "docs/quickstart.md").read_text(encoding="utf-8"))
        self.assertIn("先检查", (ROOT / "docs/quickstart.zh-CN.md").read_text(encoding="utf-8"))
        self.assertIn("www.workbuddy.ai/docs/workbuddy/Quickstart", content)
        self.assertIn("open.workbuddy.cn/en/docs/skill", content)
        self.assertIn("open.workbuddy.cn/zh/docs/skill", content)
        self.assertIn("open.workbuddy.cn/en/docs/connector", content)
        self.assertIn("open.workbuddy.cn/docs/connector", content)
        self.assertIn("open.workbuddy.cn/en/docs/openapi", content)
        self.assertIn("open.workbuddy.cn/docs/openapi", content)
        self.assertIn("open.workbuddy.cn/en/docs/third-party-app", content)
        self.assertIn("open.workbuddy.cn/docs/third-party-app", content)
        self.assertIn("what-is-open-platform", content)
        self.assertIn("https://cli.github.com/manual/gh_skill", content)
        self.assertIn("scripts/verify_release.py", content)
        self.assertIn("www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills", content)
        self.assertIn("Function-Description/Skills-Market", content)
        self.assertIn("Function-Description/Explore", content)


if __name__ == "__main__":
    unittest.main()
