---
name: "technical-spike"
display_name: "技术预研"
display_name_en: "Technical Spike"
description: "Use when an important implementation or architecture decision is blocked by a small number of unknowns. Create a time-boxed investigation with explicit questions, evidence, stop conditions, recommendation, and follow-up work."
description_zh: "用于实现或架构决策被少量关键未知数阻塞时；创建有时间盒、明确问题、证据、停止条件、建议和后续工作的技术预研。"
description_en: "Frame one decision question, inspect existing evidence, run the smallest safe prototype or experiment, record findings and limitations, and finish with an actionable decision or an explicit unresolved-risk handoff."
category: "productivity"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with repository/documentation access, an isolated disposable test area for prototypes, and an authorized path for any external service or data access"
---

# Technical Spike

## Purpose and boundary

A spike resolves a narrow technical uncertainty before implementation. It is a time-boxed investigation, not a disguised feature, production change, or commitment to the first prototype. Keep experiments isolated, use synthetic or redacted data, and require authorization before external calls, infrastructure changes, paid services, or production access.

## Spike contract

Define these fields before investigating:

- **Decision question:** one answerable question, not a broad project goal;
- **why now:** the decision or risk that remains blocked;
- **time box and stop condition:** deadline, effort limit, and what counts as enough evidence;
- **owner and audience:** decision owner, investigator, reviewers, and affected teams;
- **success criteria:** measurable facts that would support, reject, or qualify an option;
- **scope and exclusions:** systems, versions, data, environments, and questions deliberately left out;
- **deliverables:** findings, prototype/test artifact, recommendation, limitations, and follow-up tasks.

If the question cannot be made narrow or the stop condition is missing, return a framing gap instead of starting open-ended research.

## Workflow

1. **Frame the unknown.** Write the primary question, decision deadline, consequence of delay, hypotheses, and measurable success criteria. Separate facts, assumptions, and opinions.
2. **Search existing evidence.** Read repository code, current docs, issue history, contracts, provider docs, benchmarks, and prior decisions before writing new code. Record source, freshness, and confidence.
3. **Design the smallest investigation.** Choose a comparison, query, prototype, fixture, benchmark, or failure test that can falsify the leading hypothesis. Keep variables and dependencies bounded.
4. **Prepare a safe workspace.** Use an isolated branch/worktree or disposable directory, synthetic data, least-privilege credentials if unavoidable, network/request limits, and a cleanup plan. Do not copy secrets or customer data into artifacts.
5. **Run and observe.** Timestamp actions, capture commands/results and environment versions, compare alternatives fairly, and stop when the time box, safety boundary, or success criterion is reached. Do not expand scope to rescue a failing hypothesis.
6. **Analyze findings.** Distinguish observed result from interpretation. Record negative results, confounders, missing evidence, performance/cost/security implications, and whether the prototype is representative.
7. **Make the decision.** Recommend an option, reject it, or mark the question inconclusive. Explain alternatives, rationale, confidence, limitations, and what evidence would change the result.
8. **Close the spike.** Clean disposable artifacts, preserve only safe reproducible evidence, update the relevant decision/document, create implementation or follow-up tasks with owners/dates, and link the spike from the next handoff.

## Investigation patterns

| Unknown | Smallest useful probe |
|---|---|
| API capability or limit | Read current contract, then run a bounded synthetic request in a non-production account. |
| Latency or throughput | Benchmark equivalent workloads with warm/cold state and fixed concurrency; report p50/p95/p99 and resource cost. |
| Architecture fit | Build a narrow vertical slice or sequence diagram and exercise one failure/scale scenario. |
| Library/platform behavior | Pin versions, read primary docs, run a minimal isolated fixture, and record unsupported cases. |
| Migration feasibility | Validate schema/contract compatibility and a reversible sample migration; do not cut over real data. |
| Security/compliance property | Map the boundary and test the specific control with synthetic inputs and authorized scope. |

Avoid “proof by demo.” A prototype demonstrates that one path worked under one condition; it does not prove production readiness, security, scalability, or operability without the corresponding evidence.

## Evidence record

```text
Spike: <id and title>
Decision question: <one answerable question>
Owner/reviewers/deadline: <people and UTC date>
Time box/stop condition: <limit and completion rule>
Scope/exclusions: <environment, versions, data, systems>
Hypotheses: <supporting and falsifying predictions>
Evidence: <source, timestamp, method, result, confidence>
Prototype/test: <isolated artifact and reproducibility notes>
Findings: <observed facts, limits, confounders, negative results>
Recommendation: adopt | reject | defer | inconclusive
Rationale and alternatives: <decision logic>
Risks/permissions/cost: <security, privacy, reliability, spend>
Follow-ups/owners/dates: <implementation, docs, validation>
Cleanup and review trigger: <what was removed and when to revisit>
```

## Safe prototype rules

- Pin dependencies and record runtime/provider versions.
- Use fake, minimized, or redacted inputs; never embed credentials in source or output.
- Bound network calls, concurrency, storage, runtime, and spend; use a no-op or mock when it answers the question.
- Keep infrastructure changes in plan/dry-run form unless separately approved.
- Make cleanup idempotent and verify that temporary resources, test data, and credentials are removed or expired.
- If a result depends on inaccessible runtime evidence, label it unavailable rather than claiming support.

## Handoff checklist

- [ ] The spike answers one decision question with a deadline and explicit stop condition.
- [ ] Existing evidence, assumptions, hypotheses, scope, and exclusions are recorded.
- [ ] The experiment/prototype is minimal, isolated, reproducible, and within authorization.
- [ ] Results include negative findings, limitations, versions, workload, and confidence.
- [ ] Recommendation and alternatives are tied to evidence and measurable criteria.
- [ ] Security, privacy, reliability, cost, and operational implications are addressed.
- [ ] Cleanup is verified and follow-up tasks have owners, dates, and review triggers.
