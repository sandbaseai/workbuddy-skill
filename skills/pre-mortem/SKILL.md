---
name: "pre-mortem"
display_name: "项目事前验尸"
display_name_en: "Project Pre-mortem"
description: "Use before a consequential project, launch, migration, or decision to assume it failed, expose plausible causes and warning signals, and convert them into owned mitigations without replacing an existing risk process."
description_zh: "在重大项目或决策执行前假设其已经失败，用证据约束的情景分析识别风险、预警信号和可执行的缓解措施。"
description_en: "Assume a consequential project or decision has failed, then use evidence-constrained scenarios to identify risks, warning signals, and actionable mitigations before execution."
category: "business"
version: "0.1.0"
author: "charly-vibes; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Project Pre-mortem

Run a pre-mortem before commitment or at a meaningful decision gate. It complements—not replaces—the project's risk register, security review, compliance process, or go/no-go authority.

## Ground the exercise

Capture the decision or project, intended outcome, time horizon, committed constraints, current plan, owners, dependencies, success measures, and known evidence. Label assumptions and unknowns explicitly. If the source material is incomplete, do not silently invent details; state the gaps and continue with bounded hypotheses.

Choose a concrete failure outcome tied to the user's objective, such as missed adoption, unsafe migration, material customer harm, budget exhaustion, or an unrecoverable operational event. Do not default to sensational security or financial claims without a plausible path.

## Assume failure and reconstruct it

Write a short future narrative in which the project has failed. Work backward from the outcome to decisions, assumptions, handoffs, dependencies, incentives, and operating conditions present today.

Generate risks across relevant lenses rather than repeating one theme:

- customer value and adoption;
- delivery scope, schedule, staffing, and decision latency;
- technical feasibility, integration, data, security, privacy, and reliability;
- operational readiness, support, observability, and recovery;
- legal, compliance, commercial, supplier, and reputational exposure.

Keep only plausible, decision-relevant risks. Separate root conditions from triggers and downstream effects. Avoid blaming individuals; examine systems, incentives, missing controls, and ambiguous ownership.

## Prioritize and act

For each leading risk, record:

| Field | Required content |
|---|---|
| Failure path | Cause → trigger → observable impact |
| Evidence | Facts supporting it; assumptions and confidence kept separate |
| Likelihood / impact | Project-defined scale with a short rationale |
| Earliest warning | A measurable signal, threshold, and observation point |
| Prevention | A concrete change that lowers likelihood or impact |
| Contingency | A response if the warning signal fires |
| Owner / timing | One accountable owner and a decision or completion date |
| Residual risk | What remains after mitigation and who accepts it |

Favor mitigations that change the plan, add a control, reduce blast radius, stage exposure, validate a risky assumption, or create a recovery path. “Monitor closely,” “communicate better,” and “be careful” are not actions unless paired with an owner, trigger, and observable response.

## Challenge and conclude

- Check for availability bias, duplicate risks, false precision, and risks that are merely restated goals.
- Include disconfirming evidence and explain why a high-severity but low-likelihood scenario was retained or dropped.
- Identify any mitigation that introduces a new risk, dependency, cost, or delay.
- Name the top three actions that materially change the risk profile, plus unresolved decisions requiring an authorized owner.

Do not execute mitigations, change scope, contact stakeholders, or update external systems unless the current request authorizes those actions. End with a dated review trigger so the analysis is refreshed when assumptions, scope, evidence, or exposure change.
