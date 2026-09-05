---
name: "code-reviewer"
display_name: "代码审查"
display_name_en: "Code Reviewer"
description: "Use before building or merging a change to review intent, correctness, regressions, scope, maintainability, and security."
description_zh: "用于构建或合并变更前，审查用户意图、正确性、回归、范围、可维护性和安全性。"
description_en: "Perform a structured, diff-first code review with actionable findings, boundary-case reasoning, repository-native evidence, and a clear build or merge recommendation."
category: "development"
version: "0.1.0"
author: "MChat; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Git diff or reviewable patch, repository tests and checks, change context, and source history"
---

# Code Reviewer

Review the actual diff before build or merge. A verbal description without a patch is not evidence of a completed review. Assess behavior and user impact, not personal style preferences.

## Review method

1. Read the request, acceptance criteria, issue context, and compatibility promises.
2. Inspect the complete diff, surrounding code, callers, configuration, schemas, resources, and relevant history.
3. Confirm the change implements the intended behavior and does not silently broaden scope.
4. Trace success, boundary, error, retry, timeout, cancellation, concurrency, and partial-state paths.
5. Check old clients/data, version and configuration compatibility, resource references, migrations, and operational behavior.
6. Run repository-native focused checks; expand to broader tests or packaging checks when the change warrants it.

## Checkpoints

- **Correctness:** requirements, invariants, types, state transitions, edge inputs, ordering, and error semantics;
- **Regression:** defaults, fallbacks, validation, API/CLI/event contracts, schema and data behavior, and existing workflows;
- **Scope:** necessary files only, no accidental generated changes, dead code, debug output, or unrelated dependency/config edits;
- **Maintainability:** clear ownership, duplication, coupling, naming, testability, observability, and migration/cleanup path;
- **Security:** authentication and authorization, tenant isolation, input handling, secrets, unsafe paths, dependency provenance, logging, and privacy;
- **Operations:** timeouts, resource bounds, retries, rollout, alerts, rollback, performance, and failure recovery.

Prefer exact file/line evidence. Distinguish a confirmed defect from a question, suggestion, or missing evidence. Do not request speculative refactors or style-only changes as blockers. Never weaken tests, hide warnings, or mark a finding resolved without verification.

## Findings and decision

For each material finding report severity (critical/high/medium/low), location, violated expectation, evidence, impact, and concrete recommendation. A blocking finding must explain why it can cause incorrect behavior, data loss, security exposure, or an unsafe release. Include a regression test or validation step when appropriate.

When requested, use this machine-readable JSONL shape:

```json
{"severity":"high","file":"src/example.ts","line":42,"title":"Fallback is bypassed","evidence":"...","impact":"...","recommendation":"...","blocking":true}
```

End with:

- ✅ verified strengths and checks passed;
- ⚠️ non-blocking suggestions or evidence gaps;
- ❌ blocking findings that must be fixed before build/merge;
- files and commands reviewed, confidence, and the next authorized action.

If no material risk is found, state that explicitly and describe the review coverage. Do not manufacture findings to fill a quota.

