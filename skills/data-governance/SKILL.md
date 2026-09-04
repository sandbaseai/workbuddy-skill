---
name: "data-governance"
display_name: "数据治理"
display_name_en: "Data Governance"
description: "Use when defining data contracts, consent and suppression policies, identity resolution, lineage, quality monitoring, or change management for automation and cross-system data flows."
description_zh: "用于为自动化和跨系统数据流定义数据契约、同意与抑制策略、身份解析、血缘、质量监控和变更管理。"
description_en: "Govern cross-system and automation data flows with explicit contracts, ownership, consent, identity, lineage, quality signals, retention, incident response, and reversible change management."
category: "data"
version: "0.1.0"
author: "majiayu000; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Source systems, event/CRM/CDP pipelines, schema registry or catalog, consent store, monitoring, and data owners"
---

# Data Governance

Use this skill when data crosses products, automation journeys, CRM/CDP systems, analytics, or communication channels. Governance makes data use explainable and dependable: every important field has a purpose, owner, contract, quality signal, access rule, retention policy, and change path.

Do not send messages, make eligibility decisions, merge identities, or trigger destructive automation from unvalidated or stale data. Do not treat a schema existing as proof that its values are correct, consent is valid, or a downstream consumer can tolerate change.

## Map the flow and ownership

For each journey or pipeline record:

- business purpose, user/subject impact, source of truth, systems, destinations, regions, and data owner/steward;
- fields/events, classification, allowed purpose, consent/legal basis, retention, access roles, and deletion/rectification path;
- identity keys and join rules, transformations, derived fields, lineage, freshness target, quality thresholds, and fallback;
- consumers, side effects, vendor/subprocessor, incident route, change approver, and review cadence.

Use a data requirements matrix:

```text
journey | field/event | source | owner | purpose | consent | freshness | quality | fallback | destination
```

Prefer the minimum fields needed. Keep sensitive values out of logs and examples, use opaque identifiers, and document when an aggregate or bucket is sufficient.

## Write enforceable data contracts

A contract specifies field names/types, required versus optional values, semantic definitions, units/timezone, allowed values, key/grain, event ordering, freshness, retention, compatibility, owner, and failure behavior. Version contracts and publish deprecation windows. Validate producer output at ingestion and consumer assumptions in CI or contract tests.

Test null and unknown rates, duplicate keys, cardinality, referential integrity, timestamps, late/out-of-order events, volume, distribution drift, schema additions/removals, and reconciliation to an authoritative total. A pipeline that runs successfully but silently drops records has failed its contract.

For automation, define a safe fallback for stale, missing, ambiguous, or contradictory data: pause or reduce scope, queue for review, or use a documented conservative default. Add a kill switch for critical-field freshness/quality failure. The switch must be owned, audited, bounded, tested, and reversible; it must not bypass authorization or privacy policy.

## Consent and suppression

Maintain a consent policy per channel, region, purpose, subject, timestamp, policy/version shown, source, grant/deny/withdrawal, and expiry or revalidation rule. Separate product, analytics, marketing, transactional, and third-party purposes. Enforce consent at the last responsible step before a send or side effect, not only at signup.

Maintain suppression and do-not-contact signals with precedence, propagation SLA, vendor fan-out, retry behavior, and deletion/access handling. Test opt-in, opt-out, withdrawal, region change, expired consent, duplicate identity, queued work, retries, and delayed replication. Never log full message payloads or use a suppressed record as a test fixture without redaction.

## Identity resolution

Define canonical identifiers, namespace, confidence, source priority, merge/split rules, tenant boundary, and audit history. Do not merge records on a weak attribute alone or let a guessed identity grant access or trigger a consequential action. Preserve provenance for every match and make uncertain matches reviewable.

Test duplicate creation, changed email/phone, shared devices, deleted users, account transfers, cross-tenant collisions, anonymous-to-known transitions, late events, and replay. Ensure consent, suppression, retention, and access controls follow the correct subject through merges and splits.

## Monitor quality and lineage

Provide dashboards and alerts for freshness, latency, volume, null/unknown rate, duplicates, schema changes, reconciliation, identity-match confidence, consent propagation, suppression failures, and downstream side effects. Each alert needs a threshold, owner, runbook, escalation, and an action; remove noisy signals that cannot change a decision.

Track lineage from source field to transformed field to consumer and vendor. Record schema/contract version, job/build, policy version, and data-quality result in a safe audit trail. Preserve enough evidence to explain a decision without retaining unnecessary personal data.

## Change and incident management

Classify changes as additive, semantic, quality, identity, retention, access, or breaking. For each change compare consumers, migration order, backfill/replay behavior, consent impact, cost, and rollback/roll-forward. Use expand-and-migrate for breaking contracts and communicate owner, deadline, compatibility window, and removal criteria.

When quality or consent fails, stop affected automation, contain the smallest safe scope, preserve evidence, identify impacted records and destinations, repair or replay idempotently, and verify recovery. Run a blameless RCA for recurring or material failures. An action item needs an owner, due date, measurable outcome, and follow-up check.

## Governance review

- Purpose, classification, ownership, lineage, retention, and access are documented.
- Contract, identity, freshness, quality, reconciliation, and fallback behavior are testable.
- Consent and suppression are purpose/channel/region aware and verified at side-effect time.
- Critical failures have bounded kill switches, escalation, audit evidence, and recovery tests.
- Changes have compatibility, migration, communication, and removal plans.
- Consumers and vendors have acknowledged definitions, SLAs, and incident routes.

Report the flow map, requirements matrix, contract/version, quality evidence, consent/suppression state, identity decisions, findings, owners, exceptions, and next authorized action. Stop when purpose, ownership, subject identity, consent, or fallback is ambiguous.
