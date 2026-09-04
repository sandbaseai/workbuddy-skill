---
name: "site-reliability"
display_name: "站点可靠性工程"
display_name_en: "Site Reliability Engineering"
description: "Use when defining SLOs and error budgets, reducing toil, planning capacity, improving on-call, running postmortems, or designing safe progressive delivery; connect reliability targets to user journeys and explicit evidence."
description_zh: "用于定义 SLO 和错误预算、减少 toil、规划容量、改进值班、开展复盘或设计安全渐进式发布，把可靠性目标连接到用户旅程和明确证据。"
description_en: "Apply SRE practices to user-centered SLIs, SLOs, error budgets, toil reduction, incident learning, on-call health, capacity, and progressive delivery with measurable guardrails."
category: "development"
version: "0.1.0"
author: "maddhruv; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Production telemetry, incident records, deployment controls, capacity data, and service ownership"
---

# Site Reliability Engineering

Use this skill to make reliability a measurable engineering practice rather than an aspiration. Start with user journeys and business impact, then define signals, targets, ownership, response, and learning. Reliability is a trade-off with cost, speed, features, security, and recovery—not a promise of 100% uptime.

Do not set arbitrary “number of nines” targets, page on symptoms without an SLO, freeze all delivery without an explicit budget policy, or run load/chaos experiments against production without authorization, abort thresholds, and recovery evidence.

## Define the reliability contract

For each important journey document:

- user action, criticality, dependency graph, eligible population, and exclusions;
- SLI formula, event source, sampling, aggregation, freshness, and data-quality checks;
- SLO target and rolling window, external SLA relationship, owner, review date, and error budget;
- alert thresholds, page/ticket policy, escalation, dashboard, runbook, and authorized response;
- cost, latency, correctness, durability, privacy, and availability trade-offs.

Choose SLIs that represent user outcomes, not only infrastructure health. Typical signals include availability, latency, freshness, correctness, durability, and successful completion. Make denominators explicit and handle retries, cancellations, client errors, maintenance, dependency failures, and partial outages consistently.

```text
error budget = 1 - SLO target
burn rate = observed bad-event rate / allowed bad-event rate
budget remaining = total budget - consumed budget
```

Validate formulas against historical data and representative incidents. Never tighten an SLO without a reliability investment and capacity plan.

## Operate the error budget

Publish budget state with the time window, confidence, data lag, and largest contributors. Define actions before depletion:

- healthy budget: normal delivery with routine review;
- declining budget: inspect recent changes, increase observation, and prioritize reliability work;
- threatened budget: pause non-essential risk, mitigate the largest burn, and require stronger rollout evidence;
- depleted budget: use the agreed feature/release policy, restore reliability, and record the decision and exception owner.

Prefer multi-window burn-rate alerts to a single threshold so fast incidents and slow degradation are both visible. Alerts must have an owner, actionable context, deduplication, escalation, and a tested path to silence or resolve them. Do not use an alert that cannot change a decision.

## Reduce toil deliberately

Classify work before automating it. Toil is manual, repetitive, automatable, reactive, without lasting value, and grows with service load. Measure hours and interruptions by category, then prioritize high-frequency, high-risk, reversible automation.

For each automation specify trigger, permissions, idempotency, timeout, retry limit, dry-run, audit event, rollback, and human escalation. Prove that it reduces toil without hiding failures or transferring risk to users. Retire the automation when the underlying source of toil is removed.

## Incidents and blameless learning

During an incident, establish an incident commander, communications lead, operations/subject experts, scope, severity, timeline, affected journeys, hypotheses, actions, and next update. Separate diagnosis from mitigation. Prefer reversible containment, preserve evidence, and state uncertainty explicitly.

After recovery, run a blameless review for severe, costly, prolonged, or recurring incidents. Ask:

1. What happened and when?
2. Why did it happen or become severe?
3. Why was detection late or ambiguous?
4. What slowed mitigation or communication?
5. What prevents recurrence or reduces blast radius?

Every action item needs an owner, due date, measurable completion, priority, dependency, and follow-up verification. “Improve monitoring” is not done until the signal, threshold, route, test, and resulting decision are evidenced. Do not use blame as a control; improve system conditions and learning.

## On-call health

Design rotations with sustainable coverage, escalation, handoff, backup, and time for follow-up work. Track pages per shift, acknowledgement, interruption hours, false positives, repeat incidents, and unresolved action items. Review alert quality and remove noise. No response plan should depend on one person, undocumented context, or unsafe sleep deprivation.

## Capacity and graceful degradation

Forecast demand, resource ceilings, dependencies, quotas, saturation, cost, and failure domains using observed drivers and uncertainty. Load-test in an isolated or explicitly approved environment with a ramp, abort criteria, observability, and cleanup. Verify autoscaling, queues, backpressure, timeouts, load shedding, admission control, caching, and recovery under overload.

Define degraded modes per journey: what remains available, what is stale or read-only, how users are informed, and how data is reconciled. Capacity headroom is not a substitute for correcting a leak, unbounded retry, hot key, or incorrect limit.

## Safe change and progressive delivery

Use small, observable changes with a clear owner, dependency checks, rollback/roll-forward plan, and success/abort criteria. For canary or blue/green release, define cohorts, exposure, duration, guardrail metrics, statistical comparison, and who may expand or stop. Include correctness, latency, availability, cost, security, and user-support signals.

After deployment, compare against a baseline and verify the intended user journey—not only process health. If the change causes unexplained burn, data divergence, saturation, or harmful behavior, stop expansion and mitigate. Keep rollback evidence current; an untested rollback is a hypothesis.

## Handoff

Report the service/journey scope, SLI/SLO formulas, budget state, alert/runbook links, incident timeline, capacity assumptions, toil measures, rollout cohort, evidence, unresolved risks, owners, and next authorized action. Stop when service ownership, measurement quality, user impact, or rollback authority is unclear.
