---
name: "llm-app-security"
display_name: "大模型应用安全"
display_name_en: "LLM Application Security"
description: "Use when designing or reviewing an LLM-powered application for prompt injection, unsafe outputs, data leakage, tenant isolation, and abuse risks."
description_zh: "用于设计或审查大模型应用中的提示注入、不安全输出、数据泄露、租户隔离和滥用风险。"
description_en: "Assess an LLM feature across input, prompt, retrieval, tool, model, output, identity, and operations boundaries; verify controls with safe evidence; and produce prioritized mitigations without attempting exploitation."
category: "security"
version: "0.1.0"
author: "devops-skills; adapted from majiayu000/claude-skill-registry for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized application or repository, model and provider configuration, redacted fixtures, identity and tenant model, retrieval/tool contracts, and approved security scope"
---

# LLM Application Security

Review an application that accepts untrusted input, invokes a language model, retrieves data, or calls tools. Treat the model as an untrusted probabilistic component: enforce security decisions in deterministic application and service layers. Work only within an authorized scope; never exfiltrate secrets, bypass access controls, weaponize prompts, or send harmful content to users or external systems.

## Map the trust boundaries

Inventory user input, uploaded files, system and developer instructions, retrieved documents, conversation memory, model providers, tools, plugins, webhooks, logs, analytics, and downstream actions. For each flow, identify the principal, tenant, data classification, authorization decision, side effect, and owner. Keep system instructions separate from user-controlled content, and mark every assumption or unknown.

## Verify the control layers

Inspect code, configuration, prompt templates, retrieval filters, tool schemas, identity middleware, moderation policy, rate limits, telemetry, and tests. Check at minimum:

- **Input and context:** validate type, size, encoding, file content, and provenance; scan uploads for secrets or malware where appropriate; isolate retrieved and user text from instructions;
- **Identity and tenancy:** derive authorization from trusted identity state, filter retrieval and memory by tenant and object permissions, prevent cross-tenant caching, and deny by default when context is ambiguous;
- **Prompt and model:** keep secrets out of prompts, pin or approve model/provider configuration, bound context and cost, handle unavailable or degraded providers safely, and do not rely on the model to enforce authorization;
- **Tools and actions:** expose only minimum-necessary tools, validate arguments server-side, re-check authorization at execution, require confirmation for consequential actions, make retries and idempotency explicit, and log actor, target, decision, and result;
- **Output and data:** encode output for its destination, distinguish model claims from verified facts, moderate or route risky content, redact secrets and personal data, and attach provenance for retrieval-backed answers;
- **Abuse and operations:** rate-limit by meaningful principal and cost, detect anomalous usage without collecting unnecessary content, define quotas and circuit breakers, monitor provider errors, rotate credentials, and maintain incident and rollback procedures.

Use redacted or synthetic fixtures and repository-native tests. If adversarial testing is authorized, bound payloads, targets, rate, and stop conditions before running it; otherwise perform static and controlled behavioral checks only. Record commands, versions, test identities, exclusions, evidence, and limitations. A clean prompt test or moderation result does not prove the whole application is secure.

## Assess findings

Separate confirmed vulnerability, control weakness, policy gap, observation, and unknown. For each material finding, record the affected flow and location, preconditions, evidence at a safe level, impacted users or data, likelihood, impact, existing mitigation, severity rationale, owner, and recommended fix. Prioritize authorization and tenant-boundary failures, secret or personal-data exposure, uncontrolled side effects, and denial-of-service or runaway-cost paths.

Do not paste credentials, private prompts, customer data, or reusable attack payloads into reports. Describe the smallest safe reproduction and retain sensitive evidence in the approved system. Treat model-generated claims as untrusted until independently verified.

## Remediate and hand off

Prefer deterministic enforcement, least privilege, isolation, safe defaults, and reversible changes. Add regression tests for injection-resistant context handling, tenant filtering, tool authorization, output encoding, redaction, rate limits, and failure behavior as applicable. Re-test adjacent paths and degraded-provider cases, then hand off scope, evidence, limitations, findings, owners, deadlines, rollback, monitoring, residual risk, and the next authorized action.
