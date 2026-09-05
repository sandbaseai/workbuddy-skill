---
name: "java-service-standards"
display_name: "Java 服务端编码规范"
display_name_en: "Java Service Coding Standards"
description: "Use when creating or changing Java service code, especially Spring applications, controllers, services, persistence adapters, configuration, or tests; align with the repository's architecture while enforcing safe contracts, errors, logging, transactions, and verification."
description_zh: "用于创建或修改 Java 服务端代码，尤其是 Spring 应用、Controller、Service、持久化适配器、配置和测试，在遵循仓库现有架构的同时约束契约、异常、日志、事务和验证。"
description_en: "Produce maintainable Java service code with repository-aligned layering, explicit contracts, safe errors and logs, bounded transactions, authorization, persistence, configuration, and test evidence."
category: "development"
version: "0.1.0"
author: "soft6096/jee-forge; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Java service repository with a declared build tool, framework conventions, persistence layer, and repository-native tests"
---

# Java Service Coding Standards

Use this skill for Java code generation, refactoring, review, configuration, persistence adapters, APIs, jobs, listeners, and service tests. First discover the repository's actual package structure, return types, framework versions, build commands, error model, logging conventions, and authorization boundaries. Existing conventions are the primary contract; these standards fill gaps without forcing a wholesale migration.

## Establish the implementation contract

Before editing, identify the changed layer, public inputs/outputs, callers, data ownership, authentication and authorization rules, transaction boundary, external dependencies, supported Java/framework versions, and rollback plan. Reuse existing value objects, exception types, mappers, validators, logging facade, and configuration patterns. Do not invent a new response wrapper or package hierarchy when the repository already has one.

Keep responsibilities separated: transport validates and translates requests, application services own business orchestration, persistence adapters own queries, and domain types express invariants. Avoid controllers containing transactions or business branching, repositories making remote calls, and utility classes becoming unbounded service containers. Name classes, methods, variables, and collections by domain meaning rather than generic `data`, `obj`, `result`, or single letters.

## Define safe API and error behavior

Document required, optional, boundary, null, idempotency, authorization, and concurrency semantics for each endpoint or public method. Validate at the boundary, normalize only when the contract permits it, and return the repository's established error shape. Never leak stack traces, credentials, internal paths, SQL, or sensitive fields to callers or logs. Do not catch and ignore exceptions; preserve the cause and map expected failures centrally.

Treat authentication as identity, authorization as resource/action permission, and resource ownership as a separate check. Never trust an object ID from a request as proof of access. Use allowlists for file types and redirect destinations, parameterized queries for values, and safe encoding at output boundaries.

## Make persistence and transactions explicit

Keep transaction scope narrow and deterministic. Do not hold a database transaction open across a remote call, unbounded queue wait, file upload, or user interaction. Define isolation, consistency, retry, timeout, and compensation behavior when a method touches multiple resources. Writes that can be retried need an idempotency key, unique constraint, state transition, or equivalent deduplication mechanism.

For database access, avoid N+1 queries, unbounded result sets, `SELECT *`, user-controlled query fragments, and update/delete operations without a narrowly verified predicate. Index decisions require query evidence; pagination has a bounded page size and a stable ordering. Batch large writes in bounded chunks and make partial failure/restart behavior explicit. Keep SQL in the repository's established location and verify migrations are reversible or have a documented recovery path.

## Make configuration and operations observable

Keep environment-specific values outside source code and secrets outside logs, committed files, and exception messages. Validate required configuration at startup and provide safe defaults only when their behavior is intentional. Configure timeouts, connection pools, thread pools, retry limits, and backoff explicitly rather than accepting infinite or framework-accidental behavior.

Use the repository's logging facade and structured context. Log the operation, correlation/request identifier, outcome, and useful bounded measurements at the appropriate level; log exception stack traces once at the ownership boundary. Never log passwords, tokens, full personal data, or raw request bodies by default. Metrics and traces should distinguish success, validation failure, dependency failure, timeout, retry, and authorization denial.

## Write testable, resilient code

Prefer small deterministic units with injected dependencies and explicit clocks, IDs, clients, and repositories where nondeterminism matters. Test happy, invalid, boundary, empty, duplicate, retry, timeout, partial-failure, authorization, and concurrent paths. Assert externally observable contracts, not private implementation details. Use realistic factories and synthetic data; never put production secrets or personal data in fixtures.

For integrations, use repository-approved contract or container tests and verify both request/response shape and failure semantics. For asynchronous work, test redelivery, ordering assumptions, dead-letter behavior, cancellation, and idempotency. A green unit test does not prove migration safety, browser behavior, or production configuration; record the checks that remain unexecuted.

## Review and handoff gates

Before delivery, re-read changed files and inspect the diff for accidental API, dependency, configuration, logging, authorization, and data-scope changes. Run the repository's formatter, compiler, static analysis, unit/integration tests, and migration checks that apply. Record exact commands, working directory, exit codes, tool versions, baseline failures, and environment limitations.

Confirm:

- package/layer ownership and public contracts match repository evidence;
- validation, authorization, error mapping, sensitive-data handling, and encoding are explicit;
- transaction, retry, timeout, idempotency, concurrency, and rollback semantics are bounded;
- queries, migrations, configuration, logs, metrics, and resource use are safe;
- tests cover normal, negative, boundary, failure, and recovery paths;
- no unrelated files, generated artifacts, dependencies, or secrets were changed.

Return changed paths, decisions, verification evidence, known gaps, rollout/rollback notes, and the next review gate. Stop when the repository contract, ownership, authorization, or required verification is ambiguous.
