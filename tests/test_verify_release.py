from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))

from verify_release import main, verify  # noqa: E402


class VerifyReleaseTests(unittest.TestCase):
    def test_verifies_selected_assets_and_binary_checksum_format(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "demo-workbuddy-skill.zip"
            asset.write_bytes(b"release asset")
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            (root / "SHA256SUMS").write_text(f"{digest}  *{asset.name}\n", encoding="utf-8")
            self.assertEqual(verify(root, selected=[asset.name]), [asset.name])

    def test_reports_mismatch_without_silent_success(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "demo.zip"
            asset.write_bytes(b"actual")
            (root / "SHA256SUMS").write_text("0" * 64 + "  demo.zip\n", encoding="utf-8")
            output = io.StringIO()
            errors = io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                old_argv = sys.argv
                try:
                    sys.argv = ["verify_release.py", str(root)]
                    result = main()
                finally:
                    sys.argv = old_argv
            self.assertEqual(result, 1)
            self.assertIn("checksum mismatch", errors.getvalue())
            self.assertNotIn("Verified", output.getvalue())


if __name__ == "__main__":
    unittest.main()
