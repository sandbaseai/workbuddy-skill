---
name: "multi-agent-orchestration"
display_name: "多 Agent 编排"
display_name_en: "Multi-Agent Orchestration"
description: "Use when coordinating genuinely independent Agent workstreams with task decomposition, dependency graphs, ownership, handoff contracts, approvals, recovery, and synthesis."
description_zh: "用于协调真正独立的多 Agent 工作流，覆盖任务拆分、依赖图、责任人、交接契约、审批、恢复和结果汇总。"
description_en: "Design bounded multi-Agent workflows where specialization or safe parallelism outweighs coordination cost, with minimum necessary authority and verifiable integration."
category: "development"
version: "0.1.0"
author: "seb1n/awesome-ai-agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with bounded task state, isolated write scopes, approvals, and an accountable integrator"
---

# Multi-Agent Orchestration

Use multiple Agents only when specialization or safe parallelism outweighs
coordination cost. Do not delegate a small, tightly coupled, or inherently
sequential task merely to increase Agent count. Delegation never expands the
requester's authority.

## Plan contract

Capture the measurable objective, completion criteria, explicit non-goals, task
graph, available Agents/tools, concurrency limits, shared resources, authority
boundaries, deadline, budget, and final decision owner. Produce a directed
acyclic graph with one accountable owner per task, dependencies, inputs, output
contract, write scope, validation, timeout, retry bound, escalation route,
approval point, and stop condition.

## Design the workflow

1. Decompose by separable outputs, not vague roles; keep shared mutable state
   minimal and tightly coupled steps under one owner.
2. Identify the critical path. Parallelize only tasks with independent inputs
   and non-overlapping side effects.
3. Give each Agent the minimum context and permissions needed. Include source
   artifacts rather than hidden conclusions when independent judgment matters.
4. Require structured handoffs containing status, result, evidence, changed
   state, assumptions, risks, and next dependency. Acknowledge receipt before
   downstream mutation.
5. Monitor dependency state and useful progress. Bound retries and debates;
   never recursively delegate without explicit capacity and ownership.
6. Synthesize through a named integrator. Resolve disagreement from primary
   evidence, run integration checks, and verify the original criteria.
7. Close or cancel unused branches and account for completed, failed, canceled,
   superseded, and unrun tasks.

## State and authority safety

- Reserve external messages, purchases, deployments, destructive actions,
  credential access, and production changes for explicit approval points.
- Isolate credentials and sensitive context by role; never broadcast secrets in
  shared state or handoffs.
- Use single-writer ownership, isolated branches, transactions, or locks for
  mutable resources. Preserve user-owned changes and make cancellation
  recoverable.
- Tag consequential tasks and require a task-local approval reference that
  names the relevant approval point.
- A child Agent may not perform an action outside the parent authorization or
  silently broaden a target, tenant, tool, or environment.

## Verification

Validate that the graph is acyclic, every dependency and approval resolves,
owners and numeric execution bounds exist, and parallel tasks do not write the
same file, record, branch, or environment. Check every handoff against its
output contract before unblocking a dependent. Re-run end-to-end tests or
evidence checks after synthesis; individual Agent success is insufficient.

Treat plan validation as declaration checking, not proof of runtime isolation,
authorization, approval authenticity, or task behavior. Report evidence,
remaining uncertainty, unused or failed branches, and any unverified
assumption.

## Failure handling

- For a stall, inspect the last evidence; retry once only for a transient
  failure, then reassign or collapse the task.
- For disagreement, require source-backed claims and let the named integrator
  adjudicate; never average incompatible answers.
- For shared-state conflict, pause writers, preserve both versions, and
  reconcile through the single owner.
- For dependency failure, block or redesign downstream work rather than
  fabricating its input.
- If coordination overhead exceeds remaining work, stop delegation and finish
  the critical path under one owner.

## Handoff

Return the decomposition rationale, graph and critical path, owners and scopes,
handoff protocol, approvals, timeouts/retries, stop conditions, integration
evidence, task accounting, unresolved risks, and final decision owner. Do not
declare completion until the integrated result satisfies the original criteria
and all material uncertainty is explicit.
