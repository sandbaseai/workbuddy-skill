---
name: "prioritization-matrix"
display_name: "优先级矩阵"
display_name_en: "Prioritization Matrix"
description: "Impact vs Effort scoring, MoSCoW prioritization, stakeholder alignment."
description_zh: "使用影响/投入、MoSCoW 或加权评分对事项进行透明排序，并展示证据、置信度、依赖关系和敏感性。"
description_en: "Prioritize items transparently with impact/effort, MoSCoW, or weighted scoring while exposing evidence, confidence, dependencies, and sensitivity."
category: "business"
version: "0.1.0"
author: "Istara Contributors; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Prioritization Matrix

Rank features, initiatives, risks, tasks, or investments with a transparent
model that supports a decision. Use this Skill when scarce time, budget, people,
or capacity forces tradeoffs. Do not use a score to disguise an already-made
political decision.

## Frame the decision

Record the objective, decision owner, candidates, time horizon, constraints,
available capacity, and consequences of delay. Separate mandatory obligations
and prerequisites from discretionary items before scoring.

Define what each candidate includes at a comparable level of scope. Split or
normalize items that bundle materially different outcomes, costs, or owners.

## Choose the lightest valid framework

- **Impact / effort:** useful for a fast visual comparison when estimates are
  coarse and reach is similar.
- **MoSCoW:** useful for negotiating a fixed release or scope boundary; define
  what "must" means before classifying.
- **RICE:** useful when reach, impact, confidence, and effort can be estimated on
  comparable scales.
- **Weighted scoring:** useful when several explicit criteria matter and the
  decision owner can defend their weights.

Do not mix frameworks or scales in one ranking without an explicit conversion.
If the available evidence cannot support numeric precision, use ordinal bands
and explain them rather than inventing decimals.

## WorkBuddy workflow

1. Define each criterion, direction, unit, scale, and weight before scoring the
   candidates. Make sure higher always means better or normalize the direction.
2. Link every input to a source, measurement, stakeholder estimate, or clearly
   labeled assumption. Record confidence independently from expected value.
3. Score all candidates consistently. Treat zero, unknown, not applicable, and
   missing as distinct states.
4. Account for dependencies, sequencing, shared enablers, indivisible work,
   regulatory or safety obligations, and capacity by role. A prerequisite may
   need to precede a higher-scoring dependent item.
5. Calculate the ranking with visible formulas and units. Keep enough precision
   to reproduce the result, but round the displayed score to avoid false
   certainty.
6. Run sensitivity checks on uncertain inputs and weights. Identify candidates
   whose rank changes under plausible assumptions.
7. Compare the result with strategic fit, portfolio balance, concentration risk,
   and irreversible downside. Document any override with an owner and rationale.

Do not double-count the same benefit under several criteria. Do not treat sunk
cost as future value, confidence as impact, or urgency as importance unless the
chosen model explicitly defines it.

## Output

Start with the recommendation and framework rationale, then provide:

| Rank | Candidate | Score or band | Evidence | Confidence | Effort/cost | Dependencies | Sensitivity |
|---:|---|---:|---|---|---|---|---|

Include the criterion definitions, weights, formulas, source dates, capacity
assumptions, mandatory items handled outside the score, and what is deferred or
excluded. Show ties and unstable rankings rather than forcing an order.

End with the smallest evidence-gathering step that could change the decision.
When a spreadsheet or script performs the calculation, preserve the formulas
and verify totals independently.

## Boundaries

Prioritization is decision support, not an objective truth or an authorization
to spend, publish, delete, hire, contact people, or change a roadmap. Protect
confidential financial, personnel, customer, and strategy data. Do not infer
stakeholder agreement from a numeric ranking, and do not replace legal, safety,
or contractual obligations with a low score.
