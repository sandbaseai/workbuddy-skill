---
name: "backend-review"
display_name: "后端变更审查"
display_name_en: "Backend Review"
description: "Use when reviewing backend handlers, services, jobs, persistence, validation, errors, transactions, dependencies, or service contracts for correctness and operational risk."
description_zh: "用于审查后端处理器、服务、任务、持久化、校验、错误、事务、依赖或服务契约中的正确性与运营风险。"
description_en: "Perform a diff-first backend review using concrete code and test evidence; check validation, error and status semantics, transaction and dependency boundaries, authorization, idempotency, and safe defaults; then report prioritized findings and regression tests."
category: "development"
version: "0.1.0"
author: "aydabd/github-bootstrap; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized backend repository, change diff, service and data contracts, dependency configuration, repository-native tests, and relevant operational documentation"
---

# Backend Review

Review backend changes for behavior, contract, data, security, and operational correctness. Start with the diff and follow only the affected execution paths. Prefer exact evidence over style preferences or assumptions, and do not call a change safe because it compiles or a happy-path test passes.

## Establish scope and execution path

Identify entry points, handlers, workers, services, repositories, external calls, queues, database writes, caches, configuration, identities, and callers affected by the change. Read the public contract, validation rules, error model, transaction policy, retry behavior, migrations, and adjacent tests. State unknown consumers, unavailable environments, pre-existing changes, and out-of-scope systems. Never use real secrets or production data for review.

## Review the critical boundaries

Check:

- **Input and authorization:** validate type, size, encoding, requiredness, ranges, nested data, and ownership at the service boundary; authenticate and authorize every privileged or object-level operation; default to deny when identity or tenant context is absent;
- **Contracts and errors:** preserve request/response and event schemas, status codes, error identity, retryability, pagination, idempotency, and backward compatibility; avoid leaking stack traces, secrets, internal topology, or sensitive records;
- **Transactions and consistency:** keep atomic changes inside the correct boundary, order side effects deliberately, handle partial failure, isolation, retries, duplicate delivery, outbox/inbox behavior, and rollback; never assume a database transaction covers an external call;
- **Dependencies and resources:** respect service ownership and layering, timeouts, cancellation, connection limits, circuit breakers, bounded retries, backpressure, and cleanup of files, goroutines, locks, cursors, and response bodies;
- **Persistence and migrations:** check constraints, nullability, indexes, locking, query shape, tenant filters, data exposure, migration order, backfill safety, mixed-version behavior, and downgrade or recovery paths;
- **Defaults and failure behavior:** inspect empty, malformed, expired, unavailable, unauthorized, duplicated, concurrent, and oversized inputs; require safe defaults, explicit failures, useful structured logs, metrics, correlation IDs, and no sensitive telemetry;
- **Tests and operations:** verify focused and boundary tests, contract tests, race/concurrency cases, migration checks, alerting, rollout, rollback, and runbook impact. Treat untested paths and environment-dependent claims as limitations.

Use repository-native linters, tests, static analysis, and local fixtures. Record commands, versions, scope, exit codes, and limitations. Do not install or execute untrusted downloaded code merely to review a diff. Do not broaden a test or scan into unrelated systems without authorization.

## Report findings

For each material finding provide severity and rationale, file and symbol or stable location, concrete evidence, affected behavior or contract, preconditions, impact, recommended fix, and a regression-test idea. Classify confirmed defects separately from likely risks, observations, and unknowns. Prioritize authorization or tenant failures, data loss or corruption, inconsistent transactions, contract breaks, unbounded resource use, and secret or sensitive-data exposure. Avoid style-only comments unless they create a correctness, security, or maintenance risk.

Use the repository's required finding format when one exists; otherwise provide concise Markdown or JSONL. Do not include credentials, private data, or unnecessary exploit instructions. If tests fail for provider, dependency, or environment reasons, report that separately from product findings rather than downgrading or hiding it.

## Handoff and retest

Confirm the changed path, affected callers, failure behavior, tests run, and unresolved questions. Recommend the smallest durable fix, acceptance criteria, owner, rollout guard, rollback step, and monitoring where relevant. Re-test after remediation, including denied, invalid, duplicate, timeout, partial-failure, and concurrent cases as applicable. The final handoff states whether the change is ready, ready with tracked follow-ups, or blocked by evidence, and names the exact next review gate.
