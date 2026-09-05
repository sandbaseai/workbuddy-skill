---
name: "architectural-decision-record"
display_name: "架构决策记录"
display_name_en: "Architectural Decision Record"
description: "Use when documenting an important architecture or technology decision with context, constraints, alternatives, trade-offs, evidence, ownership, status, and a durable review path."
description_zh: "用于记录重要架构或技术决策，包含背景、约束、替代方案、取舍、证据、责任人、状态和可持续复查路径。"
description_en: "Create a concise, machine-readable ADR that separates facts from assumptions, preserves rejected alternatives and consequences, and makes supersession and validation explicit."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with repository decision-history access and an authorized docs/adr output path; stakeholder names, private references, and external publication require appropriate permission"
---

# Architectural Decision Record

## Purpose and boundary

Create a durable record for a consequential architecture, platform, data, security, or workflow
decision. An ADR captures why a choice was made, what it costs, what evidence supports it, and
when it should be revisited. It is not an implementation plan, a design specification, or proof
that the chosen option has already been approved.

Default to an authorized draft in `docs/adr/`; do not modify application code, silently create
architecture policy, expose private discussions, or mark a proposal accepted without the actual
decision owner. Preserve uncertainty and label inferred reasoning. Never copy secrets or private
customer information into an ADR.

## Decision contract

Before writing, identify:

- one decision question and the consequence of delaying it;
- context, constraints, goals, non-goals, scope, and affected systems/people;
- decision owner, authors, reviewers, date, target revision, and expiry/review trigger;
- observed evidence, assumptions, unknowns, and confidence for each important claim;
- alternatives considered, evaluation criteria, rejected rationale, and decision boundaries;
- status: Proposed, Accepted, Rejected, Superseded, or Deprecated;
- consequences, migration/rollback implications, validation signals, and follow-up owners.

If the decision question or owner cannot be determined, create a clearly marked framing draft or
report the missing input. Do not fill required fields with plausible names, dates, benchmarks, or
approvals.

## Step 1: discover existing decisions

Read repository instructions, existing `docs/adr/` files, architecture docs, manifests, IaC,
contracts, operational constraints, incidents, costs, security reviews, and relevant history.
Find the next available four-digit ADR number by inspecting actual files, handling gaps or
duplicates explicitly. Search for decisions that this ADR may supersede or that already constrain
the choice. Cite stable file paths, line/section anchors, immutable commits, issue/PR links, or
versioned external documentation.

Separate three ledgers:

| Ledger | Meaning |
|---|---|
| Fact | Directly observed or documented evidence |
| Assumption | A working belief that must be tested or owned |
| Unknown | Evidence unavailable or contradictory; no conclusion yet |

Do not rewrite an existing ADR in place to change history. Create a new ADR that links
`supersedes`/`superseded_by` relationships and records the migration of status.

## Step 2: frame and compare alternatives

Define the criteria before ranking options: correctness, reliability, security/privacy, performance,
cost, operability, compatibility, reversibility, delivery effort, and organizational constraints.
Use the same criteria for every viable alternative. Include “do nothing” or defer when it is a
real option. Distinguish evidence-backed comparison from preference.

For each alternative record:

- concise mechanism and scope;
- supporting evidence and confidence;
- positive and negative consequences;
- rejection, selection, or deferral rationale;
- migration, rollback, dependency, and lock-in implications;
- what future evidence could change the ranking.

Do not claim a benchmark, cost, compliance property, provider capability, or failure mode without
source evidence. If a small experiment is needed, link a bounded technical spike rather than
embedding unverified results.

## Step 3: write a machine-readable ADR

Save as `docs/adr/adr-NNNN-<title-slug>.md`, using the next unique number and a stable kebab-case
slug. Keep front matter scalar/list values valid for the repository's documentation tooling.
Use coded identifiers for repeated items so agents and humans can refer to the same consequence or
implementation note without ambiguity.

```markdown
---
title: "ADR-NNNN: <decision title>"
status: "Proposed"
date: "YYYY-MM-DD"
authors: "<roles/names permitted for publication>"
decision_owner: "<role or permitted person>"
target_revision: "<commit/tag or unknown>"
review_trigger: "<date, metric, incident, or change>"
tags: ["architecture", "decision"]
supersedes: ""
superseded_by: ""
---

# ADR-NNNN: <Decision Title>

## Status
**Proposed**

## Decision Question and Context
<Problem, goals, constraints, scope, non-goals, and why now.>

## Evidence, Assumptions, and Unknowns
- **EVD-001**: Fact — <source and confidence>
- **ASM-001**: Assumption — <owner and validation plan>
- **UNK-001**: Unknown — <impact and next evidence>

## Decision
<Chosen or deferred option, boundary, rationale, and approval state.>

## Consequences
### Positive
- **POS-001**: <benefit and evidence/acceptance signal>
### Negative
- **NEG-001**: <trade-off, risk, or cost and mitigation>

## Alternatives Considered
### <Alternative>
- **ALT-001**: Description — <mechanism and scope>
- **ALT-002**: Rationale — <selected/rejected/deferred with evidence>

## Implementation and Validation Notes
- **IMP-001**: <migration, compatibility, rollout, or rollback>
- **VAL-001**: <test/metric/review signal and owner>

## References and Follow-up
- **REF-001**: <stable source>
- **ACT-001**: <specific follow-up, owner, due/review trigger>
```

Correct the template for repository conventions; do not retain placeholders in a decision claimed
as complete. A proposed ADR may retain explicit unknowns and unfilled approval fields, but must
say that it is proposed.

## Step 4: status, integrity, and lifecycle

Use status transitions deliberately: Proposed requires review; Accepted requires a recorded
decision owner and approval evidence; Rejected records why; Superseded links the replacing ADR;
Deprecated states that the decision no longer applies. Never backdate an approval or erase an
old consequence. If implementation diverges from the decision, update follow-up notes or create a
new ADR rather than silently rewriting rationale.

Check numbering, front matter, links, terminology, source licenses, privacy, and cross-references.
Validate that the decision is internally consistent with constraints, alternatives, consequences,
architecture docs, and operational gates. Link implementation or rollback work only after it has
an owner and acceptance signal.

## WorkBuddy handoff

Return the ADR path and number, target revision/date, decision question, status and approval
state, facts/assumptions/unknowns, alternatives and rejected rationale, positive/negative
consequences, evidence links, conflicts with existing ADRs, validation results, follow-up ledger,
and review trigger. State whether the file is a draft, proposed, accepted, or blocked by missing
evidence/authority. Do not present a generated ADR as organizational approval.
