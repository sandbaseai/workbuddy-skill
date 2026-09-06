# WorkBuddy quickstart

Choose the path that matches your goal:

- **Use a curated Skill:** download a ZIP from Releases and import it into WorkBuddy.
- **Find a public Skill:** search the [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/), review provenance and risk, then install it.
- **Package a public Skill for WorkBuddy:** follow the [adaptation guide](adapting-skills.md).

Not sure how to interpret a result? Use the [catalog reading guide](catalog-guide.md)
before choosing a candidate.

For a categorized list of official docs, learning material, and evaluation references,
see the [WorkBuddy resource map](resources.md).

If you want a task-based starting point instead of a broad search, use the
[Starter packs](starter-packs.md) list.

For manually reviewed WorkBuddy documentation, MCP integrations, workflows, and
benchmarks, also browse the [Awesome WorkBuddy ecosystem index](https://github.com/sandbaseai/awesome-workbuddy).
It complements this broad, metadata-first catalog; it is not a replacement for
checking the exact source and license.

For a task-oriented community walkthrough, see the [WorkBuddyGuide](https://github.com/AlephAITech/WorkBuddyGuide).
For reproducible Agent task evaluation, see [Tencent WorkBuddy Bench](https://github.com/Tencent/workbuddy-bench).
These are reference resources, not additional catalog records or trust endorsements.

The catalog is a frozen snapshot of 21,818 indexed Skills. Use it to find and review
existing entries; new additions are not automatically published.

For platform-level instructions, use the [official WorkBuddy quickstart](https://www.workbuddy.ai/docs/workbuddy/Quickstart),
[official Skills tutorial](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills),
[MCP guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide),
and [Automation guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide).
You can also browse the official [Skill Marketplace](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
and [Explore](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Explore) pages for ready-made capabilities and examples.
This repository explains catalog discovery and packaging; the official docs remain the source of truth for product UI and platform behavior.

## Install one curated Skill in 5 minutes

### 1. Download

Download the ZIP you need from the [latest release](https://github.com/sandbaseai/workbuddy-skill/releases/latest). For a reproducible command-line download, replace `oss-review` with the package name shown in the Atlas and run:

```bash
mkdir -p workbuddy-download
gh release download \
  --repo sandbaseai/workbuddy-skill \
  --pattern 'oss-review-workbuddy-skill.zip' \
  --pattern SHA256SUMS \
  --dir workbuddy-download
```

Do not unzip and repackage the archive: `SKILL.md` is already at the archive root.

For reproducible downloads, also download `SHA256SUMS` from the same release and
verify an archive in the same directory:

```bash
cd workbuddy-download
sha256sum --check SHA256SUMS --ignore-missing
```

If `sha256sum` is unavailable, use the repository's cross-platform Python
helper instead:

```bash
python3 scripts/verify_release.py workbuddy-download
```

### 2. Import

In WorkBuddy, open **Experts · Skills · Connectors → Skills → Add Skill**, upload the ZIP, and finish the import. If the Skill uses a connector, enable that service in the current workspace.

### 3. Run a safe first check

Ask the Skill to explain its plan before allowing paid calls, data writes, or messages. Copy this prompt:

```text
Explain the capability, inputs, permissions, external side effects, and estimated cost you will use.
Perform a read-only check only. Do not call paid APIs, modify data, or send messages.
If anything is missing, list what I need to confirm.
```

After reviewing the source, permissions, and plan, run a small task with public data. Avoid confidential data, personal data, and production systems during the first test.

## Find a Skill in the catalog

1. Search the [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) for a task or capability such as `ocr`, `web search`, or `incident`.
   If you want an installable reviewed package immediately, set **WorkBuddy package → Reviewed package available** before searching.
2. Open the source link and check the license, inputs and outputs, network access, credential requirements, and side effects.
3. Prefer Skills with clear documentation, a known version, and verifiable provenance. Pin a tag or commit SHA when reproducibility matters.
4. After importing, use the safe-check prompt above before running a real task.

Hosts supporting the open Agent Skills convention can preview and install from GitHub:

```bash
gh skill search incident --limit 10
gh skill preview owner/repository skills/path/to/skill
gh skill install owner/repository skills/path/to/skill --pin v1.2.0 --dir .workbuddy/skills
```

If your host does not provide `gh skill`, use the source link from the Atlas and
follow the [adaptation guide](adapting-skills.md) instead. The catalog never
silently installs a third-party Skill.

## Copy-ready task template

```text
Use “Skill name” to complete “goal”.
First provide the plan, required permissions, input data, cost, and side effects.
Start with a read-only check; do not guess arguments or run unconfirmed paid or write operations.
Cite evidence for each conclusion. If the task fails, explain the failure point,
what was tried, and the available next steps.
```

For asynchronous image, audio, or video jobs, preserve the returned `run_id` and poll the same job until it completes or fails. Do not create duplicate paid jobs while waiting.

## Troubleshooting

- **Import fails:** confirm that you uploaded the original Release ZIP and that `SKILL.md` is at the archive root; do not compress it again.
- **Tools or connectors are missing:** enable the required service in the current workspace and reload WorkBuddy.
- **`gh skill` is unavailable:** open the result's immutable source link in the Atlas and package it with the adaptation guide.
- **No suitable Skill appears:** search with a shorter capability term or inspect related catalog entries. The catalog is a discovery surface, not an automatic trust decision.
- **Schema validation fails:** inspect the current capability schema and retry once using only its current fields; do not guess arguments.
- **Authorization, balance, or permission error:** check the account and workspace settings without pasting secrets into chat.
- **The result is uncertain:** ask for evidence, sources, and limitations; do not treat guesses as execution results.

For more help, see [Support](../SUPPORT.md). For security concerns, read the [security policy](../SECURITY.md).
