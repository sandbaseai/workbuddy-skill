#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$repo_root/skills/sandbase"
output_dir="$repo_root/dist"
archive="$output_dir/sandbase-workbuddy-skill.zip"

python3 "$repo_root/scripts/validate_skill.py"
mkdir -p "$output_dir"
rm -f "$archive"

cd "$source_dir"
zip -q -r "$archive" SKILL.md references

python3 - "$archive" <<'PY'
from pathlib import Path
from zipfile import ZipFile
import sys

archive = Path(sys.argv[1])
with ZipFile(archive) as package:
    names = set(package.namelist())
if "SKILL.md" not in names:
    raise SystemExit("package error: SKILL.md is not at archive root")
print(f"Created {archive}")
PY

