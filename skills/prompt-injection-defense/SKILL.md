---
name: "prompt-injection-defense"
display_name: "提示注入防御"
display_name_en: "Prompt Injection Defense"
description: "Use when threat-modeling or hardening an AI agent, RAG system, assistant, or tool workflow against direct, indirect, stored, cross-agent, or multimodal prompt injection."
description_zh: "用于对 AI Agent、RAG、助手或工具工作流进行威胁建模和加固，防御直接、间接、存储、跨 Agent 及多模态提示注入。"
description_en: "Threat-model untrusted content and move consequential authority outside the model through narrow tools, typed boundaries, independent authorization, safe adversarial tests, and explicit residual risk."
category: "security"
version: "0.1.0"
author: "seb1n/awesome-ai-agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized policy, tool, identity, and test controls"
---

# Prompt Injection Defense

Design for compromise of model reasoning. Prompt text, delimiters, classifiers,
and detectors are defense-in-depth signals, not reliable security boundaries.
Keep consequential authority, authorization, validation, and policy enforcement
outside the model. Never test against production, third-party, or user systems
without target-specific authorization.

## Map the attack surface

Collect the agent purpose, instructions, models, memory, orchestration, every
input source and modality, tools and privileges, identities and targets,
secrets and protected assets, output sinks, egress, authorization model,
human gates, monitoring, incident history, and safe evaluation environment.
Include web pages, email, documents, images, audio, OCR, metadata, tool
descriptions, retrieval results, persisted memory, and other agents. Label
assumptions and unknowns. Use redacted samples or synthetic fixtures; never
request production secrets or malicious artifacts in chat.

Produce a data-flow and trust-boundary map, asset/consequence inventory,
injection-path threat model, prioritized controls, regression plan, evidence
report, and residual-risk/recovery plan. Track each control as `missing`,
`planned`, `implemented`, or `verified`, with an enforcement point, owner,
evidence ID, test ID, and expiry when time-limited.

## Enforceable boundaries

- Retrieved content cannot grant permissions or change a tool allowlist.
- Untrusted text cannot choose recipients, tenants, records, or privileged
  destinations; derive sensitive targets from trusted application state.
- Model output cannot execute as code, SQL, HTML, shell, URLs, or privileged
  API arguments without destination-specific validation and safe encoding.
- Secrets unavailable to the task never enter model context or tool results.
- Every consequential effect has an independent policy and authorization check;
  reauthorize immediately before execution.

Remove unused tools, ambient credentials, generic shells, arbitrary URL fetch,
raw SQL, and unrestricted file access. Split read from write and preview from
commit. Restrict identities by tenant, object, action, fields, time, and
destination. Sandbox parsers, browsers, code, and file processing. For
multi-Agent workflows, authenticate senders, constrain delegation depth and
budgets, pass structured claims with provenance, and recalculate permissions at
each hop.

Treat untrusted content as quoted data, preserve provenance across retrieval
and handoffs, use typed messages instead of concatenated instructions and data,
and keep active content inert where possible. Do not rely on instruction
hierarchy, reminders, or a detector as the sole control.

## Safe adversarial verification

Use an isolated environment, synthetic accounts, inert destinations, benign
canary secrets, and non-destructive tools. Test direct override and disclosure
attempts; instructions in pages, mail, files, tool results, metadata, and
memory; obfuscation and language changes; splitting across turns; cross-Agent
delegation and tainted summaries; alternate modalities; tool-target
substitution; exfiltration and egress; plus benign content to measure false
positives.

Measure invariant violations, unauthorized tool attempts, canary exposure,
successful benign tasks, false-positive rate, and containment behavior. A
detector pass rate alone is insufficient. Mark a control `verified` only when
implementation and named test evidence both exist. Re-run the suite after
model, prompt, parser, retrieval, tool, permission, or orchestration changes.

## Operation and recovery

Log provenance, policy decisions, denials, tool/target metadata, and anomalous
sequences without secrets or unnecessary content. Alert on canary access,
repeated policy failures, new tool exposure, cross-tenant attempts, and
unexpected egress. For a suspected incident, isolate the workflow, disable
high-risk tools and egress, rotate exposed credentials through the owner,
quarantine malicious sources, preserve redacted evidence, inspect persisted
memory and downstream effects, restore clean state, and retest before
reenabling access. Do not silently delete memory, records, or evidence.

Finish only when the full data flow, sinks, memory stores, Agent hops,
destinations, credential boundaries, authority checks, and recovery path are
represented. Keep unverified surfaces visible and state tested scope, evidence
limits, benign utility, and residual risk; never claim prompt injection has
been eliminated.
