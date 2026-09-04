# Cached-value Contract

Use this reference when value meaning, key scope, freshness or invalidation can change correctness.

For each cached value record authority and revision, representation and serializer version, complete key dimensions, fresh and maximum ages, fill owner and publish condition, mutation invalidation path, duplicate-fill or fencing policy, degraded behavior and falsifier.

Canonicalize equivalent inputs and version incompatible namespaces. Include every response-varying tenant, principal, authorization or policy, locale, representation and query dimension. Do not put credentials, tokens or raw personal data in keys or logs. When current policy cannot be invalidated reliably, cache authority-independent data and apply policy after retrieval.

Classify a served value as `fresh`, `allowed-stale`, `forbidden-stale` or `unknown-age`. Age starts at authoritative generation or validation, not local insertion. Treat authoritative not-found separately from timeout, permission denial and dependency failure. A negative result needs bounded lifetime and create-time supersession.

Commit the authoritative mutation before publishing invalidation. Reject an older in-flight fill after a newer mutation using a revision, generation or fencing check. TTL limits damage but does not replace invalidation. If missed invalidation can exceed the maximum safe age, require durable delivery, monitoring and reconciliation ownership.
