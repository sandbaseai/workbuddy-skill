---
name: "log-monitor"
display_name: "日志监控与模式检测"
display_name_en: "Log Monitoring and Pattern Detection"
description: "Analyze structured logs, detect errors, anomalies, and security patterns, correlate events, and produce actionable alerts and reports."
description_zh: "分析结构化日志，识别错误、异常和安全模式，关联事件并生成可执行的告警与报告。"
description_en: "Analyze structured logs, detect errors, anomalies, and security patterns, correlate events, and produce actionable alerts and reports."
category: "security"
version: "0.1.0"
author: "xray; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Log Monitoring and Pattern Detection

Use this skill when a task requires inspecting logs, finding repeated or unusual
events, correlating failures across services, or designing an alert and its
follow-up report. This skill analyzes evidence that is supplied or is available
through an authorized read-only integration; it must not imply that it has
real-time access when no log source was connected.

## Establish the evidence boundary

Before analyzing anything, record the source, service, environment, time zone,
time window, ingestion delay, sampling, redaction state, and query or filter
used. Separate observed entries from inferred patterns. If the sample is
truncated, deduplicated, or missing a source, state how that limits confidence.

Prefer structured records with timestamp, severity, service, operation, outcome,
request or trace correlation ID, and a safely bounded set of dimensions. Never
ask for or reproduce credentials, access tokens, session cookies, raw personal
data, or confidential payloads. Redact them before durable storage or reporting.

## Analyze logs safely

1. Establish a known-good comparison window and define the question to answer.
2. Normalize timestamps, severity names, service identifiers, and error classes.
3. Count exact and normalized messages without hiding the original evidence
   needed to verify a finding.
4. Detect spikes, novel signatures, repeated failures, latency or queue clues,
   and changes after deployments or configuration changes.
5. Correlate events by bounded identifiers and time windows. Treat correlation
   as a lead, not proof of causation, especially across clock-skewed systems.
6. Check affected users, regions, tenants, versions, and dependency boundaries
   without exposing their identifying data.

Regex or query patterns must be narrowly scoped, documented, and tested against
benign examples. Do not use an unbounded query, expensive scan, or automatic
remediation as a substitute for defining a safe scope. For an active incident,
preserve expiring evidence and follow the incident-response authority boundary;
do not restart services, purge logs, change traffic, or disable controls merely
because a pattern was found.

## Classify findings and alerts

For every finding, return:

- the pattern or anomaly and the evidence window;
- count, rate, baseline, confidence, and affected dimensions;
- likely user or system impact, including what remains unknown;
- competing explanations such as deploys, retries, traffic shifts, or logging
  changes;
- the next read-only check that would distinguish those explanations.

An alert is actionable only when it has a symptom, threshold or detection
method, evaluation window, severity, owner, routing destination, deduplication
key, and tested runbook. Prefer sustained rates or error-budget impact over a
single noisy event. Define missing-data behavior explicitly: silence and
healthy are not equivalent. Avoid high-cardinality labels and alert rules that
include raw IDs, URLs, stack traces, or payload values.

Before enabling an alert, test normal traffic, realistic failures, recovery,
missing data, deployment churn, and a burst. Record expected false-positive and
false-negative risks. Route security-sensitive patterns through the authorized
security process and avoid including exploit details or sensitive evidence in
notifications.

## Correlate and report

Use a bounded correlation table with event time, source, normalized pattern,
correlation key, related deployment or dependency, and confidence. Flag clock
skew, sampling gaps, inconsistent IDs, and retention gaps rather than filling
them with assumptions.

The report should contain:

```text
Scope and freshness:
Observed patterns and evidence:
Baseline and deviation:
Affected services / segments:
Security and privacy handling:
Hypotheses and confidence:
Recommended read-only checks:
Alert proposal / owner / runbook:
Open gaps and next review:
```

State which conclusions are implemented and tested, which are recommendations,
and which require an authorized integration or human decision. A report is not
complete until its reader can reproduce the query, understand its limitations,
and identify a safe next action.
