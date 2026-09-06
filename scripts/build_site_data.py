#!/usr/bin/env python3
"""Build the compact browser index used by the static catalog site."""

from pathlib import Path
from collections import Counter
from html import escape
import hashlib
import json
import re
from urllib.parse import urlparse

from catalog_signals import source_context, source_signals

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog" / "skills.jsonl"
CURATED = ROOT / "catalog" / "curated.json"
OUTPUT = ROOT / "site" / "catalog.json"
PACKAGES_OUTPUT = ROOT / "site" / "packages.json"
PACKAGES_PAGE_OUTPUT = ROOT / "site" / "packages.html"
CHECKSUM_URL = "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/SHA256SUMS"
RELEASE_REPO = "sandbaseai/workbuddy-skill"

CATEGORY_RULES = (
    ("security", ("security", "audit", "pentest", "vulnerability", "sast", "threat", "auth")),
    ("media", ("video", "audio", "podcast", "voice", "music", "subtitle", "animation")),
    ("design", ("design", "ui", "ux", "frontend", "css", "figma", "brand", "visual")),
    ("research", ("research", "search", "academic", "paper", "literature", "citation", "analysis")),
    ("data", ("data", "database", "sql", "spreadsheet", "excel", "csv", "etl", "analytics")),
    ("content", ("content", "writing", "writer", "copy", "blog", "document", "markdown", "seo")),
    ("business", ("sales", "marketing", "finance", "legal", "hr", "customer", "commerce", "product")),
    ("productivity", ("task", "calendar", "email", "meeting", "note", "workflow", "automation", "planning")),
    ("development", ("code", "coding", "test", "debug", "deploy", "api", "git", "python", "javascript", "typescript")),
)
KNOWN_CATEGORIES = {category for category, _ in CATEGORY_RULES} | {"other"}


def category_for(row: dict) -> str:
    haystack = f"{row['name_hint']} {row['path']}".casefold()
    tokens = set(re.findall(r"[a-z0-9]+", haystack))
    for category, keywords in CATEGORY_RULES:
        if any(keyword in tokens for keyword in keywords):
            return category
    return "other"

source_rows = []
repositories = set()
shas = set()
with SOURCE.open(encoding="utf-8") as handle:
    for line in handle:
        row = json.loads(line)
        source_rows.append(row)
        repositories.add(row["repository"])
        shas.add(row["sha"])

curated_entries = json.loads(CURATED.read_text(encoding="utf-8"))
curated = {entry["catalog_id"]: entry for entry in curated_entries}
if len(curated) != len(curated_entries):
    raise SystemExit("catalog/curated.json contains duplicate catalog IDs")
skill_paths = [entry["skill_path"] for entry in curated_entries]
if len(set(skill_paths)) != len(skill_paths):
    raise SystemExit("catalog/curated.json contains duplicate skill paths")
catalog_ids = {row["id"] for row in source_rows}
source_by_id = {row["id"]: row for row in source_rows}
for entry in curated_entries:
    if not (ROOT / entry["skill_path"] / "SKILL.md").is_file():
        raise SystemExit(f"curated Skill is missing: {entry['skill_path']}")
    if entry["catalog_id"] not in catalog_ids:
        raise SystemExit(f"curated source is missing from catalog: {entry['catalog_id']}")
    if not entry["download_url"].startswith(
        "https://github.com/sandbaseai/workbuddy-skill/releases/"
    ):
        raise SystemExit(f"unexpected curated download URL: {entry['download_url']}")
    if entry.get("category") not in KNOWN_CATEGORIES | {None}:
        raise SystemExit(f"unknown curated category: {entry['category']}")

sha_copies = Counter(row["sha"] for row in source_rows)
category_counts = Counter()
records = []
for row in source_rows:
    adaptation = curated.get(row["id"])
    category = adaptation.get("category", category_for(row)) if adaptation else category_for(row)
    category_counts[category] += 1
    record = {
        "n": row["name_hint"],
        "r": row["repository"],
        "p": row["path"],
        "u": row["source_url"],
        "s": row["sha"],
        "w": "workbuddy-ready" if adaptation else row.get("workbuddy_status", "unreviewed"),
        "q": row.get("workbuddy_score"),
        "k": row.get("security_status", "unscanned"),
        "g": category,
        "c": sha_copies[row["sha"]],
        "o": source_context(row),
        "x": source_signals(row),
    }
    if adaptation:
        record["a"] = adaptation["download_url"]
    records.append(record)

packages = []
for entry in sorted(curated_entries, key=lambda item: item["skill"]):
    source = source_by_id[entry["catalog_id"]]
    asset = Path(urlparse(entry["download_url"]).path).name
    download_command = (
        "gh release download --repo "
        f"{RELEASE_REPO} --pattern '{asset}' --pattern SHA256SUMS "
        "--dir workbuddy-download --clobber"
    )
    packages.append(
        {
            "id": entry["catalog_id"],
            "name": entry["skill"],
            "path": entry["skill_path"],
            "repository": source["repository"],
            "source_url": source["source_url"],
            "sha": source["sha"],
            "download_url": entry["download_url"],
            "asset": asset,
            "checksum_url": CHECKSUM_URL,
            "download_command": download_command,
            "category": curated.get(entry["catalog_id"], {}).get(
                "category", category_for(source)
            ),
        }
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
temporary = OUTPUT.with_suffix(".json.tmp")
temporary.write_text(
    json.dumps(records, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)
temporary.replace(OUTPUT)
packages_temporary = PACKAGES_OUTPUT.with_suffix(".json.tmp")
packages_temporary.write_text(
    json.dumps(packages, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)
packages_temporary.replace(PACKAGES_OUTPUT)
package_items_by_category: dict[str, list[str]] = {}
for package in packages:
    package_items_by_category.setdefault(package["category"], []).append(
        "<li data-search=\""
        + escape(
            f"{package['name']} {package['repository']} {package['path']} {package['category']}",
            quote=True,
        )
        + "\"><h3>"
        f"<a href=\"{escape(package['download_url'], quote=True)}\">{escape(package['name'])}</a>"
        "</h3>"
        f"<p><span class=\"badge\">{escape(package['category'])}</span> "
        f"{escape(package['repository'])} · <code>{escape(package['path'])}</code></p>"
        f"<p><a href=\"{escape(package['source_url'], quote=True)}\">Inspect pinned source</a> · "
        f"<code title=\"Git blob SHA\">{escape(package['sha'])}</code> · "
        f"<a href=\"{escape(package['download_url'], quote=True)}\">Download ZIP</a> · "
        f"<a href=\"{escape(package['checksum_url'], quote=True)}\">SHA256SUMS</a></p>"
        f"<details><summary>Copy download command</summary>"
        f"<button type=\"button\" class=\"copy-command\" data-command=\"{escape(package['download_command'], quote=True)}\">Copy command / 复制命令</button>"
        "<span class=\"copy-status\" role=\"status\" aria-live=\"polite\"></span>"
        f"<pre class=\"command\"><code>{escape(package['download_command'])}</code></pre></details></li>"
    )
category_nav = " ".join(
    f"<a href=\"#category-{escape(category, quote=True)}\">{escape(category.title())}</a>"
    for category in sorted(package_items_by_category)
)
category_sections = "\n".join(
    f"<section id=\"category-{escape(category, quote=True)}\"><h2>{escape(category.title())} ({len(package_items_by_category[category])})</h2><ol>"
    + "\n".join(package_items_by_category[category])
    + "</ol></section>"
    for category in sorted(package_items_by_category)
)
package_item_list = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Reviewed WorkBuddy Packages",
        "numberOfItems": len(packages),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": position,
                "name": package["name"],
                "url": package["source_url"],
            }
            for position, package in enumerate(packages, start=1)
        ],
    },
    ensure_ascii=False,
    separators=(",", ":"),
).replace("</", "<\\/")
package_page = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="canonical" href="https://sandbaseai.github.io/workbuddy-skill/packages.html">
    <meta name="description" content="Browse 277 reviewed WorkBuddy packages with pinned GitHub sources, ZIP downloads, and SHA256 checksums.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://sandbaseai.github.io/workbuddy-skill/packages.html">
    <meta property="og:title" content="Reviewed WorkBuddy Packages · Skill Atlas">
    <meta property="og:description" content="Browse 277 reviewed WorkBuddy packages with pinned GitHub sources, ZIP downloads, and SHA256 checksums.">
    <meta property="og:site_name" content="WorkBuddy Skill Atlas">
    <meta property="og:image" content="https://sandbaseai.github.io/workbuddy-skill/social-preview.png">
    <meta property="og:image:width" content="1280">
    <meta property="og:image:height" content="640">
    <meta property="og:image:alt" content="Reviewed WorkBuddy packages with pinned GitHub provenance">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Reviewed WorkBuddy Packages · Skill Atlas">
    <meta name="twitter:description" content="Browse reviewed WorkBuddy packages with pinned sources, downloads, and checksums.">
    <meta name="twitter:image" content="https://sandbaseai.github.io/workbuddy-skill/social-preview.png">
    <title>Reviewed WorkBuddy Packages · Skill Atlas</title>
    <script type="application/ld+json">""" + package_item_list + """</script>
    <style>
      :root { color-scheme: light; font-family: system-ui, sans-serif; line-height: 1.5; }
      body { max-width: 980px; margin: 0 auto; padding: 2rem 1rem 4rem; color: #24302f; background: #f5f1e8; }
      a { color: #126b63; }
      header { margin-bottom: 2rem; }
      h1 { margin-bottom: .4rem; }
      ol { padding-left: 1.5rem; }
      li { margin: 1rem 0; padding: 1rem 1.2rem; background: #fffdf8; border: 1px solid #d8d0c2; border-radius: .7rem; }
      h2 { margin: 1.5rem 0 .5rem; font-size: 1.25rem; }
      h3 { margin: 0; font-size: 1.1rem; }
      p { margin: .35rem 0 0; }
      code { overflow-wrap: anywhere; }
      pre.command { margin: .6rem 0 0; padding: .7rem; overflow-x: auto; background: #eef3ef; border-radius: .45rem; white-space: pre-wrap; }
      .badge { display: inline-block; padding: .1rem .45rem; border-radius: 999px; background: #dceee8; font-size: .8rem; }
      .category-nav { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: 1rem; }
      .category-nav a { padding: .25rem .6rem; border: 1px solid #b8cec7; border-radius: 999px; text-decoration: none; }
      .package-search { margin: 1rem 0; padding: .75rem; background: #fffdf8; border: 1px solid #d8d0c2; border-radius: .7rem; }
      .package-search label { display: block; font-weight: 650; margin-bottom: .35rem; }
      .package-search input { box-sizing: border-box; width: 100%; padding: .55rem .65rem; border: 1px solid #aebeb8; border-radius: .4rem; font: inherit; }
      .package-search output { display: block; margin-top: .35rem; color: #53615e; font-size: .9rem; }
      .copy-command { margin-top: .6rem; padding: .35rem .6rem; border: 1px solid #8eaaa0; border-radius: .4rem; color: #174f49; background: #f4fbf7; cursor: pointer; font: inherit; }
      .copy-status { margin-left: .5rem; color: #53615e; font-size: .9rem; }
      .machine { margin-top: 2rem; }
    </style>
  </head>
  <body>
    <header>
      <p><a href="index.html">← WorkBuddy Skill Atlas</a></p>
      <h1>Reviewed WorkBuddy Packages / 精选 WorkBuddy 包</h1>
      <p>Browse 277 installable packages without JavaScript. Each entry keeps an immutable source link, a Release ZIP, and SHA256SUMS verification.</p>
      <p>无需 JavaScript 即可浏览 277 个可安装精选包；每条记录都保留不可变来源、Release ZIP 和 SHA256SUMS 校验入口。</p>
      <nav class="category-nav" aria-label="Package categories">""" + category_nav + """</nav>
      <form class="package-search" role="search" onsubmit="return false">
        <label for="package-filter">Filter packages by name, repository, path, or category / 按名称、仓库、路径或分类筛选</label>
        <input id="package-filter" type="search" autocomplete="off" placeholder="Try: security, playwright, or mcp / 例如：security、playwright、mcp">
        <output id="package-count" aria-live="polite">Showing all 277 packages / 共 277 个精选包</output>
      </form>
    </header>
    <main>
""" + category_sections + """
      <p class="machine"><a href="packages.json">Machine-readable JSON index</a> · <a href="packages-schema.json">JSON Schema</a> · <a href="https://github.com/sandbaseai/workbuddy-skill/blob/main/docs/quickstart.md">English quickstart</a> · <a href="https://github.com/sandbaseai/workbuddy-skill/blob/main/docs/quickstart.zh-CN.md">中文快速开始</a></p>
    </main>
    <script>
      (() => {
        const input = document.querySelector('#package-filter');
        const output = document.querySelector('#package-count');
        const items = [...document.querySelectorAll('li[data-search]')];
        const sections = [...document.querySelectorAll('main section')];
        const copyButtons = [...document.querySelectorAll('.copy-command')];
        const update = () => {
          const query = input.value.trim().toLowerCase();
          let visible = 0;
          for (const item of items) {
            const match = !query || item.dataset.search.toLowerCase().includes(query);
            item.hidden = !match;
            if (match) visible += 1;
          }
          for (const section of sections) {
            section.hidden = !section.querySelector('li:not([hidden])');
          }
          output.textContent = query
            ? `Showing ${visible} of ${items.length} packages / 匹配 ${visible} / ${items.length}`
            : `Showing all ${items.length} packages / 共 ${items.length} 个精选包`;
        };
        input.addEventListener('input', update);
        for (const button of copyButtons) {
          button.addEventListener('click', async () => {
            const status = button.nextElementSibling;
            try {
              await navigator.clipboard.writeText(button.dataset.command);
              status.textContent = 'Copied / 已复制';
              window.setTimeout(() => { status.textContent = ''; }, 1500);
            } catch {
              status.textContent = 'Copy failed / 复制失败，请手动选择下方命令';
            }
          });
        }
      })();
    </script>
  </body>
</html>
"""
packages_page_temporary = PACKAGES_PAGE_OUTPUT.with_suffix(".html.tmp")
packages_page_temporary.write_text(package_page, encoding="utf-8")
packages_page_temporary.replace(PACKAGES_PAGE_OUTPUT)
meta = {
    "categories": dict(sorted(category_counts.items())),
    "catalog_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "snapshot_frozen": True,
    "records": len(records),
    "repositories": len(repositories),
    "unique_content_shas": len(shas),
    "curated_adaptations": len(curated),
    "release_checksum_url": CHECKSUM_URL,
}
meta_output = ROOT / "site" / "catalog-meta.json"
meta_temporary = meta_output.with_suffix(".json.tmp")
meta_temporary.write_text(json.dumps(meta, separators=(",", ":")), encoding="utf-8")
meta_temporary.replace(meta_output)
print(f"OK: wrote {len(records)} searchable records to {OUTPUT.relative_to(ROOT)}")
print(f"OK: wrote {len(packages)} installable packages to {PACKAGES_OUTPUT.relative_to(ROOT)}")
print(f"OK: wrote browsable package page to {PACKAGES_PAGE_OUTPUT.relative_to(ROOT)}")
