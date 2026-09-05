---
name: "incident-postmortem"
display_name: "无责事件复盘"
display_name_en: "Incident Post-Mortem"
description: "Use after a production outage, significant degradation, data incident, or near miss to reconstruct evidence, quantify impact, identify systemic causes without blame, and create owned, dated prevention actions."
description_zh: "用于生产中断、重大降级、数据事件或险些发生的事件之后，重建证据、量化影响、无责识别系统性原因，并生成有负责人和日期的预防行动。"
description_en: "Build a time-bounded, evidence-linked blameless review that separates root causes from contributing factors, preserves uncertainty, and turns learning into verifiable follow-up work."
category: "productivity"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized incident evidence and a documentation output path; private logs, customer data, issue creation, and corrective changes require appropriate access and authorization"
---

# Incident Post-Mortem

## Purpose and boundary

Create a blameless, evidence-backed review after a production outage, material degradation, data
incident, or meaningful near miss. The goal is to understand how system and process conditions
allowed the event, improve detection and recovery, and assign concrete prevention work—not to
identify a person to blame.

Use language such as “the system did not detect” or “the process lacked a guardrail.” Do not
publish private logs, credentials, customer content, personal data, or unsupported speculation.
Default to an authorized document draft; do not page people, create tickets, change production,
or send communications unless separately authorized.

## Review contract and evidence

Capture before writing:

- incident title, severity convention, detection and resolution times with timezone;
- incident commander or accountable reviewer and affected services/environments;
- user, traffic, data, revenue, and SLA/SLO impact, with baseline and confidence;
- source revision, deploy/config changes, alerts, logs, traces, tickets, chat, and status updates;
- audience, redaction policy, retention, publication path, and unresolved evidence gaps.

Prefer immutable links, event IDs, timestamps, query descriptions, and redacted excerpts. Preserve
the distinction between observed fact, derived measurement, hypothesis, and unknown. When evidence
conflicts, record both sources and explain the resolution or leave it unresolved.

## Step 1: reconstruct the timeline

Use UTC unless the incident system requires another timezone. Build the chain from first symptom
through confirmed recovery:

1. first symptom or triggering change;
2. alert fired or issue noticed;
3. on-call paged and incident declared;
4. investigation hypotheses and key evidence;
5. mitigation or rollback applied;
6. root cause or contributing mechanism isolated;
7. full recovery and user-impact verification;
8. customer/stakeholder communication and handoff.

For each event record exact time, system observation or action, actor role (not blame), source,
confidence, and known gaps. Separate symptom start from detection-to-resolution duration. Do not
fill timeline gaps from memory when logs, alerts, deploy records, or incident notes can be checked.

## Step 2: quantify impact

Compare affected values with a stated normal baseline and measurement window:

- duration: symptom start, detection, mitigation, and confirmed recovery;
- affected services, regions, tenants, endpoints, traffic percentage, and user count;
- peak and sustained error rate, latency, availability, queue depth, or capacity;
- data loss/corruption/exposure scope and recovery status;
- revenue, workflow, SLA/SLO, regulatory, or contractual impact;
- confidence, sampling limits, and calculations for every estimate.

If impact is not measurable, say why and provide the next safe query or owner. Never turn a rough
number into a precise claim merely to complete the table.

## Step 3: identify causes without blame

Use a causal chain or 5 Whys, stopping at one or two systemic gaps that can be changed. Distinguish:

- **root cause:** a fundamental design, process, dependency, or control gap;
- **contributing factor:** a condition that increased likelihood, severity, or duration;
- **trigger:** the immediate event that exposed the weakness;
- **detection/recovery gap:** why the issue was not found or restored sooner;
- **counterevidence:** facts that weaken a proposed explanation.

“Human error,” “bad deployment,” or a person’s action is not a sufficient root cause. Ask which
interface, default, test, review, alert, runbook, access boundary, or recovery mechanism allowed
that action to cause impact. Validate proposed causes against independent evidence such as code,
configuration history, metrics, traces, alerts, and reproduction results.

## Step 4: capture learning and action items

Record what worked and what could improve without assigning blame. Every action must be a specific
deliverable with one accountable individual, a due date, priority, acceptance evidence, and review
trigger. Examples include a named regression fixture, alert threshold and owner, runbook section,
rollback guard, capacity limit, or access-control test. “Improve monitoring” or “be more careful”
is not actionable.

Prioritize by recurrence likelihood, impact, detection/recovery value, blast radius, and effort.
Separate immediate containment from durable prevention. Link actions to the evidence and preserve
an owner handoff if ticket creation is not authorized.

## Report template

Write only to an authorized path, commonly `docs/postmortems/YYYY-MM-DD-<slug>.md`:

```markdown
# Post-Mortem: <incident title>

**Date:** <UTC date>  
**Severity:** <P1–P4 or repository convention>  
**Duration:** <symptom start – confirmed recovery>  
**Incident Commander:** <role/name as permitted>  
**Status:** Resolved | Partially resolved | Open evidence

## Summary
<What happened, user impact, mitigation, and current state in 2–3 sentences.>

## Impact
| Dimension | Value | Evidence/confidence |
|---|---|---|
| Affected services/regions | | |
| Users/traffic affected | | |
| Peak versus baseline errors/latency | | |
| Data loss or exposure | | |
| SLA/SLO or business impact | | |

## Timeline
| UTC time | Event/observation | Source | Confidence |
|---|---|---|---|

## Root Cause and Causal Chain
<Systemic cause, evidence, and validated 5-Whys or causal chain.>

## Contributing, Detection, and Recovery Factors
- <factor — evidence and effect>

## What Went Well
- <system/process capability supported response>

## What Could Have Gone Better
- <specific system/process gap, no blame language>

## Action Items
| ID | Specific deliverable | Accountable owner | Due date | Priority | Acceptance evidence |
|---|---|---|---|---|---|

## Lessons, Unknowns, and Follow-up
<Non-obvious learning, unresolved gaps, publication/retention, and next review trigger.>
```

## Quality and publication gates

- Verify timeline times and links against source systems; disclose gaps and timezone conversions.
- Check that impact numbers reconcile with metrics, logs, billing, and user reports where available.
- Ensure root cause is systemic and supported; retain counterevidence and confidence.
- Ensure every action has one accountable owner, date, priority, acceptance evidence, and review trigger.
- Redact secrets, customer data, private tokens, and unnecessary personal identifiers.
- Re-read for blame language, unsupported certainty, duplicate actions, and action items without an owner.
- If ticket/issue publication is authorized, link resulting IDs and verify they contain no sensitive evidence; otherwise provide a safe backlog handoff only.

## WorkBuddy handoff

Return the report path, target revision, evidence sources and time window, impact calculations,
causal findings, counterevidence, action ledger, unresolved unknowns, redaction decisions,
validation results, publication status, and next review date. A complete document may still be
marked partial when key logs, metrics, ownership, or impact data were unavailable.
