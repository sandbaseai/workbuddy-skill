---
name: "threat-model"
display_name: "威胁建模"
display_name_en: "Threat Modeling"
description: "Use when assessing a feature, system, API, data flow, infrastructure change, or incident-prevention design for plausible abuse paths; ground threats in real assets and trust boundaries and map them to verifiable controls."
description_zh: "针对功能、系统、API、数据流与基础设施变更建立基于真实边界和攻击路径的威胁模型，并将风险映射到可验证控制。"
description_en: "Model threats for features, systems, APIs, data flows, and infrastructure changes using real boundaries and attack paths, then map risks to verifiable controls."
category: "security"
version: "0.1.0"
author: "Hung Pham; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Threat Modeling

Use this skill before or during security-sensitive design, implementation review, or incident prevention. A threat model is scoped analysis, not a penetration test, compliance certification, or guarantee of safety.

## Establish scope from evidence

Record the business purpose, deployment environment, in-scope components and versions, owners, assets, sensitive data, actors, entry points, trust boundaries, data stores, external dependencies, privileged operations, and availability or compliance requirements. Inspect real architecture, code paths, APIs, jobs, queues, configuration, identity flows, and deployment boundaries when available.

State what is out of scope and why. Distinguish verified facts, assumptions, and unknowns. Define plausible attacker types, access, knowledge, resources, and objectives without assuming either an all-powerful attacker or a benign internal actor.

Never place secrets, exploit-ready production details, customer data, or unredacted credentials in the durable model.

## Trace abuse paths

Model how data and authority cross each trust boundary. For each entry point or privileged operation, consider:

- spoofing and broken authentication;
- tampering and integrity loss;
- repudiation and missing audit evidence;
- information disclosure and privacy leakage;
- denial of service and resource exhaustion;
- elevation of privilege and authorization bypass;
- supply-chain, dependency, build, and deployment compromise;
- unsafe automation, confused deputy behavior, social engineering, and operational misuse.

Describe an end-to-end abuse path—precondition, attacker action, affected boundary or control, and impact. Do not list generic vulnerability names without a credible path through this system. Include misuse by legitimate but over-privileged users and failures caused by automation at scale.

## Assess and prioritize

For each threat, record affected assets, existing controls and their evidence, control gaps, likelihood rationale, impact dimensions, detectability, and residual risk. Use the organization's risk method when supplied; otherwise prefer transparent qualitative ratings over invented numeric precision.

Prioritize by plausible harm and exposure, not only ease of implementation. Separate prevention, detection, response, and recovery controls. A documented policy is not an implemented control, and an implemented control is not effective until its enforcement and failure behavior are verified.

## Define verifiable mitigations

Make each required mitigation specific:

- control and threat(s) addressed;
- enforcement point and owner;
- acceptance test, monitor, audit query, or other evidence;
- delivery phase and prerequisite;
- expected residual risk, failure mode, and recovery path.

Prefer reducing privilege, exposure, and blast radius before adding detection alone. Check whether a mitigation introduces availability, privacy, usability, or operational risks. Mark risks requiring human security, privacy, legal, or business acceptance.

## Handoff

Return scope, a compact data-flow or boundary summary, prioritized threat register, existing controls, gaps, required mitigations, assumptions, open questions, residual-risk owners, and a review trigger. Update the model when architecture, identities, data, dependencies, exposure, or attacker capabilities materially change.

Do not probe live systems, exploit a weakness, rotate credentials, change controls, or disclose findings externally unless the current request explicitly authorizes that action and target.
