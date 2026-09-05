---
name: "cloud-cost-optimization"
display_name: "云成本优化"
display_name_en: "Cloud Cost Optimization"
description: "Use when a cloud bill is unexplained, when reviewing architecture cost, or before changing capacity, storage, logging, transfer, or commitment plans. Start from measured cost drivers and utilization, not assumptions."
description_zh: "用于解释云账单增长、评审架构成本，或在调整容量、存储、日志、流量和承诺折扣前做成本分析；必须从实际成本驱动因素和利用率开始，而不是凭直觉。"
description_en: "Rank cost drivers, separate waste from necessary spend, validate performance and reliability trade-offs, model reversible savings, and establish attribution, budgets, and anomaly alerts before making authorized changes."
category: "business"
version: "0.1.0"
author: "nimadorostkar/Claude-Skills-collection; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to billing exports and utilization metrics, permission to inspect cloud metadata, and an approved change path for resource or commitment changes"
---

# Cloud Cost Optimization

## Purpose and boundaries

Reduce cloud spend without silently trading away reliability, security, performance, recovery, or developer productivity. Prices, discounts, quotas, and billing dimensions vary by provider, region, currency, date, and contract; cite the current billing source and label estimates.

Begin read-only. Never delete resources, scale capacity, change retention, move data, alter network topology, or purchase Reserved Instances/Savings Plans from this Skill alone. Those are authorized changes requiring an owner, impact review, rollback or recovery plan, and a measured verification window.

## Inputs

Collect the smallest useful evidence set:

- billing export or provider cost report for a stated UTC period, currency, tax treatment, and account/project scope;
- grouping by service, account, region, tag/label, usage type, and charge type;
- utilization and saturation for the largest spend items, including CPU, memory, storage, requests, network bytes, and log volume;
- workload growth, availability, latency, recovery, retention, compliance, and data-residency requirements;
- existing budgets, anomaly alerts, commitments, credits, and chargeback ownership.

If attribution is missing, report the gap and use a bounded allocation with confidence rather than presenting an inferred number as fact.

## Workflow

1. **Establish the baseline.** Record the comparison period, total and normalized cost, one-time charges, credits, exchange rate, and any deploy or traffic change. Compare like with like.
2. **Find actual drivers.** Rank service, account, region, tag, usage type, and unit-cost changes. Inspect opaque categories such as NAT/data processing, cross-zone transfer, egress, requests, and log ingestion rather than stopping at a service total.
3. **Separate waste from required spend.** Identify unattached storage, idle load balancers/IPs, expired snapshots, abandoned environments, duplicate logs, and overprovisioned capacity. Confirm ownership and retention obligations before proposing removal.
4. **Validate utilization and constraints.** Compare peak and percentile demand—not only average CPU—with memory, I/O, queue depth, latency, error rate, autoscaling behavior, and recovery headroom. A cheaper resource that violates an SLO is not a saving.
5. **Model options.** For each candidate, show current monthly cost, estimated new cost, one-time migration cost, confidence, performance/reliability impact, data-transfer effect, reversibility, and time to savings. Use current provider pricing rather than remembered figures.
6. **Sequence reversible changes first.** Apply approved schedules, retention tuning, sampling, rightsizing, architecture or placement changes, and storage tiers in small waves. Measure before/after and keep a rollback path.
7. **Evaluate commitments last.** Only model Savings Plans, Reserved Instances, committed-use discounts, or contracts after rightsizing and demand stability are proven. Include utilization risk, term, scope, exchange/flexibility, break-even, and an exit scenario.
8. **Close the control loop.** Assign cost ownership, required tags/labels, budgets, anomaly alerts, unit-cost metrics, and a review cadence. Document exceptions for shared or untaggable resources.

## Cost-driver checklist

Review these explicitly when relevant:

- compute: idle capacity, burst behavior, autoscaling limits, architecture/instance family, and non-production schedules;
- storage: unattached volumes, old snapshots, object tiering, request/replication charges, retention and restore cost;
- network: NAT processing, cross-zone/region traffic, egress, public endpoints, image pulls, and service-mesh chatter;
- observability: log ingestion, retention, high-cardinality metrics, traces, sampling, and duplicate pipelines;
- data and managed services: query scans, API requests, replicas, backups, queues, and minimum provisioned capacity;
- governance: allocation coverage, budget ownership, anomaly detection latency, and unit economics per customer/request/job.

## Safe analysis example

Run a bounded, read-only query against the provider’s current billing source. Keep the date range and account scope explicit, and do not paste credentials or raw customer identifiers into a report.

```bash
# Example shape; adapt to the provider and current account policy.
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-02-01 \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=USAGE_TYPE \
  --query 'ResultsByTime[].Groups[]' \
  --output json
```

Do not infer a saving from this report alone. Correlate the top line items with utilization, workload owners, and current pricing before proposing a change.

## Candidate record

```text
Candidate: <short name>
Scope and owner: <account/region/resource owner>
Evidence period: <UTC dates and source>
Current cost and unit: <amount / unit>
Driver: <measured cause and confidence>
Proposed change: <smallest authorized step>
Expected saving: <range, assumptions, and current-price date>
Trade-offs: <SLO, security, recovery, performance, migration, and data impact>
Rollback/recovery: <owner, trigger, and tested path>
Verification: <before/after metrics and observation window>
```

## Handoff checklist

- [ ] Billing scope, period, currency, credits, and data source are explicit.
- [ ] Top drivers are ranked by measured cost and unit economics.
- [ ] Utilization, peak demand, SLOs, recovery, security, and retention constraints are checked.
- [ ] Estimates separate recurring savings, one-time cost, assumptions, and confidence.
- [ ] Destructive, capacity, data, and commitment actions have explicit authorization.
- [ ] Approved changes are reversible or have a documented recovery path and before/after evidence.
- [ ] Owners, budgets, anomaly alerts, allocation gaps, and follow-ups are assigned.
