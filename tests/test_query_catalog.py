from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from query_catalog import query_rows  # noqa: E402


def row(name, sha, score, *, status="adaptable", security="no-static-flags", repository="owner/repo"):
    return {
        "name_hint": name,
        "repository": repository,
        "path": f"skills/{name}/SKILL.md",
        "sha": sha,
        "workbuddy_score": score,
        "workbuddy_status": status,
        "security_status": security,
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


if __name__ == "__main__":
    unittest.main()
