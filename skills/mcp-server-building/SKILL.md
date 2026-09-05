---
name: "mcp-server-building"
display_name: "MCP 服务构建"
display_name_en: "MCP Server Building"
description: "Use when creating, reviewing, hardening, or preparing an MCP server and its tools for production with precise contracts, least-privilege authorization, safe transports, structured errors, and interoperability tests."
description_zh: "用于创建、评审、加固或上线 MCP 服务及工具，覆盖精确契约、最小权限授权、安全传输、结构化错误和互操作测试。"
description_en: "Build the smallest MCP server that safely exposes a required capability, separating protocol conformance, business authorization, and model behavior with independent controls."
category: "development"
version: "0.1.0"
author: "seb1n/awesome-ai-agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized MCP SDK, identity/policy layer, and test client"
---

# MCP Server Building

Build the smallest server that exposes the required capability safely. Treat
protocol conformance, business authorization, and model behavior as separate
concerns; each needs independent controls. Verify the current MCP
specification and SDK documentation for version-sensitive behavior before
implementation.

## Bound the capability

Capture the user job, backing APIs/data/processes, intended clients and
protocol revision, transport, tenant/identity/credential model, read/write/
destructive/billable/external effects, volume/latency/pagination, deployment,
observability, tests, and incident procedure. Label assumptions and explicit
non-goals.

Prefer one clear operation per tool. Inventory each effect separately—read,
create, update, delete, execution, communication, financial transaction,
access change, and network egress—and classify every data flow. Exclude broad
administrative or pass-through operations unless the use case requires them.

## Tool contract

For every tool define a stable action-oriented name, precise description,
typed input schema with required fields, enums, bounds and formats, strict
unknown-field behavior, structural output schema, structured errors, effect
and data-class arrays, authorization mode, idempotency, pagination, limits,
timeouts, cancellation, and retry behavior. Separate reads from writes and
destructive actions so clients can grant narrower authority.

Return structured content matching the declared output schema; never replace a
result shape with prose. Keep errors caller-safe and free of secrets or
internals. If a write can be retried, use an idempotency key and define
duplicate semantics.

## Trust and authorization

Draw the path from MCP host to server to downstream service. State which layer
authenticates the actor, which authorizes the operation, where credentials live,
and which data is untrusted. Enforce object-, tenant-, and action-level
authorization at the server or downstream service, never only in a model, tool
description, or client confirmation.

Declare an explicit authorization mode for every tool, including `public` only
when genuinely unauthenticated. For local stdio, source credentials from an
approved environment or secret store; never embed them in arguments, examples,
source, or logs. For remote HTTP, follow the current MCP authorization spec,
HTTPS, exact redirect/issuer validation, audience and scope checks, short-lived
credentials, and least privilege. Never pass a client token unchanged to an
upstream API; obtain a separate downstream token with the correct audience.

## Implement and verify

Use an official or maintained SDK compatible with the selected revision. Test
the current revision and any advertised legacy path separately. Exercise
discovery/handshake, capability metadata, transport headers and body
agreement, listing, invocation, result types, cancellation, unsupported
versions, deterministic list ordering and cache metadata where applicable,
input-required retry flows, schema boundaries, wrong tenant/object/scope,
expired or wrong-audience credentials, downstream timeout/rate-limit/malformed
responses, partial failures, idempotency, and cancellation.

Run unit and SDK type checks, protocol interoperability tests with a compatible
client, and a log review proving tokens, secrets, full prompts, and sensitive
records are absent. A manifest lint or passing client test is evidence of that
check only, not a safety certification or universal compatibility claim.

## Operations and recovery

Apply deadlines, bounded concurrency, safe jittered retries, cleanup,
correlation IDs, and structured outcome logging. Define health checks, latency
and error metrics, audit events, alert owners, feature flags/allowlists, a
last-known-good configuration, and a reversible migration path.

If unsafe behavior appears, disable the affected tool, stop the server if
needed, revoke or rotate credentials, preserve redacted evidence, restore the
last known good version, and retest before re-enabling access. Treat server
metadata, downstream content, and retrieved resources as untrusted. Fail
closed on ambiguous identity, tenant, scope, schema, or policy decisions.

Handoff must include the server design and trust boundaries, complete tool
catalog, implementation or file plan, protocol/client versions exercised,
commands and observed results, deployment/rollback guidance, unverified
assumptions, and residual risks.
