---
name: "migration-validation"
display_name: "迁移后验证"
display_name_en: "Migration Validation"
description: "Use immediately after a migration, failover, cutover, restore, or platform move to verify health, performance, integrations, data integrity, security, and rollback readiness."
description_zh: "用于迁移、故障转移、切换、恢复或平台迁移后，验证健康度、性能、集成、数据完整性、安全性和回滚准备。"
description_en: "Run a validation-first post-migration gate across service health, traffic, data, dependencies, observability, security, and operations; verify platform-specific facts against authoritative documentation; and produce evidence-backed sign-off or rollback recommendations."
category: "development"
version: "0.1.0"
author: "adtork/compute-desk; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized migrated environment, migration and rollback plan, health and telemetry access, representative test transactions, dependency inventory, and applicable platform documentation"
---

# Migration Validation

Use this Skill at the post-cutover sign-off gate, not as a substitute for a migration plan. Validate the actual target environment with bounded, reversible checks and representative synthetic transactions. Do not declare success from infrastructure status alone, install components without authorization, or perform production writes beyond the approved test scope.

## Establish the baseline and scope

Record source and target environments, migration type and revision, cutover time, traffic cohort, data classes, service owners, dependencies, maintenance window, success thresholds, abort criteria, rollback point, and emergency contacts. Capture pre-migration baselines for availability, latency, error rate, throughput, capacity, queue depth, data counts/checksums, and critical business transactions where available. Mark unavailable baselines and unverified platform facts.

## Validate in layers

Run checks in increasing scope and stop when a critical gate fails:

1. **Target health:** nodes/instances, agents or extensions, drivers/runtime prerequisites, disks, network routes, time sync, certificates, configuration, secrets references, quotas, and capacity are present and healthy;
2. **Service behavior:** processes start, readiness and liveness checks are meaningful, dependencies resolve, authentication and authorization work, representative reads and approved synthetic writes succeed, and error handling is safe;
3. **Data integrity:** schema/version matches, counts and checksums or sampled records reconcile, indexes and constraints are usable, replication/queues drain as expected, idempotency holds, and no stale or cross-tenant data is exposed;
4. **Performance and resilience:** compare latency, throughput, saturation, retries, timeouts, queue lag, resource use, and error budgets with baseline; exercise bounded degraded dependencies, restart, retry, and failover paths when approved;
5. **Integrations and operations:** backups and restores are discoverable, monitoring/alerts/dashboards use the new identifiers, audit logs and security controls work, scheduled jobs/webhooks execute once, support/runbooks are updated, and owners can respond;
6. **Rollback readiness:** confirm the rollback artifact, data compatibility, traffic reversal, feature flags, checkpoints, and decision authority. Do not begin a rollback solely because a non-critical metric is noisy; use the predeclared thresholds and evidence.

Use repository-native smoke tests, health endpoints, migration checks, synthetic probes, logs, traces, metrics, and platform tools. Bound request rate, duration, target, and data. Never treat a provider's green control-plane state as proof of application correctness. Platform-specific commands, agent names, network behavior, limits, or support guarantees must be checked against the provider's current authoritative documentation and cited with its URL; if that source is unavailable, mark the claim unverified.

## Classify the gate

For each check record command or probe, revision, timestamp, target, expected result, observed result, evidence location, and limitation. Classify as **pass**, **pass with follow-up**, **fail—rollback/contain**, **not run**, or **unknown**. A missing monitoring signal, unverified data reconciliation, broken backup path, authorization failure, or inability to execute the rollback plan is not a clean pass. Separate platform/environment failures from application defects, and escalate safety, security, data-loss, or cross-tenant findings immediately.

## Sign off or recover

The handoff includes scope and baseline, migration revision, validation matrix, data and traffic evidence, performance comparison, integrations and observability, failed or skipped checks, thresholds, owners, residual risk, rollback decision, communication, and next checkpoint. Obtain the accountable sign-off before widening traffic. Re-run critical checks after remediation, after rollback, and after the stabilization window. Keep evidence immutable enough to support incident review and do not close findings because a ticket was opened.
