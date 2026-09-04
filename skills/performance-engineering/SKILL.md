---
name: "performance-engineering"
display_name: "性能工程"
display_name_en: "Performance Engineering"
description: "Use when validating capacity, diagnosing latency or resource bottlenecks, profiling CPU/memory/I/O, optimizing responsiveness, or preventing performance regressions; establish a comparable baseline before changing code or infrastructure."
description_zh: "用于验证容量、诊断延迟或资源瓶颈、分析 CPU/内存/I/O、优化响应性或防止性能回归，并在修改代码或基础设施前建立可比较基线。"
description_en: "Engineer performance with representative workloads, controlled load/stress/soak/spike tests, profiling, budgets, bottleneck evidence, safe optimization, and statistically credible regression gates."
category: "development"
version: "0.1.0"
author: "majiayu000; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Application telemetry, representative test data, isolated load environment, profiler, and deployment baseline"
---

# Performance Engineering

Use this skill to learn how a system behaves under realistic demand, identify the limiting resource, and improve user-visible performance without trading away correctness, reliability, security, or cost discipline. “It feels faster” is a hypothesis until a comparable measurement supports it.

Do not run load, stress, soak, spike, or profiling work against production without explicit authorization, a bounded workload, an abort threshold, and a recovery plan. Do not optimize a benchmark that does not represent the user journey or use a single percentile to hide failures.

## Define the performance contract

Record the user journey, endpoint/query/job, workload model, concurrency, arrival rate, payload distribution, cache state, dependency behavior, device/network class, region, build/configuration, and success criteria. Define budgets for latency, throughput, errors, freshness, memory, CPU, I/O, network, startup, battery, and cost as applicable.

Use a stable baseline:

- same code/configuration, data shape, environment, hardware class, and warm/cold state;
- enough repeated runs to describe noise, not only one lucky sample;
- p50/p95/p99, throughput, error/timeout rate, saturation, and resource breakdown;
- timestamped artifacts, tool/version, scenario, seed, and known confounders.

Compare like with like. Report effect size and uncertainty, not just a percentage. A regression gate must define the threshold, sample size, confidence approach, and exception owner.

## Choose the right test

- **Load:** expected traffic and normal operating behavior;
- **Stress:** capacity limit, failure mode, and recovery boundary;
- **Soak:** leaks, fragmentation, pool exhaustion, drift, and long-run degradation;
- **Spike:** abrupt demand, autoscaling, rate limits, queues, and graceful degradation.

Start with a small, isolated smoke scenario, then ramp using an explicit schedule. Keep test data synthetic or redacted, prevent external side effects, and verify cleanup. Monitor the system under test and dependencies for latency, errors, saturation, queue depth, retries, cache behavior, database locks, connection pools, autoscaling, cost, and user-impact signals.

## Diagnose before optimizing

1. Confirm the symptom and affected journey; check data freshness, deploys, traffic mix, and instrumentation health.
2. Localize the bottleneck across CPU, memory, garbage collection, disk/I/O, network, locks, database plans, queues, remote dependencies, serialization, rendering, or contention.
3. Capture a bounded profile or trace with symbols and safe sampling. Avoid collecting secrets or unnecessary personal data.
4. Form one causal hypothesis and change one meaningful variable at a time.
5. Re-run the same scenario and compare tail latency, throughput, errors, resource use, and cost.
6. Test correctness, concurrency, failure behavior, cache invalidation, security limits, and rollback—not only the fast path.

Profiling is evidence gathering, not an optimization plan. A high CPU number may be expected saturation; low CPU with high latency may indicate I/O, locks, queueing, or a dependency. Trace across boundaries before assigning blame.

## Common optimization levers

Choose based on measured bottlenecks:

- **Queries:** inspect plans and cardinality, fix N+1 access, add or adjust indexes with write/storage cost, paginate, bound result sets, and validate isolation.
- **Caching:** define key scope, freshness, invalidation, stampede control, memory limit, and degraded behavior; never cross tenants or cache authorization decisions unsafely.
- **APIs:** use bounded payloads, cursor pagination, compression where useful, batching, cancellation, timeouts, backpressure, and idempotent retries.
- **Concurrency:** bound workers, queues, connections, and fan-out; avoid unbounded parallelism and retry storms.
- **Frontend:** prioritize critical rendering, stable layout, responsive images, code splitting, cache headers, accessible interaction, and measured Core Web Vitals.
- **Runtime:** reduce allocations and copies, tune garbage collection only from profiles, and verify startup/background work and battery impact on the target device.

Every change includes its expected trade-off, owner, rollout, observability, rollback, and expiry/review condition. Do not add infrastructure or cache layers to conceal a data-contract or algorithmic problem.

## Capacity and failure boundaries

Model throughput, concurrency, saturation, dependency quotas, storage, cost, and growth drivers. Identify the knee of the curve and the first failing invariant. Test overload behavior: admission control, load shedding, queue limits, graceful degradation, stale reads, timeouts, circuit breakers, and recovery after demand returns to normal.

Validate autoscaling from observed signals and startup time. Verify that scaling does not amplify a hot key, database limit, vendor quota, or cost spike. Define capacity headroom, alert thresholds, and a review date; capacity estimates expire when workload shape changes.

## Safe CI and release gates

Keep fast deterministic microbenchmarks for local/CI feedback and isolated realistic scenarios for scheduled or pre-release validation. Control clock, randomness, network, data, cache, and background work. Track benchmark history and reject changes only when the difference exceeds noise and matters to a declared budget.

For a rollout, use a canary or staged cohort with latency, error, saturation, correctness, cost, and user-support guardrails. Stop expansion on unexplained tail regression, resource exhaustion, data divergence, privacy/security impact, or harmful battery behavior. Preserve traces, profiles, raw summaries, environment metadata, and the exact command/configuration used.

## Handoff

Report the journey and workload, baseline, test type and isolation, tool/version, measurements and uncertainty, bottleneck evidence, change, trade-offs, capacity boundary, budgets, guardrails, rollout/rollback, artifacts, unresolved risks, owner, and next authorized action. Stop when the workload is unrepresentative, measurement quality is uncertain, or test authority/safety is unclear.
