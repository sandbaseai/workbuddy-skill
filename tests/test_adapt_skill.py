import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from adapt_skill import immutable_github_source, resource_paths  # noqa: E402
from analyze_catalog import parse_frontmatter  # noqa: E402


class ResourceDiscoveryTests(unittest.TestCase):
    def test_finds_and_normalizes_supported_references(self):
        source = (
            "Read @references/guide.md, [run](./scripts/check.py), and inspect "
            "`templates/report.md`."
        )
        self.assertEqual(
            resource_paths(source),
            [
                PurePosixPath("references/guide.md"),
                PurePosixPath("scripts/check.py"),
                PurePosixPath("templates/report.md"),
            ],
        )

    def test_inline_code_reference_does_not_include_closing_backtick(self):
        self.assertEqual(
            resource_paths("Read `references/root-cause-tracing.md` first."),
            [PurePosixPath("references/root-cause-tracing.md")],
        )

    def test_markdown_heading_fragment_is_not_part_of_resource_path(self):
        self.assertEqual(
            resource_paths(
                "Read [state recovery](references/state-management.md#recovery)."
            ),
            [PurePosixPath("references/state-management.md")],
        )

    def test_rejects_path_traversal(self):
        with self.assertRaisesRegex(SystemExit, "unsafe bundled resource path"):
            resource_paths("Run @scripts/../../outside.sh")

    def test_resolves_immutable_catalog_source(self):
        record = {
            "raw_url": "https://raw.githubusercontent.com/acme/tools/"
            + "a" * 40
            + "/skills/demo/SKILL.md"
        }
        self.assertEqual(
            immutable_github_source(record),
            ("acme/tools", "a" * 40, "skills/demo"),
        )


class LocalPackagingTests(unittest.TestCase):
    def test_parses_folded_frontmatter_and_preserves_argument_hint(self):
        valid, fields = parse_frontmatter(
            "---\nname: demo\ndescription: >\n  First line\n  second line.\n"
            "argument-hint: \"[path]\"\n---\n\n# Demo\n"
        )
        self.assertTrue(valid)
        self.assertEqual(fields["description"], "First line second line.")
        self.assertEqual(fields["argument-hint"], "[path]")

    def test_packages_referenced_local_resources_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "demo" / "SKILL.md"
            script = source.parent / "scripts" / "check.py"
            reference = source.parent / "references" / "guide.md"
            script.parent.mkdir(parents=True)
            reference.parent.mkdir(parents=True)
            source.write_text(
                "---\nname: demo\ndescription: Demo skill\n---\n\n"
                "Read @references/guide.md then [run](scripts/check.py).\n",
                encoding="utf-8",
            )
            script.write_text("print('checked')\n", encoding="utf-8")
            reference.write_text("# Guide\n", encoding="utf-8")
            output = root / "dist"
            command = [
                sys.executable,
                str(ROOT / "scripts" / "adapt_skill.py"),
                "--source-file", str(source),
                "--output", str(output),
                "--display-name-zh", "演示",
                "--display-name-en", "Demo",
                "--description-zh", "演示技能",
                "--description-en", "Demo skill",
                "--author", "Test",
                "--source-license", "MIT",
            ]
            subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)

            with ZipFile(output / "demo-workbuddy.zip") as archive:
                skill_text = archive.read("SKILL.md").decode()
                self.assertIn("name: \"demo\"", skill_text)
                self.assertIn("license: \"MIT\"", skill_text)
                self.assertEqual(
                    sorted(archive.namelist()),
                    ["SKILL.md", "SOURCE.json", "references/guide.md", "scripts/check.py"],
                )
                provenance = json.loads(archive.read("SOURCE.json"))
                self.assertEqual(
                    provenance["adaptation"]["packaged_resources"],
                    ["references/guide.md", "scripts/check.py"],
                )

    def test_preserves_standard_license_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "licensed" / "SKILL.md"
            source.parent.mkdir()
            source.write_text(
                "---\nname: licensed\ndescription: Licensed skill\n"
                "license: Apache-2.0\n---\n\n# Licensed\n",
                encoding="utf-8",
            )
            command = [
                sys.executable, str(ROOT / "scripts" / "adapt_skill.py"),
                "--source-file", str(source), "--output", str(root / "dist"),
                "--display-name-zh", "授权技能", "--display-name-en", "Licensed",
                "--description-zh", "授权技能", "--description-en", "Licensed skill",
                "--author", "Test", "--source-license", "Apache-2.0",
            ]
            subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
            with ZipFile(root / "dist/licensed-workbuddy.zip") as archive:
                self.assertIn('license: "Apache-2.0"', archive.read("SKILL.md").decode())

    def test_preserves_compatibility_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "compatible" / "SKILL.md"
            source.parent.mkdir()
            source.write_text(
                "---\nname: compatible\ndescription: Compatible skill\n"
                "compatibility: Requires Python 3.11 and network access\n"
                "---\n\n# Compatible\n", encoding="utf-8",
            )
            command = [
                sys.executable, str(ROOT / "scripts" / "adapt_skill.py"),
                "--source-file", str(source), "--output", str(root / "dist"),
                "--display-name-zh", "兼容技能", "--display-name-en", "Compatible",
                "--description-zh", "兼容技能", "--description-en", "Compatible skill",
                "--author", "Test", "--source-license", "MIT",
            ]
            subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
            with ZipFile(root / "dist/compatible-workbuddy.zip") as archive:
                self.assertIn(
                    'compatibility: "Requires Python 3.11 and network access"',
                    archive.read("SKILL.md").decode(),
                )

    def test_preserves_string_metadata_map(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "metadata" / "SKILL.md"
            source.parent.mkdir()
            source.write_text(
                "---\nname: metadata\ndescription: Metadata skill\n"
                "metadata:\n  team: platform\n  maturity: stable\n"
                "---\n\n# Metadata\n", encoding="utf-8",
            )
            command = [
                sys.executable, str(ROOT / "scripts" / "adapt_skill.py"),
                "--source-file", str(source), "--output", str(root / "dist"),
                "--display-name-zh", "元数据技能", "--display-name-en", "Metadata",
                "--description-zh", "元数据技能", "--description-en", "Metadata skill",
                "--author", "Test", "--source-license", "MIT",
            ]
            subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
            with ZipFile(root / "dist/metadata-workbuddy.zip") as archive:
                content = archive.read("SKILL.md").decode()
                self.assertIn("metadata:\n  team: platform\n  maturity: stable", content)


if __name__ == "__main__":
    unittest.main()
