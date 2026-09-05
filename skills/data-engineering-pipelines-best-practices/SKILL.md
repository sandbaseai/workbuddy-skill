---
name: "data-engineering-pipelines-best-practices"
display_name: "数据工程流水线实践"
display_name_en: "Data Engineering Pipeline Best Practices"
description: "Design, operate, and review reliable data pipelines with explicit contracts, idempotent processing, quality gates, lineage, privacy, observability, and safe recovery."
description_zh: "通过明确契约、幂等处理、质量门禁、血缘、隐私、可观测性和安全恢复来设计与审查数据流水线。"
description_en: "Design, operate, and review reliable data pipelines with explicit contracts, idempotent processing, quality gates, lineage, privacy, observability, and safe recovery."
category: "development"
version: "0.1.0"
author: "Hermes Agent; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Data Engineering Pipeline Best Practices

Use this skill when designing, reviewing, debugging, or operating batch, stream,
ELT, or event-driven data pipelines. A pipeline is a product with producers,
consumers, contracts, freshness expectations, privacy obligations, and recovery
behavior—not just a sequence of jobs. Do not claim data quality or freshness
without evidence from the actual run and a defined baseline.

## Define the data contract

Record the business purpose, source and destination owners, schema and semantic
definitions, expected volume, freshness, latency, retention, lineage, allowed
consumers, and sensitivity classification. For every field that matters, define
type, nullability, units, validity range, identity or deduplication key, and
whether it may contain personal or confidential data.

Specify delivery semantics and failure behavior: at-most-once, at-least-once,
or effectively exactly-once; ordering scope; watermark; late-arrival policy;
replay window; checkpoint; retry and dead-letter handling; and what is
authoritative after a partial run. Version contracts deliberately and define
backward and forward compatibility before producers or consumers change.

## Build for correctness and recovery

- Make writes idempotent with stable run, event, or record keys; bound retries
  and prevent duplicate side effects.
- Separate raw, validated, transformed, and published layers where that makes
  provenance and reprocessing explicit; keep source records immutable when
  policy permits.
- Validate schema, required fields, ranges, uniqueness, referential integrity,
  volume, distribution, freshness, and reconciliation totals at meaningful
  boundaries. Route bad data safely without silently dropping it.
- Make backfills bounded, resumable, observable, and isolated from current
  traffic; document how they interact with incremental processing and deletes.
- Protect secrets and sensitive data in storage, logs, samples, notebooks,
  exports, temporary files, and failure payloads. Enforce tenant and purpose
  boundaries in queries and shared datasets.

Do not bypass quality checks, overwrite the only copy, purge a dead-letter
queue, or run an unbounded backfill to make a dashboard green. Production
mutations require explicit authorization, a recovery point, a stop condition,
and a rollback or compensating-action plan.

## Operate and observe

Give each pipeline and stage an owner, run identifier, source watermark,
destination version, code/config revision, and correlation path. Monitor user-
meaningful outcomes as well as job status:

- freshness and completeness against declared thresholds;
- volume, duplicates, nulls, invalid values, distribution and reconciliation;
- processing latency, backlog, throughput, resource pressure, cost, and retry
  or dead-letter rate;
- schema drift, lineage breakage, access violations, and sensitive-data leaks;
- deployment, dependency, checkpoint, storage, and credential failures.

Alerts need severity, owner, evaluation window, routing, deduplication, missing-
data behavior, and a tested runbook. A successful task does not prove that the
published dataset is complete or correct; verify independently at the consumer
boundary.

## Validate changes

1. Test representative happy paths, empty inputs, malformed records, duplicates,
   late events, reordering, retries, partial writes, and replay.
2. Compare before/after counts, key aggregates, schema, freshness, lineage, and
   privacy controls using a known-good fixture or bounded production sample.
3. Verify restart, checkpoint recovery, backfill isolation, cancellation,
   rollback, and downstream compatibility.
4. Record test data, run IDs, query or command, observed result, limitations,
   and the sign-off owner.

## Handoff format

```text
Pipeline / purpose / owners / revision:
Sources, destinations, contracts, lineage, and sensitivity:
Delivery semantics, keys, watermarks, retries, and replay:
Quality rules and observed evidence:
Freshness / completeness / correctness / cost signals:
Failure, checkpoint, backfill, rollback, and recovery behavior:
Security, privacy, and access controls:
Findings / severity / confidence / owner:
Rollout, monitoring, sign-off, and next review:
```

Separate observed facts from assumptions and recommendations. A pipeline is
ready when its data contract, quality evidence, ownership, recovery path, and
consumer impact are explicit and reproducible.
