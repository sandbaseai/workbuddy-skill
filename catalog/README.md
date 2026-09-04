# WorkBuddy Skill Catalog

This directory is a provenance-first index of public `SKILL.md` files. It is not a trust endorsement and does not execute or silently install third-party code.

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

The crawler uses GitHub's public code-search API, respects rate-limit headers, checkpoints progress, and atomically replaces the index. Tokens are read only from the environment and are never stored.

## Safety and licensing

The committed catalog stores metadata and links, not third-party skill bodies. Each linked repository keeps its own license and terms. Review provenance, license, instructions, bundled scripts, network behavior, and requested permissions before adapting or installing a skill.

