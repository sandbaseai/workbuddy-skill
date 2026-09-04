---
name: agent-evaluation-engineering
display_name: AI Agent Evaluation Engineering
display_name_zh: AI Agent 评估工程
description: Design reproducible evaluations for agent capabilities, trust, safety, trajectories, regressions, latency, and cost.
description_en: Design reproducible evaluations for agent capabilities, trust, safety, trajectories, regressions, latency, and cost.
description_zh: 为 Agent 的能力、可信安全、执行轨迹、回归、延迟与成本设计可复现评估。
category: research
version: 0.1.0
author: Microsoft Corporation; adapted for WorkBuddy by SandBase AI
license: MIT
compatibility: WorkBuddy and tool-capable agent runtimes
---

# AI Agent Evaluation Engineering

Use this skill when creating or reviewing an evaluation suite for an AI agent. Treat an evaluation as an executable product contract, not a collection of impressive demos.

## 1. Define the contract and risk

Write down the user goal, allowed inputs, observable outputs, available tools, permissions, side effects, latency and cost limits, and acceptable escalation behavior. Rank failure modes by impact and likelihood. Keep capability quality separate from trust and safety: an agent can complete a task and still leak data, exceed authority, or make an irreversible change.

## 2. Build representative cases

Create cases from real user journeys, production failures, domain edge cases, ambiguous requests, missing context, tool outages, permission boundaries, prompt injection, and unsafe requests. Include single-turn and multi-turn cases where memory, correction, or recovery matters.

Partition cases into:

- development examples for rapid iteration;
- a held-out regression set that prompts and graders do not see during tuning;
- adversarial cases focused on authority, privacy, injection, and irreversible effects.

Turn every confirmed production failure into a minimized regression case. Remove duplicates and document why each case exists.

## 3. Specify evidence and graders

For each case, define the expected invariant before running it. Prefer observable evidence:

- final answer facts and citations;
- tool names, arguments, results, ordering, retries, and errors;
- created or modified artifacts and their diffs;
- whether approval, refusal, or escalation happened at the right boundary;
- elapsed time, token use, external calls, and estimated cost.

Do not require hidden chain-of-thought. Evaluate outcomes and observable trajectories instead.

Use deterministic checks for schemas, exact values, permissions, forbidden actions, and file or database state. Use rubric-based human or model graders for relevance, completeness, groundedness, and communication quality. Calibrate model graders against blinded human labels, report agreement and false-positive/negative patterns, and periodically recheck drift. Never let a single uncalibrated model judge be the only release gate.

## 4. Run controlled comparisons

Freeze the agent version, model and parameters, tool versions, fixtures, seed where supported, environment, and evaluator versions. Compare a candidate with a baseline on identical cases. Repeat stochastic cases enough times to expose variance.

Record paired case outcomes rather than relying only on aggregate averages. Report pass rate by capability and risk class, severe-failure count, latency and cost distributions, and confidence intervals or run-to-run variance where useful. A gain in average quality does not excuse a new severe safety failure.

## 5. Exercise failures and recovery

Inject bounded failures such as timeouts, malformed tool responses, partial writes, stale data, unavailable dependencies, duplicate delivery, and permission denial. Verify that the agent:

- respects deadlines and retry limits;
- does not duplicate irreversible side effects;
- distinguishes confirmed success, confirmed failure, and unknown outcome;
- preserves user data and authority boundaries;
- gives a truthful, actionable recovery or escalation path.

## 6. Diagnose the earliest broken contract

When a case fails, find the earliest observable divergence:

1. input interpretation or missing clarification;
2. plan and tool selection;
3. tool arguments or permission checks;
4. environment or tool response;
5. state reconciliation and recovery;
6. final answer grounding and communication;
7. grader error or ambiguous rubric.

Attach the trace and evidence to the case. Fix the earliest cause, then rerun the affected slice and the full gate. Do not tune against a vague score alone.

## 7. Operationalize the suite

Classify tests as:

- **gate:** small, deterministic, high-severity checks required on every change;
- **regression:** broader representative suites run on releases or schedules;
- **exploratory:** experiments that inform decisions but do not block delivery.

Version datasets, rubrics, graders, fixtures, and results. Define owners, failure budgets, quarantine rules for flaky infrastructure, and an expiry date for every waiver. Publish enough provenance to reproduce a result without exposing secrets or private user data.

## Deliverable

Produce a compact evaluation report containing the contract, risk taxonomy, dataset partitions, grader definitions and calibration evidence, pinned environment, baseline-versus-candidate results, severe failures, latency and cost, known limitations, and a release recommendation. State uncertainty plainly.
