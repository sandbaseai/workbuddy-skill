---
name: "aws-resilience-assessment"
display_name: "AWS 韧性评估"
display_name_en: "AWS Resilience Assessment"
description: "Use when assessing an AWS workload's failure modes, dependencies, availability, recoverability, RTO/RPO, disaster recovery, observability, or resilience improvement roadmap from architecture evidence, IaC, or authorized read-only inventory."
description_zh: "基于架构资料、IaC 或经授权的只读资源清单，评估 AWS 工作负载的故障模式、依赖、可用性、RTO/RPO、灾难恢复、可观测性与韧性改进路线。"
description_en: "Assess AWS workload failure modes, dependencies, availability, recoverability, RTO/RPO, disaster recovery, observability, and resilience roadmaps from architecture evidence, IaC, or authorized read-only inventory."
category: "development"
version: "0.1.0"
author: "Amazon.com, Inc. or its affiliates; adapted for WorkBuddy by SandBase AI"
license: "MIT-0"
---

# AWS Resilience Assessment

Use this skill for evidence-based resilience reviews of AWS workloads. It supports architecture documents, diagrams, incident history, infrastructure as code, monitoring exports, and explicitly authorized read-only cloud inventory. It does not require live AWS access and must not infer permission to inspect an account from a request to review documents.

Default live inspection to read-only `List`, `Get`, and `Describe` operations. Confirm the exact accounts, regions, role, data sensitivity, and scope before access. Do not change infrastructure, trigger failover, stop instances, modify scaling, inject faults, restore backups, rotate credentials, or expose resource data unless the user separately authorizes that exact action.

## Establish the assessment contract

Record:

- workload, owners, environments, accounts and regions in scope;
- critical user journeys and business functions;
- availability targets, SLI/SLO/SLA definitions and measurement windows;
- maximum tolerable downtime, RTO, RPO and data-loss semantics;
- compliance, data residency, security, budget and operational constraints;
- evidence sources, observation time, known gaps and desired report audience.

Do not invent targets when none exist. Distinguish a stated objective from observed performance and a contractual commitment. RTO is a recovery-time target, not proof that recovery completes within it; RPO is acceptable data-loss time, not automatically the backup interval.

## Build a dependency and blast-radius model

Map entry points, identity, DNS, edge, networking, compute, orchestration, queues, databases, caches, object storage, external providers, control planes, observability, CI/CD and human operations. For each dependency record direction, protocol, timeout, retry, data or state, region or Availability Zone placement, ownership, quota, fallback and recovery path.

Trace every critical journey end to end. Identify shared fate hidden behind apparently redundant components: accounts, regions, subnets, routing, KMS keys, IAM roles, secrets, container registries, deployment pipelines, quotas, schema control planes, third-party APIs, operators and recovery credentials.

Draw only relationships supported by evidence. Mark inferred and unknown edges explicitly. A multi-AZ or multi-region label is not sufficient; verify traffic steering, state replication, write authority, consistency, failover criteria, capacity and tested recovery.

## Analyze failure modes

For each component and dependency, consider unavailable, slow, stale, overloaded, corrupted, misconfigured, unauthorized, partitioned, quota-exhausted and operational-error states. Include zonal and regional impairment, control-plane unavailability, deployment failure, credential or certificate expiry, data deletion, dependency throttling, retry amplification, observability loss and recovery-system failure.

Describe the initiating condition, affected journey, detection signal, propagation path, existing prevention and containment, recovery mechanism, estimated impact, and evidence that the control works. Separate single-component failure from correlated and cascading failure. Avoid scoring risks before documenting the causal path.

Treat retries, queues, caches, replicas and autoscaling as conditional controls with their own limits. Verify deadline budgets, backoff and jitter, idempotency, queue age and redrive, cache freshness, replica lag, scaling delay, quota headroom and downstream capacity. A fallback that is untested or shares the same dependency remains a hypothesis.

## Assess recovery and data protection

Inventory authoritative data, replication mode, backup policy, point-in-time recovery, retention, immutability, encryption keys, cross-account or cross-region copies, restore dependencies, runbooks and recovery ownership. Verify what is backed up, what is excluded, and whether application configuration, schemas, identities and external state can be reconstructed.

Use successful restore exercises—not backup job success—as recovery evidence. Measure detection, decision, provisioning, data restore, reconciliation, traffic shift and validation separately. Compare the full observed recovery path with RTO and the recovered data point with RPO.

For active/passive or multi-region designs, state write authority, replication and conflict semantics, failover and failback triggers, DNS or routing behavior, warm capacity, data divergence handling and operator access during a regional event. Include the risk introduced by manual coordination.

## Evaluate observability and operations

Connect telemetry to user journeys and failure modes. Check availability, latency, correctness, saturation, backlog or age, dependency health, replication lag, backup and restore, deployment status, quota headroom and failover readiness. Confirm alarm thresholds, missing-data treatment, routing, escalation, runbook links and ownership.

Avoid declaring resilience from dashboards alone. Review incident and postmortem evidence, alarm exercises, game days, restore tests, capacity tests, deployment rollbacks and actual mean time to detect, engage, mitigate and recover. Note survivorship bias and gaps in retained telemetry.

Assess change safety: small reversible deployments, health gates, automatic or manual rollback, database compatibility, immutable artifacts, configuration validation, separation of duties and the ability to deploy or recover when a primary control plane is impaired.

## Prioritize improvements

Score only after the failure path and evidence are documented. Use likelihood and impact ranges with confidence, not false precision. Include affected business function, blast radius, target violated, detection quality, control maturity, recovery evidence and residual risk.

For each recommendation provide the failure mode addressed, proposed control, assumptions, implementation owner, prerequisites, cost and complexity range, expected risk reduction, validation method, rollback, and residual risk. Offer staged options when cost and resilience trade off. Prefer removing shared fate and proving recovery over adding components that create unowned complexity.

Order work by risk reduction, dependencies and learning value. Separate immediate containment, near-term verification, architectural changes and accepted risks. Do not recommend services solely because they are AWS-native; tie each change to a demonstrated failure mode and target.

## Design safe resilience experiments

Begin with a steady-state hypothesis expressed in user-visible and system signals. Choose the smallest fault that can falsify a control, define exact resources and duration, abort thresholds, monitoring, observers, rollback or stop mechanism, expected blast radius and post-experiment reconciliation.

Prefer simulation, staging, fault-free validation, or a bounded game day before production injection. Production experiments require explicit authorization, capable operators, verified stop controls, sufficient headroom and an agreed communication window. Never run a destructive or costly experiment merely because the user requested an assessment.

## Validate and report

Cross-check the dependency map against IaC and inventory; reconcile resource counts, regions, routes, replication, backup configuration, alarms and runbooks. Distinguish configuration evidence, observed runtime evidence, tested recovery evidence and assumptions. Have every major conclusion point to at least one evidence item or be labeled unverified.

Return assessment metadata, executive summary, scope and exclusions, critical journeys, dependency and blast-radius map, target table, prioritized risk register, recovery and data-protection findings, observability gaps, recommendations with cost/resilience tradeoffs, phased roadmap, experiment or restore-test plan, evidence index, and unresolved questions. Never include credentials, full account-sensitive exports, private payloads, or unnecessary resource identifiers in the report.
