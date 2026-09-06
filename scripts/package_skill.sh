#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
output_dir="$repo_root/dist"

python3 "$repo_root/scripts/validate_skill.py"
mkdir -p "$output_dir"
for source_dir in "$repo_root"/skills/*; do
  [ -f "$source_dir/SKILL.md" ] || continue
  skill_name=$(basename "$source_dir")
  archive="$output_dir/$skill_name-workbuddy-skill.zip"
  rm -f "$archive"

  cd "$source_dir"
  # Use Python consistently so hidden resources are packaged too; a shell
  # glob such as ./* silently omits dotfiles in otherwise valid Skills.
  python3 - "$archive" <<'PY'
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import sys

archive = Path(sys.argv[1])
with ZipFile(archive, "w", compression=ZIP_DEFLATED) as package:
    for path in sorted(Path(".").rglob("*")):
        if path.is_symlink():
            raise SystemExit(f"package error: symlink is not allowed: {path}")
        if path.is_file():
            package.write(path)
PY

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
done
