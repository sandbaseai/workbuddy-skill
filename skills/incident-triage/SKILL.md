---
name: "incident-triage"
display_name: "事故响应与分诊"
display_name_en: "Incident Response and Triage"
description: "Use when triaging incidents, production errors, alerts, latency, error rates, queue backlogs, job failures, logs, metrics, traces, or post-incident runbooks."
description_zh: "通过日志、指标、链路、变更和用户影响证据对生产事故进行分级、止损、恢复验证和无责复盘。"
description_en: "Triage production incidents through logs, metrics, traces, changes, and user-impact evidence; contain harm, verify recovery, and support blameless learning."
category: "security"
version: "0.1.0"
author: "jukrap; adapted for WorkBuddy by SandBase AI"
---

# Incident Response and Triage

Use this skill for active production incidents, alerts, latency or error spikes, queue backlogs, failed jobs, logs/metrics/traces, incident playbooks, and post-incident reviews. Reduce user harm first, preserve evidence, and stabilize the system before pursuing a complete root cause.

## Operating principles

- State timestamps with a time zone and distinguish observations, reports, hypotheses, and confirmed causes.
- Treat correlation with a deployment or dependency as a lead, not proof of causation.
- Prefer read-only, narrowly scoped inspection and compare affected segments with a known-good baseline.
- Freeze unrelated changes while impact is active. Keep every mitigation small, reversible, recorded, and paired with a rollback condition.
- Never expose secrets or customer data. Redact durable evidence instead of copying raw sensitive logs.
- Do not reboot, delete, purge, drain queues, rotate credentials, alter traffic, disable security controls, or communicate externally without the required authorization and a safe recovery plan.

## Establish incident command

Scale roles to the incident, combining them for small events:

- Incident lead: owns severity, priorities, decisions, and update cadence.
- Operations lead: investigates and executes authorized mitigations.
- Communications lead: prepares audience-appropriate status updates.
- Scribe: maintains the timeline, evidence, actions, owners, and outcomes.

Record the symptom, first detection, likely start, last known good state, affected users/services/regions, data or security risk, workaround availability, recent changes, telemetry sources, current owners, and severity according to the project's policy. If a fact is unknown, label it unknown.

## Active-incident workflow

1. **Detect and acknowledge.** Confirm the signal is current, name the incident lead, open a shared timeline, and set the next update time.
2. **Assess impact.** Establish scope, user-visible harm, data/security exposure, dependencies, and whether impact is growing. Escalate through the organization's defined path when thresholds are met.
3. **Stabilize.** Prefer the safest authorized containment: rollback, feature flag, traffic shift, rate limit, queue pause, or degraded mode. Do not delay harm reduction for a perfect diagnosis, but verify preconditions and rollback safety before acting.
4. **Investigate.** Correlate deploys, configuration, migrations, dependencies, queues, jobs, capacity, and error boundaries. Preserve expiring evidence before restarts or cleanup. Change one variable at a time when practical.
5. **Verify recovery.** Require the original impact signal to recover, an independent user-path or synthetic check to pass, and a suitable observation window. A green deploy alone is not recovery; do not mark resolved while impact or material uncertainty remains.
6. **Communicate and hand off.** Report facts, impact, mitigation, remaining risk, owner, and next update time. Keep external messages in draft form unless sending is explicitly authorized.

## After stabilization

Run a blameless review that separates the trigger, contributing conditions, root causes, detection gaps, and response gaps. Preserve the decision timeline and note where evidence is incomplete. Create concrete actions with an owner, due date, and verification method; avoid vague actions such as “be more careful.” Update tests, monitors, dashboards, and runbooks where they would reduce recurrence or recovery time.

## Response format

```text
Status / timestamp / time zone:
Severity and owner:
User and system impact:
Confirmed evidence:
Working hypotheses:
Actions taken and authorization:
Recovery checks and observation window:
Next action / owner / update time:
Open risks and unknowns:
```

## References

Read `references/incident-evidence.md` for active incident intake, containment, and handoff.

Read `references/logs-metrics-traces.md` when interpreting observability evidence.
