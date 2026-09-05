---
name: "agent-session-audit"
display_name: "Agent 会话审计"
display_name_en: "Agent Session Audit"
description: "Use when local Agent sessions need an operational audit of cost, tokens, tool failures, retry loops, latency, anomalies, health, diffs, or CI readiness."
description_zh: "用于审计本地 Agent 会话的成本、token、工具失败、重试循环、延迟、异常、健康度、差异和 CI 就绪度。"
description_en: "Discover local session data, report the highest-risk operational signals, preserve capability limits, and define reproducible privacy-safe health gates without inventing metrics."
category: "observability"
version: "0.1.0"
author: "davepoon/buildwithclaude; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with local session exports or an authorized parser/CLI; no network upload is required and aggregate data cannot prove event-level behavior"
---

# Agent Session Audit

## Scope and privacy

Use this Skill for an operational read of local Agent sessions: spend, token burn, cache use, tool failures, retry loops, latency, health, anomalies, diffs, and CI gate readiness. Session prompts, code, paths, and outputs may be private; keep analysis local and never upload raw logs to an external service. This audit measures observability signals, not the truth or quality of the Agent's conclusions.

## Discover before interpreting

Start with discovery unless the operator supplied a specific export or session directory. Identify the parser/CLI and its version, detected data roots, file format, time range, redaction status, and session capability:

- `Detailed`: event/step-level records support failure, retry, and latency analysis;
- `Aggregate`: summaries support totals and trends but not event-level causality;
- `Limited`: partial metadata supports only the stated fields.

If no session data is detected, run the parser's diagnostic command if available and report detected locations plus the next collection step. Do not treat “no data” as zero cost, zero failures, or healthy behavior.

## Audit workflow

1. Preserve the supplied path or discover local exports without changing them. Confirm scope and time window.
2. Run the approved local parser in a human-readable format for investigation and JSON/structured output for automation. Keep output paths user-owned; do not overwrite existing reports unless authorized.
3. Check parser health, schema/version compatibility, redaction, clock/timestamp quality, and capability level before using metrics.
4. Compute or read only metrics supported by available fields: session count, token/cost totals, cache ratio, tool failure rate, retry loops, latency distribution, gaps, anomalies, diff/CI status, and health score.
5. Lead with highest-risk sessions and concrete evidence. Name missing fields and sampling limitations beside every affected conclusion.
6. Compare periods only when definitions, data coverage, model/cost accounting, and capability level are compatible. Never compare missing event evidence as zero.

## Report contract

Use this structure:

```text
Scope: <paths, time window, revision, parser/version>
Capability: Detailed | Aggregate | Limited
Coverage: <sessions/events present; redaction and gaps>
Highest risks: <finding, evidence, impact>
Metrics: <value + field/source; unavailable fields explicitly listed>
Failures/retries: <observed counts and bounded examples>
Cost/tokens/latency: <observed values or unavailable>
Diff/CI readiness: <exact check and result>
Health gate: <threshold, observed value, pass/fail/partial>
Privacy: <local-only handling, redactions, retention>
Next action: <specific remediation or collection step>
```

When proposing a CI gate, include the exact local command/parser configuration and thresholds, for example a minimum health score, maximum critical findings, and maximum tool-failure rate. Calibrate thresholds to a baseline and mark the first rollout as observe-only when false positives are unknown.

## Evidence and anomaly rules

- Do not invent model, price, token, cost, latency, or failure values when a parser cannot infer them.
- Distinguish parser/tool failure from Agent-task failure; report both separately.
- Preserve long gaps, repeated retries, malformed records, clock skew, and incomplete exports as data-quality findings.
- Treat tool-step records as metadata unless the format proves they are a complete execution trace.
- Do not infer causality, user impact, or security severity from a health score alone.
- Redact secrets, tokens, credentials, personal data, and raw sensitive prompts from reports; retain safe hashes or counts only when necessary.

## WorkBuddy boundaries

The audit is read-only by default. Do not mutate session exports, run production commands, change CI thresholds, or send reports externally without explicit authority. An optional parser may be installed by the operator, but this Skill must still describe the unavailable capability honestly when the binary or schema is missing. Keep raw data outside the Skill package and repository commits.

## Handoff

Deliver the report path, parser/version, exact commands, capability level, coverage, observed metrics, unavailable fields, highest risks, gate result, privacy treatment, and recommended next action. A `partial` or `unavailable` audit is a valid operational result; it must never be formatted as a successful complete audit.
