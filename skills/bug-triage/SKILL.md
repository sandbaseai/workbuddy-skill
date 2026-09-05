---
name: "bug-triage"
display_name: "缺陷分诊与修复分析"
display_name_en: "Bug Triage and Fix Analysis"
description: "Triage bug reports, analyze errors and stack traces, identify competing causes, find duplicates, and prioritize safe fixes with evidence."
description_zh: "对缺陷报告进行分诊，分析错误和堆栈，识别竞争性原因、重复问题，并基于证据安排安全修复优先级。"
description_en: "Triage bug reports, analyze errors and stack traces, identify competing causes, find duplicates, and prioritize safe fixes with evidence."
category: "development"
version: "0.1.0"
author: "xray; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Bug Triage and Fix Analysis

Use this skill when turning a bug report, exception, stack trace, failing test,
or support signal into a bounded investigation and an owned next action. It
helps distinguish a reproducible defect from a usage question, environment
issue, duplicate, regression, or insufficient evidence. It does not claim to
have accessed an issue tracker or repository unless that source was actually
provided or authorized.

## Intake and evidence quality

Capture the report ID or safe local reference, reporter context, first and most
recent occurrence, time zone, affected version, environment, user-visible
symptom, frequency, severity, workaround, and privacy classification. Preserve
the original wording separately from normalized summaries. Mark each field as
observed, reported, inferred, or unknown.

Request the smallest useful reproduction: exact input shape without secrets,
expected and actual behavior, deterministic steps, a known-good comparison,
relevant configuration, and the narrowest logs or trace. Redact tokens,
credentials, personal data, private URLs, and confidential payloads before
sharing or storing evidence. Do not ask a reporter to expose production data
just to improve a ticket.

## Analyze errors and stack traces

1. Confirm the exception or failure is from the claimed component and version.
2. Read the stack from the failure boundary outward, distinguishing the first
   application frame from framework or wrapper frames.
3. Identify inputs, state transitions, dependency calls, and error handling at
   the boundary; do not treat the deepest or loudest frame as the root cause.
4. Compare a failing and successful path, including deploy, configuration,
   schema, feature-flag, dependency, and traffic differences.
5. Form multiple hypotheses and choose the cheapest safe experiment that
   separates them. Record what result would falsify each hypothesis.
6. Confirm whether the behavior is a regression, an existing limitation, a
   duplicate, or a new failure mode before proposing a fix.

Never execute a suggested fix merely because it sounds plausible. Avoid broad
production changes, deleting data, disabling validation, suppressing an error,
or changing security controls as a debugging shortcut. Prefer read-only
inspection, a minimized test, a local or controlled reproduction, and a small
reversible change with an explicit rollback condition.

## Triage and priority

Classify severity from demonstrated user or business impact, not from emotion
or technical novelty. Consider affected scope, reproducibility, data loss or
security exposure, workaround quality, duration, frequency, and whether impact
is increasing. Keep severity, priority, confidence, and effort as separate
fields:

- severity describes harm if the bug occurs;
- priority describes when the team should act under current constraints;
- confidence describes the quality of evidence;
- effort describes the estimated cost and uncertainty of the fix.

For duplicates, compare symptom, trigger, affected version, component,
regression window, and proposed workaround. Link evidence rather than merging
reports solely because their exception names match. If a security boundary or
personal-data exposure may be involved, route it through the authorized
security process and keep sensitive details out of ordinary issue comments.

## Fix proposal and verification

A fix proposal must name the causal boundary, smallest safe change, compatibility
impact, test that would fail before the fix, regression and adjacent boundary
tests, rollout guard, rollback condition, and owner. Distinguish a mitigation
from a durable fix. If the cause is not confirmed, state the next experiment
instead of inventing certainty.

After implementation, verify the original reproduction, the relevant known-good
path, input and permission boundaries, persistence or retry behavior, and the
production signal that exposed the issue. For a rollout, compare affected and
control segments over an appropriate observation window. Do not close a bug on
the basis of a green build alone.

## Handoff format

```text
Bug reference / status / timestamp:
Observed symptom and expected behavior:
Scope, versions, environment, and user impact:
Evidence and redaction status:
Reproduction and known-good comparison:
Hypotheses with confidence and falsifying checks:
Duplicate / regression assessment:
Severity / priority / effort / rationale:
Mitigation or fix proposal / owner:
Verification, rollout, and rollback evidence:
Open unknowns and next update:
```

Return reproducible evidence and explicit uncertainty. A useful triage result
ends with one safe next action and an accountable owner, even when the root
cause remains unresolved.
