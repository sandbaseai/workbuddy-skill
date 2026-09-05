---
name: "integration-health-check"
display_name: "集成健康检查"
display_name_en: "Integration Health Check"
description: "Use first when an integration context is ambiguous or a user needs to verify connection, credentials, accessible organizations, projects, or capabilities before taking an action."
description_zh: "用于集成上下文不明确，或在执行操作前需要验证连接、凭据、可访问组织、项目和能力时优先使用。"
description_en: "Establish a safe integration context before project-specific actions: verify connection and credential status, enumerate only authorized scopes, resolve the correct organization or project, surface capability limits, and ask for a choice only when ambiguity remains."
category: "development"
version: "0.1.0"
author: "Anthropic Claude Plugins Community; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
compatibility: "Authorized integration connector, health/status operation, scoped identity, and a user request that may involve multiple organizations or projects"
---

# Integration Health Check

Run this check before integration-specific work whenever the connector, identity, organization, project, environment, or capability is unknown. Establish context with the least-privileged read-only status operation first. Do not guess a target, reuse an unverified identifier, expose credentials, or perform a write merely to discover whether the connection works.

## Confirm connection and identity

1. Identify the intended integration and the operation the user ultimately wants.
2. Call the connector's health, status, or equivalent read-only capability before project-specific operations.
3. Verify connection state, credential validity, identity, token scopes, expiration or rotation signals, and any organization or project access returned.
4. Treat a successful transport response as insufficient: distinguish authenticated, authorized, partially available, degraded, and unknown states.

Never print tokens, cookies, private keys, or full sensitive headers. Redact secrets and personal data from logs and summaries. If credentials are absent, expired, or over-privileged, explain the smallest safe remediation and stop before attempting a write.

## Resolve the target context

Extract the available organizations, workspaces, projects, tenants, environments, modules, and capabilities. Match the user's words to stable identifiers using exact names and documented ownership; do not silently select the first result. Check whether the requested operation is supported in the selected context and whether its permission level is sufficient.

If exactly one authorized target matches, state the selected target and continue. If several match, ask the user to choose using concise, non-sensitive names and identifiers. If none match, report the verified scope, likely permission or naming issue, and the next read-only diagnostic. Do not probe unauthorized targets.

## Continue safely

Carry the verified target identifier forward to subsequent calls instead of rediscovering or accepting an untrusted identifier from free text. Re-check health after authentication changes, connector errors, scope changes, or a long pause. Bound requests, respect rate limits, and keep reads and writes explicit. For consequential actions, summarize target, intended side effect, and available rollback before execution.

Record the connector, check time, identity class, selected organization/project/environment, capabilities, status, limitations, and next action. Report only the minimum evidence needed to make the context reproducible. A health check proves current connectivity and returned access; it does not prove that every downstream API, dataset, or write path is available.
