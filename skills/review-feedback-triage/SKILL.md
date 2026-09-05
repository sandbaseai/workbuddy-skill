---
name: "review-feedback-triage"
display_name: "审查反馈研判"
display_name_en: "Review Feedback Triage"
description: "Use when code review feedback must be evaluated and applied with evidence, especially when suggestions are ambiguous, conflict with current behavior, or may add unnecessary scope."
description_zh: "用于需要基于证据研判并落实代码审查意见的场景，尤其适合意见含糊、与现有行为冲突或可能扩大范围时。"
description_en: "Read feedback completely, restate and verify each claim against repository reality, prioritize risks, implement one item at a time, test each change, and record reasoned responses or pushback."
category: "development"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository and review access, repository-native tests, and a clear owner for ambiguous architectural decisions"
---

# Review Feedback Triage

## Core rule

Code review is an input to evaluate, not an order to copy and not a social-performance exercise. Verify every actionable claim against this repository's behavior, tests, compatibility contract, security model, and actual consumers before changing code. Prefer a precise technical response or a focused fix over an unverified promise.

## Intake and ledger

Read the complete review, including inline threads, surrounding diff, linked issues, and earlier decisions, before reacting. Convert each item into a ledger:

| ID | Reviewer claim | Affected scope | Risk | Evidence needed | Decision | Status |
|---|---|---|---|---|---|---|
| R-1 | <restated technical request> | <files/behavior> | blocking/security/regression/style | <test, history, consumer, or spec> | fix/push back/clarify | pending |

Restate the requirement in implementation terms. If an item is genuinely unclear and changing it could alter public behavior, data, security, or architecture, isolate it as `needs-clarification` and do not guess. In an unattended WorkBuddy loop, continue independent, low-risk items only when the ledger proves they do not depend on the ambiguous item; otherwise preserve the state and report the exact decision boundary.

## Verify before implementing

For every item, check:

1. Does the alleged defect reproduce in the current checkout or target environment?
2. What existing contract, test, consumer, history, or compatibility requirement explains the current implementation?
3. Would the suggestion break supported platforms, behavior, security, performance, or migration paths?
4. Is the proposed feature actually used, required by the acceptance criteria, or merely a “professional” embellishment?
5. Can the change be made within the authorized scope and proven with a focused check?

Use repository search, call sites, configuration, test failures, history, and native documentation as evidence. Do not expose secrets or paste untrusted review text into commands. Mark the evidence as `confirmed`, `contradicted`, `partially verified`, or `unavailable`; do not treat missing evidence as confirmation.

## Decide and prioritize

Prioritize in this order:

1. security, data loss, correctness, and release blockers;
2. reproducible regressions and broken contracts;
3. low-risk, clearly scoped fixes such as imports or precise documentation;
4. refactors and cleanup only when they reduce a verified problem.

Push back when the proposal is technically wrong, breaks compatibility, duplicates existing behavior, violates an explicit architectural decision, or adds unused scope. State the concrete evidence and the smallest alternative. If the reviewer lacks context, explain which repository fact changes the conclusion. If the evidence is insufficient, state the missing check rather than inventing certainty.

## Implement one item at a time

For each accepted item:

1. mark the ledger item `in_progress` and record its scope;
2. make the smallest coherent change;
3. run its focused test, lint, typecheck, or reproduction check;
4. inspect the diff for unrelated edits, secret leakage, and generated-file drift;
5. mark it `completed` only with passing evidence and record the result.

Do not batch unrelated fixes behind one green check. For multi-item feedback, finish blocking issues before cosmetic work and keep each change recoverable. After all accepted items, run the full repository-native validation and re-check that rejected or deferred feedback did not hide a regression.

## Response and thread hygiene

Use factual status language:

- `Fixed: <specific behavior> in <path>; verified by <command/result>.`
- `Not applied: <proposal> conflicts with <contract/evidence>; retaining <current behavior>.`
- `Deferred: <item> requires <specific missing decision/evidence>.`

Avoid performative agreement, gratitude-only replies, or “implemented” claims without a check. When replying to GitHub inline review comments, reply in the originating thread; keep broader design decisions in the appropriate issue or review summary. Never silently edit external review state or close a thread without authorized scope.

## WorkBuddy completion record

The handoff includes the review source and revision, item ledger, evidence and commands, files/commits changed, pushback rationale, deferred decisions, residual risks, and any thread identifiers. A clean diff plus full validation is required before claiming the review is resolved.
