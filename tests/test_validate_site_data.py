import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))

from validate_site_data import validate_package_consistency, validate_rows, validate_unique_fields  # noqa: E402


class ValidateSiteDataTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads((ROOT / "site/catalog-schema.json").read_text(encoding="utf-8"))
        self.packages_schema = json.loads((ROOT / "site/packages-schema.json").read_text(encoding="utf-8"))

    def test_current_compact_catalog_matches_schema_contract(self):
        rows = json.loads((ROOT / "site/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_rows(rows, self.schema), [])

    def test_current_reviewed_packages_match_schema_contract(self):
        rows = json.loads((ROOT / "site/packages.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_rows(rows, self.packages_schema), [])

    def test_rejects_unknown_fields_and_invalid_provenance(self):
        row = {
            "n": "demo", "r": "owner/repo", "p": "SKILL.md",
            "u": "https://github.com/owner/repo/blob/abc/SKILL.md",
            "s": "not-a-sha", "w": "workbuddy-ready", "q": 101,
            "k": "no-static-flags", "g": "other", "c": 1,
            "o": "primary-looking", "x": [], "unexpected": True,
        }
        errors = validate_rows([row], self.schema)
        self.assertTrue(any("unknown field unexpected" in error for error in errors))
        self.assertTrue(any("40-character lowercase hex SHA" in error for error in errors))
        self.assertTrue(any("integer from 0 to 100" in error for error in errors))

    def test_rejects_duplicate_reviewed_package_ids_and_assets(self):
        rows = [
            {"id": "one", "download_url": "https://example.com/one.zip"},
            {"id": "one", "download_url": "https://example.com/one.zip"},
        ]
        errors = validate_unique_fields(rows, ("id", "download_url"), "packages")
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("duplicate" in error for error in errors))

    def test_rejects_package_asset_url_mismatch(self):
        rows = [{"asset": "one-workbuddy-skill.zip", "download_url": "https://example.com/two-workbuddy-skill.zip"}]
        errors = validate_package_consistency(rows)
        self.assertEqual(errors, ["packages record 0 asset does not match download_url"])

    def test_rejects_package_download_command_without_matching_asset(self):
        rows = [{
            "asset": "one-workbuddy-skill.zip",
            "download_url": "https://example.com/one-workbuddy-skill.zip",
            "download_command": "gh release download --repo sandbaseai/workbuddy-skill --pattern 'two-workbuddy-skill.zip'",
        }]
        errors = validate_package_consistency(rows)
        self.assertEqual(
            errors,
            [
                "packages record 0 download_command is missing: --pattern 'one-workbuddy-skill.zip', --pattern SHA256SUMS, --clobber"
            ],
        )


if __name__ == "__main__":
    unittest.main()
