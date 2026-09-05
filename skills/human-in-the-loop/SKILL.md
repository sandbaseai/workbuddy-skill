---
name: "human-in-the-loop"
display_name: "人工监督与审批"
display_name_en: "Human in the Loop"
description: "Use when designing or verifying auditable human oversight, approval gates, escalation paths, and safe state transitions for AI agent workflows."
description_zh: "用于为 AI Agent 工作流设计或验证可审计的人工监督、审批门禁、升级路径和安全状态转换。"
description_en: "Place human judgment at the decision point where it changes risk, bind an authorized decision to an immutable action, and preserve evidence through execution and recovery."
category: "security"
version: "0.1.0"
author: "seb1n/awesome-ai-agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized identity, policy, audit, notification, and execution controls"
---

# Human in the Loop

Place human judgment where it changes risk. A confirmation dialog alone is not
oversight: bind an authorized decision to an understandable, immutable action
and preserve evidence of what happened. Designing a gate never authorizes the
underlying action.

## Inventory and risk tiers

List every Agent action, target object, effect, reversibility, scale,
sensitivity, external visibility, value, time pressure, affected rights, and
containment option. Separate reading, drafting, previewing, and recommending
from sending, publishing, purchasing, deleting, granting access, executing
code, or other consequential effects.

Assign the lightest sufficient control:

- **Autonomous with audit:** bounded, reversible, low-impact actions.
- **Notify after action:** low-impact actions needing awareness.
- **Review before action:** consequential or externally visible actions.
- **Step-up approval:** a value, sensitivity, anomaly, confidence, or scope
  threshold is crossed.
- **Dual control:** critical, irreversible, privileged, or regulated actions;
  require distinct approver subjects by default.
- **Prohibited:** the action cannot be acceptably safe.

Do not gate trivial steps until users rubber-stamp everything. Never let the
model fabricate, infer, or impersonate human approval.

## Approval contract

Define predicates, eligible roles and distinct subjects, quorum, evidence,
expiry, timeout, escalation, audit-outage behavior, execution-time
reauthorization, compensation, break-glass, separation of duties, and
retention/redaction. If policy is incomplete, output a proposed policy marked
for owner approval rather than inventing authority.

Show the approver the plain-language intent, gate reason, normalized target and
parameters, exact payload or before/after diff, expected effects, affected
parties, cost, reversibility, evidence provenance and freshness, uncertainty,
policy basis, alternatives, and the result of reject, edit, or timeout. Hide
secrets and minimize personal data; make reject/cancel as usable as approve.

Authenticate and authorize the approver outside the model. Bind actor, tenant,
action, target, material parameters, policy version, expiry, and nonce to a
canonical proposal digest. Invalidate approval after any material edit, target
or state change, expiry, or policy change. Do not interpret silence, receipt,
or generic prior consent as approval.

## Safe state machine

Use explicit, atomic, idempotent transitions such as:

`prepared -> pending_review -> approved | rejected | expired | cancelled`

`approved -> executing -> completed | failed | compensation_pending`

Recheck identity, role, policy, proposal digest, target state, preconditions,
and expiry immediately before execution. Consume one-time approvals once and
handle concurrent approvers, duplicate callbacks, stale screens, retries, and
partial downstream failure.

Timeouts must deny, cancel, or escalate—not approve. Define reminder and
escalation owners, wait/attempt limits, out-of-office coverage, and exhaustion
behavior. Critical actions fail closed when the audit store is unavailable
unless a narrowly scoped, signed buffer is explicitly approved. Break-glass
must be a distinct strongly authenticated path with named subjects, narrow
scope, short expiry, reason capture, alerting, and after-action review.

## Verification and recovery

Test risk-tier assignment, wrong-tenant and unauthorized actors, self-approval,
quorum and distinct-subject rules, parameter/target/policy/expiry changes,
duplicate callbacks, reject/edit/cancel/timeout, escalation exhaustion,
reauthorization, audit outage, partial failure, compensation, break-glass,
decision-record redaction, and approval comprehension/error rates. Verify that
the implementation and approval experience both work; a policy document is not
evidence.

On rejection, preserve the proposal and reason without executing. On failure,
stop unsafe retries, mark the true state, invoke tested compensation when
available, notify the owner, and preserve redacted evidence. Handoff must
include current state, owner, proposal digest, decision subjects and times,
next action, unresolved risks, and recovery status. Finish only when every
consequential action has a validated policy, approvals cannot replay or broaden
silently, escalation and recovery paths are tested, and residual risk is
explicit.
