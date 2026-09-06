from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from scripts.check_release_assets import compare, expected_assets


class ReleaseAssetCheckTests(unittest.TestCase):
    def test_expected_assets_are_read_from_generated_packages(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "packages.json"
            path.write_text(json.dumps([{"asset": "one-workbuddy-skill.zip"}, {"name": "ignored"}]), encoding="utf-8")
            self.assertEqual(expected_assets(path), {"one-workbuddy-skill.zip"})

    def test_compare_requires_exact_package_assets_and_checksum(self):
        errors = compare(
            {"one-workbuddy-skill.zip", "two-workbuddy-skill.zip"},
            {"one-workbuddy-skill.zip", "SHA256SUMS"},
        )
        self.assertEqual(errors, ["missing release assets: two-workbuddy-skill.zip"])

    def test_compare_rejects_unindexed_assets_and_missing_checksum(self):
        errors = compare({"one-workbuddy-skill.zip"}, {"one-workbuddy-skill.zip", "extra.zip"})
        self.assertEqual(
            errors,
            ["unindexed release assets: extra.zip", "missing release asset: SHA256SUMS"],
        )

    def test_compare_accepts_exact_package_set_with_checksum(self):
        self.assertEqual(
            compare({"one-workbuddy-skill.zip"}, {"one-workbuddy-skill.zip", "SHA256SUMS"}),
            [],
        )


if __name__ == "__main__":
    unittest.main()
