---
name: "monitoring-observability"
display_name: "监控与可观测性设计"
display_name_en: "Monitoring and Observability Design"
description: "Use when defining service objectives, instrumenting metrics, logs, or traces, designing dashboards and alerts, or auditing whether telemetry supports reliable diagnosis; ground every signal in a user journey and an operational response."
description_zh: "以用户旅程和服务目标为起点，设计可执行的指标、日志、追踪、仪表盘与告警，并验证遥测质量和响应闭环。"
description_en: "Design actionable metrics, logs, traces, dashboards, and alerts from user journeys and service objectives, then verify telemetry quality and the response loop."
category: "development"
version: "0.1.0"
author: "candeploys; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Monitoring and Observability Design

Use this skill to make a system's behavior explainable and operationally actionable. Start from the decision or failure that must be detected, not from a preferred vendor or a wish to collect everything.

## Establish the observation contract

Identify the real service boundary, owners, deployment environment, critical user journeys, dependencies, and current telemetry. Separate facts found in code, infrastructure, dashboards, and incident records from assumptions. Confirm data sensitivity, retention rules, expected traffic shape, and which tools are actually available before proposing instrumentation.

For each critical journey, define:

- the user-visible outcome and an unambiguous success event;
- a service-level indicator with numerator, denominator, filters, and aggregation window;
- the service-level objective and its business rationale;
- exclusions such as synthetic traffic, cancellations, or client errors, with justification;
- the owner and action when the objective or error budget is threatened.

Do not present a target as an SLO unless its measurement, population, and window are explicit. Distinguish product KPIs, resource utilization, internal health indicators, SLIs, SLOs, and contractual SLAs.

## Design useful telemetry

Cover the signals needed to distinguish demand, failure, latency, and resource pressure without assuming every system needs identical instrumentation.

- Metrics: choose stable names and units, document labels, and bound cardinality. Never use raw user IDs, request IDs, URLs, stack traces, or unbounded payload values as metric labels.
- Logs: prefer structured events with timestamp, severity, service, environment, operation, outcome, and correlation identifiers. Redact credentials, tokens, personal data, and confidential payloads at the source.
- Traces: propagate context across supported boundaries, sample deliberately, record errors consistently, and avoid sensitive attributes. State where asynchronous or third-party boundaries break continuity.
- Events and profiles: use them only when they answer a defined operational question and their cost, privacy, and runtime overhead are acceptable.

Specify semantic conventions and ownership centrally enough to correlate signals across services. Preserve raw evidence where appropriate, but do not claim correlation when clocks, identifiers, sampling, or retention windows make it unreliable.

## Build dashboards for decisions

Give each dashboard an audience and question. Put user impact and objective status first, then traffic, errors, latency distributions, saturation, deployments, and dependency health. Show units, time range, freshness, missing-data behavior, and relevant baselines. Prefer percentiles or distributions over averages when tails matter.

Make drill-down paths explicit: overview to service, operation, dependency, trace, and sanitized logs. A visually green dashboard does not prove health if telemetry is absent; display no-data and stale-data states distinctly.

## Create actionable alerts

Every page-worthy alert needs a symptom tied to user or SLO impact, an owner, severity, evaluation window, routing destination, deduplication/grouping behavior, and a tested runbook. Prefer multi-window burn-rate or equivalent sustained-impact alerts over brittle single thresholds when an SLO exists. Use ticket or dashboard signals for conditions that do not require immediate human action.

Before enabling a page, test normal behavior, realistic failure behavior, missing data, deployment changes, seasonality, and recovery. Record expected false-positive and false-negative risks. The runbook must identify safe first checks, authority boundaries, escalation, and verification of recovery; it must not encourage destructive production changes without explicit authorization.

## Validate the system

Test the complete path from emitted signal to storage, query, dashboard, alert evaluation, notification, acknowledgement, and useful diagnosis. Verify timestamps, units, label dimensions, sampling, redaction, access control, retention, cost, and telemetry pipeline health. Inject a bounded synthetic event or use a controlled environment when production fault injection is not explicitly authorized.

After deployment or an incident, compare detection time, acknowledgement time, diagnostic usefulness, alert volume, missed symptoms, and cost against the intended contract. Remove or revise signals that have no owner or decision value.

## Handoff

Return the observed architecture, assumptions, proposed SLIs/SLOs, telemetry schema, dashboard and alert rationale, privacy/cardinality/cost controls, validation evidence, uncovered blind spots, owners, and next review trigger. Clearly distinguish implemented and tested behavior from recommendations that still require access or approval.
