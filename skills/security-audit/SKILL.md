---
name: "security-audit"
display_name: "安全审计"
display_name_en: "Security Audit"
description: "Use when auditing an application, repository, integration, or process for security weaknesses, control gaps, or compliance evidence."
description_zh: "用于审计应用、代码库、集成或流程中的安全弱点、控制缺口和合规证据。"
description_en: "Perform a bounded, evidence-first security audit: map assets and trust boundaries, verify controls, assess vulnerabilities and compliance gaps, prioritize risk, and produce actionable remediation without unsafe scanning or exploitation."
category: "security"
version: "0.1.0"
author: "StrRay Framework; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized repository or environment, security requirements, configuration and logs, dependency metadata, and an approved audit scope"
---

# Security Audit

Conduct a security and compliance audit within an explicitly authorized scope. The goal is defensible evidence and risk reduction, not an impressive list of speculative findings. Never exploit a weakness, exfiltrate data, bypass access controls, or run an untrusted scanner without explicit authorization and isolation.

## Define scope and safety

Record the assets, environments, repositories, identities, tenants, data classes, interfaces, audit period, applicable requirements, and owner. State what is out of scope. Confirm whether testing is read-only, whether staging is available, rate limits, maintenance windows, emergency contacts, and stop conditions.

Treat credentials, tokens, personal data, production records, and vulnerability details as sensitive. Use least privilege, synthetic or redacted data, bounded requests, and approved tools. Do not install dependencies or execute downloaded code merely to inspect a system; first verify provenance, permissions, and isolation.

## Map the system

1. Inventory assets, services, repositories, dependencies, data stores, identities, secrets paths, and external providers.
2. Draw trust boundaries and data flows, including admin paths, webhooks, queues, agent/tool calls, and tenant boundaries.
3. Identify entry points, privileged operations, sensitive data, security assumptions, and control owners.
4. Map requirements to concrete controls and evidence: authentication, authorization, validation, encryption, logging, retention, backup, incident response, and change management.

Mark unknowns rather than filling gaps with assumptions. A missing inventory or stale evidence is itself an audit finding when it prevents risk evaluation.

## Verify controls

Inspect code, configuration, infrastructure definitions, dependency manifests, CI policy, access reviews, logs, alerts, runbooks, and test evidence. Verify both the intended control and its failure behavior:

- authentication, session lifetime, MFA, service identity, and credential rotation;
- authorization, object-level checks, tenant isolation, privilege boundaries, and deny-by-default behavior;
- input validation, output encoding, injection resistance, deserialization, file handling, SSRF, and resource limits;
- secret storage, key management, encryption in transit and at rest, and redaction in telemetry;
- dependency provenance, pinning, update process, build integrity, and artifact signing;
- audit events, tamper resistance, alert routing, retention, time synchronization, and investigation access;
- backups, recovery, incident ownership, vulnerability response, and safe emergency changes;
- privacy, data minimization, retention, deletion, consent, and third-party processing where applicable.

Use approved static analysis, dependency checks, configuration checks, or tests only within the declared scope. Record tool version, command, target, exclusions, and limitations. A clean scan does not prove the absence of vulnerabilities or compensate for missing threat modeling.

## Assess and prioritize risk

For every material finding, record the asset and location, violated control or requirement, evidence and reproduction at a safe level, preconditions, affected data or users, likelihood, impact, exploitability, existing mitigations, owner, and recommended fix. Classify severity consistently as critical, high, medium, or low; explain the scale and do not inflate severity without evidence.

Separate confirmed vulnerability, control weakness, compliance gap, observation, and unknown. Never include secrets or unnecessary exploit instructions in the report. Validate false positives with the smallest safe check and preserve the original evidence.

## Remediate and close

Prioritize containment for active exposure, then durable fixes, regression tests, monitoring, and documented exceptions. Define acceptance criteria, deadline, owner, dependency, rollback, and residual-risk approver for each action. Re-test the control after remediation using comparable evidence; do not close a finding because a ticket was created.

The final handoff includes scope, methodology, evidence period, tools and limitations, findings by severity, accepted risks, remediation owners and deadlines, compliance mapping, retest status, incident escalation, and the next authorized action. Set a review trigger for material architecture, dependency, threat, regulatory, or operational changes.

