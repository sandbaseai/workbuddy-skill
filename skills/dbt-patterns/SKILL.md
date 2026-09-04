---
name: "dbt-patterns"
display_name: "dbt 模式"
display_name_en: "dbt Patterns"
description: "Use when designing, reviewing, or operating a dbt project; structure SQL transformations, tests, documentation, lineage, incremental models, and production workflows with explicit data contracts."
description_zh: "用于设计、审查和运行 dbt 项目，以明确的数据契约组织 SQL 转换、测试、文档、血缘、增量模型和生产流程。"
description_en: "Design and operate dbt projects with layered SQL models, explicit contracts, data quality tests, documentation, lineage, incremental processing, and safe production workflows."
category: "data"
version: "0.1.0"
author: "majiayu000; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "dbt Core or dbt platform; warehouse-specific SQL adapter; Git and CI"
---

# dbt Patterns

Use this skill for SQL-first ELT transformations, analytics models, warehouse data quality, lineage, and dbt delivery. Treat the warehouse as a production system: preserve source semantics, make model contracts observable, and separate evidence from assumptions.

Do not use it to guess warehouse-specific SQL behavior. Confirm the adapter, dbt version, materialization semantics, timezone rules, and available privileges before proposing executable code. Do not run a production build, full-refresh, seed replacement, snapshot operation, or destructive cleanup without explicit authorization.

## Establish the project contract

Before changing a model, record:

- dbt Core/platform version, adapter, target warehouse, schemas, environments, and deployment owner;
- source tables, freshness expectations, grain, primary keys, event-time semantics, nullability, and sensitive columns;
- downstream dashboards, exports, reverse ETL, ML features, contracts, and consumers of the model;
- acceptable freshness, latency, cost, backfill window, and failure/rollback behavior;
- whether the change is additive, a semantic correction, a grain change, or a breaking contract change.

Inspect representative, redacted samples. Check duplicates, late arrivals, deletes, nulls, timezone boundaries, schema drift, maximum values, and historical anomalies. Never place production credentials or raw sensitive rows in models, logs, fixtures, or documentation.

## Layer models by responsibility

Use a predictable flow:

```text
sources -> staging -> intermediate -> marts
```

- **Sources:** declare external tables, owners, freshness, loaded-at fields, and source tests.
- **Staging (`stg_`):** one model per source relation; rename columns, cast types, normalize timestamps, and remove accidental technical noise. Avoid business rules here.
- **Intermediate (`int_`):** express joins and reusable business logic at a documented grain. Keep transformations composable and avoid hidden fan-out.
- **Marts (`fct_`, `dim_`):** publish consumer-facing facts and dimensions with stable names, documented grain, and explicit metric definitions.

Prefer names such as `stg_stripe_payments`, `int_orders_enriched`, `fct_orders`, and `dim_customers`. Use `*_id` for keys, `*_at` for timestamps, `is_*`/`has_*` for booleans, and a documented currency/unit for amounts.

## Choose materializations deliberately

- **View:** lightweight, current transformations when repeated computation is acceptable.
- **Table:** stable marts or expensive transformations where storage improves serving latency.
- **Incremental:** high-volume models only after defining the unique key, lookback window, late-arrival policy, update strategy, and backfill procedure.
- **Ephemeral:** small reusable SQL fragments that do not need independent observability; avoid hiding expensive logic in large chains.
- **Snapshot:** slowly changing dimensions only with a stable unique key, reliable change timestamp or check strategy, retention policy, and restore plan.

For incremental models, make reruns deterministic. Define how updates, deletes, duplicates, schema changes, and a late event are handled. Test a bounded backfill before changing the production predicate. A faster run is not evidence of correctness.

## Contracts, tests, and documentation

Every published model should declare its grain, owner, purpose, upstream dependencies, sensitive fields, and freshness expectations. Add tests proportionate to risk:

- `not_null` and `unique` on keys where the contract requires them;
- accepted values and relationships for controlled dimensions and foreign keys;
- custom tests for grain, reconciliation, non-negative amounts, and business invariants;
- source freshness checks and alerts with an explicit response owner.

Use singular tests for invariants that a generic test cannot express. Keep fixtures small and synthetic. Test both normal and adversarial cases: duplicate source rows, missing parents, late events, timezone cutovers, zero/negative amounts, and an empty partition. Document intentional exceptions instead of weakening tests silently.

## Safe delivery workflow

1. Inspect the manifest and lineage; identify all downstream nodes and contract changes.
2. Write the expected grain and invariants before editing SQL.
3. Implement the smallest layered change; avoid `select *` in published models and qualify joins.
4. Run focused parse, compile, unit/data tests, and a bounded target build with an isolated schema.
5. Compare row counts, key uniqueness, null rates, distributions, aggregates, freshness, query cost, and representative records against the baseline.
6. Review generated documentation and lineage; verify no secret, raw sensitive sample, or unapproved relation is exposed.
7. Promote through the approved environment order. Monitor failures, freshness, warehouse load, cost, and downstream dashboards.

For a breaking rename or grain change, use expand-and-migrate: publish a compatible model or version, migrate consumers, compare old/new outputs, announce the deprecation window, and remove the old path only after owner approval and recovery evidence. A dbt run succeeding only proves that SQL executed; it does not prove business correctness.

## Handoff

Report the dbt/adapter versions, target environment, changed nodes, model grains, tests run and results, baseline comparisons, freshness/cost impact, generated artifacts, downstream owners, unresolved anomalies, and next authorized action. Include the exact selector and invocation, but redact credentials and sensitive values. Stop and escalate on unexpected fan-out, contract violations, unexplained metric drift, source freshness failure, permission changes, or warehouse pressure beyond the agreed threshold.
