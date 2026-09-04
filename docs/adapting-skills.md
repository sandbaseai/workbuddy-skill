# Adapt an indexed skill for WorkBuddy

The catalog is a discovery surface, not an installation feed. Review the exact
GitHub source, its repository license, bundled resources, network behavior, and
requested permissions before creating a WorkBuddy package.

## Create a package

Use the record's full `id` from `catalog/skills.jsonl` or
`scripts/query_catalog.py --json`:

```bash
python3 scripts/adapt_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md' \
  --display-name-zh '中文名称' \
  --display-name-en 'English name' \
  --description-zh '说明这个技能做什么，以及何时使用。' \
  --description-en 'Explain what the skill does and when to use it.' \
  --author 'Original author; WorkBuddy adapter' \
  --source-license 'MIT'
```

The output ZIP places `SKILL.md` at its root and includes `SOURCE.json` with
the immutable source URL, blob SHA, declared source license, and adaptation
notes. The adapter does not execute the source.

## Refusal conditions

By default, adaptation stops when static review signals are present, referenced
resources were not fetched, or the output already exists. Inspect the source
before using `--allow-flagged`, retrieve and review required resources before
using `--allow-missing-resources`, and use `--force` only for an intentional
replacement.

Generated metadata is not a substitute for the original license or a security
review. Do not publish an adapted package unless the source license permits it.

