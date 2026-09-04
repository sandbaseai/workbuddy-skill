---
name: "architecture-decision"
display_name: "架构决策记录"
display_name_en: "Architecture Decision Record"
description: "Use when a technical choice changes system boundaries, contracts, data, operational characteristics, or carries meaningful reversal cost; compare viable alternatives and produce a verifiable architecture decision record."
description_zh: "以可验证的约束、候选方案、权衡、可逆性和适应度函数制定并记录重要架构决策。"
description_en: "Make and record consequential architecture decisions through verifiable constraints, alternatives, tradeoffs, reversibility, and fitness functions."
category: "development"
version: "0.1.0"
author: "Paulo Lacerda; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Architecture Decision Record

Use this skill when a choice has meaningful consequences or reversal cost. Do not create an ADR for routine implementation details, and do not use an ADR to retroactively justify a decision that has not actually been evaluated.

## Frame the decision

- State the decision to be made, why it is needed now, its owner, and the deadline.
- Separate verified facts, assumptions, constraints, preferences, and unresolved questions. Link evidence when available.
- Identify affected boundaries, interfaces, data, security/privacy, reliability, performance, cost, delivery, maintenance, and operations.
- Prioritize no more than five decision-driving characteristics. Give each an observable measure or acceptance threshold rather than labels such as “scalable” or “simple.”
- Preserve requirements and organizational constraints; do not turn a preferred vendor or tool into a requirement.

## Compare options fairly

Evaluate at least two viable alternatives plus “do not change” when it is genuinely possible. Use the same criteria and time horizon for every option. For each, record:

- evidence-backed benefits and limitations;
- delivery and ongoing operational cost;
- failure modes, security/privacy exposure, and blast radius;
- compatibility, migration, data movement, and vendor or ecosystem coupling;
- reversibility, exit cost, and what would make reversal unsafe;
- material unknowns and confidence in the assessment.

Do not invent precision or silently weight criteria. If evidence is insufficient, define a bounded spike or experiment with an owner, deadline, decision criterion, and cost ceiling. Distinguish correlation, estimates, and tested facts.

## Decide and make it testable

Explain why the selected option best satisfies the prioritized constraints, including accepted disadvantages. Record dissent or unresolved risk without weakening it into false consensus. Define:

- adoption sequence, dependency order, compatibility period, and responsible owners;
- rollback or roll-forward conditions, especially for irreversible data changes;
- fitness functions such as tests, policies, budgets, service-level indicators, or architecture checks;
- a review trigger based on a date, threshold, assumption failure, material incident, or requirement change.

Draft the record with [references/adr-template.md](references/adr-template.md). Use `Proposed` until the authorized decision owner accepts it. Do not publish, approve, or implement the decision unless the current request authorizes those actions.

## Validate the record

Before handoff, confirm that a new reader can identify the problem, evidence, options, decision owner, tradeoffs, migration path, verification method, and reassessment trigger without relying on undocumented conversation history. Preserve superseded ADRs and link replacements rather than rewriting history.
