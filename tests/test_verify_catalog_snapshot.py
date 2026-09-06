import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.verify_catalog_snapshot import verify


class VerifyCatalogSnapshotTests(unittest.TestCase):
    def test_verifies_matching_frozen_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = root / "skills.jsonl"
            catalog.write_bytes(b'{"id":"example"}\n')
            digest = hashlib.sha256(catalog.read_bytes()).hexdigest()
            metadata = root / "catalog-meta.json"
            metadata.write_text(
                json.dumps({"snapshot_frozen": True, "catalog_sha256": digest}),
                encoding="utf-8",
            )
            self.assertEqual(verify(catalog, metadata), digest)

    def test_rejects_mismatched_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = root / "skills.jsonl"
            catalog.write_bytes(b"actual\n")
            metadata = root / "catalog-meta.json"
            metadata.write_text(
                json.dumps({"snapshot_frozen": True, "catalog_sha256": "0" * 64}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "snapshot mismatch"):
                verify(catalog, metadata)


if __name__ == "__main__":
    unittest.main()
