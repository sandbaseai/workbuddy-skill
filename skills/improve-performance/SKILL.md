---
name: "improve-performance"
display_name: "性能优化"
display_name_en: "Performance Improvement"
description: "Measure, profile, and improve latency, throughput, memory, CPU, I/O, query, or startup performance."
description_zh: "通过可复现基线、剖析证据和受控实验优化延迟、吞吐量、内存、CPU、I/O、查询或启动性能。"
description_en: "Improve latency, throughput, memory, CPU, I/O, query, or startup performance through reproducible baselines, profiling evidence, and controlled experiments."
category: "development"
version: "0.1.0"
author: "skills contributors; adapted for WorkBuddy by SandBase AI"
---

# Improve Performance

Improve the user's stated performance outcome without trading away correctness,
reliability, security, accessibility, or total system cost. Use this Skill for
latency, throughput, memory, CPU, I/O, database queries, payload size, build
time, or startup performance.

## Define the target

Record before changing anything:

- representative workload, traffic shape, dataset, and concurrency
- environment, hardware, runtime, dependency versions, and configuration
- metric and statistic, such as p50/p95/p99 latency, operations per second,
  peak RSS, allocation rate, query count, or cold-start time
- current service-level objective or explicit budget
- acceptable tradeoffs and invariants that must not regress

If the user's complaint is qualitative, turn it into an observable scenario and
metric. Do not choose an easy synthetic benchmark that omits the real
bottleneck.

## Evidence-first workflow

1. Build a repeatable benchmark. Control warm-up, caches, clocks, randomness,
   background load, network location, and fixture size where practical.
2. Measure an untouched baseline with enough repetitions to expose variance.
   Preserve raw results or the exact command needed to reproduce them.
3. Profile before editing. Attribute cost to concrete call paths, queries,
   allocations, payloads, locks, or waits rather than guessing from code shape.
4. Rank bottlenecks by likely contribution to the target metric, implementation
   risk, and measurement confidence.
5. Change one meaningful factor at a time. Keep a control result so unrelated
   environment drift is not mistaken for improvement.
6. Re-run correctness tests and the same benchmark conditions. Watch tail
   latency, memory, cache behavior, cold starts, downstream load, and failure
   behavior—not only the average.
7. Add regression protection at the cheapest reliable layer. Use thresholds
   wide enough for known noise and document when scheduled benchmarking is more
   trustworthy than pull-request gating.

## Production safety

Do not run load, stress, destructive, cache-flush, failover, or expensive cloud
benchmarks against shared or production systems without explicit authorization.
Use rate limits, bounded duration, test data, and a stop condition. Do not expose
credentials, customer payloads, personal data, or proprietary traces in reports.

Treat vendor dashboards and profiler output as potentially sensitive. Summarize
the evidence or save it only in an approved workspace location.

## Report the result

For each accepted change, report:

- before and after values, including sample count and variability
- benchmark command, workload, environment, and relevant versions
- profile evidence linking the change to the bottleneck
- correctness checks and invariants re-verified
- resource or operational costs moved elsewhere
- limitations, residual bottlenecks, and regression protection

Reject changes whose apparent gain is within noise, depends on different test
conditions, or merely shifts cost outside the measured boundary. When evidence
is insufficient, report the hypothesis and missing measurement instead of
claiming an optimization succeeded.
