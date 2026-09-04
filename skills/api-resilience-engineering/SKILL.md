---
name: "api-resilience-engineering"
display_name: "API 韧性工程"
display_name_en: "API Resilience Engineering"
description: "Use when designing, implementing, reviewing, testing, or diagnosing API timeouts, retries, idempotency, rate limits, concurrency limits, circuit breakers, bulkheads, backpressure, load shedding, or ambiguous outcomes."
description_zh: "设计、实现、审查、测试和诊断 API 超时、重试、幂等、限流、并发限制、熔断、舱壁、背压、负载削减与结果不确定问题。"
description_en: "Design, implement, review, test, and diagnose API timeouts, retries, idempotency, rate limits, concurrency limits, circuit breakers, bulkheads, backpressure, load shedding, and ambiguous outcomes."
category: "development"
version: "0.1.0"
author: "Sim Studio; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
---

# API Resilience Engineering

Use this skill for synchronous APIs, SDK calls, webhooks, background submission endpoints, and service-to-service integrations. Inspect the protocol, operation semantics, client and server implementations, proxies, deadlines, quotas, storage, side effects, telemetry, and deployed versions before changing resilience behavior. Preserve published compatibility unless the user explicitly accepts a breaking change.

Resilience controls are a coupled system. A retry changes load and duplicate risk; a timeout changes ambiguity; a circuit breaker changes availability; a rate limit changes fairness. Define their combined contract rather than adding each mechanism independently.

## Define the operation contract

For each operation, record:

- read, deterministic write, non-idempotent action, or asynchronous submission;
- authoritative completion evidence and how a client reconciles an unknown outcome;
- end-to-end deadline and budgets for queueing, connection, request, processing and response;
- retryable and permanent failure classes;
- idempotency or deduplication scope, identity, fingerprint, retention and response semantics;
- caller, tenant, organization and global quotas plus burst behavior;
- concurrency and resource limits, fallback and load-shedding policy;
- observable signals, ownership, rollout and rollback.

Do not infer safety from an HTTP method alone. Verify actual side effects, including audit records, billing, notifications, downstream calls, cache fills and asynchronous jobs.

## Budget deadlines and cancellation

Start with the caller's end-to-end deadline and reserve time for useful recovery and response handling. Propagate an absolute deadline or decreasing remaining budget across hops; independently configured per-hop timeouts can multiply beyond the user deadline. Separate connection, TLS, first-byte, idle and total timeouts where the client supports them.

Cancellation ends the caller's interest, not necessarily a committed side effect. Propagate cancellation to work that is safe to stop, but preserve reconciliation identifiers for work that may continue. Bound server work after disconnect and avoid abandoning locks, transactions or shared fills.

Classify timeout outcomes as definitely not started, definitely completed, or ambiguous. An ambiguous write must be reconciled by operation identity or status lookup before resubmission.

## Retry only when safe

Retry transient transport failures, explicit throttling or service-unavailable responses only when the operation contract permits it. Do not retry malformed input, authentication or authorization failures, missing resources, deterministic conflicts, policy refusals, or permanent quota failures merely because they use a familiar status code.

Honor valid `Retry-After` or provider-specific reset guidance. Otherwise use exponential backoff with jitter and a cap, bounded by maximum attempts, total elapsed time, operation age and the caller deadline. Ensure every layer does not retry independently; multiplicative retries can turn one request into an outage.

Use retry budgets tied to successful traffic or capacity. Stop when recovery attempts consume unacceptable load. Preserve the original trace and operation identity across attempts while giving each attempt its own span.

For reads, verify consistency and staleness implications. For writes, require true idempotency or a reconciliation path. A network error after sending a body does not prove the server did nothing.

## Implement honest idempotency

Distinguish these contracts:

- duplicate suppression: repeated work may return conflict or current status;
- at-most-once claim: first identity wins, later attempts do not execute;
- response replay: the same identity and request fingerprint return the original status and body;
- state idempotence: applying the same desired state repeatedly converges, though responses may differ.

Scope the key to the authenticated principal and operation. Validate syntax and entropy; store a canonical request fingerprint, state (`in-progress`, `completed`, `failed`), result reference or response, creation time and expiry. Atomically claim the key with the business operation. A key reused with a different fingerprint is a conflict, never permission to execute again.

Define behavior for simultaneous duplicates, process crash, expired in-flight records, large responses, downstream side effects and retention cleanup. Keep durable claims at least as long as the maximum client retry and replay window. Never use an in-memory map as the only protection for durable or billable effects.

Do not label a uniqueness token as `Idempotency-Key` if the endpoint cannot replay or recover according to its documented semantics. Publish the exact behavior so clients do not assume Stripe-style response replay.

## Rate limit and shed load fairly

Identify the constrained resource and the fairness domain: IP, credential, user, tenant, organization, endpoint, cost unit or global system. A single global request count often lets cheap calls subsidize expensive ones or one tenant exhaust everyone else's capacity.

Choose token bucket for controlled bursts, leaky bucket for smoothed output, fixed or sliding windows for simpler quotas, and concurrency limits for long-running work. Apply admission before expensive parsing or dependency calls where safe, but authenticate enough to select the correct scope. Coordinate distributed enforcement or document bounded overshoot.

Return a stable machine-readable error, the scope or reason clients may act on without leaking other tenants, and `Retry-After` when waiting is the remedy. Distinguish time-based rate limits, concurrent-work saturation, daily/business quotas and billing limits; they recover differently.

Use bounded queues. Reject early when predicted wait exceeds the request deadline or when accepting more work would violate recovery objectives. Prioritize critical traffic deliberately and prevent starvation. Load shedding must be observable by caller class and reason.

## Use breakers and bulkheads as containment

Circuit breakers should protect a specific dependency and operation class, not hide arbitrary application failures. Define which outcomes count, sampling volume, open threshold, open duration, half-open probe concurrency, fallback and ownership. Do not count caller validation or cancellation as dependency failure.

Keep pools, queues, semaphores and breaker state isolated by resource and criticality when shared exhaustion would cause cascading failure. Bound fallback cost; a cache, alternate region or secondary provider can share fate or overload another dependency. Half-open probes must be limited and representative.

Expose breaker state and transitions, rejected calls, probe outcomes and dependency latency. Avoid fleet-wide synchronized recovery by adding bounded jitter or coordinated control.

## Preserve stable API semantics

Use consistent success and error envelopes, machine-readable codes, sanitized messages and field-level validation details. Validate all caller-controlled values at the boundary and again where representation changes, such as a typed value passed into SQL or a cursor decoded into query state. Caller input should not produce an unclassified 500.

Treat cursors, retry tokens and client-provided identifiers as untrusted position or correlation hints, never authorization. Re-derive tenant and resource scope from the authenticated principal. Bind pagination cursors to ordering and filtering semantics, validate decoded types, and end keysets with a unique tie-breaker.

Avoid changing established status, header or envelope behavior merely to follow a fashionable convention. Compatibility and client recovery behavior are part of resilience. Document deliberate deviations and migration plans.

## Diagnose with attempt-level evidence

Locate the earliest failing stage: DNS, connection, TLS, admission, authentication, validation, queue, handler, dependency, commit, response, proxy, client timeout, retry, reconciliation or cleanup. Capture sanitized event time, endpoint and operation class, principal scope, deadline and remaining budget, attempt count, idempotency identity presence—not value—status and machine code, wait guidance, limiter/breaker state, queue depth, dependency timing, completion evidence and recent changes.

Separate availability failures from overload, policy denial and ambiguous completion. Correlate client, gateway, service and dependency traces using a stable request or operation identifier. Do not repeatedly rerun a write to “see if it works.”

## Validate and report

Test successful calls, every permanent failure class, connection failure before send, disconnect after send, timeout before and after commit, concurrent duplicate writes, key reuse with changed payload, retry exhaustion, invalid wait headers, quota boundaries, distributed limiter overshoot, queue saturation, breaker open/half-open recovery, fallback saturation, cancellation and rolling-version compatibility as applicable.

Use deterministic fault injection in an isolated environment before production. Measure end-to-end latency distributions, success and error rates by class, attempts per operation, retry amplification, duplicate prevention, ambiguous-outcome recovery, admitted and rejected work, queue wait, limiter fairness, breaker transitions and dependency load. Prove that controls reduce failure impact without violating correctness or shifting overload elsewhere.

Return the operation and failure contracts, implementation changes, configuration and version assumptions, tests and observed evidence, capacity and fairness model, dashboards and alerts, rollout and rollback, client migration needs, unresolved ambiguity, and remaining correctness or availability risks.
