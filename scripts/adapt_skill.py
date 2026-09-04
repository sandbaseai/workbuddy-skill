#!/usr/bin/env python3
"""Create a reviewable WorkBuddy package from one indexed public skill.

The command never executes source content. It requires an explicit license
declaration, preserves provenance, and refuses flagged or incomplete packages
unless the caller deliberately opts in.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from pathlib import PurePosixPath
import re
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlparse
from urllib.request import Request, urlopen
from zipfile import ZIP_DEFLATED, ZipFile

from analyze_catalog import FRONTMATTER, analyze_text, parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "catalog" / "skills.jsonl"
DEFAULT_OUTPUT = ROOT / "dist" / "adapted"
USER_AGENT = "sandbaseai-workbuddy-skill-adapter/0.4"
MAX_FILE_BYTES = 512 * 1024
MAX_RESOURCE_BYTES = 4 * 1024 * 1024
RESOURCE_REFERENCE = re.compile(
    r"(?:@|\]\(|`)(?P<path>(?:\./)?(?:references|scripts|assets|templates)/[^\s)>'\"`]+)"
)


def catalog_record(path: Path, record_id: str) -> dict:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row["id"] == record_id:
                return row
    raise SystemExit(f"catalog id not found: {record_id}")


def fetch_bytes(url: str, *, limit: int = MAX_FILE_BYTES) -> bytes:
    request = Request(quote(url, safe=":/%"), headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        raw = response.read(limit + 1)
    if len(raw) > limit:
        raise SystemExit(f"source file exceeds the {limit // 1024} KiB review limit")
    return raw


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8", errors="replace")


def resource_paths(source: str) -> list[PurePosixPath]:
    """Return normalized, safe resource paths referenced by a SKILL.md."""
    paths: set[PurePosixPath] = set()
    for match in RESOURCE_REFERENCE.finditer(source):
        value = unquote(match.group("path")).removeprefix("./").rstrip(".,;:")
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or len(path.parts) < 2:
            raise SystemExit(f"unsafe bundled resource path: {value}")
        paths.add(path)
    return sorted(paths, key=str)


def immutable_github_source(record: dict) -> tuple[str, str, str]:
    """Resolve owner/repository, immutable commit, and skill directory."""
    parsed = urlparse(record["raw_url"])
    parts = parsed.path.lstrip("/").split("/")
    if parsed.netloc != "raw.githubusercontent.com" or len(parts) < 4:
        raise SystemExit("catalog record does not contain an immutable GitHub raw URL")
    owner, repository, commit = parts[:3]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise SystemExit("catalog source is not pinned to a full Git commit")
    skill_dir = str(PurePosixPath(*parts[3:]).parent)
    return f"{owner}/{repository}", commit, skill_dir


def collect_resources(
    source: str, *, record: dict | None = None, source_file: Path | None = None
) -> tuple[dict[str, bytes], list[str]]:
    requested = resource_paths(source)
    resources: dict[str, bytes] = {}
    missing: list[str] = []
    if record:
        repository, commit, skill_dir = immutable_github_source(record)
    for path in requested:
        relative = str(path)
        try:
            if record:
                remote_path = str(PurePosixPath(skill_dir) / path)
                url = f"https://raw.githubusercontent.com/{repository}/{commit}/{remote_path}"
                content = fetch_bytes(url)
            else:
                candidate = (source_file.parent / Path(*path.parts)).resolve()
                root = source_file.parent.resolve()
                if not candidate.is_relative_to(root) or not candidate.is_file():
                    missing.append(relative)
                    continue
                content = candidate.read_bytes()
                if len(content) > MAX_FILE_BYTES:
                    raise SystemExit(f"resource exceeds the 512 KiB review limit: {relative}")
        except (HTTPError, URLError, TimeoutError):
            missing.append(relative)
            continue
        resources[relative] = content
        if sum(map(len, resources.values())) > MAX_RESOURCE_BYTES:
            raise SystemExit("bundled resources exceed the 4 MiB package review limit")
    return resources, missing


def portable_name(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")[:64].rstrip("-")
    if not value:
        raise SystemExit("could not derive a portable skill name")
    return value


def yaml_value(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def adapted_text(source: str, args: argparse.Namespace) -> tuple[str, str]:
    valid, fields = parse_frontmatter(source)
    match = FRONTMATTER.match(source)
    body = source[match.end():] if valid and match else source
    name = portable_name(fields.get("name") or args.name_hint)
    description = fields.get("description") or args.description_en
    frontmatter = {
        "name": name,
        "display_name": args.display_name_zh,
        "display_name_en": args.display_name_en,
        "description": description,
        "description_zh": args.description_zh,
        "description_en": args.description_en,
        "category": args.category,
        "version": args.version,
        "author": args.author,
    }
    for optional in ("allowed-tools", "disable-model-invocation", "user-invocable"):
        if fields.get(optional):
            frontmatter[optional] = fields[optional]
    rendered = "---\n" + "\n".join(
        f"{key}: {yaml_value(value)}" for key, value in frontmatter.items()
    ) + "\n---\n\n" + body.lstrip()
    return name, rendered


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--catalog-id")
    source.add_argument("--source-file", type=Path)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--display-name-zh", required=True)
    parser.add_argument("--display-name-en", required=True)
    parser.add_argument("--description-zh", required=True)
    parser.add_argument("--description-en", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--source-license", required=True)
    parser.add_argument("--category", default="productivity")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--allow-flagged", action="store_true")
    parser.add_argument("--allow-missing-resources", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.catalog_id:
        record = catalog_record(args.catalog, args.catalog_id)
        source_text = fetch_text(record["raw_url"])
        source_info = {
            "catalog_id": record["id"],
            "repository": record["repository"],
            "path": record["path"],
            "sha": record["sha"],
            "source_url": record["source_url"],
        }
        args.name_hint = record["name_hint"]
    else:
        record = None
        source_text = args.source_file.read_text(encoding="utf-8")
        source_info = {"source_file": str(args.source_file)}
        args.name_hint = args.source_file.parent.name

    analysis = analyze_text(source_text)
    if analysis["security_signals"] and not args.allow_flagged:
        raise SystemExit(
            "source has static review signals; inspect before retrying with --allow-flagged: "
            + ", ".join(analysis["security_signals"])
        )
    resources, missing_resources = collect_resources(
        source_text, record=record, source_file=args.source_file
    )
    if missing_resources and not args.allow_missing_resources:
        raise SystemExit(
            "source references bundled resources that were not fetched: "
            + ", ".join(missing_resources[:10])
        )
    resource_signals = sorted({
        signal
        for path, content in resources.items()
        if path.startswith("scripts/")
        for signal in analyze_text(content.decode("utf-8", errors="replace"))["security_signals"]
    })
    if resource_signals and not args.allow_flagged:
        raise SystemExit(
            "bundled scripts have static review signals; inspect before retrying with "
            "--allow-flagged: " + ", ".join(resource_signals)
        )

    name, skill_text = adapted_text(source_text, args)
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f"{name}-workbuddy.zip"
    if archive.exists() and not args.force:
        raise SystemExit(f"output exists; use --force to replace: {archive}")

    provenance = {
        **source_info,
        "declared_source_license": args.source_license,
        "adaptation": {
            "missing_resources": missing_resources,
            "packaged_resources": sorted(resources),
            "security_signals": sorted(set(analysis["security_signals"] + resource_signals)),
            "tool": "scripts/adapt_skill.py",
        },
    }
    with tempfile.TemporaryDirectory(prefix="workbuddy-adapt-") as temporary:
        package = Path(temporary)
        (package / "SKILL.md").write_text(skill_text, encoding="utf-8")
        (package / "SOURCE.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        for relative, content in resources.items():
            destination = package / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        temporary_archive = archive.with_suffix(".zip.tmp")
        with ZipFile(temporary_archive, "w", compression=ZIP_DEFLATED) as output:
            for file in sorted(package.rglob("*")):
                if file.is_file():
                    output.write(file, file.relative_to(package))
        temporary_archive.replace(archive)
    print(f"OK: created {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
