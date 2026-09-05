---
name: "aws-cloudwatch-investigation"
display_name: "CloudWatch 证据调查"
display_name_en: "AWS CloudWatch Investigation"
description: "Use when investigating AWS incidents with CloudWatch Logs, Metrics, Alarms, CloudTrail, and Health evidence, correlating deployments, narrowing blast radius, reconstructing timelines, or testing metric anomalies."
description_zh: "用于使用 CloudWatch 日志、指标、告警、CloudTrail 和 Health 证据调查 AWS 事件，关联部署、缩小影响范围、重建时间线或验证指标异常。"
description_en: "Build bounded Logs Insights and metric queries, correlate alarms with changes, narrow account-to-resource scope, and report evidence, uncertainty, and next safe checks without mutating AWS."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized read-only AWS/CloudWatch/CloudTrail access, known account and region scope, and redaction-safe evidence storage; dashboards, alarms, deployments, and remediation require separate authorization"
---

# AWS CloudWatch Investigation

Investigate AWS incidents from bounded, auditable evidence. This skill helps turn a symptom into a time-bounded evidence set across CloudWatch Logs, Metrics, Alarms, CloudTrail, and AWS Health, then records what is known, uncertain, and safe to check next.

## Purpose and boundary

- Confirm account, region, environment, service, and time zone before querying.
- Use read-only access only: query logs and metrics, inspect alarms and history, read CloudTrail and Health events, and inspect deployment metadata.
- Never change dashboards, alarms, log retention, metric filters, resources, deployments, or incident state through this skill.
- Treat temporal correlation as a lead, not proof of causality; seek independent evidence and counterevidence.

## Investigation contract

Before running a query, record:

1. The reported symptom, impact hypothesis, and first-known-good/first-known-bad times.
2. Account ID, region, environment, service/resource identifiers, and the source of each identifier.
3. Query purpose, time range, log groups or namespaces, filters, limit, and expected result shape.
4. Redaction requirements and evidence retention destination.

If scope or timestamps are missing, ask for them or state the narrow assumption. Do not silently query every account or region.

## First signal and alarm correlation

Start with the earliest reliable signal, then compare it with alarm state transitions, deployment/change records, CloudTrail events, and AWS Health events. Preserve event timestamps with their source time zone and ingestion delay where available.

For Logs Insights, use a bounded shape and adapt fields to the log schema:

```sql
fields @timestamp, @message, @logStream
| filter @timestamp >= datefloor(now() - 30m, 1m)
| filter level in ["ERROR", "FATAL"] or ispresent(error)
| stats count() as errors, min(@timestamp) as first_seen, max(@timestamp) as last_seen by @logStream
| sort errors desc
| limit 100
```

For a suspected request or trace, filter by an exact redacted identifier when possible, then inspect a small surrounding window. Avoid unbounded wildcard searches and avoid copying full customer payloads.

## Narrow blast radius

Use a decision tree:

- One resource or stream: compare its peers, recent changes, and local saturation signals.
- One service across many resources: compare AZ, task, pod, or instance dimensions and look for a shared dependency.
- Multiple services in one region: check shared networking, identity, quota, endpoint, and regional Health evidence.
- Multiple regions or accounts: verify the common release, dependency, policy, or provider event before claiming a platform-wide incident.

For every narrowing step, record the population sampled, dimensions compared, missing dimensions, and why the evidence increases or decreases confidence.

## Metric evidence

Prefer the smallest metric query that can falsify the current hypothesis. State namespace, metric, statistic, period, dimensions, account, region, and alignment. Validate formulas and units before interpreting metric math; do not compare counts, rates, and percentages as if they were interchangeable.

Compare the incident window with a declared baseline (for example, the same service and dimensions over the prior seven comparable windows). Report missing data, delayed data, aggregation effects, and whether the anomaly is absolute, relative, or only visible after normalization.

## Timeline and handoff

Build a table with `time`, `source`, `event`, `scope`, `evidence reference`, `confidence`, and `counterevidence`. Separate observed facts from hypotheses. Include query IDs or immutable references where available, plus a completeness label: `complete`, `partial`, or `unknown`.

The handoff must contain:

- impact and currently affected scope;
- earliest and latest observed signals;
- correlated changes and why they are or are not causal;
- key queries, baselines, gaps, and counterevidence;
- the next safe read-only checks;
- explicit remediation/rollback actions requiring separate authorization.

Redact secrets, tokens, authorization headers, session identifiers, customer content, and unnecessary personal data before sharing. Keep raw evidence access-controlled and provide summaries to broader audiences.

## Quality gates

- [ ] Account, region, service, time range, and time zone are explicit.
- [ ] Queries are bounded, read-only, schema-aware, and reproducible.
- [ ] Baselines, metric units, missing data, and aggregation are checked.
- [ ] Alarm, deployment, CloudTrail, and Health timestamps are compared without overstating causality.
- [ ] Blast-radius claims identify the sampled population and gaps.
- [ ] Evidence is redacted, access-controlled, and labeled for completeness.
- [ ] No mutation or customer-impacting action was performed.
