#!/usr/bin/env python3
"""Small, dependency-free validator for curated WorkBuddy skills."""

from pathlib import Path
import re
import sys

from adapt_skill import resource_paths

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
REQUIRED = {
    "description",
    "description_zh",
    "description_en",
    "version",
    "author",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


skills = sorted(SKILLS_ROOT.glob("*/SKILL.md"))
if not skills:
    fail("no curated skills found")

for skill in skills:
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{skill.relative_to(ROOT)} must start with YAML frontmatter")

    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()

    missing = sorted(key for key in REQUIRED if not fields.get(key))
    if missing:
        fail(f"{skill.relative_to(ROOT)} missing frontmatter: " + ", ".join(missing))

    name = fields.get("name", "").strip('"\'')
    if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(f"{skill.relative_to(ROOT)} name must use lowercase letters, digits, and hyphens")

    for reference in resource_paths(text):
        if not (skill.parent / Path(*reference.parts)).is_file():
            fail(f"{skill.relative_to(ROOT)} missing referenced file: {reference}")

print(f"OK: {len(skills)} WorkBuddy skills and their references are valid")
