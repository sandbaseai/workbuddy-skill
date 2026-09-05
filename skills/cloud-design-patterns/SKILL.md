---
name: "cloud-design-patterns"
display_name: "云设计模式"
display_name_en: "Cloud Design Patterns"
description: "Use when designing or reviewing distributed cloud systems and choosing patterns for resilience, performance, messaging, security, deployment, or migration. Select patterns from explicit constraints and trade-offs rather than applying a checklist mechanically."
description_zh: "用于设计或评审分布式云系统，选择韧性、性能、消息、安全、部署或迁移模式；必须从明确约束和取舍出发，而不是机械套用清单。"
description_en: "Translate functional and non-functional requirements into a small set of justified patterns, test their failure and operational consequences, document alternatives, and verify the chosen design against measurable fitness functions."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with access to current architecture, workload, security, cost, telemetry, and operational evidence, plus an approved design and implementation path"
---

# Cloud Design Patterns

## Purpose and boundary

Use patterns as named hypotheses about a recurring problem, not as proof that a design is correct. A pattern can add latency, cost, state, operational burden, or new failure modes. Keep analysis and plans read-only until the owner authorizes implementation; this Skill does not provision infrastructure, change routing, migrate data, or alter access policy.

## Start with constraints

Capture the workload, critical user journeys, dependencies, data flows, trust boundaries, traffic shape, latency, availability, recovery, compliance, data residency, cost, team ownership, and provider limits. Define measurable fitness functions such as p99 latency, error rate, queue age, recovery time, data loss, unit cost, or operator effort.

Ask before choosing a pattern:

- What failure or change is the pattern meant to contain?
- What is the authoritative state and who owns it?
- Is the operation synchronous, asynchronous, replayable, idempotent, or compensatable?
- What happens under timeout, duplication, reordering, overload, stale data, partition, and partial deployment?
- What new credentials, network paths, storage, logs, queues, retries, or on-call work does it create?
- How will the decision be tested, rolled back, retired, and reviewed?

## Pattern selection workflow

1. **Frame the problem.** Describe the user or system outcome and the current failure mode; do not start with a favorite pattern.
2. **Map the boundary.** Identify callers, dependencies, data ownership, trust boundaries, failure domains, and operational owners.
3. **Shortlist patterns.** Choose the smallest set that addresses the stated constraint. Include “no pattern,” a simpler design, or a modular monolith where credible.
4. **Compare consequences.** For each candidate, record benefits, costs, latency, state, consistency, security, operability, provider coupling, migration effort, and failure behavior.
5. **Define contracts.** Specify deadlines, retries, idempotency, delivery/ordering, versioning, authorization, limits, observability, and degraded behavior.
6. **Validate before implementation.** Use a small prototype, contract test, load test, failure test, recovery rehearsal, or plan review that targets the fitness functions.
7. **Stage and verify.** Introduce one change in an approved environment, compare against baseline, keep rollback, and observe enough time to catch delayed cost or consistency effects.
8. **Record the decision.** Document chosen and rejected patterns, assumptions, evidence, residual risk, owner, expiry/review trigger, and what would falsify the decision.

## Pattern map

### Reliability and resilience

Use **Ambassador** to isolate client-to-service communication concerns; **Bulkhead** to contain resource exhaustion; **Circuit Breaker** to stop repeated calls to an unhealthy dependency; **Compensating Transaction** or **Saga** for multi-step workflows without one distributed transaction; **Retry** only for transient, idempotent operations with a bounded budget; **Health Endpoint Monitoring** for actionable health checks; **Leader Election** where one active coordinator is required; **Sequential Convoy** when ordered processing is essential.

For every resilience pattern, specify timeout budgets, retry ownership, cancellation, overload behavior, stale/fallback semantics, and how a storm or split-brain is prevented. A circuit breaker without a useful degraded mode only moves the failure.

### Performance and capacity

Use **Async Request-Reply** for work that exceeds a synchronous deadline; **Cache-Aside** when freshness and invalidation are understood; **CQRS** when read/write models have materially different needs; **Index Table** or **Materialized View** for repeated expensive projections; **Priority Queue** for differentiated urgency; **Queue-Based Load Leveling** for burst absorption; **Rate Limiting** and **Throttling** for fair capacity; **Sharding** only with a stable partition key and rebalancing plan.

Measure hit rate, freshness, queue age, tail latency, hot keys, backpressure, storage, egress, and cost. Do not hide capacity problems behind unlimited queues, retries, or caches.

### Messaging and integration

Use **Competing Consumers** for parallel work, **Publisher-Subscriber** for fan-out, **Pipes and Filters** for independently testable stages, **Messaging Bridge** for incompatible brokers, **Claim Check** for oversized payloads, **Choreography** when loose coupling is worth distributed coordination cost, and a **Scheduler/Agent/Supervisor** arrangement when periodic orchestration needs explicit ownership.

Define delivery semantics, schema/version compatibility, ordering scope, deduplication, poison-message handling, replay, retention, privacy, and deletion. “At least once” requires idempotent consumers; event publication is not automatically a transaction with the originating database.

### Architecture and migration

Use **Anti-Corruption Layer** to protect a new domain from a legacy model; **Backends for Frontends** for materially different client needs; **Gateway Aggregation** to reduce client chattiness; **Gateway Offloading** for shared cross-cutting work; **Gateway Routing** for controlled destinations; **Sidecar** for independently deployable platform concerns; and **Strangler Fig** for incremental replacement.

Document ownership and removal criteria. Gate every migration with compatibility, data integrity, traffic shift, observability, rollback, and decommissioning evidence. An adapter that becomes permanent without an owner is new architecture debt.

### Deployment, operations, and security

Use **Compute Resource Consolidation** where isolation and capacity allow; **Deployment Stamps** for repeatable isolated units; **External Configuration Store** with access control, versioning, and rollback; **Geode** or regional placement only when locality and failure behavior are proven; **Static Content Hosting** when the content and invalidation model fit.

Security patterns include **Federated Identity** with audience/issuer/tenant validation, **Quarantine** for untrusted content or workloads, and **Valet Key** for narrowly scoped temporary access. Treat pattern names as prompts to verify controls, not as security guarantees.

## Anti-pattern checks

- Retries without deadlines, idempotency, jitter, or a total budget can amplify outages.
- Caches without ownership, invalidation, privacy, and stale-data behavior can serve incorrect or cross-tenant data.
- Queues without limits, age alerts, poison handling, and capacity planning merely defer failure.
- Gateways can become a single bottleneck or policy bypass; define scaling, auth, and failure behavior.
- Event sourcing, CQRS, multi-region, and multi-cloud add state and operations; require a concrete need and recovery proof.
- Shared databases and hidden synchronous chains can preserve a distributed monolith despite separate deployables.
- Pattern counts are not architecture quality; prefer the smallest design that passes the measured fitness functions.

## Decision record

```text
Problem and outcome: <user/system outcome and failure mode>
Constraints and evidence: <fresh requirements, metrics, limits, owners>
Candidate patterns: <chosen, simpler option, and alternatives>
Decision and rationale: <why this pattern fits>
Contracts: <deadlines, retries, idempotency, consistency, auth, versioning>
Failure and operations: <degraded mode, telemetry, runbook, recovery>
Cost and complexity: <resources, network, data, operator and provider effects>
Validation and rollout: <test, baseline, stages, rollback, retirement>
Risks, owner, review trigger: <residual risk and conditions>
```

## Handoff checklist

- [ ] The problem, outcome, constraints, evidence freshness, and owners are explicit.
- [ ] A simpler/no-pattern alternative was considered.
- [ ] Each chosen pattern has a stated problem, trade-offs, failure behavior, and fitness function.
- [ ] Data ownership, consistency, delivery, privacy, identity, and deletion behavior are defined.
- [ ] Deadlines, retries, idempotency, limits, backpressure, and observability are bounded.
- [ ] Cost, provider coupling, operations, recovery, and migration/decommissioning are addressed.
- [ ] Validation, rollout, rollback, residual risk, and review trigger are recorded.
