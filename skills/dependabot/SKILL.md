---
name: "dependabot"
display_name: "Dependabot 依赖治理"
display_name_en: "Dependabot Management"
description: "Use when configuring or optimizing GitHub Dependabot for dependency discovery, security updates, version updates, grouped PRs, monorepos, multi-ecosystem coverage, schedules, cooldowns, or alert triage."
description_zh: "用于配置或优化 GitHub Dependabot，覆盖依赖发现、安全更新、版本更新、PR 分组、Monorepo、多生态、调度、冷却期和告警分流。"
description_en: "Inventory dependency ecosystems and directories, design least-noise update policies, preserve security coverage, and validate Dependabot configuration without silently weakening supply-chain protection."
category: "security"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with repository manifests and GitHub configuration access; security settings, dependency updates, PR merging, and alert dismissal require authorization"
---

# Dependabot Management

## Purpose and boundary

Design and review GitHub Dependabot configuration so dependency security updates remain covered,
version updates are maintainable, and pull-request noise is controlled. Dependabot has three
distinct surfaces: vulnerability alerts, security update PRs, and version update PRs. Do not
assume one is enabled because another is configured.

Default to read-only analysis and a proposed `.github/dependabot.yml`. Do not merge or close PRs,
dismiss alerts, change repository security settings, expose dependency tokens, or apply config
changes without the corresponding authorization. Never trade away security coverage solely to
reduce PR count.

## Step 1: inventory ecosystems and boundaries

Read repository instructions and discover dependency manifests, lockfiles, containers, IaC,
workflows, dev containers, submodules, and generated files. Map each to the Dependabot ecosystem:

| Evidence | Ecosystem |
|---|---|
| `package.json`, npm/pnpm/yarn lock | `npm` |
| `pyproject.toml`, `requirements.txt`, Pipfile | `pip` or `uv` when `uv.lock` exists |
| `Dockerfile`, Compose | `docker` or `docker-compose` |
| `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle` | `gomod`, `cargo`, `maven`, `gradle` |
| Terraform/OpenTofu, Helm, Composer, Bundler, NuGet, Swift, Pub | matching supported ecosystem |
| `.github/workflows/*.yml` | `github-actions` |
| `devcontainer.json`, `.gitmodules` | `devcontainers`, `gitsubmodule` |

Record repository revision, default branch, manifest path, lockfile, owner, support policy, and
whether the directory is a workspace, standalone package, generated artifact, or intentionally
excluded. There must be one canonical `.github/dependabot.yml` on the default branch; do not
silently create competing configurations.

## Step 2: map directories correctly

Use `directory: "/"` for a single package. Use `directories:` for workspace globs such as
`/apps/*`, `/packages/*`, or `/services/*`; the singular key does not support globs. Include
standalone packages outside the workspace when they have their own lockfile. Check that each
configured directory actually contains the declared ecosystem and that no important manifest is
left unowned.

Each update entry minimally needs:

```yaml
- package-ecosystem: "npm"
  directory: "/"
  schedule:
    interval: "weekly"
```

Use the narrowest schedule supported by the repository's risk and maintenance capacity. Security
updates must not be delayed by a version-update cooldown. State timezone, day/time, and any
organization-level policy assumptions.

## Step 3: design grouping and update policy

Group only dependencies that can be reviewed and tested together. Useful dimensions include
development versus production dependencies, name patterns, SemVer update types, same dependency
across monorepo directories, and explicitly bounded multi-ecosystem infrastructure groups.

Check these interactions:

- first matching group wins where patterns overlap;
- ungrouped dependencies still receive individual PRs;
- multi-ecosystem groups need a schedule and a pattern for each participating entry;
- incompatible constraints or independent lockfiles may require separate PRs;
- `open-pull-requests-limit: 0` disables version-update PRs but must not be presented as disabling security updates;
- target branches affect version updates, while security updates still target the default branch.

Use labels, commit-message prefixes, assignees, milestones, branch separators, and target branch
only when they exist in the repository's ownership and review model. Do not invent labels or
milestone IDs. Preserve major updates for explicit review; grouping minor/patch updates is not
permission to auto-merge them.

## Step 4: schedule and cooldown safely

Choose `daily`, `weekly`, `monthly`, `quarterly`, `semiannually`, `yearly`, or a justified cron
schedule. Align update times with CI capacity and reviewer availability. Cooldowns can reduce
early-release churn, for example:

```yaml
cooldown:
  default-days: 5
  semver-major-days: 30
  semver-minor-days: 7
  semver-patch-days: 3
```

Document exclusions for critical libraries and confirm cooldowns do not apply to security updates.
For a monorepo, estimate PR volume and CI minutes before and after the policy; mark estimates as
modeled until observed in live runs.

## Step 5: verify security coverage

Inspect, but do not change without authorization:

- Dependabot alerts, security updates, grouped security updates, and relevant Advanced Security settings;
- workflow permissions and checks that run on Dependabot PRs;
- action, container, IaC, and transitive dependency coverage;
- whether generated lockfiles, private registries, credentials, or network restrictions block updates;
- auto-triage rules, severity filters, and any dismissal rationale with owner and expiry;
- update PR validation, branch protection, required checks, and rollback path.

Never recommend dismissing a vulnerability only because it is a development dependency, noisy, or
unreachable without evidence. A dismissal needs a documented reason, scope, owner, expiry/review
trigger, and compensating control. Treat Dependabot PR comments as workflow commands, not as a
replacement for repository-authorized `gh`/UI operations; do not merge or close from this Skill.

## Step 6: validate and hand off

Parse YAML, verify supported keys and value types, check every ecosystem/directory against the
repository, inspect group overlap, and compare the policy with ownership and branch protection.
If live GitHub settings or alert state cannot be read, label them unknown. Use a disposable or
non-default branch for any authorized experiment, then verify dependency resolution, lockfile
changes, CI, security checks, PR labeling, and expected update cadence.

Return:

```text
Dependabot review: <revision/date/default branch>
Ecosystems/directories: <complete map and exclusions>
Security coverage: <alerts/security updates/triage evidence or unknowns>
Policy: <schedule, groups, limits, cooldowns, labels, branch behavior>
Noise/cost model: <PR and CI estimates versus measured data>
Findings: <severity, file/setting, evidence, impact, owner>
Validation: <YAML, repository, live, and unavailable checks>
Proposed config: <authorized path or report-only snippet>
Publication/merge: <not attempted unless separately authorized>
Next review: <owner, trigger, date>
```

The handoff is complete only when all manifests are accounted for, security and version-update
policies are distinguished, grouping trade-offs are explicit, and unknown GitHub settings are not
presented as verified facts.
