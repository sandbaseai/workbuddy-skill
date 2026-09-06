from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from query_catalog import main, query_rows  # noqa: E402
from catalog_categories import category_for  # noqa: E402


def row(name, sha, score, *, status="adaptable", security="no-static-flags", repository="owner/repo", category=None):
    return {
        "name_hint": name,
        "repository": repository,
        "path": f"skills/{name}/SKILL.md",
        "sha": sha,
        "workbuddy_score": score,
        "workbuddy_status": status,
        "security_status": security,
        **({"category": category} if category else {}),
    }


class QueryCatalogTests(unittest.TestCase):
    def test_filters_deduplicates_and_sorts_by_score(self):
        rows = [
            row("research", "same", 80),
            row("research-copy", "same", 80, repository="mirror/repo"),
            row("research-best", "best", 95),
            row("research-risk", "risk", 100, security="flagged"),
            row("research-low", "low", 70),
        ]
        results, copies = query_rows(
            rows,
            ["research"],
            security="no-static-flags",
            min_score=80,
            unique=True,
            order="score",
            limit=10,
        )
        self.assertEqual([item["sha"] for item in results], ["best", "same"])
        self.assertEqual(copies["same"], 2)

    def test_zero_is_a_valid_minimum_score(self):
        results, _ = query_rows(
            [row("zero", "zero", 0), row("missing", "missing", None)],
            ["zero"],
            min_score=0,
        )
        self.assertEqual([item["sha"] for item in results], ["zero"])

    def test_copy_sort_uses_all_catalog_occurrences(self):
        rows = [
            row("alpha", "popular", 70),
            row("alpha-copy", "popular", 70),
            row("alpha-best", "single", 100),
        ]
        results, _ = query_rows(rows, ["alpha"], unique=True, order="copies")
        self.assertEqual([item["sha"] for item in results], ["popular", "single"])

    def test_filters_source_context(self):
        rows = [
            row("active", "active", 90),
            {**row("archived", "archived", 95), "path": "_archive/skills/archived/SKILL.md"},
        ]
        results, _ = query_rows(rows, ["a"], source="primary-looking")
        self.assertEqual([item["sha"] for item in results], ["active"])

    def test_source_sort_is_stable_by_repository_and_path(self):
        rows = [
            row("zeta", "zeta", 90, repository="z/repo"),
            {**row("alpha", "alpha", 90, repository="a/repo"), "path": "z/SKILL.md"},
            {**row("beta", "beta", 90, repository="a/repo"), "path": "a/SKILL.md"},
        ]
        results, _ = query_rows(rows, [], order="source")
        self.assertEqual(
            [(item["repository"], item["path"]) for item in results],
            [("a/repo", "a/SKILL.md"), ("a/repo", "z/SKILL.md"), ("z/repo", "skills/zeta/SKILL.md")],
        )

    def test_unique_prefers_primary_source_over_mirror(self):
        rows = [
            {**row("alpha-copy", "same", 80, repository="mirror/repo"), "path": "mirrors/alpha/SKILL.md"},
            row("alpha", "same", 70, repository="owner/repo"),
        ]
        results, _ = query_rows(rows, ["alpha"], unique=True, order="name")
        self.assertEqual(results[0]["repository"], "owner/repo")

    def test_search_includes_review_metadata(self):
        flagged = {
            **row("workflow", "flagged", 80, security="flagged"),
            "security_signals": ["prompt-injection"],
            "workbuddy_missing_fields": ["description_zh"],
        }
        self.assertEqual(query_rows([flagged], ["prompt-injection"])[0], [flagged])
        self.assertEqual(query_rows([flagged], ["description_zh"])[0], [flagged])

    def test_search_includes_compatibility_metadata(self):
        compatible = {
            **row("python-tool", "compat", 80),
            "compatibility": "Requires Python 3.12",
        }
        results, _ = query_rows([compatible], ["Python", "3.12"])
        self.assertEqual(results, [compatible])

    def test_category_filter_uses_inferred_category(self):
        results, _ = query_rows(
            [row("research-notes", "research", 90), row("invoice-tool", "invoice", 90)],
            [],
            category="research",
        )
        self.assertEqual([item["sha"] for item in results], ["research"])

    def test_category_filter_prefers_curated_override(self):
        record = row("workflow", "workflow", 90)
        record["id"] = "github:owner/repo:skills/workflow/SKILL.md"
        results, _ = query_rows(
            [record],
            [],
            category="research",
            category_overrides={record["id"]: "research"},
        )
        self.assertEqual(results, [record])

    def test_category_inference_matches_shared_site_rule(self):
        self.assertEqual(category_for(row("api-client", "api", 90)), "development")
        self.assertEqual(category_for(row("unknown-capability", "misc/SKILL.md", 90)), "other")

    def test_search_includes_full_catalog_id(self):
        record = row("research", "sha", 90)
        record["id"] = "github:owner/repo:skills/research/SKILL.md"
        results, _ = query_rows([record], ["github:owner/repo:skills/research/SKILL.md"])
        self.assertEqual(results, [record])

    def test_cli_high_signal_shortcut_applies_review_defaults(self):
        records = [
            {**row("research-best", "best", 95), "source_url": "https://example.test/best"},
            {**row("research-low", "low", 70), "source_url": "https://example.test/low"},
            {**row("research-risk", "risk", 100, security="flagged"), "source_url": "https://example.test/risk"},
        ]
        with TemporaryDirectory() as directory:
            catalog = Path(directory) / "skills.jsonl"
            catalog.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                old_argv = sys.argv
                try:
                    sys.argv = ["query_catalog.py", "research", "--high-signal", "--catalog", str(catalog)]
                    main()
                finally:
                    sys.argv = old_argv
        rendered = output.getvalue()
        self.assertIn("research-best", rendered)
        self.assertNotIn("research-low", rendered)
        self.assertNotIn("research-risk", rendered)

    def test_cli_suggests_next_discovery_step_when_no_match(self):
        with TemporaryDirectory() as directory:
            catalog = Path(directory) / "skills.jsonl"
            catalog.write_text(json.dumps(row("research", "sha", 90)) + "\n", encoding="utf-8")
            output = io.StringIO()
            with redirect_stderr(output):
                old_argv = sys.argv
                try:
                    sys.argv = ["query_catalog.py", "invoice", "--catalog", str(catalog)]
                    main()
                finally:
                    sys.argv = old_argv
        self.assertIn("No catalog matches", output.getvalue())
        self.assertIn("shorter capability term", output.getvalue())
        self.assertIn("filename%3ASKILL.md", output.getvalue())

    def test_cli_json_no_match_remains_valid_json(self):
        with TemporaryDirectory() as directory:
            catalog = Path(directory) / "skills.jsonl"
            catalog.write_text(json.dumps(row("research", "sha", 90)) + "\n", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                old_argv = sys.argv
                try:
                    sys.argv = ["query_catalog.py", "invoice", "--catalog", str(catalog), "--json"]
                    main()
                finally:
                    sys.argv = old_argv
        self.assertEqual(json.loads(output.getvalue()), [])

    def test_filters_reviewed_and_catalog_only_packages(self):
        reviewed = {**row("reviewed", "reviewed", 90), "id": "github:owner/repo:skills/reviewed/SKILL.md"}
        catalog_only = {**row("catalog-only", "catalog-only", 90), "id": "github:owner/repo:skills/catalog-only/SKILL.md"}
        rows = [reviewed, catalog_only]
        reviewed_results, _ = query_rows(
            rows,
            [],
            package_status="reviewed",
            curated_ids={reviewed["id"]},
        )
        catalog_results, _ = query_rows(
            rows,
            [],
            package_status="catalog-only",
            curated_ids={reviewed["id"]},
        )
        self.assertEqual(reviewed_results, [reviewed])
        self.assertEqual(catalog_results, [catalog_only])

    def test_cli_prints_copyable_catalog_id(self):
        record = row("research", "sha", 90)
        record.update({
            "id": "github:owner/repo:skills/research/SKILL.md",
            "source_url": "https://github.com/owner/repo/blob/sha/skills/research/SKILL.md",
        })
        with TemporaryDirectory() as directory:
            catalog = Path(directory) / "skills.jsonl"
            catalog.write_text(json.dumps(record) + "\n", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                old_argv = sys.argv
                try:
                    sys.argv = ["query_catalog.py", "research", "--catalog", str(catalog)]
                    main()
                finally:
                    sys.argv = old_argv
        self.assertIn("catalog id: github:owner/repo:skills/research/SKILL.md", output.getvalue())

    def test_cli_prints_reviewed_package_url_in_human_output(self):
        record = row("research", "sha", 90)
        record.update({
            "id": "github:owner/repo:skills/research/SKILL.md",
            "source_url": "https://github.com/owner/repo/blob/sha/skills/research/SKILL.md",
        })
        package_url = "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/research-workbuddy-skill.zip"
        with TemporaryDirectory() as directory:
            catalog = Path(directory) / "skills.jsonl"
            curated = Path(directory) / "curated.json"
            catalog.write_text(json.dumps(record) + "\n", encoding="utf-8")
            curated.write_text(json.dumps([{
                "catalog_id": record["id"],
                "download_url": package_url,
            }]), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                old_argv = sys.argv
                try:
                    sys.argv = [
                        "query_catalog.py", "research", "--catalog", str(catalog),
                        "--curated", str(curated), "--package-status", "reviewed",
                    ]
                    main()
                finally:
                    sys.argv = old_argv
        self.assertIn(f"WorkBuddy package: {package_url}", output.getvalue())
        self.assertIn("WorkBuddy asset: research-workbuddy-skill.zip", output.getvalue())
        self.assertIn("WorkBuddy checksum: https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/SHA256SUMS", output.getvalue())
        self.assertIn("WorkBuddy download: gh release download --repo sandbaseai/workbuddy-skill", output.getvalue())

    def test_cli_includes_reviewed_package_url_in_json(self):
        record = row("research", "sha", 90)
        record.update({
            "id": "github:owner/repo:skills/research/SKILL.md",
            "source_url": "https://github.com/owner/repo/blob/sha/skills/research/SKILL.md",
        })
        package_url = "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/research-workbuddy-skill.zip"
        with TemporaryDirectory() as directory:
            catalog = Path(directory) / "skills.jsonl"
            curated = Path(directory) / "curated.json"
            catalog.write_text(json.dumps(record) + "\n", encoding="utf-8")
            curated.write_text(json.dumps([{
                "catalog_id": record["id"],
                "download_url": package_url,
            }]), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                old_argv = sys.argv
                try:
                    sys.argv = [
                        "query_catalog.py", "research", "--catalog", str(catalog),
                        "--curated", str(curated), "--package-status", "reviewed", "--json",
                    ]
                    main()
                finally:
                    sys.argv = old_argv
        result = json.loads(output.getvalue())[0]
        self.assertEqual(result["workbuddy_package_url"], package_url)
        self.assertEqual(result["workbuddy_package_asset"], "research-workbuddy-skill.zip")
        self.assertTrue(result["workbuddy_checksum_url"].endswith("/SHA256SUMS"))
        self.assertIn("--pattern 'research-workbuddy-skill.zip'", result["workbuddy_download_command"])

    def test_cli_includes_reviewed_package_metadata_in_all_json_results(self):
        record = row("research", "sha", 90)
        record.update({
            "id": "github:owner/repo:skills/research/SKILL.md",
            "source_url": "https://github.com/owner/repo/blob/sha/skills/research/SKILL.md",
        })
        package_url = "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/research-workbuddy-skill.zip"
        with TemporaryDirectory() as directory:
            catalog = Path(directory) / "skills.jsonl"
            curated = Path(directory) / "curated.json"
            catalog.write_text(json.dumps(record) + "\n", encoding="utf-8")
            curated.write_text(json.dumps([{
                "catalog_id": record["id"],
                "download_url": package_url,
            }]), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                old_argv = sys.argv
                try:
                    sys.argv = [
                        "query_catalog.py", "research", "--catalog", str(catalog),
                        "--curated", str(curated), "--json",
                    ]
                    main()
                finally:
                    sys.argv = old_argv
        result = json.loads(output.getvalue())[0]
        self.assertEqual(result["workbuddy_package_asset"], "research-workbuddy-skill.zip")
        self.assertIn("workbuddy_download_command", result)


if __name__ == "__main__":
    unittest.main()
