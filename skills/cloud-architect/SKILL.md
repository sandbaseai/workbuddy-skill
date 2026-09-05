---
name: "cloud-architect"
display_name: "云架构设计"
display_name_en: "Cloud Architect"
description: "Use when designing or reviewing AWS, Azure, GCP, or multi-cloud architecture, planning a migration, or defining disaster recovery. Produce evidence-backed options, trade-offs, and a staged change plan before implementation."
description_zh: "用于设计或评审 AWS、Azure、GCP 或多云架构、规划迁移，或定义灾难恢复方案；在实施前产出有证据的选项、取舍与分阶段变更计划。"
description_en: "Assess current state and requirements, map security, reliability, cost, performance, and compliance constraints, compare service choices, validate failure and migration paths, and hand off an implementable architecture with rollback and verification."
category: "development"
version: "0.1.0"
author: "Jeffallan/claude-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to architecture, deployment, billing, telemetry, and policy evidence, plus an approved path for infrastructure changes"
---

# Cloud Architect

## Mission and boundary

Design cloud systems that meet stated business and technical outcomes across availability, security, performance, cost, operations, sustainability, and portability. An architecture document is not authorization to provision resources, change routing, migrate data, or alter identity policies. Keep discovery and planning read-only until an owner approves an implementation plan.

## Inputs and required questions

Gather repository, deployment, traffic, dependency, data-classification, compliance, billing, and operational evidence. Ask for:

- user journeys, criticality tiers, regions, tenancy, data residency, and expected growth;
- availability target, SLOs, RTO/RPO, maintenance windows, latency, throughput, and recovery assumptions;
- identity, trust boundaries, encryption, secrets, network ingress/egress, audit, retention, and regulatory constraints;
- current provider resources, quotas, contracts, managed-service limits, ownership, and migration dependencies;
- team skills, delivery cadence, observability, incident capability, budget, and acceptable vendor lock-in.

Label assumptions, unknowns, and stale evidence. Do not fill missing requirements with a favorite provider or architecture pattern.

## Architecture workflow

1. **Discover current state.** Map users, services, data stores, queues, external systems, trust boundaries, regions, deployment paths, and operational ownership. Record actual dependencies and failure modes.
2. **Define decision criteria.** Turn requirements into weighted constraints and measurable fitness functions: availability, p95/p99 latency, recovery time, data durability, unit cost, security control coverage, operability, and portability.
3. **Compare options.** Present at least a recommended option and credible alternatives. Explain service selection, managed-vs-self-hosted trade-offs, coupling, quotas, failure domains, migration cost, and lock-in.
4. **Design the topology.** Show request/data flows, identities, network segmentation, encryption boundaries, backups, replicas, queues, caching, scaling, observability, and control-plane dependencies. Identify every single point of failure or explicitly accept it.
5. **Review the well-architected dimensions.** Check operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Tie each finding to an evidence source or mark it as a validation task.
6. **Plan delivery.** Use incremental migration waves with compatibility windows, dual-read/write risks, data validation, cutover criteria, rollback, decommissioning, and ownership. Validate connectivity and permissions before any irreversible cutover.
7. **Prove operability.** Define alerts, dashboards, runbooks, capacity triggers, degraded modes, chaos or recovery tests, and the evidence that will demonstrate RTO/RPO and SLO compliance.
8. **Handoff implementation.** Produce an implementation backlog, dependency order, infrastructure-as-code boundaries, change approvals, verification commands, residual risks, and a review date.

## Non-negotiable design checks

- Prefer least privilege, short-lived identity, encryption in transit/at rest, and separated administrative access.
- Use multiple failure domains for critical paths; do not call a topology highly available without testing failover and recovery.
- Design backup, restore, replication, and deletion behavior together. A backup that cannot be restored within the RTO is not a recovery plan.
- Model peak demand, quotas, retries, backpressure, connection pools, and provider throttling—not only average utilization.
- Allocate costs to owners and units; include egress, cross-zone traffic, logs, backups, idle resources, and migration costs.
- Keep public and private paths intentional. Document ingress, egress, proxy, DNS, service discovery, and policy behavior.
- Keep data movement reversible where possible and verify integrity, ordering, privacy, and access during each migration wave.
- Avoid needless multi-cloud symmetry. Use portability where it reduces material risk or meets a requirement, not as an unpriced slogan.

## Safe validation examples

Use provider-native read-only inspection or plan output during discovery. Never run apply, create, delete, cutover, or policy mutation commands as part of an architecture review.

```bash
# Examples: inspect current state and validate a planned target.
aws ec2 describe-vpcs --output json
aws elbv2 describe-target-health --target-group-arn "$TARGET_GROUP_ARN"
az network vnet peering list --resource-group "$RESOURCE_GROUP" --vnet-name "$VNET"
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
```

Redact account IDs, tokens, private addresses, customer data, and sensitive topology before sharing artifacts. Confirm that the selected environment and region match the decision record.

## Migration and disaster-recovery gates

Before cutover, verify schema/version compatibility, network and identity paths, quotas, observability, backup freshness, restore rehearsal, data validation, rollback ownership, and a tested abort window. After cutover, compare traffic, errors, latency, saturation, cost, and business outcomes against the baseline before decommissioning the old path.

For DR, record the failure scenario, recovery sequence, dependencies, actual RTO/RPO evidence, operator actions, customer communication, data-loss boundary, and the date of the next exercise. A diagram or successful deployment is not proof of recovery.

## Architecture decision record

```text
Decision: <short title and date>
Outcome: <business/technical outcome>
Constraints and evidence: <requirements, links, freshness>
Options considered: <recommended and alternatives>
Trade-offs: <security, reliability, performance, cost, operations, portability>
Failure domains and recovery: <SLO/RTO/RPO and proof plan>
Migration waves: <compatibility, validation, cutover, rollback>
Authorization and owners: <decision/change owner>
Assumptions and open risks: <explicit unknowns>
Review trigger: <event or date>
```

## Handoff checklist

- [ ] Current state, requirements, assumptions, owners, and evidence freshness are recorded.
- [ ] Options and trade-offs cover security, reliability, performance, cost, operations, and compliance.
- [ ] Topology includes trust boundaries, data flows, dependencies, failure domains, and observability.
- [ ] Capacity, quotas, retries, degraded modes, backup/restore, and recovery evidence are addressed.
- [ ] Migration waves include compatibility, data validation, cutover criteria, rollback, and decommissioning.
- [ ] Implementation actions are separated from architecture decisions and require the appropriate approval.
- [ ] Residual risks, validation tasks, owners, and review triggers are explicit.
