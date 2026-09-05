---
name: "debugging-methodology"
display_name: "系统化调试"
display_name_en: "Debugging Methodology"
description: "Use when investigating a software defect, intermittent failure, incorrect result, crash, or unexplained operational symptom."
description_zh: "用于调查软件缺陷、间歇性故障、错误结果、崩溃或无法解释的运行时症状。"
description_en: "Apply a disciplined reproduce-isolate-explain-fix-verify loop with evidence, controlled experiments, minimized cases, causal hypotheses, safe changes, and regression protection."
category: "development"
version: "0.1.0"
author: "Hermes Agent community; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Source code, logs or traces, reproducible environment, test runner, and authorized access to affected systems"
---

# Debugging Methodology

Use the lifecycle **REPRODUCE → ISOLATE → EXPLAIN → FIX → VERIFY**. Debugging is an evidence-gathering process, not a sequence of guesses. Preserve the original symptom and avoid changing several variables at once.

## Reproduce safely

Record the user-visible symptom, expected behavior, first known good version, first known bad version, environment, inputs, timing, frequency, and impact. Capture the exact command, request, fixture, configuration, dependency versions, seed, and relevant logs or traces while redacting secrets and personal data.

Prefer a local or staging reproduction with synthetic data. Do not replay destructive requests, probe production, disable security controls, or alter live data without explicit authorization, a bounded scope, and an abort plan. If the failure is intermittent, collect repeated observations and compare successful versus failing cases instead of declaring it unreproducible after one pass.

## Isolate the failure

1. Reduce the input, test, request, or workload to the smallest case that still fails.
2. Draw the execution path across callers, services, queues, storage, caches, external dependencies, and feature flags.
3. Bisect versions, configuration, data shape, concurrency, timing, and environment one dimension at a time.
4. Add temporary observation at boundaries: inputs, outputs, invariants, retries, timeouts, state transitions, and correlation IDs.
5. Use a control case and record what was held constant.

Separate symptom location from cause location. A timeout may originate in a lock, queue, dependency, or retry storm; an incorrect UI may originate in a stale cache or contract mismatch. Avoid logging sensitive payloads merely to gain visibility.

## Form and test a causal hypothesis

State the hypothesis, predicted observation, falsifying observation, confidence, and next smallest experiment. Check invariants before and after the suspected boundary. Prefer experiments that can distinguish competing causes: disable one flag in an isolated environment, replace one dependency with a deterministic stub, replay a minimal fixture, or compare one known-good commit.

Do not confuse correlation with causation. Consider stale artifacts, clock and timezone, randomness, ordering, concurrency, retries, resource exhaustion, deployment drift, schema versions, and observer effects. Treat a passing retry as evidence of nondeterminism, not proof that the defect disappeared.

## Fix the cause

Choose the smallest durable change that restores the violated invariant. Explain why it addresses the root cause and what trade-offs it introduces. Preserve validation, authorization, tenant isolation, idempotency, timeout, cancellation, and error semantics while fixing the happy path. Do not hide errors, broaden retries, weaken assertions, or increase limits without evidence and an operational budget.

Add a regression test at the narrowest useful layer, plus a boundary or integration test when the defect crosses components. Keep the minimized reproducer when it documents a non-obvious invariant. For performance or concurrency defects, use a representative workload and record baseline, variance, resource limits, and failure boundary.

## Verify and close

Run the reproducer before and after the fix, then run targeted and repository-native broader checks. Verify success, the original failure mode, neighboring error paths, old data and clients, rollback behavior, observability, and security controls. For an intermittent issue, define a sufficient observation window or repetition count and report residual uncertainty.

The handoff includes symptom and impact, reproduction steps, environment, evidence, minimized case, causal hypothesis and alternatives, root cause, fix, tests and commands, limitations, rollout/rollback, monitoring, owner, and next action. If no root cause is proven, report the strongest evidence and the investigation checkpoint rather than overstating certainty.

