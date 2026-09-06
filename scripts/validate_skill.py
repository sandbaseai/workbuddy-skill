#!/usr/bin/env python3
"""Small, dependency-free validator for curated WorkBuddy skills."""

from pathlib import Path
import argparse
import json
import re

from adapt_skill import resource_paths
from analyze_catalog import parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
REQUIRED = {
    "name",
    "description",
    "description_zh",
    "description_en",
    "version",
    "author",
    "license",
}


def validate_metadata(frontmatter: str, relative: Path) -> None:
    """Validate the Agent Skills metadata map without adding a YAML dependency."""
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("metadata:"):
            continue
        value = line.split(":", 1)[1].strip()
        if value in {"{}", "{ }"}:
            return
        if value and not value.startswith("#"):
            raise ValueError(f"{relative} metadata must be a mapping of string values")
        entries = []
        for child in lines[index + 1:]:
            if not child or child[0].isspace():
                if child.strip() and ":" in child:
                    entries.append(child.strip())
                continue
            break
        if not entries:
            raise ValueError(f"{relative} metadata must be a mapping of string values")
        for entry in entries:
            key, item = entry.split(":", 1)
            if not key.strip():
                raise ValueError(f"{relative} metadata must contain string key-value pairs")
            raw = item.strip().strip('"\'')
            if raw.lower() in {"true", "false", "null", "~"} or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", raw):
                raise ValueError(f"{relative} metadata values must be strings")
        return


def validate_skill(skill: Path, root: Path) -> None:
    relative = skill.relative_to(root)
    for path in skill.parent.rglob("*"):
        if path.is_symlink():
            raise ValueError(
                f"{relative} contains unsupported symlink: "
                f"{path.relative_to(skill.parent)}"
            )

    text = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    valid, fields = parse_frontmatter(text)
    if not valid or not match:
        raise ValueError(f"{relative} must start with YAML frontmatter")

    validate_metadata(match.group(1), relative)
    missing = sorted(key for key in REQUIRED if not fields.get(key))
    if missing:
        raise ValueError(f"{relative} missing frontmatter: " + ", ".join(missing))

    name = fields["name"].strip('"\'')
    if "--" in name:
        raise ValueError(f"{relative} name must not contain consecutive hyphens")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"{relative} name must use lowercase letters, digits, and hyphens")
    if name != skill.parent.name:
        raise ValueError(f"{relative} name must match its directory ({skill.parent.name})")
    if len(name) > 64:
        raise ValueError(f"{relative} name must be at most 64 characters")
    description = fields["description"].strip('"\'')
    if len(description) > 1024:
        raise ValueError(f"{relative} description must be at most 1024 characters")
    compatibility = fields.get("compatibility", "").strip('"\'')
    if len(compatibility) > 500:
        raise ValueError(f"{relative} compatibility must be at most 500 characters")
    source_file = skill.parent / "SOURCE.json"
    if source_file.is_file():
        try:
            source = json.loads(source_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{relative} has invalid SOURCE.json: {exc}") from exc
        declared_license = source.get("declared_source_license")
        if declared_license and fields["license"].strip('"\'') != declared_license:
            raise ValueError(
                f"{relative} license must match SOURCE.json ({declared_license})"
            )
        adaptation = source.get("adaptation", {})
        packaged_resources = adaptation.get("packaged_resources", [])
        if not isinstance(packaged_resources, list) or not all(
            isinstance(item, str) for item in packaged_resources
        ):
            raise ValueError(
                f"{relative} SOURCE.json packaged_resources must be a string list"
            )
        listed_resources = set(packaged_resources)
        actual_resources = {
            str(path.relative_to(skill.parent))
            for directory in ("references", "scripts", "assets", "templates")
            for path in (skill.parent / directory).rglob("*")
            if path.is_file()
        }
        if listed_resources != actual_resources:
            missing_from_package = sorted(listed_resources - actual_resources)
            missing_from_manifest = sorted(actual_resources - listed_resources)
            details = []
            if missing_from_package:
                details.append("not packaged: " + ", ".join(missing_from_package))
            if missing_from_manifest:
                details.append("not declared: " + ", ".join(missing_from_manifest))
            raise ValueError(
                f"{relative} SOURCE.json packaged_resources mismatch ("
                + "; ".join(details)
                + ")"
            )
    allowed_tools = fields.get("allowed-tools")
    if allowed_tools and allowed_tools.lstrip().startswith(("[", "{")):
        raise ValueError(f"{relative} allowed-tools must be a space- or comma-separated string")
    if not text[match.end():].strip():
        raise ValueError(f"{relative} must contain a non-empty instruction body")

    for reference in resource_paths(text):
        if not (skill.parent / Path(*reference.parts)).is_file():
            raise ValueError(f"{relative} missing referenced file: {reference}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate curated WorkBuddy skills")
    parser.add_argument("--skills-root", type=Path, default=SKILLS_ROOT)
    args = parser.parse_args()
    skills = sorted(args.skills_root.glob("*/SKILL.md"))
    if not skills:
        raise SystemExit("ERROR: no curated skills found")

    try:
        for skill in skills:
            validate_skill(skill, args.skills_root.parent)
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print(f"OK: {len(skills)} WorkBuddy skills and their references are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
