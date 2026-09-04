---
name: "cache-engineering"
display_name: "缓存工程"
display_name_en: "Cache Engineering"
description: "Use when deciding, designing, reviewing, migrating, or diagnosing application, distributed, HTTP, or CDN caches; prove that caching removes measured work while preserving freshness, isolation, invalidation, and degraded behavior."
description_zh: "评估、设计、审查、迁移和诊断应用缓存、分布式缓存、HTTP 缓存与 CDN，并验证收益、新鲜度、隔离、失效和降级行为。"
description_en: "Evaluate, design, review, migrate, and diagnose application, distributed, HTTP, and CDN caches with evidence for value, freshness, isolation, invalidation, and degradation."
category: "development"
version: "0.1.0"
author: "Dankosik; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Cache Engineering

Use this skill for cache decisions and failures across request-local memoization, process caches, Redis or other distributed caches, HTTP caches, and CDNs. Preserve the application's source of truth, authorization model, availability target, and chosen infrastructure unless the user asks to change them.

A cache is a bounded copy, not a second authority. Every accepted design must define value semantics, complete key scope, freshness, fill ownership, invalidation, degraded behavior, observability, and a condition that would disprove its value.

## Establish scope and evidence

Identify the user-visible operation, authoritative data source, cache layers, principals and tenants, mutation paths, consistency limit, request deadline, origin capacity, target environment, and representative workload. Inspect existing code, configuration, metrics, and deployment topology before proposing a mechanism.

Measure a comparable baseline: end-to-end latency distribution, throughput and errors; origin request rate, concurrency, latency and limiting resource; and repeated work the proposed cache can actually remove. Do not subtract unrelated percentile values or call a percentile a maximum. If evidence is unavailable, return a bounded measurement plan rather than claiming an improvement.

For the full value test, read [references/value.md](references/value.md).

## Define the cached-value contract

Record:

- authority and revision or generation;
- positive, negative, and derived value meaning plus serializer version;
- every key dimension, including tenant, principal or policy, locale, representation, query semantics, and schema version when they affect output;
- fresh age, maximum safe age, and the origin timestamp from which age begins;
- fill owner, deadline, concurrency control, and publish condition;
- mutation ordering, invalidation delivery, reconciliation, and TTL backstop;
- safe behavior for timeout, partition, eviction, cold start, and dependency failure.

Equal keys must be interchangeable for the requesting principal. Keep secrets and personal data out of key text, logs, metrics labels, and diagnostic output. Prefer caching authority-independent data and applying current policy after retrieval when response variants cannot be invalidated reliably.

Read [references/contract.md](references/contract.md) when key scope, freshness, authorization, negative caching, or invalidation affects correctness.

## Control fills and degraded behavior

Choose the narrowest sharing boundary that removes the measured work. Each additional cache layer adds latency, partitions, eviction, cold-start, and operational surfaces and must remove a distinct cost.

Collapse only equivalent concurrent misses. Bound origin concurrency, queueing, waiter count, and fill duration. Caller cancellation should normally end that caller's wait, not cancel a shared fill needed by others. Publish only a result from the current authority generation; never convert a timeout or dependency error into a cached not-found result.

Budget cache access inside the request deadline. During outage or recovery, cap fallback demand within origin capacity. Serve stale only when its age and semantics are explicitly safe; otherwise bypass or fail closed according to the product contract. Treat broad flushes and synchronized expiry as load events.

Read [references/runtime.md](references/runtime.md) for hot keys, stampedes, layered caches, outages, and recovery.

## Change and migrate safely

Version incompatible key and serialization semantics. For rolling deployments, define old/new read and write behavior, mixed-version compatibility, namespace cleanup, cold-fill demand, canary ramp, bypass switch, rollback, and retirement of obsolete invalidators. A rollback must tolerate entries and in-flight fills created by the newer version.

Do not flush a shared or production cache, delete broad keyspaces, change eviction policy, or alter live cluster topology without explicit authorization and an exact target. Prefer namespace changes or bounded invalidation that preserve rollback and limit origin load.

Read [references/rollout-proof.md](references/rollout-proof.md) when implementing, migrating, deploying, or evaluating a cache change.

## Diagnose by earliest failure

Locate the first broken stage: key construction, lookup, deserialization, freshness classification, authorization check, miss collapse, origin read, publish, mutation commit, invalidation delivery, replica propagation, eviction, or recovery. Capture sanitized evidence for the exact key dimensions—not secrets—the value revision and age, hit class, cache node or layer, origin result, deadlines, retries, and relevant deployment versions.

Test competing hypotheses such as incomplete keys, stale writes racing invalidation, negative-cache poisoning, serializer mismatch, clock error, hot-key saturation, memory eviction, connection-pool exhaustion, cross-tenant reuse, or fallback overload. Avoid treating a cache flush as diagnosis; it removes evidence and may amplify the incident.

## Validate and report

Falsify both key directions: equivalent requests should reuse an entry, while every response-changing tenant, policy, locale, representation, or query difference must not retrieve another variant. Exercise update during fill, negative then create, timeout/error fill, eviction, cold fleet, cache outage, recovery, mixed versions, and rollback where relevant.

Compare the same before/after workload. Report end-to-end distributions, origin load, hit/miss/fill/stale/error/eviction rates, value age, skew, resource cost, and recovery time. Claim success only if the user target and origin-load goal improve without violating correctness, freshness, isolation, availability, or rollback.

Return the decision or change, cache contract, assumptions, evidence, tests, rollout and rollback controls, operational ownership, unresolved risks, and the trigger for reconsidering whether the cache should exist.
