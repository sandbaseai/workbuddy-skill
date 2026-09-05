---
name: "checkpointed-agent-loop"
display_name: "可恢复 Agent 检查点循环"
display_name_en: "Checkpointed Agent Loop"
description: "Use for long-running or failure-prone WorkBuddy tasks that need bounded retries, durable recovery state, and explicit verification evidence before completion."
description_zh: "用于长时间运行或容易失败的 WorkBuddy 任务，需要有限重试、可持久恢复状态，并在完成前记录明确验证证据。"
description_en: "Run bounded attempts through a durable planned/running/verifying state machine, record sanitized evidence, resume from the next action after interruption, and fail closed at external decision boundaries."
category: "productivity"
version: "0.1.0"
author: "davepoon/buildwithclaude; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with Python 3.9+, a project-local checkpoint path, authorized tool execution, and repository-native verification commands"
---

# Checkpointed Agent Loop

## Purpose

Use a durable checkpoint when work may span sessions, be interrupted, require bounded retries, or need proof that verification actually ran. The checkpoint stores task state, a next action, attempt count, sanitized reasons, and verification evidence. It does not execute commands, call models, spawn Agents, access secrets, or contact a network service; WorkBuddy remains responsible for each tool call and policy decision.

Do not use this for a one-line edit or a workflow that already has its own durable runner. A checkpoint is recovery state, not a license to loop forever or bypass approval.

## State machine

Only these states and transitions are valid:

```text
planned -> running
running -> verifying | failed | blocked
verifying -> succeeded | running | failed | blocked
```

Entering `running` consumes one attempt. A finite positive `max_attempts` cannot be exceeded. `succeeded`, `failed`, and `blocked` are terminal; terminal state cannot be edited. `succeeded` is rejected unless at least one `passed` evidence record was added while in `verifying`.

## Initialize safely

Choose a project-local checkpoint path excluded from application commits, such as `.agent/checkpoints/task.json`. Verify the directory and ignore policy before use. Keep objectives, reasons, check names, and artifact paths free of API keys, tokens, passwords, PII, and raw secret-bearing logs.

```bash
python3 <skill-dir>/scripts/checkpoint-loop.py init \
  --file .agent/checkpoints/task.json \
  --task "data-migration" \
  --objective "Migrate the user table without losing records" \
  --max-attempts 3 \
  --next-action "Inspect the current migration and test fixture"
```

Initialization must not overwrite an existing checkpoint. Treat a malformed or manually edited checkpoint as invalid and stop for review; do not infer missing state.

## Operating protocol

1. Read the checkpoint status at the start of every session. Inspect the current repository/workspace and confirm the saved `next_action` is still safe and relevant.
2. Transition `planned` or a retrying `verifying` task to `running` with one bounded action. Do not expand one attempt into an unbounded plan.
3. Perform only the authorized action with normal WorkBuddy tools. Keep unrelated edits and external effects outside the checkpoint scope.
4. Transition to `verifying` before deciding the outcome. Run the focused check yourself; the helper only records the observed result.
5. Record `passed` or `failed` evidence with a safe check name and existing artifact path. Never rewrite a failed outcome into a pass.
6. On a pass, transition to `succeeded`. On a reproducible fixable failure, transition to `running` with a concrete next action and reason, respecting the attempt ceiling. Use `failed` for terminal technical failure and `blocked` only for a real external dependency or decision boundary.
7. After success, run integrated repository validation when the task changes shared behavior, then retain the checkpoint as part of the handoff or archive it under the repository policy.

Commands:

```bash
python3 <skill-dir>/scripts/checkpoint-loop.py status --file .agent/checkpoints/task.json --format summary
python3 <skill-dir>/scripts/checkpoint-loop.py transition --file .agent/checkpoints/task.json --to running
python3 <skill-dir>/scripts/checkpoint-loop.py transition --file .agent/checkpoints/task.json --to verifying
python3 <skill-dir>/scripts/checkpoint-loop.py evidence --file .agent/checkpoints/task.json --check "pytest tests/test_migration.py" --outcome passed --artifact artifacts/migration-test.txt
python3 <skill-dir>/scripts/checkpoint-loop.py transition --file .agent/checkpoints/task.json --to succeeded
```

For a retry, provide both `--next-action` and `--reason`. For `blocked` or `failed`, provide a sanitized reason. Never automatically retry destructive actions, deployments, payments, permission changes, or third-party writes.

## Evidence contract

Evidence is an observation, not a promise. Record command/check identity, outcome, timestamp, and a relative or absolute artifact path only after confirming the artifact exists and is safe to share. Keep the checkpoint small; store detailed logs separately under the repository's retention policy. A missing tool, timeout, permission denial, or rate limit is evidence of unavailable coverage, not a passing result.

## Recovery and safety

On resume, read `status`, `attempts`, `next_action`, `history`, and `evidence`; inspect the working tree before repeating anything. Do not repeat a completed attempt merely because chat context is gone. If the checkpoint is malformed, has an impossible transition, exceeds its attempt budget, or disagrees with repository state, stop and report the discrepancy.

Destructive or externally visible work still follows the normal WorkBuddy approval and authority boundary. A checkpoint cannot grant tools, credentials, production access, or merge/push authority. Keep concurrent Agents in separate checkpoints and scopes; reconcile their results before integrated verification.

## Handoff

Report task/objective, checkpoint path, final state, attempt count, completed actions, exact verification checks and outcomes, artifact paths, blocked/failed reasons, deviations, residual risks, and the next safe action. A task is complete only when the terminal state and passing evidence both exist and the repository-level claim is supported by fresh validation.
