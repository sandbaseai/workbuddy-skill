---
name: "github-actions-efficiency"
display_name: "GitHub Actions 效率优化"
display_name_en: "GitHub Actions Efficiency"
description: "Use when auditing GitHub Actions runtime, CI cost, wasted runs, caching, concurrency, path filters, matrix breadth, duplicate coverage, or job critical paths."
description_zh: "用于审查 GitHub Actions 的运行时间、CI 成本、无效运行、缓存、并发取消、路径过滤、矩阵规模、重复覆盖或关键路径。"
description_en: "Measure workflow waste first, rank evidence-backed optimizations, preserve required validation and parallelism, and distinguish expected savings from live measurements."
category: "productivity"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to workflow YAML and GitHub Actions run metadata; changing workflows, repository settings, or triggering test runs requires authorization"
---

# GitHub Actions Efficiency

## Purpose and boundary

Reduce GitHub Actions time and cost using measured evidence while preserving required validation,
security boundaries, release behavior, and useful parallelism. This is an optimization review,
not permission to delete checks, weaken gates, change organization settings, or trigger expensive
runs. Default to read-only inspection and report-only recommendations unless workflow edits are
explicitly authorized.

## Step 1: establish a baseline

Inspect every `.github/workflows/*.{yml,yaml}`, reusable workflow, composite action, dependency
manifest, and repository-native test/build command that contributes to CI. Record the target
revision, workflow triggers, jobs, matrix dimensions, dependencies, caches, artifacts, concurrency
groups, path filters, runner labels, and protected release/deploy jobs.

When `gh` access is available, inspect recent runs and job durations, not just YAML:

```bash
rg -n "on:|concurrency:|paths:|paths-ignore:|strategy:|matrix:|cache:" .github/workflows
gh run list --limit 20
gh run view <run-id> --json jobs,conclusion,headSha
```

Separate total runner minutes from pull-request wall-clock time. Compare representative runs by
event and changed-path class; do not infer savings from one unusually fast or failed run. If live
history is unavailable, label the review static-only and leave measured savings unavailable.

## Step 2: identify waste sources

Check for:

- dependency installation without a lockfile-keyed cache or with a cache that never hits;
- missing `concurrency` cancellation for superseded pull-request runs;
- broad triggers that run documentation-only or unrelated jobs unnecessarily;
- duplicate lint/test/build coverage across workflows;
- matrix legs without a documented version/platform/support commitment;
- independent jobs serialized on the critical path;
- artifacts, containers, or setup work repeated without evidence of need;
- write-back or formatter jobs running automatically when opt-in would suffice.

Trace `needs:` and reusable workflow inputs before calling a job duplicate. A job may look
redundant while enforcing a release, migration, schema, security, or cross-platform contract.
Never optimize away a check because it is slow without identifying its owner and replacement
evidence.

## Step 3: apply optimization guardrails

Evaluate each proposal against these invariants:

1. Required release, schema, migration, security, and shared-library validation remains covered.
2. Parallelism is preserved unless the requester explicitly trades latency for cost and the new critical path is measured.
3. Matrix reduction removes no committed support target; unsupported legs need an explicit owner decision.
4. Path filters are complete for generated files, shared libraries, workflow changes, and release inputs.
5. Repository-editable YAML changes are separated from organization, billing, runner, or account settings.
6. Cache keys include the correct lockfiles and do not allow untrusted content to poison privileged jobs.
7. Any cancellation or skip behavior has a clear exception for release, deployment, cleanup, or required status checks.

Reject a proposal that is supported only by intuition, hides a required check, creates a trust
boundary regression, or cannot explain what evidence will verify it.

## Step 4: rank the best changes

For each candidate, estimate:

```text
estimated daily runner-minute savings = per-run minutes saved × eligible runs per day
```

Include confidence, affected events, implementation effort, correctness risk, and whether the
estimate is measured or modeled. Rank up to three high-confidence changes first; include more
only when each has independent evidence and a bounded rollout. Typical candidates are lockfile-
based caching, safe concurrency cancellation, precise path gating, removal of verified duplicate
coverage, matrix tuning, and parallelization of independent jobs.

## Step 5: verify safely

If edits are authorized, make the smallest isolated change and preserve a rollback diff. Validate
YAML syntax, workflow expression structure, required status checks, cache scope, permissions, and
the resulting `needs:` graph locally. Use a non-protected branch or dry-run where possible.

For live verification, compare before/after runs with the same event, changed paths, matrix, and
runner class. Confirm skipped jobs are intentionally skipped, required checks still report, caches
hit without cross-boundary contamination, cancellation does not interrupt release/deploy/cleanup,
and failure diagnostics remain usable. Treat unexpected live behavior as a defect even if static
YAML review passed. If live verification cannot be performed, state that limitation explicitly.

## Required report

Return these sections:

1. **Baseline** — revision, runs and jobs inspected, runner-minute and wall-clock signals.
2. **Waste sources** — concrete file/job evidence and confidence.
3. **Proposed fixes** — ranked changes, guardrail checks, expected savings, effort, and risk.
4. **Validation** — live evidence, local-only checks, skipped checks, and rollback status.
5. **Impact** — measured savings versus modeled savings, separated by runner minutes and PR latency.

Do not claim a cost reduction from a recommendation alone. Report unknown organization-level
settings, unavailable run history, flaky timing, and any assumptions about run frequency.

## WorkBuddy handoff

Provide the target revision, inspected workflows, baseline window, calculation inputs, exact
recommendations, changed files if any, validation outputs, required-check impact, remaining
uncertainty, owner, and review trigger. Keep the final report safe for sharing: exclude tokens,
Secrets, private logs, and customer data.
