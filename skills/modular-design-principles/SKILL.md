---
name: "modular-design-principles"
display_name: "模块化设计原则"
display_name_en: "Modular Design Principles"
description: "Design and review modular systems through explicit boundaries, state ownership, public contracts, replaceable dependencies, isolation, and failure containment."
description_zh: "通过明确边界、状态所有权、公共契约、可替换依赖、隔离和故障遏制来设计与审查模块化系统。"
description_en: "Design and review modular systems through explicit boundaries, state ownership, public contracts, replaceable dependencies, isolation, and failure containment."
category: "development"
version: "0.1.0"
author: "Omni Skills Team; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Modular Design Principles

Use this skill when splitting a codebase, introducing a bounded context,
reviewing package boundaries, or deciding whether a dependency belongs behind
an interface. Modularity is a property of ownership, contracts, and change
independence—not merely a folder layout or a number of services.

## Establish the boundary

Name the context and its purpose in domain language. Identify the decisions it
owns, the facts for which it is authoritative, its lifecycle and invariants,
and what is explicitly out of scope. Reject vague names that collide with
another context or hide unrelated responsibilities.

Evaluate a proposed split against:

- vocabulary: do different areas use conflicting meanings?
- change cadence: do they change for unrelated reasons?
- scale and SLO: do they need different throughput, latency, or availability?
- consistency: do they require different transaction boundaries?
- ownership: would clear owners reduce conflict and review churn?
- deployment and failure: must they roll out or fail independently?

Do not split solely because a file is large, and do not keep a boundary solely
because components currently share a process. Record the decision, alternatives,
and evidence for the chosen boundary.

## Preserve ownership and contracts

For each module, define:

1. authoritative state and the invariants it protects;
2. the smallest public API, event, command, or shared type;
3. input validation, authorization, idempotency, timeout, and error semantics;
4. integrations and whether consistency is immediate, eventual, or batch;
5. observability identifiers and the owner of operational response.

Prefer a module to access another module through an explicit contract rather
than another module's tables, buckets, repositories, or internal types. Shared
kernels must contain only stable concepts with genuine cross-boundary ownership.
Keep orchestration thin at composition roots; place business rules with the
module that owns them. Version public contracts deliberately and define mixed-
version behavior before a rollout.

## Test modularity

Check whether the module's core behavior can be tested without starting
unrelated contexts. Use fakes or contract tests at ports where appropriate,
then test real integration boundaries separately. Look for:

- reach-through persistence or hidden shared mutable state;
- duplicated global names or schemas with divergent meanings;
- transport or UI layers containing domain rules;
- unscoped transactions crossing ownership boundaries;
- leaky exports of repositories or implementation types;
- synchronous calls without deadlines or async work without idempotency;
- retries, caches, queues, or events that violate ownership or isolation.

For every violation, show the path, the invariant or contract it breaks, the
smallest corrective refactoring, and a regression test. Do not recommend a
large rewrite when a boundary adapter or contract test can establish safety.

## Evolve safely

Map consumers before changing a public contract. Prefer additive or expand-and-
contract evolution where mixed versions may coexist. Define migration order,
backfill ownership, compatibility window, feature-flag behavior, telemetry,
rollback condition, and cleanup trigger. For an extracted module, verify that
old and new paths cannot silently write conflicting sources of truth.

Do not move data, change production routing, or delete an old path without
explicit authorization and recovery evidence. State when a proposed boundary
requires an architectural decision, security review, data migration, or owner
approval.

## Handoff format

```text
Context / scope / commit / owners:
Boundary rationale and non-goals:
State ownership, invariants, and lifecycle:
Public contracts and versioning:
Dependencies, consistency, timeouts, retries, and failure behavior:
Isolation and contract-test evidence:
Violations / severity / confidence / owner:
Migration, rollout, rollback, and observability:
Decision, open risks, and next review trigger:
```

Return observed evidence separately from assumptions and recommendations. A
modular design is ready when ownership is unambiguous, the public surface is
small and testable, and each remaining coupling has an explicit reason and
failure strategy.
