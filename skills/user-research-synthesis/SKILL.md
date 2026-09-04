---
name: "user-research-synthesis"
display_name: "用户研究综合"
display_name_en: "User Research Synthesis"
description: "Use when combining interviews, support tickets, surveys, usability studies, feedback, or behavioral data into traceable user insights; preserve source context, contradictions, segment differences, and uncertainty instead of merely summarizing notes."
description_zh: "将访谈、工单、调查、可用性测试和行为数据综合为可追溯的洞察、矛盾信号、研究缺口与行动建议。"
description_en: "Synthesize interviews, tickets, surveys, usability tests, and behavioral data into traceable insights, conflicting signals, research gaps, and actions."
category: "research"
version: "0.1.0"
author: "itseffi; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# User Research Synthesis

Use this skill to turn fragmented research into decision-ready insights. Synthesis is not note compression: preserve who said or did what, in which context, and how strongly the evidence supports a conclusion.

## Establish the evidence base

Inventory each source with its method, date, sample size, participant segment, recruitment criteria, product/version context, and relevant question. Include interviews, observations, support cases, surveys, usability sessions, analytics, sales feedback, and prior studies only when they bear on the decision.

Assess recency, coverage, independence, missing segments, selection bias, survivorship bias, leading questions, instrumentation gaps, and whether stated preference conflicts with observed behavior. Protect participant privacy: minimize personal data, use stable anonymous identifiers, redact sensitive quotes, and honor consent and retention constraints.

Treat stakeholder anecdotes as evidence with limited scope, not as representative user findings. Do not invent quotes, participant counts, percentages, or statistical significance.

## Code observations before drawing conclusions

- Extract atomic observations with a source identifier and relevant context.
- Separate direct quotes, observed behavior, reported behavior, analytics, researcher interpretation, and hypotheses.
- Code consistently across sources; retain negative cases and evidence that challenges an emerging theme.
- Normalize duplicated records so repetition across copies is not mistaken for independent support.
- Segment only on meaningful differences supported by the data; do not create personas from stereotypes or tiny samples.

## Form traceable insights

An insight should explain a recurring need, motivation, barrier, behavior, or decision pattern—not merely restate a feature request. For each insight, report:

| Field | Required content |
|---|---|
| Insight | One specific, decision-relevant statement |
| Evidence | Source IDs, context, and representative redacted excerpts or measures |
| Coverage | Supporting and contradicting sources and affected segments |
| Confidence | High, medium, or low with rationale based on quality, triangulation, and sample limits |
| Implication | What this changes for the current decision, without presenting speculation as a requirement |
| Validation | The signal or next study that would confirm or disconfirm it |

Map insights to the research questions, user jobs or needs, and business outcomes only when the connection is supported. Keep user need, proposed solution, and expected business effect distinct.

## Reconcile conflicting signals

Surface contradictions rather than averaging them away. Test explanations such as segment, task, lifecycle stage, environment, timing, question framing, or stated-versus-observed behavior. State what evidence would distinguish the explanations. If the current decision cannot wait, recommend the most reversible path and name the residual uncertainty.

## Prioritize responsibly

Rank findings using transparent criteria such as evidence strength, user impact, frequency, severity, strategic relevance, and decision urgency. Frequency alone does not determine importance, and a severe accessibility, safety, or trust issue may matter despite a small observed sample.

End with:

- high-confidence findings and their supported implications;
- material conflicting signals;
- assumptions confirmed, contradicted, or still untested;
- research gaps prioritized by the decisions they block;
- concrete next research or product actions with owners and validation measures.

Do not contact participants, publish research, change a roadmap, or update external systems unless the current request authorizes those actions. Make the handoff auditable: a reviewer must be able to trace every material conclusion back to controlled source evidence.
