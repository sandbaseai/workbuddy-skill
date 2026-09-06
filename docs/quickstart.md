# WorkBuddy quickstart

Choose the path that matches your goal:

- **Use a curated Skill:** download a ZIP from Releases and import it into WorkBuddy.
- **Find a public Skill:** search the [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/), review provenance and risk, then install it.
- **Package a public Skill for WorkBuddy:** follow the [adaptation guide](adapting-skills.md).
- **Report a reviewed package problem:** use the [package feedback form](https://github.com/sandbaseai/workbuddy-skill/issues/new?template=package-feedback.yml) and include the failure stage.

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
Use these references alongside the exact source and license of any Skill you choose.

The catalog is a review-oriented snapshot of 21,818 indexed Skills. Use it to narrow
your search, then follow each result's source link for the latest upstream version.

## The shortest path

| If you want to… | Do this first |
|---|---|
| Install a reviewed package now | Open [curated packages](https://sandbaseai.github.io/workbuddy-skill/packages.html), download its ZIP, verify `SHA256SUMS`, and upload the original ZIP in WorkBuddy. |
| Find a capability | Search the [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/), enable **Reviewed package available** when you need an installable result, then inspect the source and license. |
| Search from a checkout | Run `python3 scripts/query_catalog.py <term> --package-status reviewed --sort score --limit 10`. |
| Turn a public source into a package | Use the [adaptation guide](adapting-skills.md) after reviewing the immutable source and license. |

For platform-level instructions, use the [official WorkBuddy quickstart](https://www.workbuddy.ai/docs/workbuddy/Quickstart),
[official Skills tutorial](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills),
[MCP guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide),
and [Automation guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide).
Before starting a task, use the official [Task Bar guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar)
to choose the workspace, model, installed Skills, connectors, and permission mode.
If an imported Skill needs a connector, use the [official Connector guide](https://open.workbuddy.cn/en/docs/connector)
to choose MCP + Skill or CLI + Skill and review authentication and permissions.
You can also browse the official [Skill Marketplace](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
and [Explore](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Explore) pages for ready-made capabilities and examples.
For the Open Platform's exact ZIP layout, required frontmatter, and parser troubleshooting,
see the [official Open Platform Skill guide](https://open.workbuddy.cn/en/docs/skill).
If you plan to publish a Skill, Connector, or other ecosystem asset, start with the
[Open Platform overview](https://open.workbuddy.cn/en/docs/what-is-open-platform)
and [onboarding guide](https://open.workbuddy.cn/en/docs/onboarding) for verification,
testing, review, and publishing prerequisites.
This repository explains catalog discovery and packaging; the official docs remain the source of truth for product UI and platform behavior.

## Choose an installation path

| Path | Best for | Scope | Notes |
|---|---|---|---|
| WorkBuddy UI | Most users | Current workspace | Upload the original Release ZIP from **Experts · Skills · Connectors → Skills**. No local CLI is required. |
| `gh skill install` | Agent Skills-compatible hosts | The directory passed to `--dir` | Use a project directory such as `.workbuddy/skills` for version-controlled, project-specific skills. The command is still preview. |
| Local `~/.workbuddy/skills/` | Local development and repeated experiments | User-wide | Copy only after reviewing the source; reload the host if it does not discover the new directory automatically. |

Do not mix these paths in one installation step. Pick the scope first, record
the source commit or release, and use the same path when updating or removing a
Skill.

## Install one curated Skill in 5 minutes

### 1. Download

Download the ZIP you need from the [latest release](https://github.com/sandbaseai/workbuddy-skill/releases/latest). The reviewed package index exposes a ready-to-copy `download_command`; the equivalent command for `oss-review` is:

```bash
mkdir -p workbuddy-download
gh release download \
  --repo sandbaseai/workbuddy-skill \
  --pattern 'oss-review-workbuddy-skill.zip' \
  --pattern SHA256SUMS \
  --dir workbuddy-download \
  --clobber
```

The `--clobber` flag makes the command safe to repeat when you are refreshing
an existing download directory.

Do not unzip and repackage the archive: `SKILL.md` is already at the archive root.

For reproducible downloads, also download `SHA256SUMS` from the same release and
verify an archive in the same directory:

```bash
cd workbuddy-download
sha256sum --check SHA256SUMS --ignore-missing
```

If `sha256sum` is unavailable, use the repository's cross-platform Python
helper instead. The helper also rejects an extra WorkBuddy ZIP that is absent
from `SHA256SUMS`:

```bash
python3 scripts/verify_release.py workbuddy-download
```

When the repository is available locally, prefer the Python helper for the
complete package-set check; use `sha256sum` when you only need to verify the
selected archive.

### 2. Import

In WorkBuddy, open **Experts · Skills · Connectors → Skills → Add Skill**, upload the ZIP, and finish the import. If the Skill uses a connector, enable that service in the current workspace.

If a connector is involved, complete this preflight before the first real task:

1. Identify the connector's required service, account, scopes, and whether it uses MCP + Skill or CLI + Skill.
2. Prefer MCP + Skill for a network API. Choose CLI + Skill only when the CLI is mature and cross-platform; the two approaches cannot be mixed in one connector.
3. Authenticate through WorkBuddy's connector flow; never paste tokens or API keys into the conversation.
4. Run its status or read-only operation first, and confirm the target workspace and data boundary.
5. Ask the Skill to name every write, message, paid call, and external side effect before approving it.

For CLI connectors, use the connector's declared install and status steps rather than assuming a system-wide Node.js or Python installation. WorkBuddy can provide a managed runtime when the connector declares one; see the [official Connector guide](https://open.workbuddy.cn/en/docs/connector) for the current fields and authentication flow.

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
The command details are maintained in the [official GitHub CLI `gh skill` manual](https://cli.github.com/manual/gh_skill); this command family is currently in preview.

```bash
gh skill search incident --limit 10
gh skill preview owner/repository skills/path/to/skill
gh skill install owner/repository skills/path/to/skill --pin v1.2.0 --dir .workbuddy/skills
```

For a host-managed destination, choose the host and scope explicitly. This
also avoids silently installing an unpinned default-branch version:

```bash
gh skill preview sandbaseai/workbuddy-skill skills/oss-review
gh skill install sandbaseai/workbuddy-skill skills/oss-review \
  --agent codex --scope project --pin v4.66.0
```

Use `--scope user` for a user-wide installation, or `--dir` for a custom
directory. Supported agents and scopes change with this preview command; check
the [current install reference](https://cli.github.com/manual/gh_skill_install)
before copying a command into automation.

If your host does not provide `gh skill`, use the source link from the Atlas and
follow the [adaptation guide](adapting-skills.md) instead. Installation is always
an explicit step after you review the source and permissions.

## Update, disable, or remove a Skill

Choose the same scope you used during installation:

- **WorkBuddy Marketplace:** open the installed Skills view to update one Skill
  or batch-update several. Disable a Skill before a sensitive task, and
  uninstall it when it is no longer needed. See the [official Skills
  Marketplace guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market).
- **Release ZIP:** download the replacement ZIP from the same release channel,
  verify its checksum, and import it through the same WorkBuddy flow. Keep the
  old version until a small read-only check passes if rollback matters.
- **Project-scoped `gh skill`:** review the new source and pin, then install the
  replacement into the same project directory. Commit the resulting change so
  teammates receive the same version.
- **Custom `--dir` or user directory:** remove only the exact Skill directory
  after checking its path; do not delete the parent directory or unrelated
  Skills. Reload the host and confirm that the Skill is no longer listed.

Record the source URL, commit/tag, package version, and checksum in the project
when reproducibility matters. If an update changes permissions, connectors, or
external side effects, repeat the safe first check before using real data.

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
