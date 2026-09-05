---
name: "schema-design"
display_name: "数据库 Schema 设计"
display_name_en: "Database Schema Design"
description: "Use when designing or reviewing relational schema changes, initialization SQL, migrations, privileges, seed data, constraints, indexes, or schema tests; preserve authority boundaries and verify the real database contract."
description_zh: "用于设计或审查关系数据库 Schema、初始化 SQL、迁移、权限、种子数据、约束、索引或 Schema 测试，保持权限边界并验证真实数据库契约。"
description_en: "Design relational schemas with explicit initialization strata, constraints, ownership, least privilege, safe writers, approved seeds, and catalog-level validation without hiding invalid dependencies."
category: "development"
version: "0.1.0"
author: "iamthenop/infurnet-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized relational database repository with migration or initialization files, declared roles, and repository-native schema tests"
---

# Database Schema Design

Use this skill for schema changes, DDL, migrations, indexes, privileges, seed data, or database contract review. The committed schema and migration sources define the current shape; they are not a license to redesign unrelated tables. A work order, issue, or explicit change scope defines what may change. Read existing bindings, neighboring SQL, naming rules, migration order, roles, and tests first.

## Establish authority and boundaries

Record the target database, allowed files/objects, current version or initialization order, owners, application roles, writers, readers, affected services, data classification, and rollback plan. Separate facts from proposed behavior. Never invent principals, grants, seed identities, schema strata, or production data. Do not change multiple databases or rename/split service accounts without explicit authority for each.

Keep foundational invariants independent of later application layers. Separate structural definitions, audit observation, notifications, connection bootstrap, views/grants, mutation writers, and approved seeds according to the repository's declared strata. Do not introduce a new stratum, duplicate an object in two strata, or use conditional SQL to hide an ordering error.

## Design for database-enforced integrity

Use clear table and column names, primary/foreign keys, `NOT NULL`, `CHECK`, uniqueness, appropriate indexes, and explicit referential actions to enforce invariants. Application comments and hoped-for behavior are not substitutes for database constraints. Add an index only for a demonstrated access path, constraint, or concurrency requirement; verify with the repository's query plan evidence and avoid redundant or low-selectivity indexes.

Keep each object in one ownership boundary. An invariant trigger decides whether a mutation is valid; an audit trigger observes an accepted event without changing its outcome; a notification signals a committed fact but is not a durable record. A view exposes approved state; a purpose-built writer owns an approved mutation surface. Do not blur these roles or grant a read role mutation authority.

## Apply least privilege safely

Give application roles only the privileges required by their documented service boundary. Distinguish database/schema reachability from object access. Avoid broad `GRANT ALL`, persistent default privileges, or elevated role capabilities unless explicitly approved and bounded. For privileged writer functions, fix the search path, schema-qualify objects, revoke public execution, grant only to approved roles, and keep the function narrower than the owner's authority. Never put passwords, tokens, or connection secrets in schema files or reports.

## Preserve initialization and migration correctness

Initialization files run in a declared order: earlier files must not depend on later objects, and each object belongs to one stratum. Migrations should be forward-readable, idempotency expectations explicit, and destructive changes preceded by impact/data checks and a recoverable backup or rollback strategy. Use online or staged changes for large tables where the platform requires it. Preserve existing behavior unless the authorized change says otherwise.

Do not suppress SQL errors, skip a failed migration, add compatibility objects “just in case,” or claim a migration is safe because it worked on an empty database. Verify upgrade, fresh initialization, mixed-version behavior, backfill/restart, constraint validation, and rollback or compensating recovery with representative synthetic data.

## Control seeds and generated data

Seed records are changes to durable state. Require explicit approval for production seeds, roles, grants, policies, vocabulary, or service identities. Keep development fixtures separate from production baseline data. Do not invent principals or stable identifiers, and do not confuse generated test data with evidence that a production invariant is correct.

## Test the actual catalog

Use repository-native migration and schema tests against the real database engine or an approved equivalent. Verify tables, columns, types, defaults, constraints, foreign-key actions, indexes, triggers, functions, initialization boundaries, roles, privileges, and writer behavior. Include invalid writes, duplicate keys, missing references, privilege denial, transaction rollback, concurrent access, and representative query plans. A parser-only check cannot prove runtime permissions or trigger interaction.

## Handoff and stop conditions

Return the proposed object/stratum mapping, dependency direction, invariants, roles and grants, migration sequence, data/rollback plan, seed approvals, tests and exact evidence, compatibility risks, and unresolved decisions. For review findings include path/line, impact, proof, smallest safe correction, and regression check. Stop before mutation when target ownership, authorized scope, role authority, migration order, or destructive recovery is ambiguous.
