---
name: "mysql"
display_name: "MySQL 数据库操作"
display_name_en: "MySQL Database Operations"
description: "Use when inspecting a MySQL schema, writing or reviewing queries, diagnosing plans, designing indexes, or preparing database changes; default to read-only analysis and require explicit production mutation authority."
description_zh: "安全地检查 MySQL 模式、编写和验证查询、分析执行计划、设计索引，并对生产变更设置明确授权和恢复边界。"
description_en: "Safely inspect MySQL schemas, write and validate queries, analyze execution plans, design indexes, and bound production changes with explicit authorization and recovery."
category: "data"
version: "0.1.0"
author: "ssrjkk; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# MySQL Database Operations

Use this skill for MySQL-specific schema, query, indexing, transaction, and operational work. Establish the actual server version, SQL mode, storage engine, character set/collation, topology, and environment before relying on version-dependent behavior.

## Discover before querying

Prefer repository migrations, schema definitions, ORM mappings, and read-only metadata queries. Confirm table grain, primary and unique keys, foreign keys, nullability, generated columns, partitions, indexes, data volume, and relationships. Do not infer physical column names from application fields.

Protect credentials and row data. Never print connection strings, secrets, full customer records, or unnecessary personal data. Use the least-privileged account and a non-production or read replica when that satisfies the task.

## Write correct, bounded queries

- Select named columns rather than `SELECT *` when the contract is known.
- Use typed parameters for values; never concatenate untrusted input into SQL identifiers or expressions.
- Make join cardinality explicit and check for multiplication before aggregating.
- Handle `NULL`, time zones, collations, precision, and inclusive/exclusive time bounds deliberately.
- Add deterministic ordering for pagination or repeatable extracts. Prefer keyset pagination for large mutable sets when applicable.
- Bound exploratory reads with selective predicates and a limit, but do not add a limit that silently changes a required aggregate or completeness guarantee.

Validate results with counts, denominators, edge cases, and an independent calculation where the decision is material.

## Analyze performance safely

Use the least invasive available plan command. Prefer `EXPLAIN` or documented non-executing formats; use `EXPLAIN ANALYZE` only when executing the statement and its workload is authorized and bounded. Inspect estimated versus actual rows, access type, chosen and possible keys, join order, temporary tables, sorting, covering behavior, and predicate selectivity.

An index is a tradeoff. Evaluate column order, equality/range predicates, ordering, covering needs, prefix length, write amplification, storage, lock/build behavior, redundant indexes, and actual workload frequency. Do not assert that every filter or join column needs its own index.

## Control mutations and transactions

Before `INSERT`, `UPDATE`, `DELETE`, DDL, lock, maintenance, replication, or configuration changes, confirm the target environment, affected-row estimate, authorization, transaction/locking behavior, backup or rollback path, and observable stop conditions. Preview the exact target set with a read-only query when possible.

Use transactions according to the actual engine and operation; do not assume all DDL or external effects roll back. Keep transactions short, use stable predicates, check deadlock/retry behavior, and verify affected rows before commit. For schema/data migrations, use a staged compatibility approach rather than destructive in-place changes.

Never execute production mutations, create/drop indexes, change users or privileges, alter replication, kill sessions, or modify server configuration without explicit authorization for that operation and environment.

## Handoff

Return the SQL or change plan, assumptions, schema/version evidence, parameters, expected cardinality, plan findings, safety boundary, and verification steps. If execution was authorized, include environment, timestamp, affected rows, transaction outcome, before/after evidence, residual risk, and recovery state. A successful command is not enough; verify the requested data or operational outcome.
