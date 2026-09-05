---
name: "respec"
display_name: "规格回修"
display_name_en: "Respec"
description: "Use when implementation, testing, or review reveals that an existing feature specification must be revised before work can proceed safely."
description_zh: "当实现、测试或审查发现现有功能规格需要修订，才能安全继续工作时使用。"
description_en: "Revise an existing feature specification from concrete implementation feedback while preserving traceability, separating requirement changes from implementation notes, and validating the revised acceptance contract before resuming delivery."
category: "development"
version: "0.1.0"
author: "fadiwahba; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Existing feature specification, implementation or review evidence, acceptance criteria, decision owner, and repository change history"
---

# Respec

Use this skill when a blocker, failed test, discovered constraint, or stakeholder clarification proves that an existing feature specification no longer describes the intended or feasible behavior. Revise the specification deliberately; do not silently change requirements in code or rewrite history.

## Establish the revision

1. Locate the canonical specification and confirm its version, status, owner, and affected feature.
2. Record the feedback that triggered revision: implementation evidence, test output, incident, dependency constraint, security review, or clarified user need.
3. Identify which requirement, acceptance criterion, interface, data rule, quality attribute, or non-goal is affected.
4. Separate facts, assumptions, decisions, and open questions. Preserve links to the original evidence.
5. Define the revision scope and explicitly list unaffected requirements.

Do not use a specification revision to conceal an implementation defect, evade a failing test, remove a safety requirement, or expand scope without approval. If the evidence is insufficient, create an investigation with an owner, deadline, and decision criterion.

## Revise the contract

Update the smallest canonical section needed. Keep user intent and observable behavior precise:

- actors, preconditions, triggers, and state transitions;
- inputs, outputs, errors, authorization, privacy, and tenant boundaries;
- functional acceptance criteria with observable pass/fail evidence;
- performance, reliability, accessibility, security, and operational budgets;
- compatibility with existing clients, data, migrations, and rollout states;
- explicit non-goals, dependencies, risks, and unresolved questions.

For each changed criterion, show old behavior, revised behavior, reason, evidence, owner, and effective version. Avoid implementation prescriptions unless they are required by a contract or constraint. Do not weaken a criterion merely because the current implementation fails it.

## Validate before resuming

Review the revised specification against the triggering evidence and ask:

1. Can another engineer distinguish the old and new behavior?
2. Is every changed requirement observable and testable?
3. Do examples, schemas, API contracts, data rules, and diagrams agree?
4. Are rollback, migration, compatibility, authorization, and failure paths covered?
5. Are affected tests, implementation tasks, documentation, and owners identified?
6. Is the decision authority and approval state explicit?

Create or update tests from the revised acceptance criteria, but keep implementation changes separate unless explicitly requested. Run the narrowest safe validation, then the repository-native broader checks required by the release gate. Report failures honestly and distinguish a spec defect from an implementation defect.

## Record and hand off

Add a revision note containing date, reason, evidence, changed sections, decision owner, approval, affected artifacts, compatibility/migration impact, follow-up tasks, and review trigger. Preserve prior versions or links; never erase historical decisions.

Handoff the revised contract, acceptance evidence, unresolved questions, implementation delta, test plan, risks, and next authorized action. Resume delivery only when the revised specification is internally consistent and the required approval or explicit exception is recorded.

