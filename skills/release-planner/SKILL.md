---
name: "release-planner"
display_name: "发布规划"
display_name_en: "Release Planner"
description: "Use when planning a production release, phased rollout, migration sequence, canary, rollback, or measurable go/no-go decision."
description_zh: "用于规划生产发布、分阶段放量、迁移顺序、金丝雀、回滚策略或可度量的发布准入决策。"
description_en: "Create an actionable release plan that connects deployment order, data migration, rollout waves, blast-radius controls, observability, rollback, ownership, and stakeholder communication."
category: "development"
version: "0.1.0"
author: "GustavoGutierrez; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Deployment pipeline, telemetry, release owner, migration tooling, incident response, and stakeholder channels"
---

# Release Planner

Use this skill to produce a release execution plan that is safe to operate and easy to audit. Treat deployment sequence, migration plan, rollout waves, risk controls, and rollback strategy as separate artifacts that must agree with one another.

## Establish release readiness

Record the release scope, owner, target window, dependencies, affected users, change classification, blast radius, and success measures. Confirm the artifact is immutable, provenance is known, configuration is reviewable, and the release can be observed before the first user is exposed.

Resolve backward/forward compatibility before sequencing incompatible changes. If rollback is impossible or could lose data, call this out as a blocking constraint and define a roll-forward or recovery plan before proceeding.

Define measurable go/no-go gates, such as error-rate delta, p95/p99 latency, saturation, queue depth, correctness checks, business KPI deviation, migration lag, support volume, or security alerts. Specify the measurement source, observation window, threshold, decision owner, and stop condition.

## Build the five release artifacts

### 1. Deployment sequence

List each component, configuration, feature flag, schema change, and operational task in dependency order. Explain why the order is safe, which steps are reversible, and what must be validated before the next step.

### 2. Migration plan

Prefer expand-and-contract for schema and data changes: introduce compatible structures, deploy readers/writers, backfill in bounded batches, verify counts and invariants, switch traffic, and remove temporary paths only after the compatibility window. Define throttling, pause/resume, idempotency, checkpoints, locks, retry behavior, and recovery for partial failure. Never treat a successful command as proof of data correctness.

### 3. Rollout waves

Start with internal or low-risk exposure, then increase by an explicit cohort, region, tenant, percentage, or time window. For every wave state entry criteria, exposure, duration, metrics, approval owner, and exit or rollback gate. Keep feature flags deterministic, auditable, expiring, and safe by default.

### 4. Risk and blast-radius register

For each step and wave, record failure mode, affected boundary, likelihood, impact, detection signal, mitigation, owner, and residual risk. Include dependency quotas, capacity, data divergence, privacy/security impact, incompatible clients, and support readiness. Reduce blast radius through isolation, rate limits, canaries, circuit breakers, and bounded concurrency.

### 5. Rollback and recovery

Define a specific trigger and the exact command or procedure, owner, authorization, expected duration, data implications, verification, and communication. Distinguish code rollback, flag disablement, traffic reversal, schema rollback, and data restore. If a migration is irreversible, define safe forward repair and preserve evidence; do not promise a rollback that cannot work.

## Operate the release

Before exposure, verify dashboards, alerts, logs, traces, synthetic checks, runbooks, access, on-call coverage, support macros, status messaging, and an abort channel. Use a deployment lock or clear ownership so concurrent releases cannot invalidate the plan.

During each wave:

1. Record the exact artifact, configuration, cohort, start time, and baseline.
2. Validate health, correctness, user impact, capacity, cost, and security signals.
3. Hold for the declared observation window; do not advance on intuition alone.
4. Stop and execute the recovery path on a breached gate or unexplained anomaly.
5. Record evidence and the decision before advancing.

Communicate what changes, who is affected, timing, expected impact, monitoring, and escalation. Notify stakeholders at preparation, wave start, gate decision, incident, completion, and post-release review points.

## Close and improve

After full rollout, verify adoption, error budgets, data reconciliation, alerts, costs, and support impact. Remove temporary flags, dual writes, compatibility code, access, and migration infrastructure only when their exit criteria are met. Publish the final outcome, deviations, unresolved risks, owners, evidence links, and review date. Feed incidents and near misses into the next release plan.

