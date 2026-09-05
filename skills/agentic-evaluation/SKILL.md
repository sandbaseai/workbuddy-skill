---
name: "agentic-evaluation"
display_name: "Agent 评测与迭代"
display_name_en: "Agentic Evaluation"
description: "Use when measuring or improving an Agent's output with explicit criteria, reflection, evaluator-optimizer loops, rubric or judge comparisons, code-test refinement, and bounded convergence checks."
description_zh: "用于用明确标准评测和改进 Agent 输出，包括反思循环、评测器-优化器、量规或裁判比较、代码测试迭代和有界收敛检查。"
description_en: "Define an evidence-backed evaluation contract, score outputs with structured results, refine only failed dimensions, and stop with honest quality and uncertainty reporting."
category: "productivity"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with access to the task output and evaluation evidence; any model judge, test runner, external dataset, or production replay requires separate authorization"
---

# Agentic Evaluation

## Purpose and boundary

Evaluate and improve Agent outputs through a bounded, evidence-based loop:

```text
Generate → Evaluate → Critique → Refine → Verify
```

This is an evaluation workflow, not permission to run arbitrary tools, expose private data, or
accept a model's self-rating as proof. Prefer deterministic checks and independent evaluators
when available. Keep prompts, outputs, traces, and test data within the authorized audience;
redact secrets and personal data before storing or sending them to a judge.

## Evaluation contract

Define before generating or judging:

- **task and expected outcome:** what the output must accomplish and what counts as failure;
- **dimensions and weights:** accuracy, completeness, safety, clarity, format, latency, cost, or other relevant measures;
- **evidence source:** deterministic test, reference answer, human review, retrieval citation, judge, or a combination;
- **threshold and stop rule:** minimum acceptable score, maximum iterations, time/cost budget, and what happens when evidence conflicts;
- **scope and permissions:** models, tools, datasets, environments, retention, and who may approve a release;
- **report contract:** scores, failed dimensions, trajectory, uncertainty, limitations, and follow-up owner.

Separate observed test results from judge interpretation and from the final decision. A score is
not evidence of correctness unless its measurement method and coverage are stated.

## Step 1: establish a baseline

Capture the task version, model/provider/version, prompts or configuration identifiers, input
fixture, output, timestamp, and available cost/latency signals. Use a representative but safe
fixture: synthetic or redacted data by default, fixed seeds where supported, and a versioned
evaluation set for regression work. Do not silently replace a missing reference with a model
guess; label it as unavailable.

For code, run repository-native tests, linters, type checks, or a narrow executable contract
before asking a language model to judge style. For documents or analysis, check citations,
required fields, arithmetic, and policy constraints deterministically first.

## Step 2: choose the evaluation pattern

### Reflection

Use one Agent to critique its output against a small structured rubric, then revise only failed
dimensions. Require machine-readable results such as one object per criterion with `status`,
`score`, `evidence`, and `feedback`; reject malformed or unsupported claims instead of guessing.

### Evaluator-optimizer

Separate generation, evaluation, and optimization responsibilities when quality matters. Pass
the evaluator's structured findings to the optimizer, preserve the original output, and record
each attempt. Independent prompts, models, or deterministic checks reduce correlated mistakes.

### Code-test refinement

Generate or modify code only in an isolated, authorized workspace. Run the smallest relevant
tests, feed the exact failure evidence to the next iteration, and inspect the diff. A passing
test suite proves only the exercised contracts; it does not prove security, performance, or
uncovered behavior.

### Pairwise or rubric judging

For two candidates, freeze the criteria and order where practical to reduce position bias. For
rubrics, define anchors for each score and weight before seeing outputs. Ask for evidence and
uncertainty, not just a winner. Human review is required for high-impact, ambiguous, or safety-
critical decisions.

## Step 3: run a bounded loop

1. Generate a baseline and preserve it.
2. Apply deterministic checks and the declared evaluator.
3. Record per-dimension score, evidence, confidence, cost, latency, and failure reason.
4. Refine only when the feedback identifies an actionable gap.
5. Re-run the same checks on the new output; do not change the rubric mid-run.
6. Stop when the threshold is met, the maximum iteration/budget is reached, or the score fails to improve.

Use a default maximum of three iterations unless the contract justifies another limit. Detect
non-convergence: if the total score stalls or oscillates, preserve the best candidate and report
the unresolved dimensions rather than looping. Never lower a threshold merely to declare success.

## Evidence record

```text
Evaluation: <id and purpose>
Task/input revision: <immutable fixture or safe reference>
Generator/evaluator: <model, version, prompt/config identifiers>
Rubric: <dimensions, weights, score anchors, threshold>
Baseline: <output, deterministic results, cost/latency>
Attempts: <per-attempt output hash, findings, score, evidence, confidence>
Decision: pass | fail | inconclusive | human-review
Stopping reason: <threshold, limit, budget, or non-convergence>
Coverage/limitations: <untested paths, judge bias, missing references>
Privacy/permissions: <data class, audience, retention, approvals>
Follow-up: <owner, regression fixture, next review trigger>
```

## Safety and quality gates

- Do not send secrets, credentials, private prompts, customer data, or unrestricted traces to a judge.
- Bound model calls, retries, concurrency, token usage, runtime, network access, and spend.
- Treat evaluator outputs as untrusted data; validate schema, ranges, criterion names, and evidence references.
- Keep a reproducible history, but store hashes or redacted excerpts when full content is unnecessary.
- Calibrate model judges against human labels or deterministic references before using scores as gates.
- Report disagreement, missing evidence, distribution shifts, flaky checks, and known blind spots.
- Require explicit human approval before high-impact external actions or production rollout.

## WorkBuddy handoff

Return the evaluation contract, baseline and best output, per-dimension results, exact evidence,
iteration and budget usage, stopping reason, confidence, coverage gaps, privacy boundaries, and
the next regression or human-review action. If no reliable evaluator or reference exists, return
`inconclusive` rather than presenting a self-consistent answer as verified.
