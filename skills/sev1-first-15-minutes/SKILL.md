---
name: "sev1-first-15-minutes"
display_name: "Sev1 前 15 分钟"
display_name_en: "Sev1 First 15 Minutes"
description: "Use when a confirmed high-severity production incident needs a bounded first response, clear ownership, safe stabilization, and an auditable timeline."
description_zh: "用于确认发生高严重度生产事故时，在前 15 分钟内完成分级、分工、沟通、低风险止血和可审计时间线。"
description_en: "Coordinate the first 15 minutes of a Sev1 incident with explicit roles, customer-impact communication, read-first diagnosis, reversible stabilization, and escalation evidence."
category: "security"
version: "0.1.0"
author: "bregman-arie/devops-sre-skills; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
compatibility: "WorkBuddy with authorized incident, observability, and deployment tools"
---

# Sev1 First 15 Minutes

Use this Skill only for a confirmed or strongly suspected high-severity
production incident. It coordinates people and evidence; it does not silently
page people, change production, or claim recovery without observable proof.

## Establish the operating boundary

Capture the service, symptoms, suspected start time, affected customer or
tenant scope, current operator, and the source of each fact. Open or identify
the incident channel and page only the responders authorized by the service's
policy. Do not paste secrets, tokens, private customer data, or raw sensitive
logs into the channel or report.

Default to read-only inspection. Any rollback, feature disablement, traffic
shedding, write freeze, or other production mutation requires the applicable
human approval or pre-authorized runbook, an explicit expected effect, and a
reversible path. If no authority or safe action is established, escalate rather
than improvising commands.

## First 15-minute checklist

1. Declare the provisional severity and record the clock time and timezone.
2. Assign an incident commander, communications lead, and operations lead;
   name an evidence/timeline keeper when staffing permits.
3. State customer impact in one sentence, including what is unknown.
4. Gather bounded error-rate, latency, saturation, deployment, dependency, and
   customer-report evidence. Preserve query windows and timestamps.
5. Choose the lowest-risk authorized stabilization: rollback, disable a
   feature, shed load, isolate a dependency, or freeze writes when integrity is
   at risk. Record why it is expected to help.
6. Publish a status update with the next update time, then maintain a cadence
   appropriate to the incident policy.
7. Escalate to security for authentication abuse, suspected data exposure, or
   suspicious activity; escalate to leadership when an SLA/SLO breach or
   material customer impact is likely.

## Decision and evidence rules

- If impact is unknown, measure and narrow scope before making broad changes.
- If a low-risk, reversible mitigation is likely effective, propose it early;
  never present a proposed mutation as completed.
- If data integrity may be affected, stop writes only through an authorized
  control and involve the data owner.
- Keep a timeline of observations, hypotheses, approvals, actions, outcomes,
  and reversals. Separate facts from hypotheses and label stale data.
- Use stable links, query names, deployment IDs, and time ranges instead of
  copying sensitive payloads.

## Communication template

```text
Severity: <provisional level> | Start: <timestamp with timezone>
Impact: <who/what is affected; unknowns>
Current evidence: <bounded observations and source links>
Mitigation: <proposed/in progress/completed; owner and approval>
Next update: <timestamp>
Escalation: <team, reason, and time>
```

## Verify, hand off, and undo

Treat stabilization as successful only when leading indicators improve across
an appropriate comparison window, customer reports trend down, and no new
integrity or security signal appears. If impact worsens, stop the action or
revert through the approved path and record the result. Handoff must include
the current commander, impact statement, timeline, active hypothesis,
mitigation state, unresolved risks, next update time, and links to redacted
evidence. Continue to post-incident review only after the incident owner
confirms the service is stable and the follow-up owner is assigned.
