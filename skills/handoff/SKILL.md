---
name: "handoff"
display_name: "工作交接"
display_name_en: "Work Handoff"
description: "Writes a session handoff report to handoffs/ with project state, work done, decisions, and next steps. Use at session end or after significant work."
description_zh: "在会话或阶段结束时，将已验证的项目状态、完成事项、决策、风险和下一步整理成可继续执行的交接记录。"
description_en: "Create an actionable handoff from verified project state, completed work, decisions, risks, and next steps at a session or phase boundary."
category: "productivity"
version: "0.1.0"
author: "quarcs-lab; adapted for WorkBuddy by SandBase AI"
---

# Work Handoff

Preserve enough verified context for another person or future session to resume
without replaying the entire history. Use this Skill at a session boundary,
before ownership changes, after a release or incident, or when pausing a
multi-step task.

## Determine the destination

Use the location and naming convention already established by the workspace.
If none exists and the user asked for a saved artifact, use
`handoffs/YYYYMMDD_HHMM.md`. Otherwise provide the handoff in the conversation
instead of creating a new directory without need.

Before writing, inspect the latest relevant handoff, task plan, repository
status, recent changes, and verification output that are available. Treat the
current workspace and external system state as authoritative; do not copy stale
claims forward merely because they appeared in an earlier handoff.

## Build the handoff

Include only sections that carry useful information:

1. **Objective and scope** — the requested outcome, constraints, and explicit
   non-goals.
2. **Current state** — branch, revision, environment, deployed version, or
   artifact identifiers needed to resume accurately.
3. **Completed work** — concrete changes and results, linked to files, commits,
   issues, or artifacts where possible.
4. **Decisions** — the choice, rationale, alternatives rejected, and conditions
   that would justify revisiting it.
5. **Verification** — exact checks performed and their outcomes. Distinguish
   passing, failing, skipped, and not yet run.
6. **Open work and risks** — blockers, unresolved questions, known failures,
   dependencies, and assumptions that remain unverified.
7. **Next actions** — ordered, executable steps with owners or prerequisites
   when known. Put the best restart point first.

Prefer commands that are safe to rerun. When a command would mutate external
state, label that consequence instead of presenting it as routine setup.

## Accuracy and privacy rules

- Never describe planned or attempted work as completed.
- Preserve exact identifiers, paths, versions, dates, and error messages when
  they materially affect resumption.
- Do not include passwords, tokens, cookies, private keys, connection strings,
  personal data, or copied secret values. Refer to the approved secret name or
  credential location without exposing its contents.
- Do not claim a deployment, merge, message, or external update succeeded
  unless it was independently verified.
- Separate observed facts from inference and record uncertainty explicitly.
- Keep links stable and use repository-relative paths for repository files when
  the target format supports them.

## Verify before finishing

Compare the handoff against the live task state. Confirm that referenced files
and artifacts exist, commands are syntactically intact, statuses are current,
and the first next action can be executed by someone without hidden context.
If a file was requested, verify it was saved at the reported path.

End with a compact restart instruction. A handoff is successful when the next
worker can continue safely and correctly, not when it is a complete transcript.
