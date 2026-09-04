# WorkBuddy Skill Catalog

This directory is a provenance-first index of public `SKILL.md` files. It is not a trust endorsement and does not execute or silently install third-party code.

## Current snapshot

- 10,000 indexed GitHub paths
- 6,483 unique Git blob SHAs
- 5,044 source repositories

Multiple paths can contain byte-identical skills. The catalog preserves those occurrences for provenance and reports unique SHA counts separately.

## Schema

`skills.jsonl` contains one JSON object per GitHub path:

- `id`, `repository`, `path`, and Git blob `sha` identify the exact occurrence.
- `source_url`, `raw_url`, and `repository_url` preserve provenance.
- `name_hint` is inferred from the parent directory; it is not trusted metadata.
- `workbuddy_status` begins as `unreviewed` until compatibility checks run.
- `security_status` begins as `unscanned`; users must review scripts and permissions before installation.

Duplicate content can occur in multiple repositories. Consumers should group by `sha` when they need unique content and retain all source occurrences for attribution.

## Refresh

```bash
GH_TOKEN="..." python3 scripts/crawl_github_skills.py --target 10000
python3 scripts/validate_catalog.py --minimum 10000
```

The crawler uses GitHub's public code-search API, respects rate-limit headers, retries transient network/server errors with bounded backoff, and atomically checkpoints after each size shard. It starts with a broad byte-size range and bisects only ranges that exceed GitHub's 1,000-result search cap. Tokens are read only from the environment and are never stored.

The scheduled workflow rebuilds this index weekly in temporary storage and can
also be started from the Actions tab. Only a complete, validated 10,000-record
snapshot replaces the committed files. It then opens an update pull request and
enables auto-merge after required checks pass.

## Search locally

Use the included dependency-free helper to find candidate paths without loading
the entire JSONL file into memory:

```bash
python3 scripts/query_catalog.py browser --limit 10
python3 scripts/query_catalog.py invoice OCR --json
```

The helper searches `name_hint`, repository, and path. Every result includes
the original source URL and review states; a match never means the Skill is
trusted or safe to install.

## Safety and licensing

The committed catalog stores metadata and links, not third-party skill bodies. Each linked repository keeps its own license and terms. Review provenance, license, instructions, bundled scripts, network behavior, and requested permissions before adapting or installing a skill.
