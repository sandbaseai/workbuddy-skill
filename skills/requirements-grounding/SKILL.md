---
name: "requirements-grounding"
display_name: "需求溯源"
display_name_en: "Requirements Grounding"
description: "Ground proposed requirements in an actor-bound problem, explicit scope, authoritative sources, evidence, assumptions, priority, and validation confidence."
description_zh: "将客户、产品、合同、法规或现有系统输入整理为可追溯、无方案预设、带置信度和可观察完成条件的需求。"
description_en: "Turn customer, product, contract, regulatory, or existing-system input into traceable, solution-free requirements with confidence and observable completion conditions."
category: "business"
version: "0.1.0"
author: "L-GEVITY; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Requirements Grounding

Turn raw customer, product, contractual, regulatory, operational, or existing-
system input into requirement candidates that are traceable, solution-free, and
honest about uncertainty. Use this before implementation planning when the real
problem, authority, scope, or completion conditions are not yet stable.

## Core rules

1. **Problem before solution.** Do not derive a feature from an unconfirmed
   problem statement.
2. **Separate source classes.** Authority, evidence, interpretation, and
   hypothesis imply different confidence and validation work.
3. **One actor, one outcome.** Split material role, lifecycle, or completion
   differences instead of hiding them in a compound requirement.
4. **Observable completion.** State how a reviewer can know the capability is
   complete without prescribing implementation.
5. **Implementation is evidence, not intent.** Code shows what the inspected
   version can do; it does not prove what should happen or why.
6. **Completion is not impact.** Passing acceptance conditions does not prove a
   downstream business or user outcome occurred.

## Source discipline

For every material source, identify its class, owner, applicability, version,
date, and status. Prefer the canonical editable source over generated views.
Preserve original wording for laws, contracts, policies, and approved decisions;
record interpretation separately.

Surface conflicting sources instead of silently selecting one. If source
currency, authority, or applicability cannot be verified, mark the affected
requirements provisional. Do not claim legal, compliance, security, or
contractual certainty beyond the source.

When recovering requirements from an existing system, inspect public behavior,
tests, schemas, validation, authorization, state transitions, configuration,
migrations, and history. Classify findings as documented intent, executable
contract, enforced behavior, observed surface, or inference. Do not turn dead
code, defects, disabled experiments, or compatibility shims into intended
requirements merely because they exist.

## WorkBuddy workflow

1. Inventory the input, source classes, terminology, prior decisions, and current
   system evidence.
2. Frame the problem as actor, situation, desired outcome, and current obstacle,
   without naming a technical design.
3. Confirm decisive assumptions that materially affect scope or an expensive,
   hard-to-reverse commitment. Do not re-ask facts already established.
4. Explore adjacent actors, before/after workflows, obligations, variants,
   reused data, operational layers, and explicit non-goals.
5. Draft atomic requirement candidates with stable readable IDs.
6. Give each candidate two to four observable completion conditions and link it
   to the supporting source or evidence.
7. Assign basis, priority, validation decision, and confidence independently.
   A high priority does not make weak evidence strong.
8. Record consequential choices, alternatives, owner, date, superseded items,
   revisit trigger, and unresolved questions.
9. Identify downstream outcome hypotheses separately when they could change the
   decision to build, retain, expand, simplify, or stop the capability.

## Requirement shape

```text
Requirement: <stable-readable-id>
Actor: <one actor>
Must be able to: <one solution-free capability or outcome>
So that: <purpose, only when it adds information>
Complete when:
- <observable condition>
- <observable condition>
Basis: authoritative | interpreted | evidenced | hypothesized
Source or evidence: <direct reference>
Priority: must | should | could | won't-now
Validation decision: accept | test | watch | reject
Confidence: low | medium | high
```

Do not invent metrics to make a non-functional requirement look measurable.
Record an unknown baseline or threshold and the measurement or decision owner
needed to establish it.

## Output

Lead with a compact decision record:

```text
Subject: <problem scope or requirement set>
Decision: GROUNDED | PROVISIONAL | NOT-GROUNDED
Problem: <actor / situation / outcome / obstacle>
Basis profile: <source-class mix>
Confidence: low | medium | high
Blocking gaps: <missing source, actor, evidence, or completion condition>
Next action: <confirm, source, split, test, or reject>
Verification: <sources and decisions checked>
Revisit when: <required for provisional work>
```

Then include only the additional requirement table, assumptions, conflicts,
scope placements, outcome hypotheses, and decision log needed for the current
decision. For recovery work, clearly separate observed behavior from confirmed
intent and provide a confirmation queue.

## Guardrails

- Do not convert stakeholder requests directly into implementation commitments.
- Do not make an authoritative source say more than it says.
- Do not bury unresolved decisions in polished prose.
- Do not use priority as a proxy for certainty.
- Do not put downstream impact metrics inside completion conditions.
- Do not expose confidential contracts, customer data, personal information, or
  credentials in the output.
- Do not edit the canonical requirements source or notify stakeholders unless
  that state change is within the user's requested and authorized scope.

Finish by naming what is grounded, what remains provisional, and the next
decision needed. A long document is not evidence that requirements are ready.
