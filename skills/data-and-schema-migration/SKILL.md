---
name: "data-and-schema-migration"
display_name: "数据与模式迁移"
display_name_en: "Data and Schema Migration"
description: "Use when changing a persisted database schema, configuration shape, event contract, or serialized format that existing data or running versions already use; design compatibility, backfill, cutover, and recovery before mutation."
description_zh: "安全迁移数据库、配置和序列化格式，通过兼容扩展、幂等回填、分阶段切换和可验证恢复保护已有数据。"
description_en: "Safely migrate databases, configuration, and serialized formats through compatible expansion, idempotent backfills, staged cutover, and verifiable recovery."
category: "data"
version: "0.1.0"
author: "Kushagra Bainsla; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Data and Schema Migration

Use this skill for persisted database tables, configuration, messages/events, indexes, and serialized on-disk formats. The invariant is: old data must remain readable during the supported transition, and every destructive step must have verified prerequisites and a recovery path.

Do not use it for code-only symbol renames. Do not assume a database transaction can reverse an external side effect, a large backfill, or a destructive data transformation.

## Establish the migration contract

Before changing data, record:

- current and target schemas, invariants, volume, growth, ownership, and retention;
- readers and writers, including jobs, older application versions, replicas, consumers, exports, caches, and recovery tooling;
- compatibility window and deployment order;
- data sensitivity, regulatory constraints, availability budget, and acceptable lag;
- objective completion checks, abort thresholds, and who may authorize cutover or destructive cleanup.

Inspect representative production-shaped data safely. Include nulls, duplicates, invalid legacy values, maximum sizes, different encodings/time zones, and partially migrated records. Redact sensitive samples and do not copy production data into an uncontrolled environment.

## Prefer expand, migrate, contract

1. **Expand:** add backward-compatible fields, tables, indexes, or readers. Avoid renaming, narrowing, dropping, or changing semantics in place.
2. **Deploy compatibility:** make readers tolerate old and new shapes. If dual writes are necessary, define the source of truth, ordering, retries, idempotency key, and reconciliation process.
3. **Backfill:** use deterministic, restartable batches with checkpoints, bounded load, progress metrics, and dead-letter handling. Do not treat “rows processed” as proof of correctness.
4. **Verify:** compare counts, checksums or aggregates, constraints, sampled records, application reads, and business invariants. Account for writes that occurred during the backfill.
5. **Cut over:** switch reads or ownership gradually when possible. Observe error rate, latency, replication lag, resource saturation, and correctness signals against explicit thresholds.
6. **Contract:** remove old paths only after the compatibility window closes, all known consumers migrate, recovery is proven, and the authorized owner approves the irreversible step.

For files or local configuration, use the same pattern through read-old/write-new support, atomic replacement, preserved permissions, version markers, and recoverable backups.

## Safety and recovery

- Make schema changes and migration steps idempotent or explicitly detect completed work.
- Test from a snapshot of pre-existing data and test interruption/resumption at multiple checkpoints.
- Prefer online/concurrent operations supported by the actual engine; verify lock behavior and disk requirements rather than inferring them.
- Backups are useful only when restore scope, credentials, integrity, and recovery time have been tested.
- Never run a production migration, delete data, drop compatibility paths, pause consumers, or alter retention without explicit authorization for that environment and operation.
- Stop on invariant violations, unexpected error or lag growth, lost reconciliation coverage, or resource pressure beyond the agreed threshold.

Rollback code when it is safe, but do not promise rollback after an irreversible schema or data change. Define roll-forward and repair procedures for that case.

## Handoff

Report the schema versions, completed phase, commands or migration identifiers, evidence, batch/checkpoint state, compatibility status, residual mismatches, monitoring links, abort thresholds, recovery procedure, owners, and next authorized step. Completion requires old and new supported data to load correctly, repeated execution to be safe, reconciliation to pass, and recovery evidence to exist—not merely a successful migration command.
