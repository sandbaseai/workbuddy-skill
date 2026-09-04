---
name: "feature-flags"
display_name: "功能开关"
display_name_en: "Feature Flags"
description: "Use when implementing feature gates, gradual or percentage rollouts, A/B variants, dark launches, runtime configuration, model switching, or emergency kill switches; make evaluation deterministic, secure, observable, and temporary by default."
description_zh: "用于实现功能门控、渐进或按比例发布、A/B 变体、暗发布、运行时配置、模型切换或紧急关闭开关，并确保评估确定、安全、可观测且默认有期限。"
description_en: "Design feature flags for deterministic evaluation, safe progressive delivery, experimentation, runtime configuration, emergency mitigation, access control, observability, and disciplined lifecycle cleanup."
category: "development"
version: "0.1.0"
author: "majiayu000; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Flag service or versioned configuration; identity/tenant context; deployment and metrics systems"
---

# Feature Flags

Use feature flags to separate code delivery from user exposure and to make a reversible decision explicit. A flag is a production contract with an owner, purpose, evaluation context, default, expiry, and removal plan—not an unbounded second configuration system.

Do not use flags to bypass authorization, hide an irreversible migration, or keep dead branches indefinitely. Never target users by sensitive attributes without a documented purpose and access policy. Confirm the failure behavior when the flag service, cache, network, or configuration is unavailable.

## Define the flag contract

For every flag record:

- key, type (boolean, percentage, targeted, multivariate), description, owner, purpose, environments, and creation date;
- default and fallback value, evaluation context, target population, tenant boundary, and whether exposure is sticky;
- success and guardrail metrics, rollout stages, approval authority, expiry/removal date, and kill-switch policy;
- data classification, audit requirements, cache TTL, propagation delay, consistency expectation, and failure mode;
- migration plan for code, configuration, schemas, experiments, and consumers after the flag is removed.

Prefer typed schemas and a single source of truth. Reject unknown keys, invalid variants, impossible percentages, missing owners, expired approvals, and targeting rules that exceed the allowed context.

## Evaluate deterministically and safely

Evaluate server-side for authorization, entitlements, billing, and sensitive actions. Treat client-side evaluation as presentation only. Use a verified context containing principal, tenant, environment, app/version, and request ID; do not accept roles, plan, or identity supplied only by model or client text.

For percentage rollout, use a stable hash of a non-sensitive, opaque subject key plus flag key/salt. Keep assignment stable across requests and services, document the randomization unit, and avoid leaking the raw identifier into logs. For variants, validate weights, preserve a control, and record exposure separately from outcome.

Define safe behavior for:

- missing or malformed flag: conservative default;
- stale cache: bounded stale window and explicit risk classification;
- unavailable service: local last-known-safe value or fail-closed for sensitive actions;
- conflicting environments or policies: deny the broader scope and alert;
- partial propagation: show version and propagation status, never assume instant consistency.

Bound evaluation latency, result size, retries, and refresh frequency. Use idempotent updates, monotonic configuration versions, atomic snapshots, and a tested rollback or kill-switch path.

## Roll out progressively

1. Ship dormant code with unit, integration, accessibility, security, and migration tests.
2. Enable internally or for a synthetic cohort; verify logs, metrics, permissions, data paths, and recovery.
3. Expand by explicit cohorts or stable percentage; define exposure duration and stop criteria.
4. Compare outcome and guardrail metrics against a baseline, including errors, latency, cost, support, accessibility, privacy, and revenue where relevant.
5. Pause or roll back on unexplained regression, data drift, cross-tenant exposure, policy violation, or harm.
6. Remove the flag, dead branch, configuration, tests, dashboards, and documentation after the expiry criteria are met.

A rollout percentage is not evidence of success. Record eligible population, actual exposure, assignment stability, contamination, missing evaluations, time window, uncertainty, and practical effect. Do not infer causality from a flag that was targeted, changed mid-test, or exposed to a shifting population without accounting for it.

## Secure administration

Separate read, evaluate, propose, approve, and mutate permissions. Require stronger approval for security, payment, data, model, infrastructure, or high-impact user changes. Keep an immutable audit trail of who changed what, old/new values, scope, reason, ticket, timestamp, and propagated version; exclude secrets and unnecessary personal data.

Protect flag definitions and targeting data like production configuration. Encrypt in transit/at rest, restrict export, rotate service credentials, review access, and alert on unusual changes, broad targeting, disabled guardrails, or repeated emergency toggles. Never store API keys, passwords, or raw personal data in flag values.

## Lifecycle hygiene

Classify flags as release, experiment, operational kill switch, permission/entitlement, or configuration. Each class has different expiry, approval, and audit rules. At every review list active flags, owner, age, exposure, dependencies, stale branches, risk, and removal date. Treat an expired flag as a failing governance check, not a harmless reminder.

Test flag combinations deliberately: defaults, on/off, variant boundaries, service outage, stale data, permission changes, old app versions, rollback, and migration replay. Avoid combinatorial explosion by defining incompatible pairs and contract tests for high-risk combinations.

## Handoff

Report the flag contract, evaluation path, defaults, context and privacy controls, rollout cohort, metrics and baseline, approvals, propagation/version evidence, failure behavior, rollback, expiry, and removal state. Stop when ownership, authorization, default safety, or a side effect is unclear.
