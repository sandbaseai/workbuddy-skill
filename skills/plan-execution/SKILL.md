---
name: "plan-execution"
display_name: "计划执行"
display_name_en: "Plan Execution"
description: "Use when a written implementation plan exists and the work must be executed in small, reviewable batches with explicit verification and a durable handoff."
description_zh: "用于已有书面实施计划、需要按小批次执行，并通过明确验证和可追踪交接完成工作的场景。"
description_en: "Load and critically review a plan, establish safe workspace and authority boundaries, execute bite-sized tasks in order, verify each checkpoint, and close with integrated evidence."
category: "productivity"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with repository access, an isolated or explicitly authorized workspace, task tracking, and project-native verification commands"
---

# Plan Execution

## Use this skill when

Use this workflow when the user or repository provides a concrete implementation plan and the next action is execution rather than discovery. It is appropriate for feature work, migrations, documentation changes, and operational runbooks whose steps can be made observable.

Do not treat an incomplete wish list as a plan. If the plan lacks an objective, scope, dependencies, acceptance evidence, or a safe authority boundary, record the gap and resolve it from repository evidence when possible. If a critical ambiguity cannot be resolved safely, stop at that boundary and report the exact missing decision.

## Work contract

Before changing anything, record:

- **Objective:** the user-visible or operational outcome.
- **Scope:** files, services, environments, and exclusions.
- **Task ledger:** small ordered tasks with dependencies, owner, status, and proof command.
- **Authority:** operations explicitly allowed, protected branches/environments, and whether direct integration is authorized.
- **Recovery:** disposable workspace, checkpoint commit, rollback/abort path, and data-loss boundary.

Translate vague steps into observable completion criteria. Each task should produce a small diff or a concrete artifact and name the check that proves it. Preserve the plan's intent, but adapt provider-specific commands to WorkBuddy's available tools and repository-native conventions.

## Phase 1: load and review

1. Locate the canonical plan and read it completely, including linked requirements and constraints.
2. Inspect the current repository state, branch, uncommitted changes, relevant history, and existing checks before editing.
3. Verify an isolated workspace when parallel or risky work is involved. If the user explicitly authorizes the current workspace, record that exception and avoid unrelated files.
4. Review dependencies, ordering, assumptions, security boundaries, and missing acceptance evidence. Do not silently invent a destructive or externally visible step.
5. Convert the plan into a task ledger. Keep at most one dependent task in progress at a time; independent tasks may use the WorkBuddy parallel-agent-dispatch workflow with isolated scopes.

## Phase 2: execute in checkpoints

For each task:

1. Mark it `in_progress` with its scope and expected evidence.
2. Re-check prerequisites and the working tree immediately before editing.
3. Make the smallest coherent change that satisfies the task. Keep generated files synchronized when the repository requires them.
4. Run the task's focused check, inspect the diff, and classify failures as implementation, environment, or plan defects.
5. Record command output, changed paths, unresolved risks, and the next dependency. Mark the task `completed` only when its acceptance evidence passes.
6. Create a recoverable checkpoint when the repository's workflow benefits from it; never hide failing state behind a success claim.

Do not proceed past a failed prerequisite, a missing required input, or an authority boundary. Safe read-only diagnosis may continue; mutations require a valid scope and recovery path. Never expose secrets in logs, plans, or handoffs.

## Phase 3: integrated completion

After all tasks are individually complete:

- Re-read the original objective and map every requirement to evidence.
- Run the repository's full native validation, including lint, tests, build/package, and migration or deployment checks where relevant.
- Review the complete diff for scope creep, stale generated data, accidental credentials, incompatible interfaces, and unverified claims.
- Confirm branch, remote, release, and deployment state before reporting externally visible completion.
- Write a durable handoff containing the objective, completed ledger, exact verification commands/results, artifacts or commit identifiers, remaining risks, and rollback instructions.

If integration reveals a conflict, return to the affected task rather than patching around it. If a plan step is obsolete, preserve the evidence, document the deviation, and update the canonical plan or handoff before closing.

## WorkBuddy execution boundaries

WorkBuddy may perform direct repository edits, commits, pushes, releases, or merges only when the current user authorization covers them. Prefer disposable workspaces and protected-branch checks. Keep production, credentials, personal data, and third-party communications outside an Agent's scope unless separately authorized. When multiple Agents are used, isolate context and writes, review every result, reconcile conflicts centrally, and run integrated verification after merging their work.

## Handoff template

```text
Objective: <outcome>
Plan: <canonical plan and revision>
Tasks: <completed/blocked ledger with scope>
Evidence: <exact commands and results>
Changes: <files, commit, artifact, release, or deployment identifiers>
Deviations: <none, or reason and updated decision>
Risks/rollback: <remaining risks and recovery path>
Next action: <explicit follow-up or "none">
```
