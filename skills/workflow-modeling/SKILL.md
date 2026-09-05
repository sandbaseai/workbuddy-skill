---
name: "workflow-modeling"
display_name: "工作流状态建模"
display_name_en: "Workflow State Modeling"
description: "Use when designing or reviewing staged workflows, lifecycle schemas, work packages, results, derivations, or pipeline stages; keep workflow gates as state and avoid multiplying objects, services, enums, or tables per stage."
description_zh: "用于设计或审查分阶段工作流、生命周期模型、工作包、结果、派生关系或流水线阶段，将阶段建模为状态，避免为每个阶段复制对象、服务、枚举或数据表。"
description_en: "Model staged work as a stable lineage of assets, packages, units, results, and derivations; keep gates and statuses as data, prevent stage-by-stage architecture multiplication, and verify ownership and migration boundaries."
category: "development"
version: "0.1.0"
author: "iamthenop/infurnet-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Workflow or pipeline design with an identified state store, work contracts, and repository-native schema/tests"
---

# Workflow State Modeling

Use this skill when a process has stages, gates, lifecycle positions, queues, or derived outputs. The central rule is simple: work items are objects; workflow gates are states. Do not turn every stage into a new object family merely because a record passed through it.

## Establish the workflow contract

Define the durable source asset, work package, work unit, accepted result, derivation/lineage, gate keys, work types, allowed transitions, owners, retention, retry behavior, and authorization for changes. Identify the system of record and current schema or event contracts before proposing new tables, services, enums, queues, or APIs. Treat existing bindings, migrations, tests, and work orders as evidence—not permission to expand scope.

## Model one stable lineage

Prefer a lineage such as:

```text
asset -> work package -> work unit -> accepted result -> derivation -> next work package
```

Record a gate with fields such as `gate_key`, `work_type`, `result_schema`, `display_state`, timestamps, and owner where the repository's contract supports them. A result exists only after acceptance; an accepted timestamp is an event, not a class name. A derivation records how an output came from an input, including the relevant contract and transformation identity.

Do not create `StageAItem`, `StageBItem`, `StageCService`, or a table and enum family for each gate unless each is a genuinely durable object with independent ownership, lifecycle, retention, and behavior. If the only difference is workflow position, keep it in state data, a work contract, a handler, or a projection.

## Keep vocabulary and status bounded

Use short names that carry one concept and at most one necessary qualifier. Avoid stacking generic carriers such as `content`, `data`, `item`, and `information`, or embedding every stage name in identifiers. Gate names are appropriate in documentation, registered work-type values, result schemas, routing keys, display labels, and narrow validators/adapters. They should not define generic architecture.

Keep control status generic and orthogonal to gate meaning: for example `available`, `leased`, `paused`, `completed`, `failed`, `cancelled`, and `expired`. Put domain meaning in `work_type`, `gate_key`, accepted results, derivations, and projections; do not encode a cross-product such as `stage_a_accepted` into every status enum.

Separate workflow stage from media, tenant, or product family. When behavior varies by family, use explicit handlers or strategies behind a shared work contract. Do not create every stage × family combination as a class, service, table, or migration unless the difference is a real independent domain boundary.

## Review transitions and failure semantics

For each transition, define preconditions, ownership, idempotency key, lease/timeout, ordering or watermark assumptions, retry/backoff, cancellation, dead-letter or quarantine behavior, accepted output schema, and recovery/rollback. Make replay safe and preserve lineage. Do not let a failed attempt masquerade as an accepted result, and do not overwrite an input asset when the system needs auditability or reprocessing.

Check concurrent claims, duplicate delivery, stale workers, partial writes, and cross-service failure. Put transaction boundaries around the state and result updates that must be atomic; use an outbox or equivalent when events must reflect committed state. Keep remote calls outside narrow database transactions unless the repository has a proven compensation contract.

## Challenge new architecture objects

Before adding a stage-named object, answer:

1. Is it a durable object with its own lifecycle and owner?
2. Is it a registered contract validator or adapter rather than generic architecture?
3. Would it need to be copied for every gate, media type, tenant, or version?
4. Can `gate_key`, `work_type`, `result`, `derivation`, handler, or projection express the requirement?
5. What migration, index, query, API, retention, and rollback cost does it add?

If the proposal multiplies architecture without a durable boundary, stop and report the conflict. If a new boundary is justified, document why, its invariants, compatibility period, ownership, and removal/migration criteria.

## Verify and hand off

Use repository-native schema, migration, contract, integration, and concurrency tests. Verify actual columns/types/constraints, transition guards, uniqueness/idempotency, lineage, authorization, retry/replay, and initialization order where applicable. Test empty, duplicate, out-of-order, late, failed, cancelled, retried, partially committed, and replayed work. Do not claim a transition is covered because an unrelated trigger or default made one example pass.

Return the state model, lineage, transition table, ownership, failure/recovery semantics, rejected alternatives, migration/rollback plan, exact checks and evidence, unresolved decisions, and next review gate. Stop when gate ownership, durable-object boundaries, authorization, or accepted-result semantics are ambiguous.
