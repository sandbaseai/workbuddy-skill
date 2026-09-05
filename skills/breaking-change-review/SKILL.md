---
name: "breaking-change-review"
display_name: "破坏性变更审查"
display_name_en: "Breaking Change Review"
description: "Use when reviewing changes to public APIs, events, configuration, feature flags, CLI behavior, schemas, or migrations for compatibility impact."
description_zh: "用于审查公共 API、事件、配置、Feature Flag、CLI 行为、Schema 或迁移变更的兼容性影响。"
description_en: "Perform a diff-first compatibility review across producers, consumers, persisted data, and operational rollout; identify breaking behavior and missing migration evidence; and recommend a versioned, reversible handoff without silently approving risk."
category: "development"
version: "0.1.0"
author: "aydabd/github-bootstrap; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized repository, public contracts and consumers, change diff, compatibility policy, migration or rollout plan, and repository-native tests"
---

# Breaking Change Review

Determine whether a proposed change breaks an existing consumer, contract, data assumption, or operational procedure. Review the actual diff and surrounding evidence; do not call a change safe merely because it compiles or a unit test passes. If the compatibility promise is unknown, state the uncertainty and route it to the contract owner.

## Map the contract surface

Identify the changed artifact and every boundary it crosses: HTTP/RPC APIs, SDKs, events and queues, webhooks, files, database schemas, configuration, environment variables, CLI flags and output, feature flags, permissions, generated clients, dashboards, runbooks, and external integrations. Inventory producers, consumers, versions, rollout cohorts, data states, and deprecation policy. Search repository documentation, tests, schemas, and deployment configuration for implicit consumers; mark unverified dependencies.

## Inspect compatibility dimensions

Check for:

- removed or renamed fields, endpoints, commands, flags, environment variables, events, scopes, or configuration keys;
- changed defaults, requiredness, nullability, enum values, formats, ordering, status codes, error shapes, pagination, timeouts, or retry semantics;
- narrowed accepted input, broadened or changed output, altered authorization, tenant behavior, idempotency, rate limits, or side effects;
- event and webhook shape changes, delivery ordering, replay behavior, schema evolution, consumer lag, and dual-read/dual-write needs;
- persistence, serialization, indexes, backfills, data loss, downgrade behavior, and old binaries reading new data;
- feature-flag targeting, mixed-version behavior, cache compatibility, generated artifacts, observability queries, and operational procedures.

Classify each change as additive-compatible, conditionally compatible, breaking, or unknown under the stated policy. Consider old clients with new servers, new clients with old servers, mixed deployments, retries, partial rollout, rollback, and restored backups. Verify claims against contract tests, consumer fixtures, schema diffs, migration tests, telemetry, and actual implementation where available.

## Require a safe migration path

For a breaking or conditionally compatible change, define the smallest safe sequence: introduce an additive form, support old and new consumers, migrate or backfill data, observe adoption and errors, deprecate with a dated owner-backed plan, remove only after evidence, and retain rollback or recovery steps. Specify versioning, compatibility window, feature-flag defaults, rollout waves, kill switch, success and abort thresholds, communication, and post-release cleanup. Do not recommend a flag as a substitute for a contract or migration plan.

If a change is intentionally breaking, require an owner, affected-consumer inventory, version or release boundary, migration instructions, deadline, acceptance tests, and explicit approval. If no consumer evidence exists, report that as an unknown rather than assuming there are none.

## Report findings and hand off

For each finding record severity, contract and location, old behavior, new behavior, affected producer/consumer or data state, evidence, preconditions, compatibility direction, recommended fix, migration or rollback step, owner, and retest. Separate confirmed breaks, likely risks, observations, and unknowns. Avoid secrets and customer data in the report.

The final handoff includes scope, contract inventory, compatibility matrix, diff evidence, classification, consumer and data impact, migration sequence, rollout and rollback gates, deprecation/communication plan, tests run and gaps, approvals required, and the exact release gate. Re-run the review when the contract, consumer set, migration, or rollout plan changes.
