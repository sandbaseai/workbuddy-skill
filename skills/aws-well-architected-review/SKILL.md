---
name: "aws-well-architected-review"
display_name: "AWS Well-Architected 审查"
display_name_en: "AWS Well-Architected Review"
description: "Use when reviewing an AWS workload against the six Well-Architected pillars using IaC and authorized live evidence, classifying risks, documenting trade-offs, and preparing a remediation backlog."
description_zh: "用于基于 IaC 和经授权的线上证据，按 AWS Well-Architected 六大支柱审查工作负载、分级风险、记录取舍并准备修复待办。"
description_en: "Discover the workload, map services and trust boundaries, review operational excellence, security, reliability, performance, cost, and sustainability, and produce evidence-linked findings without applying changes by default."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with repository/IaC access and optionally authorized read-only AWS evidence; current AWS framework references, account permissions, and any issue creation or remediation require separate authorization"
---

# AWS Well-Architected Review

## Purpose and boundary

Perform a structured review of an AWS workload against the six Well-Architected pillars:
operational excellence, security, reliability, performance efficiency, cost optimization, and
sustainability. Combine repository/IaC evidence with authorized read-only live evidence; do not
pretend that a static template proves deployed state.

The default deliverable is a report and remediation backlog in an authorized documentation path.
Do not create GitHub Issues, change IaC, call mutating AWS APIs, alter budgets/alarms, or deploy
fixes unless the user separately authorizes that exact side effect. Never include credentials,
secret values, customer data, or unrestricted policy documents in findings.

## Review contract

Define before inspection:

- workload, account, regions, environments, revision, and review date;
- IaC sources and live resource scope, including systems deliberately excluded;
- relevant AWS Framework version, lenses, regulatory or business constraints;
- evidence permissions, sensitive-data handling, and intended audience;
- risk scale, owner, remediation deadline, and whether backlog publication is authorized.

Label every statement as **observed**, **derived**, **inferred**, or **unknown**. A missing live
permission or absent IaC file is a coverage gap, not evidence that the control is absent.

## Step 1: load current references and discover the workload

Use the current AWS Well-Architected Framework and relevant lenses, recording URL, retrieval date,
and version or revision when available. Read repository instructions and locate:

- Terraform/OpenTofu `*.tf`, CloudFormation/SAM templates, CDK `lib/`, `bin/`, and `cdk.json`;
- modules, parameter files, environment overlays, deployment workflows, ownership, and runbooks;
- compute, data, networking, identity, security, observability, messaging, backup, and edge services;
- public endpoints, trust boundaries, cross-account/region links, data classifications, and dependencies.

Build a service inventory and a Mermaid architecture diagram from actual references. Mark inferred
links and services separately from confirmed deployment state. If no IaC is present, use only
authorized live read-only discovery and prominently report the reproducibility gap.

## Step 2: establish evidence safely

Confirm account, principal class, region, environment, and timestamp before live queries. Prefer
read-only `describe-*`, `list-*`, and `get-*` calls with narrow filters; use the AWS Resource Query
workflow for bounded inventory. Capture command family, scope, permission gaps, pagination status,
and result fingerprints rather than sensitive payloads. Do not retrieve Secrets Manager values or
run any `create`, `put`, `update`, `modify`, `delete`, `invoke`, `send`, or deployment command.

Reconcile IaC intent with live observations by immutable IDs, tags, and revision. Flag drift,
unmanaged resources, stale templates, missing regions, or ambiguous ownership. Distinguish a
control not found in the inspected source from a control proven absent in the deployed account.

## Step 3: review all six pillars

Use the following prompts as evidence questions, not automatic pass/fail claims.

### Operational excellence

- Are ownership, runbooks, deployment and rollback paths, change records, and recovery exercises defined?
- Are infrastructure changes reproducible through IaC and protected CI/CD with required approvals?
- Are CloudTrail, CloudWatch alarms, dashboards, logs, and actionable alert routing present?
- Are tags, service catalogs, operational metrics, and post-change learning maintained?

### Security

- Are IAM roles and resource policies least-privilege, scoped by resource and condition, and reviewed?
- Are secrets in managed stores with rotation and no hardcoded values in IaC, logs, or artifacts?
- Are public exposure, network paths, security groups, TLS, encryption, KMS key policy, and tenant boundaries explicit?
- Are CloudTrail, GuardDuty, Security Hub, AWS WAF, vulnerability management, and incident paths appropriate?

### Reliability

- Are failure domains, quotas, dependencies, retries, timeouts, idempotency, and degradation behavior explicit?
- Are backups, retention, point-in-time recovery, versioning, restore tests, and multi-AZ/region choices evidenced?
- Are health checks, dead-letter handling, autoscaling, deployment rollback, and data recovery verified?
- Are single points of failure and unbounded blast radius recorded as findings?

### Performance efficiency

- Are workload patterns, latency/error objectives, capacity signals, and scaling policies measured?
- Are compute, storage, database, network, caching, and data-transfer choices sized to the workload?
- Are managed/serverless, Graviton, CDN, caching, and asynchronous designs evaluated with evidence rather than slogans?
- Are performance tests representative, repeatable, and protected from production impact?

### Cost optimization

- Are cost allocation tags, budgets, anomaly alerts, ownership, and regular review in place?
- Are idle/unattached resources, data lifecycle, storage tiers, NAT/data transfer, commitments, and utilization measured?
- Are savings options compared against reliability, performance, lock-in, and operational cost?
- Are price assumptions, currency, period, and estimates clearly timestamped?

### Sustainability

- Is resource utilization measured and over-provisioning reduced without compromising objectives?
- Are efficient architectures, lifecycle policies, autoscaling, managed services, and suitable regions considered?
- Are environmental trade-offs documented as workload-specific evidence, not assumed from a service label?

For every pillar, record controls checked, supporting files/resources, evidence freshness, result,
confidence, and unanswered questions. Avoid declaring compliance from a checklist alone.

## Step 4: classify and prioritize findings

Each finding needs a stable ID, pillar, affected resource or module, observation, expected practice,
impact, evidence links, confidence, owner, and remediation verification. Use:

| Risk | Use when |
|---|---|
| High | credible security exposure, unrecoverable data risk, critical single point of failure, or severe unbounded blast radius |
| Medium | material reliability, performance, cost, or operational weakness with mitigations available |
| Low | best-practice deviation or optimization with limited immediate impact |
| Unknown | evidence or permission gap prevents a defensible risk decision |

Prioritize by user impact, exploitability/failure likelihood, blast radius, reversibility, evidence
confidence, and remediation effort. Do not inflate severity to compensate for missing evidence.
Preserve counterevidence and accepted trade-offs; an intentional exception with an owner, expiry,
and compensating control is not the same as an overlooked gap.

## Step 5: remediation and validation

Recommend IaC-first fixes with exact module/resource locations, a safe sequence, permissions,
cost and operational effects, rollback, and a proof plan. Prefer a dry-run, plan, what-if, or
read-only validation before any deployment. For each fix define:

- precondition and approval owner;
- expected state and measurable acceptance signal;
- data/traffic backup or migration protection;
- blast-radius limit and abort path;
- post-change observation window and rollback evidence;
- residual risk and next review trigger.

Only after separate authorization may the report be converted into GitHub Issues or implementation
changes. If publication fails, retain the complete safe Markdown backlog locally and state that
no external issue was created.

## Review report

```text
Review: <workload, account/region scope, immutable revision, date>
References: <Framework/lenses and retrieval dates>
Coverage: <IaC/live sources, permissions, exclusions, freshness>
Architecture: <diagram path and observed/inferred boundaries>
Summary: <pillar counts, high/medium/low/unknown, confidence>
Findings: <ID, pillar, resource, observation, evidence, impact, risk, owner>
Trade-offs/exceptions: <decision, compensating control, expiry>
Remediation backlog: <ordered action, IaC location, acceptance signal, rollback>
Validation: <checks run, results, unavailable checks>
Publication: <report path; issue creation authorized/not authorized/not attempted>
Residual risk and next review: <unknowns, trigger, owner/date>
```

The review is complete only when all six pillars have evidence or explicit coverage gaps, findings
are traceable and calibrated, and remediation/validation boundaries are clear. State that the
review is partial when live infrastructure, current references, or required permissions were not
available.
