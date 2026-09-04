# Adapt an indexed skill for WorkBuddy

The catalog is a discovery surface, not an installation feed. Review the exact
GitHub source, its repository license, bundled resources, network behavior, and
requested permissions before creating a WorkBuddy package.

## Create a package

Use the record's full `id` from `catalog/skills.jsonl` or
`scripts/query_catalog.py --json`:

Generate a non-executing review report first:

```bash
python3 scripts/review_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

The report retrieves referenced resources, separates instruction and script
signals, shows missing WorkBuddy fields, and leaves license, instruction,
network, and permission checks explicitly incomplete for human review. Add
`--json` for machine-readable output.

After completing that review, create the package:

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
the immutable source URL, blob SHA, declared source license, adaptation notes,
and a list of packaged resources. References to files under `scripts/`,
`references/`, `assets/`, and `templates/` are fetched from the same immutable
Git commit (or copied beside a local source file) and retain their relative
paths. The adapter never executes source content.

Resource paths cannot escape the skill directory. Each source or resource file
is limited to 512 KiB, and bundled resources are limited to 4 MiB total.
Referenced scripts receive the same conservative static scan as `SKILL.md`.

## Refusal conditions

By default, adaptation stops when static review signals are present, referenced
resources cannot be fetched, or the output already exists. Inspect the source
before using `--allow-flagged`, use `--allow-missing-resources` only when the
package can operate without those files, and use `--force` only for an
intentional replacement.

Generated metadata is not a substitute for the original license or a security
review. Do not publish an adapted package unless the source license permits it.
