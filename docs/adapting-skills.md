# Adapt a public Skill for WorkBuddy

This guide is for turning a public catalog entry into an importable WorkBuddy package. If you only want to use an existing curated Skill, start with the [quickstart](quickstart.md).

## Before adapting: confirm that redistribution is allowed

The catalog is a discovery surface, not an installation feed. Open the exact source and check:

- whether the repository license permits redistribution or adaptation;
- whether the Skill’s purpose, inputs, outputs, and dependencies fit your use case;
- whether files under `scripts/`, `references/`, `assets/`, or `templates/` are referenced;
- whether it accesses the network, reads credentials, writes data, sends messages, or incurs cost.

## Step 1: Find and review the source

Search the [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) or the local catalog. Use the record’s full `id`; do not infer a path from its display name:

```bash
python3 scripts/query_catalog.py invoice OCR --json
```

Generate a non-executing review report first:

```bash
python3 scripts/review_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

The report lists provenance, referenced resources, instruction and script signals, and missing WorkBuddy fields. It does not replace human review of the license, security, network behavior, or permissions.

## Step 2: Generate the WorkBuddy package

After completing the review and confirming that the source license permits adaptation, run:

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

The resulting ZIP can be imported into WorkBuddy. It places `SKILL.md` at the archive root and includes `SOURCE.json` with the immutable source URL, blob SHA, declared license, adaptation notes, and packaged resources.

## Step 3: Verify before sharing

Inspect the ZIP structure and `SOURCE.json` before importing. After importing, run a small read-only test using the prompt in the [quickstart](quickstart.md). Share or use the package with real data only after the source, permissions, cost, and side effects are clear.

By default, adaptation stops when static risk signals are present, referenced resources are missing, or the output already exists:

- use `--allow-flagged` only after confirming the risk is acceptable;
- use `--allow-missing-resources` only when the Skill does not depend on the missing files;
- use `--force` only for an intentional replacement.

Generated metadata does not replace the original license or a security review. Do not publish an adapted package when the source license does not permit it.
