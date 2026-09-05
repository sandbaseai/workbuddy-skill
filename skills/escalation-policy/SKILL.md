---
name: "escalation-policy"
display_name: "升级策略"
display_name_en: "Escalation Policy"
description: "Use when a support, operations, or service request crosses a safety, legal, urgency, authority, value, or service-level threshold requiring a specialized owner."
description_zh: "用于支持、运营或服务请求触及安全、法律、紧急性、权限、金额或服务级别阈值，需要转交专业责任人时。"
description_en: "Apply explicit escalation triggers and non-triggers, acknowledge the request without promising an outcome, preserve context and sensitivity, assign a safe reference, and route to the accountable specialist with measurable follow-up."
category: "development"
version: "0.1.0"
author: "Microsoft Agent Framework; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized support or operations context, documented thresholds and owners, case/ticket identifier, service-level commitments, and approved escalation channel"
---

# Escalation Policy

Route a request to the right accountable owner when it exceeds the current agent's authority, safety boundary, expertise, or service level. Use the configured policy and thresholds for the actual service; do not invent a deadline, reference number, refund, diagnosis, legal conclusion, or other outcome. If no policy exists, state that the threshold is undefined and escalate to the designated policy owner.

## Check for escalation

Inspect the request, current case history, identity and authorization, service level, affected users, data sensitivity, and prior commitments. Escalate immediately when any documented trigger applies, such as:

- injury, safety incident, self-harm, abuse, security breach, or imminent material harm;
- legal process, regulator, law enforcement, media, privacy rights, or a formal complaint;
- a request outside the agent's authority, a privileged action, an account-access dispute, or a high-impact automated decision;
- a materially breached service-level commitment, repeated unresolved failure, or a financial/contractual threshold defined by the service owner;
- a pattern suggesting systemic outage, abuse, fraud, or cross-tenant impact.

Do not escalate routine requests that are within documented policy and authority merely because they are inconvenient. Keep the distinction between an operational handoff and an emergency response. When signals conflict or the threshold is ambiguous, choose the safer authorized owner and record the uncertainty.

## Acknowledge and route safely

1. Acknowledge the request and immediate impact without admitting fault or promising a result.
2. State that it is being routed to the appropriate specialist and why, at the minimum useful level.
3. Create or preserve the approved case reference; never expose internal secrets, personal data, or an unverified reference.
4. Transfer a concise context packet: requester and authorization class, issue, timeline, evidence location, actions already taken, urgency, sensitivity, requested decision, and explicit restrictions.
5. State only the policy-backed service level or next checkpoint. If none is known, say so and assign an owner to establish it.

Do not ask the requester to repeat sensitive information unnecessarily. Do not close the original case, erase evidence, or contact a third party unless the policy authorizes it. For urgent safety or security conditions, follow the approved emergency channel and stop ordinary troubleshooting that could increase harm.

## Continue and hand off

The receiving owner confirms scope, authority, next action, and response time. Keep a timestamped audit trail of the trigger, decision, handoff, status, and requester-visible communication. Re-escalate if the response deadline is missed, impact grows, the case crosses a new threshold, or ownership is rejected. Close only when the accountable owner confirms resolution or an explicitly approved disposition; record residual risk, follow-up, and policy gaps.

The final summary includes the trigger, current status, owner, reference, policy-backed timing, actions taken, evidence location, communication constraints, unresolved uncertainty, and next checkpoint. Never promise a specific remedy that only the specialist can authorize.
