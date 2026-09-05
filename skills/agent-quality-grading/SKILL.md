---
name: "agent-quality-grading"
display_name: "智能体交付质量评估"
display_name_en: "Agent Quality Grading"
description: "Use when evaluating how well an agent completed real tasks, used tools, communicated, or produced assets; grade each dimension from traceable evidence and keep quality separate from reliability."
description_zh: "用于评估智能体是否完成真实任务、是否正确使用工具、沟通质量和产物质量，基于可追溯证据分别评分，并将交付质量与可靠性分开。"
description_en: "Evaluate agent conversations, tool traces, generated assets, and instructions across task completion, timeliness, tool correctness, and message quality with evidence-bounded grades and actionable improvements."
category: "development"
version: "0.1.0"
author: "ever-just/agentskills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized, redacted conversation/tool traces and generated assets; supported channel and agent metadata"
---

# Agent Quality Grading

Use this skill to measure how well an agent served a user, independently of whether the underlying system was reliable. A polished message does not prove the task happened, and a successful tool call does not prove the result was useful. Grade only the evidence available for the requested scope.

## Establish scope and privacy

Define the time window, channels, agents, task classes, asset types, comparison baseline, and scoring audience. Obtain authorization for every trace and artifact. Prefer redacted or synthetic data; never copy credentials, personal data, private prompts, tokens, or raw secret-like content into the report. Record missing logs, clock assumptions, unavailable assets, and sampling limits.

Reconstruct each conversation or task from inbound request, agent turns, tool calls/results, generated artifacts, and final user-visible outcome in chronological order. Preserve IDs or hashes only when needed to join evidence. A claim such as “sent,” “updated,” or “deployed” requires a matching successful operation in the same trace; otherwise grade task completion as unverified or fabricated according to the repository policy.

## Grade four independent axes

Give each relevant task or channel a grade from A–F, with a short rationale and exact evidence reference:

- **TASK** — did the agent satisfy the requested outcome fully, partially, not at all, or claim work without a matching operation? Check scope, correctness, side effects, constraints, and user-visible result.
- **SPEED** — compare request and response timestamps using the channel's stated expectation. Report latency distribution and long-tail delays; do not penalize necessary authorized work as “slow” without a threshold.
- **TOOLS** — was the right tool selected at the right moment with valid arguments, correct target, appropriate scope, and proper handling of failures? Distinguish missing, wrong, unnecessary, and malformed calls.
- **MESSAGE** — was the response accurate, clear, appropriately concise, channel-safe, human-readable, and honest about uncertainty? Check formatting, localization, accessibility, tone, next action, and whether markdown or internal details leaked into plain-text channels.

Do not average away a critical failure. A fabricated completion claim, unauthorized side effect, leaked sensitive data, or materially wrong user-facing result must remain visible even if other axes score well. Explain the weighting and severity policy used.

## Evaluate generated assets

For each document, image, video, chart, or other artifact, join the request to the tool result and persisted asset. Distinguish generation failure, persistence failure, retrieval failure, and content mismatch. Follow only authorized, safe URLs; do not upload or execute untrusted material. Inspect the artifact with an appropriate renderer or parser, checking requested content, factual/numerical integrity, layout, typography, pagination, accessibility, and production readiness.

Report asset ID or hash, request summary, generation outcome, inspection evidence, grade, defect, and reproduction path. Calculate success rate from the defined sample and state exclusions. A missing asset is not automatically a persistence bug, and an HTTP response or tiny redirect body is not proof that the intended media was retrieved.

## Evaluate prompts and configurations

Inspect the active agent instructions and prompt assembly for conflicting rules, vague roles, unfilled placeholders, missing examples, unsafe tool permissions, unsupported capabilities, and declared personalization that is absent in production. Verify whether important guarantees—no false confirmation, channel formatting, authorization, privacy, and length—are enforced during generation or merely repaired afterward.

Treat private system prompts and user data as confidential. Report a minimal redacted excerpt or stable evidence pointer, never the complete hidden prompt. Separate configuration defects from runtime behavior and cite which trace demonstrates the impact.

## Report findings and improvements

Produce a scope/limitations section, channel or task grade table, per-agent report cards, asset grades, prompt/config grades, best and worst evidence moments, and a prioritized improvement backlog. Every material grade includes an evidence pointer, timestamp or sequence, affected channel/agent, confidence, and a concrete next check. Separate confirmed defects, likely risks, observations, and unknowns.

Prioritize fabricated success claims, incorrect or harmful outcomes, unauthorized actions, sensitive-data exposure, inaccessible communication, broken tool routing, missing recovery, and severe latency before stylistic preferences. Recommend the smallest durable change and define acceptance evidence across the affected tasks and channels. Retest after changes; passing one trace or snapshot proves only that exercised case.

Return the grading method, score definitions, evidence matrix, findings, sample denominator, tested environments, privacy redactions, skipped checks, owners, and next review gate. Stop when authorization, trace integrity, timestamp semantics, or artifact provenance is insufficient for a defensible grade.
