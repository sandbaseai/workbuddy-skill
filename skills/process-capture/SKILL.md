---
name: "process-capture"
display_name: "重复流程捕获"
display_name_en: "Recurring Process Capture"
description: "Use when a task has repeated or is explicitly worth preserving, to capture its stable pattern as a bounded backlog item or a tested Skill skeleton rather than losing it in chat."
description_zh: "用于某项工作已重复出现或明确值得沉淀时，把稳定模式记录为受控待办或可测试 Skill 骨架，而不是让经验留在聊天记录里。"
description_en: "Recognize repeatable work, extract its tools, inputs, outputs, corrections, and judgment, then produce either a backlog capture or a bounded Skill skeleton for later authoring."
category: "productivity"
version: "0.1.0"
author: "OKHP3/skillz; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "A version-controlled project with a durable backlog or Skill directory and repository-native validation"
---

# Recurring Process Capture

Use this Skill when the user says a task keeps recurring, asks to capture it,
or a clearly repeatable pattern emerges at the end of work. It is an intake and
structure step, not permission to fully author, publish, or broadly refactor a
Skill without the relevant authorization.

## Extract the observed pattern

Use the current conversation and repository evidence to record the task, times
observed, trigger language, inputs, tools/Skills used, ordered steps, outputs,
corrections, decisions, exceptions, and verification. Separate observed facts
from guesses. Do not infer a durable process from one-off work or from a
successfully completed command alone.

## Decide whether it is ready

Classify the pattern:

- **Developing judgment:** important decisions are still novel each time,
  evidence is sparse, or ownership is unclear. Capture a concise backlog item
  with date, task, observations, candidate family, evidence, and status
  `captured`; stop without creating a misleading Skill.
- **Stable procedure:** inputs, sequence, output, and acceptance checks recur
  with bounded variation. Continue to a skeleton and record the evidence that
  supports readiness.

Do not turn a personal preference, secret, temporary workaround, or
project-specific value into a generic Skill. Preserve privacy and authorization
boundaries; keep credentials and sensitive source material out of the capture.

## Shape the capture artifact

For a ready pattern, inspect nearby Skills and choose an existing family before
proposing a new one. Produce a minimal skeleton containing valid frontmatter,
precise positive and negative triggers, scope, prerequisites, section headings,
expected input/output, safety boundaries, validation gates, and pointers to
detail that still needs authoring. Mark assumptions and unresolved decisions;
do not invent references or helpers that do not exist.

Update the repository's canonical index or backlog according to its local
convention. A skeleton is explicitly `planned` until its body, references,
tests, packaging, and quality audit are complete; move it to active only with
that evidence. Avoid changing unrelated files or duplicate trigger rows.

## Handoff to authoring

Pass a ready skeleton to the Skill authoring workflow with the observed
examples, edge cases, correction history, acceptance assertions, and missing
research. The next authoring pass should evaluate trigger precision, safety,
portability, context cost, failure behavior, and packaging. Never claim the
skeleton itself is production-ready.

Return the chosen classification, evidence count, capture/backlog or skeleton
path, family decision, unresolved judgment, exact files changed, validation
performed, and the next authoring/review trigger. Keep the capture reversible
and auditable.
