#!/usr/bin/env python3
"""Small, dependency-free validator for curated WorkBuddy skills."""

from pathlib import Path
import argparse
import json
import re

from adapt_skill import resource_paths

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


def validate_skill(skill: Path, root: Path) -> None:
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{skill.relative_to(root)} must start with YAML frontmatter")

    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()

    relative = skill.relative_to(root)
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
