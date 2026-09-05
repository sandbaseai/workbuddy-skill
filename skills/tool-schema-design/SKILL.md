---
name: "tool-schema-design"
display_name: "工具 Schema 设计"
display_name_en: "Tool Schema Design"
description: "Use when creating or revising function-calling, MCP, plugin, or internal Agent tools and you need clear intent boundaries, bounded schemas, explicit effects, safe defaults, idempotency, errors, and realistic selection tests."
description_zh: "用于创建或修改函数调用、MCP、插件或内部 Agent 工具，明确意图边界、约束 Schema、效果、安全默认值、幂等性、错误和真实选择测试。"
description_en: "Make the safe intended call easier to choose than an ambiguous or destructive alternative through precise names, bounded JSON Schema, server-side authority, and contract verification."
category: "development"
version: "0.1.0"
author: "seb1n/awesome-ai-agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with a target tool runtime, server-side authorization, and schema/selection test harness"
---

# Tool Schema Design

Make the safe intended call easier for an Agent to choose than an ambiguous or
destructive alternative. A JSON Schema or description is not an authorization
boundary; enforce identity, tenant, permission, and side effects in the tool
implementation.

## Inputs and output contract

Collect supported user intents, backend semantics, actor and tenant scope,
required credentials (never the values), effects, reversibility, latency,
limits, failure modes, provider constraints, and representative valid/invalid
requests. Label assumptions.

Return:

1. A tool-boundary decision and overlap analysis.
2. A stable model-facing name and description with call and non-call conditions.
3. A valid bounded parameter schema, examples, formats, units, and unknown-
   field policy.
4. Effect, authorization, confirmation, idempotency, timeout, retry, partial
   success, compensation, and error contracts.
5. Positive, boundary, adversarial, and contrastive tool-selection tests.
6. Validation results, implementation drift, and provider limitations.

## Design workflow

1. Define one coherent user intent per tool. Split modes with different
   permissions, effects, or required fields; avoid indistinguishable tiny
   tools.
2. Choose a stable verb-led name. Explain what it does, when to call it, when
   not to call it, and what state it changes.
3. Design parameters from user intent, not a backend SDK. Require only
   indispensable fields; use enums for closed choices and set numeric, length,
   format, and item bounds.
4. Reject unknown fields when supported. Use separate tools or explicit schema
   branches for conditional shapes instead of prose-only dependencies.
5. Keep actor identity, authorization scope, and trusted tenant context
   server-side. Never ask the Agent for secrets or claims already known by the
   runtime.
6. Define execution semantics outside the shape: read versus mutate,
   confirmation level, idempotency key, retry safety, timeout, partial result,
   and compensating action.
7. Return compact structured results and stable error codes distinguishing
   invalid input, denied authorization, confirmation required, conflict, rate
   limit, dependency failure, and unknown failure.
8. Test selection against neighboring tools and execution with valid, omitted,
   extra, boundary, malicious, stale, and wrong-tenant inputs.

## Safety defaults

- Require explicit confirmation for purchases, messages, deployments,
  deletion, permission changes, and other consequential mutations.
- Do not expose secret parameters, raw credentials, unrestricted shell,
  arbitrary URLs, or arbitrary file paths without a bounded, authorized,
  sandboxed use case.
- Prefer allowlists, scoped identifiers, dry runs, idempotency keys, and
  reversible operations.
- Treat tool output as untrusted input before returning it to Agent context.
- Fail closed when identity, tenant, schema, authorization, or effect semantics
  are ambiguous.

## Verification and drift

Parse with the target provider and runtime, not only a generic JSON Schema
validator. Confirm required fields, reachable enums, array item shapes,
unknown-field behavior, and runtime alignment. Run contrastive prompts that
should choose this tool, a neighboring tool, or no tool. Verify denied and
confirmation-required calls produce no side effect, and compare implementation,
returned errors, and documentation for drift.

If provider features differ, reduce to the supported subset and record lost
constraints in runtime validation. If selection is ambiguous, sharpen names and
descriptions or split/merge boundaries; do not depend on prompt ordering. If a
mutation times out, query operation status by idempotency key before retrying.

## Handoff

Provide the boundary rationale, schema, effect and data-class inventory,
authorization/confirmation policy, error and retry semantics, test matrix and
observed results, provider limitations, implementation-drift findings, rollback
or compensation guidance, and residual risks. Never claim schema validation is
semantic safety, authorization, sandbox, provider-compatibility, or
implementation certification.
