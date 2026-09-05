---
name: "agent-observability"
display_name: "Agent 可观测性"
display_name_en: "Agent Observability"
description: "Use when instrumenting or debugging an AI agent and you need privacy-aware traces, structured events, metrics, cost attribution, dashboards, alerts, or audit evidence."
description_zh: "用于为 AI Agent 建立或排查隐私安全的链路、结构化事件、指标、成本归因、看板、告警和审计证据。"
description_en: "Design privacy-aware observability from request entry through model, retrieval, tool, handoff, approval, and response spans, with explicit limits and verification."
category: "development"
version: "0.1.0"
author: "seb1n/awesome-ai-agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized telemetry, tracing, and metrics systems"
---

# Agent Observability

Make agent behavior explainable from request entry through model, retrieval,
tool, handoff, approval, retry, and final-response spans. This Skill designs
the evidence contract; it does not enable production capture, export data, or
widen telemetry access without authorization.

## Define the boundary and questions

Record the workflow graph, runtime boundaries, incident questions, traffic and
failure expectations, telemetry stack, data classification, retention policy,
sampling limits, owners, and what cannot be observed. Start with decisions such
as “Which tool causes timeouts?” or “Why did cost per completed task rise?” Do
not collect fields without a documented use.

## Trace and event contract

Produce one trace per user-visible attempt. Define spans for model calls,
retrieval, tools, handoffs, approvals, retries, and final validation. Preserve
parent-child relationships and propagate a correlation ID across queues. For
each field specify its meaning, unit, owner, cardinality, retention, and
redaction rule. Useful stable metadata includes versions, status, duration,
token and cost measures, retry counts, tool names, policy outcomes, and
evaluation tags.

Separate content from metadata. Default to content-free telemetry. Prompt,
response, or tool-payload capture requires explicit authorization, reliable
redaction, least-privilege access, a retention limit, and an audit trail. Never
record secrets, tokens, raw credentials, payment data, or unapproved personal
data; do not place suspected values in reports.

## Metrics, dashboards, and alerts

Define a small set of indicators with units, denominators, exclusions, windows,
and owners: task success, critical-policy violations, end-to-end latency, tool
failure rate, escalation rate, and cost per completed task. Build dashboards
from user outcome to dependency detail. Alert only on actionable sustained
impact, attach an owner and runbook, and avoid high-cardinality dimensions.

Control sampling, cardinality, and storage cost. Retain critical failures when
authorized; sample normal traffic without losing rare error classes. Do not
let instrumentation failures block the user path unless a mandated audit
control explicitly requires fail-closed behavior.

## Verification workflow

1. Send a synthetic request end to end and verify one trace ID, exactly one
   root, and one acyclic connected parent graph.
2. Exercise a tool error, timeout, retry, refusal, approval, and handoff path;
   check status and parentage for each.
3. Search emitted telemetry for seeded secret and personal-data canaries using
   field names and reason classes; do not print matched values.
4. Recalculate dashboard metrics from a bounded sample and confirm units,
   denominators, and time windows.
5. Verify each alert names an owner, carries diagnostic context, and has a
   bounded runbook. Record missing telemetry as an evidence limitation.

## Failure handling and handoff

- If propagation breaks, preserve local correlation fields and mark cross-
  service conclusions incomplete.
- If clocks disagree, prefer monotonic in-process durations and avoid false
  cross-host ordering.
- If volume exceeds budget, reduce verbose attributes and normal-traffic
  sampling before dropping critical errors.
- If sensitive content appears, stop or restrict capture through the authorized
  control, follow the incident policy, and involve the retention owner before
  any purge.

Return the observability objective, boundary, trace/event schema, redaction
rules, indicator definitions, dashboard and alert specifications, sampling and
retention plan, verification results, known blind spots, and accountable next
owner. Treat traces as partial evidence: absent telemetry does not prove that
an action did not occur.
