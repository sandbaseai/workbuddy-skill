---
name: "regression-risk-review"
display_name: "回归风险审查"
display_name_en: "Regression Risk Review"
description: "Use when reviewing behavior changes that may break existing users, flows, integrations, contracts, or production data."
description_zh: "用于审查可能破坏现有用户、流程、集成、契约或生产数据的行为变更。"
description_en: "Perform an evidence-first regression review of changed behavior, identify affected contracts and failure modes, prioritize actionable findings, and report reproducible evidence with safe follow-up."
category: "development"
version: "0.1.0"
author: "aydabd; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Git diff, repository tests and checks, issue or change context, and access to affected interfaces"
---

# Regression Risk Review

Review behavior changes for likely breakage in existing users, workflows, integrations, contracts, and production data. Focus on correctness and user impact; do not turn style preferences into findings.

## Establish scope and evidence

1. Read the change description, acceptance criteria, compatibility promises, and migration notes.
2. Inspect the complete diff, surrounding code, callers, configuration, schemas, fixtures, and relevant history.
3. Identify affected personas, paths, clients, tenants, data states, and operational dependencies.
4. Run the smallest repository-native checks that exercise the changed behavior, then expand to integration or end-to-end checks when the blast radius warrants it.
5. Prefer exact evidence from code, tests, logs, traces, or reproducible commands. Mark assumptions and unverified paths explicitly.

Do not infer safety from a passing unit test alone. Check defaults, error paths, retries, permissions, concurrency, old data, old clients, and partial rollout states.

## Review the high-risk behavior changes

Look specifically for:

- changed fallback or degraded behavior;
- deleted branches or unreachable recovery paths;
- changed defaults, configuration precedence, or feature-flag behavior;
- changed validation, coercion, normalization, or boundary handling;
- changed ordering, pagination, deduplication, or ranking;
- changed error mapping, status codes, retryability, or timeout behavior;
- changed schemas, migrations, serialization, or data ownership;
- changed authorization, tenant isolation, secrets, or privacy boundaries;
- changed event names, payloads, API contracts, CLI output, or automation assumptions.

Trace each suspicious change through its callers and consumers. Verify both the new path and the compatibility path for existing inputs. Check empty, malformed, duplicate, stale, maximum-size, unauthorized, concurrent, and partially migrated states.

## Prioritize findings

Report only actionable risks. For each finding include:

1. **Severity:** critical, high, medium, or low, based on impact and exploitability or likelihood.
2. **Location:** file and line or the smallest precise diff hunk.
3. **Behavior:** what changed and which existing contract or invariant it can violate.
4. **Evidence:** exact code path, test result, input, command, or trace that supports the claim.
5. **Impact:** affected users, integrations, data, security, reliability, or operations.
6. **Fix:** a concrete mitigation, compatibility guard, test, migration, flag, or rollback step.

Use this JSONL shape when machine-readable output is requested:

```json
{"severity":"high","file":"src/example.ts","line":42,"title":"Existing fallback is bypassed","evidence":"...","impact":"...","recommendation":"..."}
```

Keep one finding per line, valid JSON, and avoid secrets or personal data. If no material risk is found, say so and list the paths and checks reviewed. Do not manufacture a finding to fill a quota.

## Close the review safely

Recommend regression tests for each accepted risk, including representative old inputs and failure states. For high-blast-radius changes, require a canary, compatibility window, feature flag, migration checkpoint, or explicit rollback/roll-forward procedure. Confirm that monitoring can detect the regression and name the owner for unresolved risk.

Handoff the scope, checks run, findings, confidence, unknowns, required approvals, and next authorized action. Re-review when the implementation, contract, rollout cohort, or data migration changes.

