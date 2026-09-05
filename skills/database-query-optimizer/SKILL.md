---
name: "database-query-optimizer"
display_name: "数据库查询优化"
display_name_en: "Database Query Optimizer"
description: "Use when investigating slow SQL, execution plans, missing or redundant indexes, lock contention, deadlocks, or database scaling bottlenecks in PostgreSQL or MySQL."
description_zh: "用于排查 PostgreSQL 或 MySQL 中的慢 SQL、执行计划、缺失或冗余索引、锁竞争、死锁和数据库扩展瓶颈。"
description_en: "Capture a safe performance baseline, explain the bottleneck, design one measurable change, apply it in an approved environment, and compare latency, resource use, write amplification, locks, and replication health before declaring success."
category: "data"
version: "0.1.0"
author: "Jeffallan/claude-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to query plans and database metrics, a disposable or approved test database, and an authorized migration/change path"
---

# Database Query Optimizer

## Purpose and safety boundary

Optimize database performance from measured evidence, not intuition. Start with read-only inspection and a reproducible query shape. Do not run arbitrary customer queries, expose sensitive rows, change schemas, tune global configuration, kill sessions, or rebuild indexes in production without explicit authorization, a maintenance plan, and recovery evidence.

`EXPLAIN ANALYZE` executes a statement. Never run it against an untrusted write query or live production traffic without a reviewed transaction/rollback plan. Prefer a sanitized representative dataset, a read-only transaction where valid, or plain `EXPLAIN` when execution itself is unsafe.

## Inputs and baseline

Record database engine/version, schema and statistics freshness, query fingerprint, parameter class, dataset scale, concurrency, cache state, connection pool, replica role, and the exact environment. Capture:

- wall time and p50/p95/p99 latency under representative load;
- execution plan with estimates vs. actual rows, buffers/I/O, sort/hash spills, and parallelism;
- CPU, memory, I/O, cache hit rate, locks, deadlocks, connections, and replication lag;
- read/write mix, query frequency, business SLO, and acceptable change window.

Redact literals, identifiers, tokens, and customer data. Preserve the query fingerprint and enough shape to reproduce the issue.

## Workflow

1. **Reproduce safely.** Confirm the symptom and query fingerprint in a test or approved replica. Verify that the measured query is the same shape as the production hotspot.
2. **Read the plan.** Compare estimated and actual rows, scan type, join order, join method, filter selectivity, sort/hash memory, buffer hits/reads, and planning/execution time.
3. **Rank bottlenecks.** Separate stale statistics, missing/poor indexes, non-sargable predicates, bad cardinality, excessive rows, lock waits, connection pressure, I/O, and application-level N+1 behavior.
4. **Design one change.** Choose the smallest candidate: query rewrite, predicate/parameter correction, targeted index, statistics refresh, partition/pruning adjustment, pool/backpressure change, or configuration change. Explain why it addresses the evidence.
5. **Check side effects.** Estimate storage, write amplification, vacuum/maintenance, lock duration, replication, cache churn, plan stability, and compatibility with other queries. Reject redundant indexes and changes that trade an unmeasured regression for a local win.
6. **Validate in isolation.** Apply one approved change in a disposable or canary environment. Use a bounded representative workload and keep the previous plan and rollback steps.
7. **Compare fairly.** Repeat the same query class and workload, report warm/cold cache separately, and compare latency, rows, buffers, CPU/I/O, locks, writes, and replication. A lower planner cost alone is not success.
8. **Promote cautiously.** Use a reviewed migration or deployment path, observe the agreed window, and stop/rollback if SLO, write latency, lock time, error rate, or replication health worsens.
9. **Document and monitor.** Store before/after evidence, decision, scope, owner, expiry/review trigger, and a dashboard or alert for regression.

## Plan-reading cues

| Evidence | Questions to test |
|---|---|
| Large sequential scan | Is the table large, the predicate selective, and the data type/index expression compatible? |
| Estimated rows far below actual | Are statistics stale, correlated, skewed, or filtered after a join? |
| Nested loop with a large outer side | Is the inner lookup indexed and is the join order stable at production cardinality? |
| Sort/hash spills to disk | Is the query shape or per-operation memory budget appropriate, without unsafe global tuning? |
| High buffers read / low hit rate | Is the working set, access path, cache, or storage throughput the actual limit? |
| Lock waits or deadlocks | Which transaction holds the lock, what is the order, and can scope/duration be reduced safely? |
| Fast read but slow writes after an index | What is the write amplification, maintenance cost, and index usage over a representative window? |

## Safe inspection examples

Use placeholders and a reviewed environment; do not paste raw customer data.

```sql
-- PostgreSQL: inspect a plan without executing the query.
EXPLAIN (COSTS, BUFFERS, FORMAT TEXT)
SELECT id, total_amount
FROM orders
WHERE status = $1 AND created_at >= $2;

-- PostgreSQL: inspect index usage before proposing another index.
SELECT schemaname, relname, indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE relname = 'orders'
ORDER BY idx_scan ASC;

-- MySQL: inspect the optimizer's JSON plan.
EXPLAIN FORMAT=JSON
SELECT id, total_amount
FROM orders
WHERE status = ? AND created_at >= ?;
```

For an approved PostgreSQL index, prefer `CREATE INDEX CONCURRENTLY` where supported and plan for its longer build, failure cleanup, storage, and replica effects. Never assume a new index is useful until usage and write cost are measured.

## Optimization record

```text
Query fingerprint/environment: <sanitized shape and database>
Business SLO and evidence window: <target and UTC period>
Baseline: <latency, plan, rows, buffers, CPU/I/O, locks, replica health>
Root cause hypothesis: <evidence and confidence>
Single change: <query/index/statistics/config and scope>
Side effects: <writes, storage, locks, cache, replication, compatibility>
Rollback: <owner, trigger, and tested path>
After metrics: <same workload and warm/cold qualification>
Decision: keep | revert | inconclusive
Follow-up: <monitor, owner, date, review trigger>
```

## Handoff checklist

- [ ] Query shape, engine/version, environment, data scale, and sensitive data handling are explicit.
- [ ] Baseline includes execution evidence and system/replication health, not only planner cost.
- [ ] Root cause and proposed change are tied to plan evidence.
- [ ] Only one approved change is tested at a time with rollback available.
- [ ] Read-only versus executing plan analysis is deliberate and safe.
- [ ] Before/after comparisons use equivalent workload and account for cache state.
- [ ] Write amplification, locks, maintenance, replicas, and neighboring queries are checked.
- [ ] Result, residual risk, monitoring, owner, and review trigger are documented.
