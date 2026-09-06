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

    def test_rejects_unlisted_workbuddy_zip_assets(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            signed = root / "signed-workbuddy-skill.zip"
            signed.write_bytes(b"signed")
            digest = hashlib.sha256(signed.read_bytes()).hexdigest()
            (root / "unsigned-workbuddy-skill.zip").write_bytes(b"unsigned")
            (root / "SHA256SUMS").write_text(
                f"{digest}  {signed.name}\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "release assets without checksums"):
                verify(root)

    def test_rejects_checksum_paths_outside_release_directory(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            digest = "0" * 64
            (root / "SHA256SUMS").write_text(
                f"{digest}  ../outside-workbuddy-skill.zip\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "invalid release asset filename"):
                verify(root)

    def test_rejects_symlinked_checksum_manifest(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "real-checksums"
            target.write_text("0" * 64 + "  demo.zip\n", encoding="utf-8")
            (root / "SHA256SUMS").symlink_to(target)
            with self.assertRaisesRegex(ValueError, "checksum file must not be a symlink"):
                verify(root)

    def test_rejects_symlinked_release_asset(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "outside.zip"
            target.write_bytes(b"must not be followed")
            asset = root / "demo-workbuddy-skill.zip"
            asset.symlink_to(target)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            (root / "SHA256SUMS").write_text(
                f"{digest}  {asset.name}\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "release asset must not be a symlink"):
                verify(root)


if __name__ == "__main__":
    unittest.main()
