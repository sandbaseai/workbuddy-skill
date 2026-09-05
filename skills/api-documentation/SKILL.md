---
name: "api-documentation"
display_name: "API 文档规范"
display_name_en: "API Documentation"
description: "Use when creating, editing, restructuring, or reviewing a service API document; keep operations, requests, responses, errors, types, routes, examples, and conventions precise and aligned with the authoritative contract."
description_zh: "用于创建、编辑、重构或审查服务 API 文档，确保操作、请求、响应、错误、类型、路由、示例和约定准确并与权威契约一致。"
description_en: "Produce standalone, readable API references with stable operation structure, explicit request/response/error tables, bounded types and routes, semantic anchors, and controlled contract changes."
category: "content"
version: "0.1.0"
author: "iamthenop/infurnet-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized API contract, service repository, or supplied specification with an established documentation format"
---

# API Documentation

Use this skill when the deliverable is an API reference or contract document. This skill governs document form and clarity; route semantics, fields, authorization, status codes, and vocabulary remain owned by the repository's API contract, architecture records, and service implementation. Never invent a route or field to make a table look complete.

## Establish the source of truth

Identify the API version, service/surface owner, transport, audience, canonical contract, supported environments, paired documents, and change scope. Read the existing document and authoritative schema/OpenAPI/implementation/tests before editing. Record whether a value is observed, specified, inferred, deprecated, or undecided. If sources conflict, report the conflict instead of silently choosing one.

Keep each API document standalone enough to read. State transport, authentication, content type, common headers, type notation, optionality, success/error conventions, pagination, idempotency, and versioning once in a conventions section. Do not use a convention section to redefine business semantics owned elsewhere.

## Use a stable operation shape

Organize operations under one operations section. Give every operation a stable, backtick-wrapped route heading, a human-readable purpose/authority description, and explicit `Request`, `Response`, and `Errors` sections. Include caller, authorization, asynchronous behavior, idempotency, integrity gates, and workflow references in the description when they are part of the contract.

Use durable semantic anchors derived from the HTTP method and operation slug. Update the operations list, anchor, counterpart documents, examples, and conventions together when adding an operation. Never renumber anchors or make a broad formatting rewrite while changing API semantics.

## Make tables unambiguous

Use field tables with `Field | Type | Description` and error tables with `Code | Message`. Keep field names in the Field column and scalar/structural types in the Type column; do not encode descriptions, brackets, or optionality inconsistently. Use named schemas for complex structures and define arrays/nullability according to the contract's notation.

Document required, optional, nullable, default, format, constraints, redaction, and ownership explicitly where applicable. Put success codes and failures in the same predictable error/status section, using bounded messages that identify the failure class without exposing internal state, paths, queries, secrets, or raw external payloads.

Keep transport metadata separate from payload fields. Define cross-cutting headers and fields once, then state whether they are required, echoed, forwarded, signed, or durable. Do not repeat them in every operation table unless the API contract genuinely varies.

## Keep routes and examples contractual

Use the repository's versioning and route vocabulary consistently. A resource reference, action, or status route must match the service's actual conventions. State HTTP method, authentication, authorization/resource ownership, request encoding, response shape, pagination, retry/idempotency, rate limits, and error behavior from evidence. Examples use synthetic values and must not contain tokens, personal data, internal hostnames, or production identifiers.

Make API semantics explicit in prose rather than relying on a table to imply them. If an operation is idempotent, state the key and the same-input/same-result rule. If behavior is asynchronous, document acceptance versus completion and how the result is observed. Mark undecided values plainly and track the decision outside the durable document when the repository does so.

## Change surgically

When adding an operation, update its list entry, stable anchor, conventions, schemas, examples, auth notes, counterpart API documents, tests, and changelog as applicable. A convention-only restructure must preserve every field, code, route, and semantic rule. Migrate legacy form only when the authorized change includes that migration; do not silently combine presentation cleanup with a contract change.

Review for terminology drift, duplicate definitions, contradictory optionality, unstable anchors, missing error cases, undocumented permissions, sensitive examples, broken links, stale generated output, and claims unsupported by implementation or tests. Preserve unrelated work and record compatibility, deprecation, and rollback implications for public changes.

## Verify and hand off

Run repository-native schema/OpenAPI lint, link checks, documentation builds, contract tests, and relevant integration checks. Re-read the rendered document and compare representative requests, responses, errors, auth failures, pagination, idempotent retries, and asynchronous states against the source contract. Record exact commands, exit codes, environment/tool versions, generated artifacts, and unavailable checks. A valid Markdown file does not prove the API behavior is correct.

Return scope and authority, document structure, changed operations, source evidence, contract checks, links/examples, compatibility notes, unresolved values, and rollback/review gate. For review findings include path/line, contract impact, evidence, smallest correction, and regression check. Stop when route ownership, vocabulary, status semantics, authorization, or source-of-truth precedence is ambiguous.
