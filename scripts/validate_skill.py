#!/usr/bin/env python3
"""Small, dependency-free validator for the packaged WorkBuddy skill."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "sandbase" / "SKILL.md"
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


if not SKILL.is_file():
    fail(f"missing {SKILL.relative_to(ROOT)}")

text = SKILL.read_text(encoding="utf-8")
match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
if not match:
    fail("SKILL.md must start with YAML frontmatter")

fields = {}
for line in match.group(1).splitlines():
    if ":" in line and not line.startswith((" ", "\t")):
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

missing = sorted(key for key in REQUIRED if not fields.get(key))
if missing:
    fail("missing required frontmatter: " + ", ".join(missing))

name = fields.get("name", "")
if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
    fail("name must use lowercase letters, digits, and hyphens")

for ref in re.findall(r"@references/([A-Za-z0-9._-]+)", text):
    if not (SKILL.parent / "references" / ref).is_file():
        fail(f"missing referenced file: references/{ref}")

print("OK: WorkBuddy skill structure and references are valid")

