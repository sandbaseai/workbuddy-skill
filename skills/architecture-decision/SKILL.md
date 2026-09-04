---
name: "architecture-decision"
display_name: "架构决策"
display_name_en: "Architecture Decision"
description: "Use when a technical choice changes system boundaries, contracts, quality attributes, data, or operations and has meaningful reversal cost."
description_zh: "当技术选择会改变系统边界、契约、质量属性、数据或运维方式，且回退成本较高时，用于形成可验证、可审查的架构决策。"
description_en: "Create a durable, evidence-backed architecture decision by defining context and constraints, comparing alternatives, recording trade-offs, and setting measurable fitness functions, migration, ownership, and review triggers."
category: "development"
version: "0.1.0"
author: "placerda; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Repository context, system diagrams, requirements, operational constraints, and decision stakeholders"
---

# Architecture Decision

Use this skill when a choice can alter boundaries, APIs, data ownership, deployment, security, reliability, performance, cost, or operational responsibility. Produce a decision that another engineer can verify and revisit; do not turn a tool preference into an architectural requirement.

## Establish the decision frame

1. State the decision to make and the deadline.
2. Describe the current context, users, components, data flows, and relevant dependencies.
3. Record constraints: compatibility, regulation, team capability, delivery window, budget, latency, availability, and migration limits.
4. Identify up to five prioritized quality attributes and measurable targets (for example p95 latency, recovery time, availability, cost per request, or deploy frequency).
5. List assumptions and missing evidence. If evidence is insufficient, record an investigation, owner, deadline, and decision criterion.

Do not claim a quality attribute without a measurement plan. Separate requirements from preferences and reversible experiments from durable commitments.

## Compare options

Compare at least two viable alternatives and the option of not changing. For each, cover:

- boundary and contract changes;
- data ownership, consistency, migration, and rollback;
- security, privacy, reliability, performance, and cost implications;
- developer and operator experience, dependencies, and failure modes;
- implementation effort, time to value, reversibility, and lock-in.

Use the same criteria for every option. Mark unknowns explicitly and distinguish evidence from judgment. A scorecard is useful only when its scale and weighting are explained; it must not hide a disqualifying risk behind an average score.

## Record the decision

Write an ADR with: title, status, date, owners, context, decision drivers, considered options, decision, consequences, risks, mitigations, dependencies, operational impact, and links to evidence. State what is deliberately out of scope.

Define fitness functions that can be checked in CI, staging, or production: the metric, threshold, measurement source, sampling window, and owner. Include adoption steps, migration slices, compatibility period, data backfill or dual-write safeguards, cutover criteria, rollback trigger, and cleanup of temporary paths.

## Govern the outcome

Before implementation, confirm affected teams, contracts, dashboards, alerts, runbooks, access controls, and support procedures. During rollout, use a canary or bounded cohort when risk warrants it; monitor correctness and user impact as well as technical metrics. Stop when a guardrail is breached or an assumption is disproven.

Set a review trigger: date, workload or dependency change, incident, metric regression, regulatory change, or expiry of an exception. Revisit the ADR when the trigger fires. Handoff the decision, evidence, owner, rollout state, unresolved risks, and next authorized action.
