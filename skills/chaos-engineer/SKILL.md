---
name: "chaos-engineer"
display_name: "混沌工程与韧性演练"
display_name_en: "Chaos Engineer"
description: "Use when designing or running authorized resilience experiments, failure-injection tests, or game days for distributed systems. Requires a written hypothesis, verified steady state, bounded blast radius, and tested rollback."
description_zh: "用于设计或执行经授权的分布式系统韧性实验、故障注入测试或故障演练；必须先有书面假设、已验证基线、受控影响范围和经过测试的回滚。"
description_en: "Map dependencies and failure modes, define measurable steady state and abort thresholds, run one bounded fault at a time in an approved environment, collect evidence, restore service, and turn findings into tracked improvements."
category: "development"
version: "0.1.0"
author: "Jeffallan/claude-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with repository and observability access, an explicitly authorized disposable or canary environment, a tested rollback path, and an approved experiment window"
---

# Chaos Engineer

## Mission and hard boundary

Use controlled experiments to test whether a system withstands realistic failures. This Skill is not permission to break production: never inject faults, terminate workloads, alter traffic, or consume load-test capacity without an explicit scope, owner, window, abort authority, and recovery plan.

Default to a disposable environment or isolated canary. Production experiments require separate written approval, customer-impact safeguards, a narrow target, and an operator who can abort immediately.

## Required experiment contract

Before any change, write an experiment record containing:

- target service, dependency, environment, owner, operator, start/end window, and authorization reference;
- one falsifiable hypothesis and the steady-state metrics that define “healthy”;
- one failure variable, target selector, maximum duration, maximum affected percentage, and explicit exclusions;
- expected user and business impact, telemetry sources, abort thresholds, and automatic/manual rollback steps;
- preflight evidence, communication and escalation path, cleanup owner, and post-experiment review deadline.

If any field is unknown, do not execute. Convert the gap into a read-only discovery task or a proposed experiment for approval.

## Safety invariants

1. **Baseline first:** verify normal traffic, latency, error rate, saturation, dependency health, and alert delivery before injection.
2. **Smallest blast radius:** start with one instance, pod, zone, tenant, or synthetic request; expand only after evidence supports it.
3. **One variable at a time:** isolate the fault type and avoid overlapping deploys, migrations, load tests, or unrelated incidents.
4. **Fast abort:** the abort path must be executable, observable, and tested before the experiment; automated rollback should normally begin within 30 seconds of a threshold breach.
5. **No secret or payload capture:** minimize logs and traces, redact identifiers, and use synthetic data where possible.
6. **Stop on uncertainty:** abort on unexpected scope, missing telemetry, loss of rollback control, or any safety threshold breach.
7. **Close the loop:** restore normal state, prove recovery, record what was learned, and track at least one remediation or explicitly justified no-change decision.

## Workflow

### 1. Map the system

Read architecture and deployment facts. Identify critical user journeys, synchronous and asynchronous dependencies, queues, caches, load balancers, identity boundaries, retry behavior, circuit breakers, rate limits, single points of failure, and recovery objectives. Mark assumptions and unknowns rather than inventing topology.

### 2. Define and review the hypothesis

Express the expected behavior in measurable terms, for example: “If one canary instance is unavailable for 60 seconds, the remaining capacity keeps p99 checkout latency below the agreed threshold and error budget.” Define the steady state before the fault, the expected degradation, and the exact evidence that would falsify the hypothesis.

### 3. Preflight

- confirm authorization and the experiment window;
- validate selectors and exclusions with a dry run;
- verify dashboards, alerts, logs, traces, and time synchronization;
- test rollback in the same environment and record the command/result;
- check capacity headroom, backups, rate limits, and concurrent changes;
- notify the owner, on-call, and observers with the abort procedure.

### 4. Execute conservatively

Start the smallest approved fault. Timestamp every phase. Observe service-level indicators, dependency behavior, queue depth, retries, saturation, customer signals, and recovery progress. Do not increase scope merely because the first observation is quiet; require the contract’s next checkpoint.

### 5. Abort, restore, and verify

Abort immediately when a threshold or invariant is breached. Remove the fault using the tested path, confirm workloads and traffic have returned to the intended state, and rerun the original steady-state checks from the affected path. Escalate if restoration is incomplete; do not hide evidence by restarting blindly.

### 6. Learn and improve

Produce a blameless summary with hypothesis verdict, timeline, observed impact, telemetry links, unexpected behavior, recovery evidence, residual risk, and concrete owners/dates. Feed fixes into tests, alerts, capacity plans, runbooks, architecture, or the next smallest experiment.

## Safe planning examples

Use dry-run and staging/canary placeholders until authorization and selectors are verified:

```bash
# Inspect only; replace placeholders after the experiment contract is approved.
kubectl get deploy "$TARGET" -n "$NAMESPACE" --show-labels
kubectl top pods -n "$NAMESPACE" -l "$SELECTOR"
kubectl diff --server-side --filename "$MANIFEST"  # review; do not apply yet

# Record a rollback command and test it in the same disposable environment.
kubectl rollout status deployment/"$TARGET" -n "$NAMESPACE" --timeout=60s
```

For a network fault, prefer an isolated proxy or synthetic dependency in a disposable environment. For a workload fault, target one canary replica and enforce an admission/policy guard that rejects selectors outside the approved scope. Never paste production credentials or disable TLS verification to make an experiment pass.

## Experiment report template

```text
Experiment: <short id>
Authorization/window/owner: <reference / UTC interval / owner>
Hypothesis: <falsifiable statement>
Environment and target: <exact scope and exclusions>
Steady state: <metrics, thresholds, baseline evidence>
Fault and maximum duration: <single variable>
Abort thresholds and rollback: <commands/owner/observed result>
Timeline and evidence: <timestamps, dashboards, logs, traces>
Verdict: confirmed | falsified | inconclusive | aborted
Recovery proof: <original checks rerun from affected path>
Follow-ups: <owner, due date, risk if deferred>
```

## Handoff checklist

- [ ] Authorization, scope, exclusions, and abort authority are recorded.
- [ ] Hypothesis, baseline, thresholds, and one fault variable are measurable.
- [ ] Telemetry and rollback were tested before injection.
- [ ] The experiment ran in the approved window and stopped at its boundary.
- [ ] Blast radius and sensitive data stayed within contract.
- [ ] Normal state and original user path were verified after cleanup.
- [ ] Findings, residual risk, and owned improvements were documented.
