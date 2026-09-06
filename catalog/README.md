# WorkBuddy Skill Catalog

This directory is a provenance-first index of public `SKILL.md` files. It is not a trust endorsement and does not execute or silently install third-party code.

中文用户可先阅读[中文快速开始](../docs/quickstart.zh-CN.md)和[目录条目解读](../docs/catalog-guide.zh-CN.md)。

## Current snapshot

<!-- CATALOG-SNAPSHOT:START -->
- 21,818 indexed GitHub paths
- 12,740 unique Git blob SHAs
- 6,497 source repositories
<!-- CATALOG-SNAPSHOT:END -->

Multiple paths can contain byte-identical skills. The catalog preserves those occurrences for provenance and reports unique SHA counts separately.

## Schema

`skills.jsonl` contains one JSON object per GitHub path:

- `id`, `repository`, `path`, and Git blob `sha` identify the exact occurrence.
- `source_url`, `raw_url`, and `repository_url` preserve provenance.
- `repository_fork` and `github_query` preserve crawl context.
- `name_hint` is inferred from the parent directory; it is not trusted metadata.
- `workbuddy_status` begins as `unreviewed` until compatibility checks run.
- `security_status` begins as `unscanned`; users must review scripts and permissions before installation.

After `scripts/analyze_catalog.py` runs, records also include frontmatter validity,
a WorkBuddy compatibility score and missing-field list, line count, and conservative
static risk signals. The compatibility check requires the standard `name` and
WorkBuddy metadata fields. `no-static-flags` is not a security guarantee; it only means
the documented patterns did not match.

Duplicate content can occur in multiple repositories. Consumers should group by `sha` when they need unique content and retain all source occurrences for attribution.

## Snapshot maintenance

```bash
python3 scripts/validate_catalog.py --minimum 10000 --require-analysis --check-stats
python3 scripts/build_site_data.py
```

The published snapshot is frozen. Do not run the crawler or add records; use the
validation and site-build commands above to verify documentation and presentation
changes without changing the catalog.

The Atlas build derives deterministic work categories from skill names and
paths and counts identical SHA occurrences. Categories and copy counts are
navigation aids, not quality or safety endorsements.

The refresh workflow is a read-only frozen-catalog check. It does not crawl GitHub,
write catalog files, open pull requests, or enable auto-merge.

## Search locally

Use the included dependency-free helper to find candidate paths and apply
review filters locally:

```bash
python3 scripts/query_catalog.py browser --limit 10
python3 scripts/query_catalog.py invoice OCR --json
python3 scripts/query_catalog.py research --security no-static-flags --source-context primary-looking --min-score 80 --unique --sort score
```

The helper searches `name_hint`, repository, path, and review metadata. Filter by
WorkBuddy status, static review state, inferred source context, or minimum compatibility score; group identical
blob SHAs with `--unique`; and sort by score, copy count, or name. Every result
includes the original source URL and review states; a match never means the
Skill is trusted or safe to install.

## Safety and licensing

The committed catalog stores metadata and links, not third-party skill bodies. Each linked repository keeps its own license and terms. Review provenance, license, instructions, bundled scripts, network behavior, and requested permissions before adapting or installing a skill.
