---
name: "worktree-isolation"
display_name: "Git 工作区隔离"
display_name_en: "Git Worktree Isolation"
description: "Use when feature work, plan execution, or parallel Agents need isolation from the current checkout and changes must remain recoverable."
description_zh: "用于功能开发、计划执行或并行 Agent 需要与当前检出隔离，且变更必须可恢复的场景。"
description_en: "Detect existing isolation, choose a safe workspace, verify ignore and branch boundaries, establish a passing baseline, and clean up authorized temporary worktrees after integration."
category: "development"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with Git, an authorized repository checkout, repository-native setup/test commands, and permission to create or reuse worktrees"
---

# Git Worktree Isolation

## Purpose

Use a linked Git worktree when edits, experiments, plan execution, or parallel Agent work must be separated from the current checkout. Isolation is a safety boundary, not a substitute for authorization: record the allowed branch, files, remotes, and external effects before creating or reusing a workspace.

## Step 0: detect current state

Before creating anything, inspect the checkout without mutating it:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree 2>/dev/null
git branch --show-current
git status --short --branch
git worktree list --porcelain
```

Treat `git-dir != git-common-dir` as a linked worktree only after confirming the checkout is not a submodule. If already isolated, reuse it when its branch, path, cleanliness, and authority match the task; do not nest another worktree by habit. A detached HEAD requires an explicit branch or externally managed handoff before integration.

## Step 1: choose and verify a workspace

Honor an explicit WorkBuddy or user workspace preference. Otherwise prefer an existing project-local `.worktrees/`, then `worktrees/`, and finally a sibling path that does not overlap another checkout. Before using a project-local directory, verify it is ignored:

```bash
git check-ignore -q .worktrees || git check-ignore -q worktrees
```

If the directory is not ignored, do not place a worktree there until the repository's ignore policy is safely updated and reviewed. Never use a broad system directory, an existing user-data directory, or an ambiguous path. Use a descriptive, bounded branch name and confirm it does not already exist.

Create only within authorized scope:

```bash
git worktree add <path> -b <branch> <base>
```

Verify the new path, branch, base commit, remote, and repository instructions. Do not force-create, overwrite, delete, or reset a worktree to solve a naming conflict; choose a new bounded path or report the conflict.

## Step 2: establish a baseline

Detect project setup from repository instructions and manifests. Use the native setup/build command only when required and authorized; do not install arbitrary dependencies. Run the narrow baseline checks appropriate to the project (for example, the documented test, lint, typecheck, or package command) before editing.

Record:

- commit and branch used as the base;
- setup/tool versions and commands;
- baseline result and known failures;
- files or generated outputs that are intentionally excluded.

If baseline checks fail, preserve the evidence and classify the failure before proceeding. Continue only when the task explicitly owns the failure or the user has authorized work on it; never attribute pre-existing failures to the new change.

## Step 3: work and integrate safely

Keep one task or Agent write scope per worktree. Do not give parallel Agents concurrent write access to the same branch, generated file, lockfile, migration, release ref, or external record. Keep secrets and production credentials outside the worktree context.

Before integration, verify:

1. the worktree is clean except for task-owned changes;
2. the diff has no unrelated files, credentials, or generated drift;
3. focused checks pass and the task's acceptance evidence is recorded;
4. the target branch has not advanced unexpectedly;
5. merge/rebase/push authority is explicitly covered by the current task.

After integration, run full repository-native validation from the target checkout. If integration conflicts or validation fails, preserve the worktree and diagnostic state; resolve the task or abort through the repository's recoverable path rather than force-resetting broad files.

## Step 4: cleanup and handoff

Delete a temporary worktree only after its changes are integrated or explicitly abandoned, its useful evidence is recorded, and no process still depends on it. Confirm the exact path with `git worktree list` first, then use the least destructive native removal operation. Prune stale administrative metadata only for confirmed missing worktrees. Never delete another branch, fork, remote, or user worktree merely because it appears unused; verify ownership and scope first.

The handoff must state the worktree path, branch, base and integration commits, baseline/full checks, unresolved risks, cleanup result, and rollback path. A clean parent checkout and a passing target-branch validation are required before claiming completion.

## WorkBuddy exception

When the user explicitly authorizes direct work in the current shared checkout—as in an automated repository-maintenance loop—record that exception, skip unnecessary worktree creation, preserve pre-existing changes, and enforce the same branch, diff, validation, and recovery checks in place.
