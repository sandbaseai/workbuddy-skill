---
name: "kafka-engineering"
display_name: "Kafka 事件流工程"
display_name_en: "Kafka Event Streaming Engineering"
description: "Use when designing, implementing, reviewing, migrating, or diagnosing Apache Kafka producers, consumers, topics, schemas, delivery semantics, transactions, replay, or cluster-facing application behavior."
description_zh: "设计、实现、审查、迁移和诊断 Apache Kafka 生产者、消费者、主题、Schema、交付语义、事务、重放与集群交互。"
description_en: "Design, implement, review, migrate, and diagnose Apache Kafka producers, consumers, topics, schemas, delivery semantics, transactions, replay, and cluster-facing behavior."
category: "development"
version: "0.1.0"
author: "ssrjkk; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Kafka Event Streaming Engineering

Use this skill for Kafka client code, event contracts, topic and partition design, consumer groups, Kafka Connect or Streams integrations, migrations, incidents, and production-readiness reviews. Inspect the application language and client version, broker mode and version, security configuration, topic settings, schema system, deployment topology, and existing operational practices before changing anything. Preserve the user's chosen client, serialization format, and platform unless replacement is requested.

## Define the event contract first

For each event, record its business meaning, producer, authoritative source, immutable event identifier, event time, schema identity and version, partition key, ordering scope, retention or compaction expectation, sensitivity, consumers, and compatibility policy. Distinguish facts that happened from commands requesting work and snapshots describing current state.

Do not rely on global ordering: Kafka orders records only within a partition. Select a stable key whose ordering and load-distribution consequences match the business invariant. Null or changing keys can silently break entity ordering. Detect skew and hot partitions using per-partition rate, size, lag, and processing-time distributions.

Treat headers, keys, schemas, tombstones, and null values as contract surfaces. Redact secrets and regulated data from event payloads, headers, keys, logs, dead-letter records, and tracing attributes. Retention is not erasure; document deletion and compaction limits before placing personal data on a topic.

## Choose explicit delivery semantics

State the end-to-end guarantee, not only producer settings:

- At-most-once accepts loss to avoid duplicate processing.
- At-least-once requires idempotent effects or durable deduplication.
- Kafka transactions can atomically consume and produce within compatible Kafka flows, but do not make arbitrary databases, HTTP calls, emails, or payments exactly once.

Enable idempotent production and compatible acknowledgement, retry, and in-flight settings when duplicate suppression and ordering are required. Use a stable transactional identity per producer instance when transactions apply, fence abandoned producers, commit offsets with produced output in the same transaction, and configure consumers to avoid exposing aborted records. For database-to-Kafka publication, prefer an outbox plus change-data capture or another durable reconciliation mechanism over an unsafe dual write.

Make downstream side effects idempotent with a business operation key, uniqueness constraint, compare-and-set, or durable inbox. Bound deduplication retention by the maximum replay and retry window; an in-memory set is not durable proof.

## Engineer producers

Budget serialization, batching, queueing, broker acknowledgement, retry, and delivery timeout inside the caller's deadline. Define backpressure when the local buffer is full. Retries must preserve the intended ordering and must not exceed the event's usefulness window.

Classify errors as retriable, authorization/configuration, serialization/contract, record-too-large, fenced transaction, or ambiguous outcome. Do not retry permanent failures forever. Report delivery using broker acknowledgement and topic/partition/offset metadata rather than treating a successful client enqueue as publication.

Validate message size against client, broker, topic, replica-fetch, and downstream limits. Prefer storing large objects in controlled object storage and publishing an integrity-checked reference when that fits the security and lifecycle contract.

## Engineer consumers

Set group identity deliberately; changing it changes ownership and offset history. Define start position for a new group, offset reset behavior when history is unavailable, maximum processing time, poll cadence, batch size, concurrency, per-partition ordering, and shutdown behavior.

Commit an offset only after the corresponding work is durably complete. For batches, track per-partition completion so a later record cannot hide an earlier failure. Pause and resume partitions when downstream capacity is exhausted; do not keep polling unbounded work into memory. Ensure processing and heartbeat settings tolerate expected work, or move long-running work behind a durable handoff.

Handle cooperative or eager rebalances according to client support. On revocation, stop admitting work, finish or abandon it under a bound, commit only completed offsets, and release partition-scoped state. On assignment, initialize state before processing. Verify that instance count and consumer concurrency do not promise more useful parallelism than partition count.

## Handle poison records and retry

Separate transient dependency failures from invalid schemas, unsupported versions, authorization failures, and deterministic business rejection. Use bounded retries with jitter and an overall age or attempt limit. Retry topics change ordering and must carry original topic, partition, offset, event identity, schema, attempt, first-failure time, and sanitized reason.

A dead-letter topic is quarantine, not completion. Define access control, retention, alerting, triage owner, correction policy, replay tooling, idempotency, and audit trail. Never skip or replay records silently. Preserve enough immutable context to reproduce the decision without leaking sensitive payloads.

## Evolve schemas and topics

Check compatibility using the actual registry or consumer contract, not intuition. Additive changes are not automatically safe: defaults, semantic constraints, enum values, required fields, numeric ranges, and generated-client behavior matter. Test old producer/new consumer and new producer/old consumer combinations required during deployment.

Treat partition-count increases as an ordering and key-to-partition remapping change. Treat replication factor, min in-sync replicas, unclean leader election, cleanup policy, retention, compaction, and quotas as availability or data-lifecycle decisions. Do not alter or delete production topics, reset offsets, reassign partitions, elect preferred leaders, or change ACLs without explicit authorization, exact targets, an impact estimate, and recovery steps.

## Diagnose with correlated evidence

Locate the earliest failing stage: serialization, client buffer, metadata, DNS/TLS/SASL, authorization, leader selection, broker append, replication, fetch, deserialization, group assignment, processing, side effect, offset commit, or retry/replay. Capture broker and client versions, sanitized configuration, topic and group, partition and offset, timestamps, correlation/event identifiers, error class, lag components, rebalance history, and recent deploy or configuration changes.

Consumer lag is an offset distance, not directly a time duration or root cause. Compare arrival rate, processing rate, records-lag-max, per-partition skew, fetch latency, processing latency, errors, pauses, rebalances, downstream saturation, and disk/network/broker health. Distinguish producer timestamp, broker append time, fetch time, processing start, side-effect completion, and commit time.

Avoid destructive offset resets or topic recreation as diagnosis. If a reset or replay is authorized, snapshot current group offsets, calculate exact target offsets and record counts, isolate side effects, canary a bounded range, observe results, and retain a rollback or forward-repair plan.

## Validate and hand off

Test schema compatibility, partition determinism, duplicate delivery, update ordering, producer retry, broker failover, consumer crash before and after side effects, rebalance during processing, poison records, downstream slowdown, cache or database outage, replay, deployment overlap, and graceful shutdown as applicable. Verify observable end-to-end business outcomes, not only record movement.

Return the event and delivery contracts, exact configuration changes, assumptions, broker/client/schema versions, test evidence, throughput and latency distributions, partition balance, failure and recovery results, rollout and rollback plan, monitoring and alert thresholds, replay ownership, and unresolved correctness or privacy risks.
