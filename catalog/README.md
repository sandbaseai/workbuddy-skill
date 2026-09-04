# WorkBuddy Skill Catalog

This directory is a provenance-first index of public `SKILL.md` files. It is not a trust endorsement and does not execute or silently install third-party code.

## Current snapshot

<!-- CATALOG-SNAPSHOT:START -->
- 11,001 indexed GitHub paths
- 7,028 unique Git blob SHAs
- 5,706 source repositories
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

## Refresh

```bash
GH_TOKEN="..." python3 scripts/crawl_github_skills.py --target 10000
python3 scripts/validate_catalog.py --minimum 10000
python3 scripts/analyze_catalog.py
# Re-run all immutable source analyses after changing review rules:
python3 scripts/analyze_catalog.py --refresh
```

Analysis is incremental: unchanged blob SHAs reuse their prior result, while
new or changed contents are fetched and inspected. Daily refreshes run this
step before validation and publication.

The crawler searches `SKILL.md` files up to 100 KB by default so longer,
reference-rich Skills are not silently excluded. Use `--max-bytes` to widen
the range for a broader scan; the catalog stores metadata and immutable source
links only, and never executes downloaded Skill content.

The Atlas build derives deterministic work categories from skill names and
paths and counts identical SHA occurrences. Categories and copy counts are
navigation aids, not quality or safety endorsements.

The crawler uses GitHub's public code-search API, respects rate-limit headers, retries transient network/server errors with bounded backoff, and atomically checkpoints after each size shard. It starts with a broad byte-size range and bisects only ranges that exceed GitHub's 1,000-result search cap. Tokens are read only from the environment and are never stored.

The scheduled workflow rebuilds this index daily in temporary storage and can
also be started from the Actions tab. Only a complete, validated 10,000-record
snapshot replaces the committed files. It then opens an update pull request and
enables auto-merge after required checks pass.

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
