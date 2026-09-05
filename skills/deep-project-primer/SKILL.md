---
name: "deep-project-primer"
display_name: "深度项目预检"
display_name_en: "Deep Project Primer"
description: "Build an evidence-backed project baseline before significant work by inspecting repository guidance, architecture, runtime, tests, and delivery constraints."
description_zh: "在重大工作前检查仓库规范、架构、运行方式、测试和交付约束，建立有证据支撑的项目基线。"
description_en: "Build an evidence-backed project baseline before significant work by inspecting repository guidance, architecture, runtime, tests, and delivery constraints."
category: "workflow"
version: "0.1.0"
author: "Jeffrey Emanuel; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Deep Project Primer

Use this skill at the start of work in an unfamiliar repository, after context
loss, or before a consequential architectural or delivery change. The goal is
not to read every file indiscriminately; it is to establish the smallest
reliable model of the project needed for the requested work and to expose what
is still unknown.

## Establish repository authority

Begin at the repository root and inspect, in order:

1. `AGENTS.md`, `CONTRIBUTING`, `SECURITY`, and other local instruction files,
   following the most specific applicable guidance.
2. `README` and documented development, test, build, release, and deployment
   commands.
3. Package manifests, lockfiles, workspace boundaries, generated-file markers,
   CI workflows, container or infrastructure definitions, and entry points.
4. The requested feature's owning modules, public interfaces, persistence and
   integration boundaries, tests, and recent relevant history.

Record the repository commit, branch, working-tree state, runtime assumptions,
and commands actually executed. Distinguish facts observed in files or command
output from inferences and recommendations. Do not treat an outdated README,
an example configuration, or a green unrelated workflow as proof of current
behavior.

## Build the project model

Map the request to:

- user or operator outcome and non-goals;
- entry points, data/control flow, and ownership boundaries;
- public contracts, compatibility obligations, and feature flags;
- dependencies, external services, credentials, and authorization boundaries;
- state, migrations, queues, caches, retries, and failure behavior;
- test layers, fixtures, observability, rollout, and rollback paths.

For every important claim, keep a pointer to the file, symbol, command, test,
or runtime observation that supports it. Identify stale, contradictory, or
missing evidence explicitly. Ask for clarification only when an ambiguity would
change scope or create a meaningful safety or compatibility risk; otherwise
make a bounded assumption and label it.

## Verify before changing

Select the cheapest repository-native checks that validate the baseline: a
targeted test or inspect command, build/type check, lint or format check, and a
safe runtime or integration probe when one is available. Never run unknown
scripts, install unreviewed dependencies, expose secrets, or mutate production
systems merely to complete reconnaissance. Treat generated files and lockfiles
according to repository policy, and keep the initial diff empty unless the task
explicitly requires a change.

Before a major change, state the affected contracts, likely regression paths,
required approvals, verification evidence, and rollback or recovery condition.
If the requested work crosses an authority boundary, stop at that boundary with
an actionable handoff instead of guessing access or permission.

## Context-restoration handoff

Return a compact, reproducible primer:

```text
Repository / commit / branch / working-tree state:
Applicable instructions and constraints:
Request, outcome, and non-goals:
Architecture and ownership map:
Relevant files, contracts, dependencies, and data flow:
Commands run and observed results:
Tests, runtime evidence, and freshness:
Assumptions, unknowns, and risks:
Proposed next action / owner / verification:
```

The primer is complete only when another agent can restart from it without
repeating broad exploration, while still knowing which claims require fresh
verification. Keep sensitive values out of the handoff and preserve links to
redacted evidence rather than copying secrets or customer data.
