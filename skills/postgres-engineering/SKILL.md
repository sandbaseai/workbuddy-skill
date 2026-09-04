---
name: "postgres-engineering"
display_name: "PostgreSQL 数据库工程"
display_name_en: "PostgreSQL Database Engineering"
description: "Use when designing, changing, querying, securing, or diagnosing PostgreSQL databases; establish the real version and workload, prefer read-only evidence, and bound production effects before schema, index, maintenance, replication, or recovery actions."
description_zh: "安全设计、审查和诊断 PostgreSQL 模式、查询、索引、锁、连接、RLS、维护、复制与恢复。"
description_en: "Safely design, review, and diagnose PostgreSQL schemas, queries, indexes, locks, connections, RLS, maintenance, replication, and recovery."
category: "data"
version: "0.1.0"
author: "Supabase; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# PostgreSQL Database Engineering

Use this skill for PostgreSQL-specific design and operations, whether hosted by Supabase or elsewhere. Establish the server and extension versions, hosting constraints, topology, workload, data sensitivity, and environment before relying on version-dependent features or executing commands.

## Inspect before changing

Prefer migrations, schema files, application queries, and read-only catalog views as evidence. Confirm table grain, keys, constraints, data types, defaults, generated columns, partitions, indexes, row counts, growth, dependencies, RLS policies, roles, and ownership. Do not infer physical names or production state from an ORM alone.

Use a least-privileged account and a non-production database or read replica when it answers the question. Redact credentials, connection strings, query parameters, personal data, and tenant identifiers. Before any production write, DDL, maintenance, role/policy, replication, failover, restore, or configuration action, require explicit authority for that operation and environment.

## Design schemas deliberately

Choose types and constraints that encode the real domain: distinguish timestamps with and without time zone, use exact numeric types where rounding matters, and avoid an enum or extension when its migration and portability cost outweighs its value. Make primary, unique, foreign-key, check, and exclusion constraints match the intended invariant.

Index foreign-key referencing columns when delete/update and join behavior justify it; PostgreSQL does not create those indexes automatically. For partitioning, prove pruning, lifecycle, or scale benefits against the operational cost. A partition key changes uniqueness and foreign-key options, so do not prescribe partitioning from table size alone.

Evolve schemas with compatible stages. Estimate rewrite, scan, validation, and lock behavior for the deployed PostgreSQL version. Use `NOT VALID` plus later validation, concurrent index creation, or phased backfills only where their semantics fit. A transaction does not make a long blocking lock safe.

## Write and validate queries

Use parameters for values and allowlist any dynamic identifiers. Make join cardinality, `NULL` semantics, collation, time zones, precision, and inclusive/exclusive bounds explicit. Select required columns, avoid accidental cross joins, and use deterministic ordering for pagination. Prefer keyset pagination for large, mutable ordered results when consumers can use cursors.

Validate the result with row counts, denominators, edge cases, and an independent check when the decision is material. Never add a `LIMIT` that silently changes a required aggregate or completeness claim.

## Diagnose performance with evidence

Start with the user-visible symptom and representative query shape. Inspect aggregate statistics and a sanitized plan. `EXPLAIN` does not execute a statement; `EXPLAIN ANALYZE` does, so use it on production only when execution and impact are explicitly authorized. For modifying statements, wrap controlled analysis in a transaction only when all effects are actually transactional and rollback is verified.

Read estimated versus actual rows, loops, access paths, filters, buffers, I/O and timing when available. Large estimate errors may point to stale or insufficient statistics, correlation, skew, or a query shape problem. Measure before and after under comparable parameters and cache state.

Design indexes around observed predicates, joins, ordering, and selectivity. Evaluate column order, partial predicates, included columns, expression volatility, operator classes, write amplification, storage, build duration, lock behavior, and overlap with existing indexes. Verify an index is usable and beneficial; “index every filtered column” is not a strategy.

## Control concurrency and capacity

For lock or transaction incidents, capture blockers, waiters, lock modes, transaction age, query age, application identity, and safe ownership before intervening. Do not terminate sessions, cancel queries, promote replicas, or alter timeouts without explicit production authorization and an assessed blast radius. Fix transaction scope and access order rather than treating termination as the root-cause fix.

Treat connection slots as a bounded resource. Account for application instances, pool modes, background workers, migrations, administration, and failover headroom. More connections can reduce throughput. Verify whether prepared statements, session state, advisory locks, or temporary objects are compatible with the selected pool mode.

## Secure rows and functions

Use least privilege, separate owner/migration/runtime roles, and test grants after schema changes. For row-level security, define the actor and tenant boundary, enable policies on every intended table, understand owner and bypass behavior, and test allowed and denied `SELECT`, `INSERT`, `UPDATE`, and `DELETE` paths. Index policy predicates when justified by workload.

Review `SECURITY DEFINER` functions for owner privilege, immutable `search_path`, input validation, qualification of objects, and unnecessary execute grants. Never rely on client-side filters for tenant isolation.

## Maintain and recover

Diagnose bloat and autovacuum from dead tuples, modification rate, table-specific settings, transaction age, freeze risk, I/O capacity, and long-running transactions. Do not run broad `VACUUM FULL`, `REINDEX`, or aggressive maintenance on production without an impact window and recovery plan.

A replica is not a backup. Define recovery point and recovery time objectives, retention, encryption, offsite or failure-domain separation, credential access, extension and role dependencies, and point-in-time recovery boundaries. Test restoration into an isolated environment, then validate schema, constraints, counts, checksums or domain invariants, application reads, permissions, and measured recovery time. Never overwrite the sole recoverable copy during a test.

## Handoff

Return the server/environment evidence, SQL or proposed change, assumptions, expected cardinality and locks, plan findings, authorization boundary, rollout and rollback, verification results, and remaining risks. For executed work, include affected rows, transaction outcome, elapsed time, before/after evidence, replication or backup state, and whether the requested user-visible outcome was independently confirmed.
