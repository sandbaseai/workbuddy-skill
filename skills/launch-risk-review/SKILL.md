---
name: "launch-risk-review"
display_name: "发布风险审查"
display_name_en: "Launch Risk Review"
description: "Use before shipping a feature, product, campaign, or integration to identify contractual, privacy, security, IP, third-party, regulatory, operational, and AI risks with evidence and owners."
description_zh: "用于功能、产品、活动或集成发布前，基于证据识别合同、隐私、安全、知识产权、第三方、监管、运营和 AI 风险，并明确责任人。"
description_en: "Run a calibrated launch-readiness review from the PRD and implementation evidence, distinguish blockers from follow-ups and unknowns, route specialized reviews, and produce a decision-ready memo without presenting generic guidance as legal advice."
category: "security"
version: "0.1.0"
author: "Anthropic Claude for Legal; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
compatibility: "Authorized product or engineering repository, PRD/specification, launch tracker, implementation evidence, applicable policy owners, and an approved review scope"
---

# Launch Risk Review

Review whether a proposed release is ready for its intended users, market, and operational environment. This is an evidence-gathering and routing workflow, not a substitute for qualified legal, privacy, security, safety, or compliance advice. Never clear a launch by assumption, hide an unresolved finding, or post privileged or sensitive material to a broad destination.

## Establish the matter and destination

Collect the PRD or change description, design and technical documents, launch date, users and jurisdictions, data flows, vendors, model or automation use, rollout plan, and launch tracker history. Record what is in and out of scope, the decision owner, and where the memo may be shared. If a destination is public or broader than the approved review group, produce a sanitized summary and keep sensitive evidence in the authorized system.

## Understand what is changing

Explain in plain language what the feature does, who uses it, what is new versus previously reviewed, which data or vendors change, which claims are made, and what happens on failure. Detect AI even when it is not labelled as such: third-party or internal models, generated content, recommendations, scoring, classification, prediction, personalization, or automated decisions. Mark missing inputs and uncertain assumptions instead of filling them with invented facts.

## Walk the risk categories

For each category, record evidence, applicability, severity, owner, required action, deadline, and decision gate:

- **User and contractual commitments:** compare behavior, pricing, SLA, retention, accessibility, marketing, and support promises with the actual change;
- **Privacy and data:** identify collection, purpose, sharing, retention, deletion, consent, sensitive data, cross-border processing, and subject-rights impact;
- **Security and abuse:** inspect new attack surface, identity and authorization paths, secrets, tenant isolation, logging, abuse controls, and incident readiness;
- **IP and content:** check dependencies, licenses, third-party assets, user content, generated output provenance, attribution, and claim substantiation;
- **Third parties:** assess new providers, subprocessors, integrations, data access, contractual controls, service limits, and exit or outage plans;
- **Regulatory and safety:** route regulated-sector, age-sensitive, high-impact, accessibility, consumer-protection, or safety questions to the accountable specialist; do not infer clearance from a generic checklist;
- **AI and automated decisions:** classify use and impact, verify human oversight, evaluation, transparency, privacy, security, fallback, appeal, monitoring, and governance evidence;
- **Operations and release:** verify support ownership, observability, capacity, migration and rollback, staged rollout, kill switch, communications, and post-launch review triggers.

Use repository-native evidence, approved research systems, policy documents, implementation checks, and test results. Cite the source and evidence date. Separate stable general guidance from jurisdiction-specific or time-sensitive claims; label unverified material and escalate rather than presenting it as settled. Route deeper work to privacy, security, AI governance, accessibility, marketing-claims, or specialist reviews when indicated.

## Calibrate the decision

Classify each item as **blocker**, **must resolve before launch**, **follow-up with owner and date**, **accepted risk with approver**, **observation**, or **unknown**. Calibrate severity to the actual users, data, jurisdictions, exposure, reversibility, and evidence—not novelty or fear. A missing artifact can itself block a decision when it prevents evaluation. Do not silently convert an unknown into a low risk.

For every blocker or material finding, include the affected flow, evidence and location, preconditions, impact, rationale, required fix, acceptance criteria, owner, deadline, and retest method. Avoid secrets, personal data, privileged content, or unnecessary exploit details in the memo.

## Produce the handoff

The final memo includes scope and inputs, plain-language launch summary, category results, AI detection, evidence and limitations, findings by decision class, required specialist reviews, rollout and rollback gates, owners and dates, accepted residual risks, communication constraints, and the next authorized action. Re-check changed claims or implementation before launch and define triggers for post-launch review after material incidents, architecture, vendor, model, data, market, or regulatory changes.
