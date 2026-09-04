---
name: "product-analytics"
display_name: "产品分析"
display_name_en: "Product Analytics"
description: "Use when defining product metrics, event taxonomies, funnels, cohorts, retention, experiments, or dashboards; connect measurable user value to decisions without compromising privacy or statistical validity."
description_zh: "用于定义产品指标、事件模型、漏斗、分群、留存、实验和仪表板，把可衡量的用户价值连接到决策，同时保护隐私并维护统计有效性。"
description_en: "Define product metrics, event taxonomies, funnels, cohorts, retention, experiments, and dashboards with privacy-aware instrumentation and statistically defensible decisions."
category: "data"
version: "0.1.0"
author: "majiayu000; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Product analytics platform or warehouse; event SDK; SQL; experimentation tooling"
---

# Product Analytics

Use this skill to decide what to measure, instrument product behavior, investigate conversion or retention, and communicate evidence-backed actions. Start with the decision the measurement must support—not with a dashboard or a vendor feature.

Do not equate activity with value. Do not track everything by default, expose raw identity data, infer causality from correlation, or recommend a rollout from an underpowered experiment. Confirm consent, retention, access, regional requirements, and the actual event pipeline before collecting data.

## Define the measurement contract

Before adding an event or metric, document:

- the product question, decision owner, expected action, and review cadence;
- the North Star or outcome metric, its numerator/denominator, grain, time window, and known failure modes;
- input metrics for acquisition, activation, engagement, retention, revenue, and referral, with guardrails for quality and harm;
- event name, trigger, actor/entity, properties, timestamp semantics, deduplication key, version, and source of truth;
- privacy classification, consent purpose, retention period, deletion path, access roles, and whether a less identifying signal is sufficient.

Prefer a small taxonomy with stable names and versioned schemas. Do not put email addresses, tokens, free-form user text, payment data, or secrets in event properties. Use opaque identifiers where necessary, document joins, and redact or aggregate exports.

## Instrument trustworthy events

An event should describe a meaningful product action, not an implementation detail. Define the trigger precisely: attempted versus completed, client versus server authority, timezone, retries, offline replay, and whether duplicate delivery is possible.

Use a schema such as:

```yaml
name: onboarding_completed
version: 1
actor_id: opaque_user_id
occurred_at: UTC timestamp from the authoritative service
properties:
  plan: controlled enum
  workspace_size_bucket: bounded integer bucket
deduplication_key: stable event id
privacy: purpose-limited, 90-day retention
owner: product analytics
```

Validate required fields, allowed values, timestamp ranges, cardinality, volume, and schema compatibility in CI or at ingestion. Monitor missing events, duplicate rates, late arrivals, unknown versions, and sudden distribution shifts. Treat a tracking change as a data contract migration: support old and new versions during rollout, backfill only with explicit provenance, and deprecate consumers deliberately.

## Analyze funnels and cohorts

Define funnel steps, identity rules, conversion window, entry population, and exclusion criteria before reading the result. Report counts and rates at every step, not only the final percentage. Segment by relevant, predeclared dimensions such as platform, plan, region, or acquisition channel; avoid slicing until a favorable result appears.

For cohorts, state the cohort entry event and date, active definition, observation window, censoring, and treatment of reactivation. Compare like with like. Retention curves should show cohort sizes and uncertainty; a flattening curve can be useful evidence, but no universal “good” threshold applies across products.

Check data quality before interpreting a change:

- event volume and delivery latency versus baseline;
- unique actors, duplicate rate, null/unknown property rate, and identity stitching;
- denominator drift, bot/test traffic, seasonality, release exposure, and timezone boundaries;
- aggregate reconciliation with billing, orders, support, or other authoritative systems.

## Design and evaluate experiments

Write the hypothesis, eligible population, randomization unit, treatment exposure, primary metric, guardrails, minimum detectable effect, power target, duration, and stopping rule before launch. Ensure assignment is stable and treatment actually reaches the intended unit.

Do not peek and stop at the first favorable p-value. Check sample-ratio mismatch, contamination, novelty, multiple comparisons, missing outcomes, and practical effect size. Report estimate, uncertainty interval, sample size, exposure, analysis window, and limitations. If randomization or power is inadequate, call the result directional and seek corroborating evidence rather than claiming causality.

Roll out gradually when risk warrants it. Monitor guardrails such as errors, latency, cancellations, accessibility, support contacts, and revenue—not only the target metric. Predefine rollback authority and a stop condition for harm or data-quality failure.

## Build useful dashboards and handoffs

Keep executive views small: outcome metric, trend, target, segment context, and clearly labeled freshness. Product views should connect activation, feature adoption, funnels, retention, and guardrails. Every chart needs an owner, definition, source, last-updated time, and a link to the underlying query or catalog.

When reporting an insight, include the question, population, time window, metric definitions, data-quality checks, result with uncertainty, plausible alternatives, recommendation, owner, and next measurement. Separate observed facts, interpretations, and decisions. Preserve the query/version used so another analyst can reproduce it.

## Safety checklist

- Obtain the required consent and document purpose limitation before instrumentation.
- Minimize identity and property collection; never log credentials or raw sensitive text.
- Restrict dashboards and exports by role; audit access and honor deletion requests.
- Do not target vulnerable users or optimize a proxy that predictably harms them.
- Stop analysis when tracking breaks, denominators shift unexpectedly, privacy boundaries are unclear, or an experiment violates its predeclared rules.
