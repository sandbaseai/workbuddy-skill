---
name: "agent-red-teaming"
display_name: "Agent 红队评估"
display_name_en: "Agent Red Teaming"
description: "Use when planning or documenting an authorized security assessment of an AI agent or multi-agent workflow with safe adversarial cases, synthetic identities, canaries, and evidence-based retesting."
description_zh: "用于在明确授权的环境中，对 AI Agent 或多 Agent 工作流进行安全评估，使用安全对抗用例、合成身份、金丝雀和基于证据的复测。"
description_en: "Assess authorized agent systems through explicit rules of engagement, privilege mapping, safe test matrices, traceable findings, bounded execution, cleanup, and remediation retesting."
category: "security"
version: "0.1.0"
author: "seb1n/awesome-ai-agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with target-specific authorization, isolated test environments, and approved security controls"
---

# Agent Red Teaming

Find exploitable control failures without creating uncontrolled harm. Written
authorization and rules of engagement are prerequisites for execution, not
paperwork to complete afterward. Public reachability is not permission.

## Authorization and scope

Before execution, record the named owner, authorization reference, exact
targets, environment, models and configuration digest, tester identity, time
window, in/out-of-scope systems and tenants, allowed techniques, rate/cost
limits, stop conditions, emergency contact, cleanup owner, and evidence policy.
If target-specific authorization or scope is missing, produce only a
non-executable plan and threat model. Never probe a live target to infer scope.

Use synthetic accounts, inert destinations, non-destructive tools, and benign
canary values that grant no access. Confirm how to disable test tools, revoke
credentials, restore fixtures, and report an unexpected effect before testing.

## Assessment contract

Deliver:

1. Approved or explicitly pending rules of engagement.
2. A system and privilege map plus prioritized threat hypotheses.
3. A case plan with unique case IDs, target, environment, configuration
   digest, authorization reference, limits, stop conditions, safe oracle, and
   cleanup duty.
4. Execution records tied to approved cases and unique test IDs, including
   timestamps, observed limits, structured redacted evidence, and cleanup.
5. Deduplicated findings with reproduction, impact, likelihood, prerequisites,
   root control failure, remediation, and regression case.
6. Metrics using all approved case IDs as the denominator, distinguishing pass,
   failure, blocked, error, missing, and not-run.
7. Retest results, residual risk, scope deviations, and cleanup confirmation.

## Map authority and build the test matrix

Trace user input, instructions, retrieval, memory, tools, code execution,
browsers, plugins, handoffs, identities, approvals, output sinks, and egress.
Show tenants, objects, actions, network destinations, delegation, and
credential boundaries. Write each hypothesis as attacker-controlled source +
control weakness + attempted action + observable safe oracle.

Cover applicable direct, indirect, stored, encoded, and multimodal injection;
tool misuse and target substitution; excessive agency and unsafe chaining;
authentication, authorization, tenant isolation, approval binding,
confused-deputy paths; sensitive-data disclosure and egress; memory/RAG and
dependency poisoning; cross-Agent impersonation and delegation escalation;
resource or cost amplification; monitoring, containment, revocation, and
recovery. Include benign tasks to measure false positives and retained utility.

## Execute incrementally and safely

Start offline or mocked, then isolated staging, then any separately authorized
higher-risk environment. Run low-impact cases first and capture the case ID,
authorization, target, environment, configuration, tester subject, timestamps,
input provenance, tool trace, policy decisions, observed rate/cost/time,
result, evidence, and cleanup state. Respect limits; do not evade controls.

Pause immediately for unexpected cross-tenant access, real secrets, external
effects, service degradation, canary exposure, or scope ambiguity. Stop, notify
the emergency contact, contain access, preserve redacted evidence, and support
restoration; incident response takes precedence over campaign completion.

## Triage, remediate, and retest

Distinguish a confirmed invariant violation, a blocked attack showing the
expected control, a harness/environment error, and an observation needing more
evidence. A pass requires the protected invariant to hold; blocked, errored,
missing, and not-run cases are not passes. Deduplicate findings by root control
failure while retaining meaningful variants.

Prefer architectural remediation: reduce privilege, enforce authorization
outside the model, constrain tools and egress, isolate untrusted content,
validate outputs, bind approvals, and protect memory provenance. Prompts and
detectors are defense in depth, not the sole fix. Retest the original case,
nearby variants, and representative benign tasks; record owner, evidence, and
whether the risk is fixed, partially mitigated, accepted, transferred, or open.

## Safety, cleanup, and completion

Do not use real secrets, personal data, malware, persistence, destructive
actions, denial of service, uncontrolled propagation, social engineering, or
real transactions when synthetic proof is sufficient. Keep evidence minimal,
redacted, access-controlled, and traceable. Remove synthetic records, restore
fixtures, disable test endpoints, revoke test credentials, and confirm no jobs
or callbacks remain.

Complete only when every result maps to an approved case, high-risk paths have
safe evidence, findings agree with observed invariants, remediation is
retested, benign utility and false positives are measured, limits and cleanup
are evidenced, and residual or untested risk is explicit. Never declare a
target secure or certified from campaign results.
