---
name: "cloud-resource-health"
display_name: "云资源健康诊断"
display_name_en: "Cloud Resource Health"
description: "Use when diagnosing an unhealthy or degraded cloud resource from provider status, metrics, logs, dependencies, deployments, and permissions. Start with bounded read-only evidence and produce a classified remediation plan."
description_zh: "用于根据云厂商状态、指标、日志、依赖、部署和权限证据诊断不健康或降级的云资源；先进行有边界的只读检查，再产出分级修复计划。"
description_en: "Identify the exact resource and scope, assess service-specific health signals, correlate logs and metrics with changes, classify impact and confidence, and propose authorized, reversible remediation with verification and escalation paths."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to provider resource metadata, logs, metrics, deployment history, and permissions, plus an approved change and incident-management path"
---

# Cloud Resource Health

## Purpose and safety boundary

Diagnose a named cloud resource using evidence from the resource, its dependencies, recent changes, and the affected user path. This Skill is read-only by default. It does not reboot, resize, delete, change IAM/network policy, alter concurrency, or enable logging. Any remediation must have an owner, authorization, impact window, rollback/recovery plan, and post-change verification.

Do not assume that a provider status of “available” means the workload is healthy. Resolve the exact account/project, region, resource identifier, tenant scope, and time window before drawing conclusions. Redact account identifiers, customer data, tokens, private addresses, and raw log payloads.

## Inputs

Capture:

- exact error, affected user journey, first/last occurrence, frequency, and severity;
- provider, account/project, region, resource type and identifier, environment, and owner;
- recent deploys, config/IAM/network changes, scaling events, provider events, and incident timeline;
- relevant health metrics, logs, traces, dependency status, quotas, limits, and alert state;
- baseline comparison window and any concurrent changes or known data gaps.

If multiple resources match, stop and request a narrower scope. If telemetry is missing, report the blind spot and lower confidence rather than treating “no data” as “healthy.”

## Workflow

1. **Preserve and scope the symptom.** Create a short sanitized timeline and identify the failing user or system path. Separate current impact from historical warnings.
2. **Identify the resource.** Resolve type, immutable identifier, region/account, lifecycle state, tags/labels, owner, and dependencies. Verify the target before querying or proposing action.
3. **Check provider and control-plane state.** Read resource status, recent events, quotas, scheduled maintenance, deployment state, and permission errors. Keep provider state separate from data-plane behavior.
4. **Assess service-specific signals.** Choose only the metrics that test the symptom: availability, error/throttle rate, latency percentiles, saturation, capacity, queue age, connections, storage, health of backends, or replication.
5. **Correlate logs and changes.** Use bounded time ranges and narrowly filtered queries. Align timestamps with deployments, scaling, certificates, credentials, network changes, dependency failures, and provider events.
6. **Test dependencies from the failing path.** Check DNS, routing, policy, identity, upstream/downstream health, rate limits, and circuit breakers without broad scans or intrusive probes.
7. **Classify and rank.** Report impact as critical/high/medium/low only with an explicit rubric; distinguish confirmed, probable, possible, and unknown causes. Record competing hypotheses and missing evidence.
8. **Produce a phased plan.** Separate immediate containment, short-term repair, and long-term prevention. For every action include authority, blast radius, expected effect, rollback/recovery, owner, and verification. Never hide a mutation inside a “diagnostic” command.
9. **Verify and close.** After an authorized change, rerun the original failing-path check, compare baseline metrics, inspect dependency and customer signals, and record residual risk. Escalate when impact, permissions, data integrity, or recovery is uncertain.

## Health signal guide

| Resource family | Useful signals | Common blind spot |
|---|---|---|
| Compute/container | readiness, restarts, CPU/memory, throttling, task/replica count, exit reasons | process liveness can hide dependency or capacity failure |
| Function/serverless | errors, throttles, duration p95/p99, concurrency, cold starts, downstream calls | retries can multiply cost and hide the original error |
| Database | connections, lock waits, query latency, storage, I/O, replication, failover state | “available” does not prove query or write health |
| Load balancer/API | backend health, response latency, 4xx/5xx, saturation, TLS, route/policy changes | aggregate success can hide one bad backend or tenant |
| Queue/stream | age, depth, throughput, retries, poison messages, consumer lag | a growing queue may be a symptom, not the root cause |
| Object/data store | request errors, throttling, capacity, replication, lifecycle, access policy | a successful request can still violate retention or residency rules |

Use the smallest signal set that can distinguish the leading hypotheses. Do not dump all logs or metrics into a report.

## Safe read-only examples

Use placeholders, current provider syntax, and an approved account policy. These commands inspect state; they do not authorize a change.

```bash
# Example AWS discovery and health reads with explicit scope.
aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --region "$REGION"
aws ec2 describe-instance-status --instance-ids "$INSTANCE_ID" --region "$REGION"
aws ecs describe-services --cluster "$CLUSTER" --services "$SERVICE" --region "$REGION"
aws rds describe-db-instances --db-instance-identifier "$DB_ID" --region "$REGION"
aws cloudwatch get-metric-data --metric-data-queries file://queries.json \
  --start-time "$START_UTC" --end-time "$END_UTC" --region "$REGION"
```

For log queries, bound the time range, filter to the named resource, cap results, and exclude payload fields. For permissions, report the denied action and required owner; never broaden a role just to make diagnosis succeed.

## Findings report

```text
Resource/scope/owner: <immutable id, account/project, region, owner>
Symptom/impact/window: <user path, severity, UTC interval, frequency>
Baseline and evidence: <metrics, logs, traces, provider events, freshness>
Health result: healthy | degraded | unhealthy | unknown
Issues: <impact, evidence, confidence, competing hypotheses>
Root cause: confirmed | probable | possible | unknown
Immediate containment: <authorized action, blast radius, rollback, owner>
Repair/prevention: <change, dependency, cost, security, recovery impact>
Verification: <original path, before/after signals, observation window>
Gaps/escalation: <missing access/data, next owner, deadline>
```

## Handoff checklist

- [ ] Exact resource, scope, owner, environment, and time window are verified.
- [ ] The user/system symptom is preserved and separated from unrelated warnings.
- [ ] Provider state, data-plane behavior, dependencies, changes, and telemetry are correlated.
- [ ] Metrics/log queries are bounded, relevant, current, and privacy-safe.
- [ ] Severity, root cause, confidence, unknowns, and evidence are explicit.
- [ ] Remediation is separated from diagnosis and includes authorization, blast radius, rollback, and verification.
- [ ] The original failing path is retested after any approved change.
- [ ] Residual risk, telemetry gaps, escalation, and prevention owner are recorded.
