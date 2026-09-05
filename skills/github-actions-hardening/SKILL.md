---
name: "github-actions-hardening"
display_name: "GitHub Actions 加固"
display_name_en: "GitHub Actions Hardening"
description: "Use when reviewing, authoring, auditing, or hardening GitHub Actions workflows for trigger trust, expression injection, token permissions, action supply chain, secrets, outputs, OIDC, and runner exposure."
description_zh: "用于审查、编写或加固 GitHub Actions 工作流，重点检查触发器信任、表达式注入、令牌权限、Action 供应链、Secrets、输出、OIDC 和 Runner 暴露。"
description_en: "Map workflow privilege boundaries, inspect untrusted interpolation and checkout behavior, verify least privilege and immutable dependencies, and produce evidence-linked findings with safe remediations."
category: "security"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to .github/workflows and related action/config files; write changes, secret access, cloud credentials, and production verification require explicit authorization"
---

# GitHub Actions Hardening

## Purpose and boundary

Review GitHub Actions as a security-sensitive program: YAML triggers determine trust, `${{ }}`
expressions become runner input, `uses:` references execute dependency code, and permissions or
Secrets define blast radius. This workflow complements application-code scanning; it does not
prove that a workflow is safe merely because YAML parses or a linter passes.

Default to read-only inspection and a review report. Do not edit workflows, rotate credentials,
run untrusted workflow code, access cloud accounts, or apply remediations without authorization.
Never print secret values or copy private workflow logs into the report.

## Step 1: inventory and establish scope

List every `.github/workflows/*.{yml,yaml}` file, reusable workflow, local action, composite
action, environment rule, Dependabot action update, and referenced script that affects the job.
Record commit/revision, repository visibility, default token policy if observable, runner type,
deployment environments, and whether forks or external contributors can trigger execution.

For each workflow, capture trigger, jobs, `uses:`, `run:`, `with:`, `env:`, `permissions:`,
`secrets:`, checkout configuration, artifacts/caches, and deployment steps. Quote exact file and
line locations in findings. If a referenced file or repository setting cannot be inspected,
mark it unknown rather than assuming the secure or insecure state.

## Step 2: map trigger privilege

Classify the effective trust before reading individual steps:

| Trigger or context | Default concern |
|---|---|
| `push`, same-repository `pull_request` | repository code runs; still inspect untrusted commit content |
| fork `pull_request` | fork code is untrusted; normally no repository Secrets and restricted token |
| `pull_request_target`, `workflow_run`, `issue_comment`, `issues` | base-repository token/Secrets context may be reachable from outside input |
| `schedule`, `workflow_dispatch` | trusted initiation is not proof that checked-out code or inputs are trusted |
| reusable workflow or environment deployment | inherited secrets, caller permissions, and approvals must be traced |

Flag a critical path when a privileged workflow checks out a fork or PR head and then builds,
tests, installs, or executes it. The safer design separates untrusted execution in a restricted
`pull_request` workflow from a privileged workflow that consumes only trusted, validated results.
Do not label ordinary fork `pull_request` execution dangerous solely because it runs fork code;
verify the actual token and secret boundary.

## Step 3: find expression and shell injection

Inspect every `run:` block, `script:` passed to `actions/github-script`, and action input. Treat
attacker-controlled event fields as data, not shell source, especially issue/PR/comment titles
and bodies, branch names, commit messages, labels, and fork metadata. A value such as
`${{ github.event.issue.title }}` embedded directly in a shell command is expanded before the
shell parses it and can change the command.

Prefer passing untrusted values through the step `env:` and quoting them as data; validate type,
length, encoding, and allowed values before use. Review multiline writes to `$GITHUB_ENV` and
`$GITHUB_OUTPUT` for delimiter or newline injection. Check custom-action inputs and generated
scripts too; moving the expression without changing its parsing context is not a fix.

## Step 4: verify token and secret least privilege

- Require an explicit top-level `permissions:` policy, commonly `{}` or `contents: read`, then grant only the job-level scopes needed.
- Flag `write-all`, broad write scopes, and write permissions on jobs that only read, build, test, or publish artifacts.
- Trace `secrets.*` to the step that consumes it; never expose Secrets to untrusted checkout/build code or unnecessary third-party actions.
- Check `actions/checkout` uses `persist-credentials: false` before untrusted code runs, unless a documented trusted operation needs the token.
- Prefer short-lived OIDC with constrained subject/audience and cloud role policy over long-lived cloud credentials; verify environment approvals for deployments.
- Treat artifact downloads, caches, and outputs crossing a trust boundary as untrusted until integrity, scope, and provenance are checked.

## Step 5: audit the Action supply chain and runners

For each `uses:` reference, record owner, repository, action path, version, and trust rationale.
Recommend a full 40-character commit SHA for third-party Actions, with a human-readable version
comment. Flag mutable branches and tags, especially `@main`, `@master`, or floating major tags,
as supply-chain risk; verify that pinning corresponds to the intended release before changing it.
Check Dependabot or another update process so immutable pins do not silently become stale.

Review self-hosted runners on public repositories for workspace persistence, network reachability,
cross-job contamination, cleanup, and untrusted PR access. Inspect shell error handling, artifact
retention, caches, Docker socket access, and any privileged container or deployment command.

## Step 6: produce an actionable report

Start with a severity summary, then group findings by issue type rather than only by file:

| Severity | Meaning |
|---|---|
| CRITICAL | Secret/token theft or remote code execution reachable through an outside contributor |
| HIGH | Exploitable mutable dependency, broad write authority, or injection on a privileged path |
| MEDIUM | Missing boundary, secret exposure condition, or hardening gap with contextual exploitability |
| LOW | Defense-in-depth improvement with limited direct impact |
| INFO | Verified observation or unknown requiring owner confirmation |

Each finding must include: severity, file and line, trigger/job, exact risky construct (redacted),
trust boundary, realistic impact, evidence and confidence, a minimal before/after YAML pattern,
and residual risk. Do not auto-apply a fix in a report-only review. If no findings are supported,
say what was checked and list uninspected settings or dependencies.

## Validation and handoff

Re-parse workflow YAML with the repository's supported validator, run static checks that do not
execute untrusted code, and inspect the final diff if changes were authorized. Verify that each
remediation preserves required behavior, narrows permissions, does not reintroduce interpolation,
and has a rollback path. Never claim a workflow is fully secure when repository settings, action
source, environment rules, or runtime evidence were unavailable.

Return the target revision, workflows inspected, trigger/privilege map, severity counts, finding
ledger, exact validation results, unavailable evidence, owner decisions, remediation status, and
the next review trigger (such as a workflow, action, runner, or permission change).
