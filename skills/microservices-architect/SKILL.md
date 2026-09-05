---
name: "microservices-architect"
display_name: "微服务架构设计"
display_name_en: "Microservices Architect"
description: "Use when designing distributed systems, decomposing a monolith, reviewing service boundaries, or choosing synchronous/asynchronous communication, data ownership, resilience, and observability patterns."
description_zh: "用于设计分布式系统、拆分单体、评审服务边界，或选择同步/异步通信、数据所有权、韧性与可观测性方案。"
description_en: "Derive service boundaries from domain and change ownership, choose communication from latency and failure requirements, define data consistency and migration paths, and validate resilience, tracing, deployment, and operational ownership before implementation."
category: "development"
version: "0.1.0"
author: "Jeffallan/claude-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with access to domain, API, data, deployment, incident, and telemetry evidence, plus an approved implementation and migration path"
---

# Microservices Architect

## Purpose and boundary

Design independently evolvable services only when the operational and domain benefits justify their complexity. Do not split a system because a diagram looks cleaner. An architecture proposal does not authorize creating services, changing schemas, routing traffic, or migrating production data.

## Inputs and decision criteria

Gather domain vocabulary, change ownership, user journeys, current modules, API/event contracts, data stores, traffic/latency, failure history, deployment topology, team ownership, compliance, and recovery requirements. Make these explicit:

- bounded contexts, invariants, aggregate and transaction boundaries;
- synchronous latency/deadline requirements and asynchronous delivery/ordering needs;
- data ownership, consistency model, idempotency, replay, deletion, and migration compatibility;
- failure domains, retries, timeouts, rate limits, circuit breakers, bulkheads, fallbacks, and load shedding;
- trace/log/metric correlation, health/readiness, rollout, rollback, capacity, and on-call ownership;
- the cost of network hops, serialization, duplication, operational tooling, and eventual consistency.

Mark assumptions and unresolved evidence. “Database per service” and “always async” are useful patterns, not universal laws; justify exceptions against invariants and failure behavior.

## Core workflow

1. **Map the current system.** Trace request and event flows, module ownership, data reads/writes, external dependencies, synchronous chains, queues, and deployment units. Identify seams and accidental coupling.
2. **Discover boundaries.** Group behavior by business capability, invariant, rate of change, ownership, and data lifecycle. Test candidate boundaries with concrete scenarios, failure cases, and likely team changes.
3. **Define contracts.** For each service, specify API/events, versioning, authentication, authorization, idempotency, errors, timeouts, limits, compatibility window, and consumer ownership.
4. **Choose communication.** Use synchronous calls only where the caller needs a bounded immediate answer and can tolerate dependency failure. Use asynchronous messaging for long-running, fan-out, or independently retryable work; define delivery, ordering, deduplication, and replay behavior.
5. **Design data ownership.** Prefer one authoritative owner for each invariant. Define read models, replication, eventual-consistency UX, outbox/inbox or equivalent delivery guarantees, backfills, dual-read/write risks, and deletion propagation.
6. **Design failure behavior.** Give every external call a deadline, bounded retry budget, cancellation, and a graceful degradation path. Prevent retry storms and cascading failure with breakers, bulkheads, queue limits, and load shedding.
7. **Design operability.** Propagate a correlation/trace ID across HTTP, RPC, and messages; define golden signals, structured logs, actionable alerts, runbooks, health/readiness semantics, and service ownership.
8. **Plan migration.** Start with a reversible seam or modular monolith where appropriate. Sequence compatibility, extraction, data migration, traffic shift, verification, rollback, and old-path retirement. Do not create a distributed monolith by moving files while retaining shared writes.
9. **Validate the architecture.** Use contract, failure, load, recovery, security, and deployment tests. Compare actual latency, error rate, cost, operational load, and recovery evidence with the stated decision criteria.

## Boundary validation table

| Boundary question | Evidence to require |
|---|---|
| Can it deploy independently? | Build, release, configuration, ownership, and rollback path are independent enough for the stated cadence. |
| Does it own an invariant? | One authoritative write owner, explicit consistency, and no hidden cross-service transaction. |
| Is its interface stable? | Versioned contract, consumer inventory, compatibility window, errors, limits, and deprecation plan. |
| Can it fail safely? | Deadline, retry budget, breaker/bulkhead, fallback/degraded mode, and overload behavior. |
| Can it be operated? | Trace continuity, metrics, logs, alerts, runbook, on-call owner, and health/readiness checks. |
| Is the split worth it? | Measured benefit exceeds network, data, deployment, testing, and operational complexity. |

## Resilience requirements

- Propagate correlation IDs without trusting them as identity; validate length and characters and prevent log injection.
- Make retries selective, bounded, jittered, and aware of idempotency. Never retry an unknown side effect blindly.
- Keep timeout budgets shorter than the caller’s deadline and leave room for cleanup/fallback.
- Define what happens when a dependency is slow, unavailable, stale, duplicated, out of order, or over quota.
- Use health probes that distinguish process liveness from readiness to serve; do not make liveness depend on every downstream system.
- Test partial failure, duplicate delivery, delayed messages, poison messages, partition, deploy skew, and recovery—not only the happy path.

## Safe implementation examples

These snippets illustrate contracts; adapt them to the repository’s framework and review dependencies before adding them.

```js
// Correlation is for tracing, not authorization; bound and sanitize it.
const incoming = req.get("x-correlation-id");
const correlationId = /^[A-Za-z0-9._:-]{1,128}$/.test(incoming || "")
  ? incoming
  : crypto.randomUUID();
req.log = logger.child({ correlationId });
res.set("x-correlation-id", correlationId);
```

```text
External call contract:
deadline: <caller budget>
retry: <max attempts, jitter, idempotency condition>
failure: <fallback/degraded response>
breaker: <open/half-open policy>
telemetry: <trace, metrics, structured error>
owner: <service/team>
```

## Architecture decision record

```text
Problem/outcome: <why a boundary or topology must change>
Current evidence: <modules, data flows, traffic, incidents, ownership>
Boundaries and owners: <service, invariant, authoritative data>
Communication: <sync/async, deadlines, delivery and compatibility>
Failure behavior: <timeouts, retries, breakers, degraded modes>
Migration: <waves, data validation, traffic shift, rollback>
Operations: <SLOs, telemetry, alerts, runbooks, on-call>
Alternatives and trade-offs: <including modular monolith/no split>
Decision, risks, review trigger: <owner/date/conditions>
```

## Handoff checklist

- [ ] Boundaries follow domain invariants, change ownership, and data lifecycle rather than naming alone.
- [ ] Each authoritative datum has an owner and an explicit consistency/deletion model.
- [ ] API/event contracts include versioning, auth, idempotency, errors, deadlines, and limits.
- [ ] Communication choices account for latency, ordering, delivery, retries, and partial failure.
- [ ] Every dependency has bounded failure behavior and a graceful degradation decision.
- [ ] Traces, correlation IDs, metrics, logs, health checks, alerts, runbooks, and owners are defined.
- [ ] Migration and rollback preserve compatibility, integrity, privacy, and recoverability.
- [ ] Alternatives, complexity cost, residual risk, and validation evidence are documented.
