---
name: "finops"
display_name: "云成本运营"
display_name_en: "FinOps"
description: "Use when managing cloud cost and usage, allocation, forecasting, budgets, commitments, rightsizing, anomalies, unit economics, sustainability, or FinOps governance; maximize business value rather than optimizing spend in isolation."
description_zh: "用于管理云成本与用量、分摊、预测、预算、承诺折扣、资源调优、异常、单位经济学、可持续性和 FinOps 治理，在业务价值约束下持续优化云投资。"
description_en: "Apply the FinOps Framework to make cloud cost and usage visible, connect spend to business value, optimize rates and workloads, and operate accountable governance with measurable evidence."
category: "business"
version: "0.1.0"
author: "James Barney; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "AWS, Azure, or GCP billing/usage data; cost allocation metadata; warehouse or FinOps tooling"
---

# FinOps

Use this skill to make technology cost a timely, shared operating signal for engineering, finance, product, procurement, and leadership. FinOps is not cost cutting in isolation: optimize business value while making trade-offs among cost, reliability, performance, security, sustainability, and speed explicit.

Do not delete resources, purchase commitments, change production capacity, or alter chargeback without authorization and evidence. Never infer savings from list prices alone, hide shared costs, or publish a forecast without assumptions, freshness, and uncertainty.

## Start with context and principles

Record the cloud providers, accounts/subscriptions/projects, billing currency and period, workloads, owners, environments, business drivers, data latency, and current allocation coverage. Identify the decision, approver, affected teams, acceptable service impact, and review cadence.

Apply these principles:

1. Teams collaborate in near real time.
2. Business value drives technology decisions.
3. Everyone owns the usage they influence.
4. Data is accessible, timely, accurate, and appropriately scoped.
5. A central practice enables standards and rate expertise.
6. Variable cloud cost is used as a deliberate advantage.

Do not pursue maturity for its own sake. Invest in the next capability only when its expected business value exceeds its operational cost.

## Work through the iterative cycle

```text
INFORM -> OPTIMIZE -> OPERATE -> INFORM
```

### Inform: visibility and allocation

- Ingest billing and usage exports with explicit refresh time, currency, discounts, credits, and adjustments.
- Normalize provider dimensions and map accounts, tags, labels, services, environments, products, and cost centers.
- Reconcile totals to provider invoices; document shared, unallocated, tax, support, and marketplace treatment.
- Provide role-appropriate dashboards for engineers, finance, product, and leadership.
- Detect anomalies using a baseline and business context, not a single arbitrary threshold.

Prefer showback while allocation is maturing; use chargeback only when ownership rules, exceptions, disputes, and finance integration are ready. Track allocation coverage, unallocated spend, data freshness, forecast variance, anomaly time-to-detect, and time-to-explain.

### Optimize: rates, usage, and architecture

First remove waste and correct allocation. Then assess rightsizing, schedules, storage tiering, architecture, licensing, and rate commitments. For each recommendation show current usage, eligible scope, baseline, expected savings, implementation effort, service risk, reversibility, confidence, and owner.

For Reserved Instances, Savings Plans, or Committed Use Discounts:

- use a representative history, normally at least 90 days, and include planned growth and seasonality;
- calculate coverage, utilization, effective savings, flexibility, break-even, and downside if demand falls;
- commit only after workload optimization; start with stable, well-owned demand;
- define approval, purchase scope, expiry, transferability, and review cadence.

For Spot or preemptible capacity, prove interruption tolerance, retry behavior, checkpointing, and user impact before treating the discount as savings. Never count avoided future spend as realized savings without a consistent baseline.

### Operate: governance and learning

Define lightweight policies for tagging, budgets, forecast variance, commitment approvals, exception expiry, data access, and automated remediation. Use guardrails that report or quarantine safely before they mutate production. Review costs with the teams that can change them, and turn recurring anomalies into engineering or product work.

Use a Crawl/Walk/Run assessment across process, people, tools, metrics, and coverage:

- **Crawl:** basic provider data, ownership map, manual quick wins, visible exceptions;
- **Walk:** documented allocation, recurring forecasts, cross-functional reviews, controlled automation;
- **Run:** reliable near-real-time data, unit economics, automated guardrails, continuous optimization.

Choose a target state per capability. A workload may reasonably be Run for allocation and Crawl for commitments.

## Connect spend to value

Define unit economics such as cost per transaction, active workspace, successful job, customer, or revenue unit. State the denominator, quality threshold, time window, and source of truth. A lower cost per unit is not an improvement if latency, reliability, conversion, or customer value degraded.

Forecast using the simplest defensible method: trend-based for stable demand, driver-based when users/transactions explain cost, rolling forecasts for continuous planning, or probabilistic models for complex patterns. Include historical range, known launches, seasonality, rates, commitments, exchange rates, and confidence. Report variance against the prior forecast and explain the largest drivers.

## Investigate anomalies safely

1. Confirm the anomaly is real and not a billing delay, credit, currency, taxonomy, or duplicate-ingestion issue.
2. Compare service, account, region, environment, owner, usage quantity, unit rate, and business driver against baseline.
3. Check recent deploys, traffic, data volume, retries, autoscaling, commitment changes, and provider incidents.
4. Estimate current and projected impact, then rank reversible actions by value and risk.
5. Assign an owner, deadline, evidence required, and follow-up check; preserve the original baseline.

Do not automatically stop workloads, delete idle resources, or reduce capacity based only on an anomaly. Require health, dependency, retention, and recovery checks plus the authorized change boundary.

## Handoff and evidence

Report the period and data freshness, allocation method, baseline, assumptions, business metric, recommendation, expected value, confidence, service risk, owner, approval, implementation state, and verification result. Include both realized savings and cost avoidance labels. Stop when ownership, billing provenance, service impact, or authorization is ambiguous.
