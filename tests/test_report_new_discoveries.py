import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))

from report_new_discoveries import compare  # noqa: E402


class NewDiscoveryTests(unittest.TestCase):
    def test_filters_existing_ids_and_duplicate_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = root / "catalog.jsonl"
            discovery = root / "discovery.jsonl"
            output = root / "new.jsonl"
            catalog.write_text(
                json.dumps({"id": "existing", "sha": "a" * 40, "repository": "one/repo"}) + "\n",
                encoding="utf-8",
            )
            discovery.write_text(
                "\n".join([
                    json.dumps({"id": "existing", "sha": "a" * 40, "repository": "one/repo"}),
                    json.dumps({"id": "moved", "sha": "a" * 40, "repository": "two/repo"}),
                    json.dumps({"id": "new", "sha": "b" * 40, "repository": "three/repo"}),
                ]) + "\n",
                encoding="utf-8",
            )
            stats = compare(catalog, discovery, output)
            self.assertEqual(stats["new_records"], 1)
            self.assertEqual(stats["new_repositories"], 1)
            rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([row["id"] for row in rows], ["new"])


if __name__ == "__main__":
    unittest.main()
