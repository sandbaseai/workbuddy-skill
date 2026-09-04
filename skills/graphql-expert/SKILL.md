---
name: "graphql-expert"
display_name: "GraphQL API 设计与审查"
display_name_en: "GraphQL API Design and Review"
description: "Use when designing, implementing, or reviewing a GraphQL schema or operation; ground the contract in real client workflows and check resolver correctness, authorization, pagination, cost, performance, and safe evolution."
description_zh: "从真实客户端需求出发设计和审查 GraphQL 模式、解析器、授权、分页、错误、性能与演进兼容性。"
description_en: "Design and review GraphQL schemas, resolvers, authorization, pagination, errors, performance, and evolution compatibility from real client needs."
category: "development"
version: "0.1.0"
author: "candeploys; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# GraphQL API Design and Review

Use this skill for GraphQL-specific contracts and execution behavior. Inspect the repository's schema, resolver layer, data model, authorization policy, client operations, federation configuration, and runtime/version constraints before proposing changes. Do not substitute generic REST conventions for observed GraphQL behavior.

## Ground the graph in client workflows

Start with concrete operations clients need to perform and the identities allowed to perform them. Record the object graph, ownership boundaries, stable identifiers, nullability guarantees, expected list sizes, consistency needs, and downstream data sources. Separate requirements supported by code or product evidence from assumptions.

Model domain concepts rather than storage tables. Prefer cohesive object types, explicit inputs, and reusable interfaces only when consumers benefit. Use enums for closed sets and custom scalars only with documented serialization and validation. Nullability is a compatibility promise: make a field non-null only when every execution path can supply it, including authorization failures, partial dependency failures, and legacy data.

## Design operations and errors

Queries should expose the data a client needs without encoding a UI layout into the schema. Mutations should describe a domain action, accept a single named input when evolution is likely, return the affected entity or a purposeful payload, and specify idempotency or retry behavior where duplicate execution is harmful.

Choose one pagination contract per connection. For mutable or large ordered sets, prefer opaque cursors backed by a deterministic, unique order. Define filters, sort fields, maximum page size, empty results, deleted cursor behavior, and snapshot/consistency limitations. Never imply that an opaque cursor is a stable business identifier.

Use GraphQL errors and typed domain results deliberately. Distinguish transport failure, parse/validation failure, authorization denial, domain rejection, and partial field failure. Do not leak stack traces, internal identifiers, secrets, or sensitive existence through error text.

## Enforce security at execution time

Authentication establishes identity; authorization must be enforced for the object, field, action, and tenant represented by each resolver path. Do not rely on a field being absent from a client query, UI hiding, or a parent resolver's check when a nested resolver can be reached another way.

Validate inputs, bound list and text sizes, and control introspection according to the environment and threat model. Apply depth, breadth, alias, recursion, and complexity limits based on measured resolver cost. Rate limits should account for operation cost and caller identity rather than treating every document as equal. Persisted or allowlisted operations can reduce exposure, but only if registration and versioning are controlled.

## Implement predictable resolvers

Keep resolver responsibilities clear: validate and authorize, coordinate domain services, map results to the schema, and preserve request context. Avoid hidden writes in queries. Make transaction boundaries and side effects explicit for mutations.

Detect N+1 behavior with resolver-level evidence. Batch and cache only within an appropriate scope—commonly a single request—and include tenant, authorization context, locale, or other result-shaping dimensions in cache keys. Preserve input-to-output ordering and represent missing rows safely. Do not use a global loader cache for user-specific data.

For subscriptions, define authentication at connection and operation time, reauthorization for long-lived sessions, event filtering, ordering, replay expectations, backpressure, disconnect recovery, and resource limits. Do not promise exactly-once delivery unless the complete transport and consumer protocol proves it.

## Measure and evolve safely

Capture operation name or persisted-operation ID, duration, error outcome, resolver hotspots, dependency time, and sampled traces without logging raw variables or sensitive response data. Monitor validation failures, rejected complexity, cache/load batching behavior, subscription counts, and schema usage. Anonymous operations and uncontrolled cardinality reduce diagnostic value.

Treat field and argument removal, type changes, enum changes, and tighter nullability as potentially breaking. Prefer additive changes and deprecation with a reason and replacement. Check actual operation registries or client documents before removal; schema validation alone cannot prove consumer compatibility. In federation, also validate entity keys, ownership, shareability, composition, and cross-subgraph execution plans against the deployed router version.

## Verify

Test parse and validation behavior, successful and denied authorization paths, null propagation, partial failures, pagination boundaries, duplicate mutations, batch behavior, cost controls, and representative client operations. Measure query count and latency with realistic cardinality rather than claiming an N+1 or performance fix from code shape alone.

Return the proposed schema or finding, client workflow, evidence and assumptions, compatibility impact, security boundary, resolver/data-source plan, performance measurements, test coverage, rollout or deprecation plan, and unresolved risks. Clearly state when repository access, runtime telemetry, client operations, or production authorization was unavailable.
