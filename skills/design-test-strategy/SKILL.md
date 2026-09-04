---
name: "design-test-strategy"
display_name: "测试策略设计"
display_name_en: "Test Strategy Design"
description: "Design a risk-based mix of unit, integration, contract, end-to-end, performance, and manual tests."
description_zh: "根据用户旅程、系统边界和失败影响，设计可追溯、分层且成本合理的测试策略。"
description_en: "Design a traceable, layered, cost-aware test strategy from user journeys, system boundaries, and failure impact."
category: "development"
version: "0.1.0"
author: "skills contributors; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Design Test Strategy

Build the smallest test portfolio that gives decision-relevant confidence. Use
this Skill when planning a feature, release, migration, integration, incident
fix, or quality investment—not only when someone asks for a test plan.

## Establish the contract

Before proposing tests, identify:

- critical user journeys and business outcomes
- invariants, inputs, outputs, state transitions, and compatibility promises
- trust boundaries, external dependencies, permissions, and sensitive data
- supported platforms, versions, environments, and operational constraints
- evidence already available from tests, monitoring, incidents, or production

Separate confirmed requirements from assumptions. If code or documentation is
available, inspect it before inventing behavior. Record material gaps rather
than silently treating them as requirements.

## Risk-first workflow

1. Enumerate failures across normal behavior, boundaries, malformed input,
   partial failure, retries, concurrency, recovery, upgrades, rollback, and
   dependency degradation.
2. Rank each risk by likelihood, impact, and detectability. Give special weight
   to data loss, security, privacy, accessibility, billing, and irreversible
   actions.
3. Map each material risk to the lowest-cost test seam that faithfully observes
   it: static analysis, unit, property, component, integration, contract,
   end-to-end, performance, resilience, security, accessibility, or manual.
4. Define the oracle: the exact observable result that distinguishes pass from
   fail. Avoid assertions on incidental implementation details.
5. Specify fixtures, factories, clocks, random seeds, service doubles, test
   accounts, environment needs, and cleanup. Keep tests isolated and
   deterministic where practical.
6. Identify what belongs in pull-request, scheduled, pre-release, canary, or
   production monitoring gates. Give slow or flaky tests an explicit owner and
   containment plan.
7. Define measurable non-functional checks only where a requirement or known
   risk justifies them, including latency percentiles, throughput, resource
   budgets, compatibility, recovery objectives, and accessibility criteria.

Do not run destructive scenarios against production or real user data. Use
disposable fixtures and reversible environments. Never recommend weakening
security controls, suppressing failures, or retrying indefinitely to make a
suite green.

## Deliverable

Produce a traceability matrix with these fields:

| Risk or requirement | Scenario | Test level | Oracle | Fixture/environment | Gate | Owner | Status |
|---|---|---|---|---|---|---|---|

Follow it with:

- the minimum release-blocking suite
- complementary scheduled or exploratory coverage
- explicit exclusions, residual risks, and untested areas
- flaky-test prevention and failure-triage expectations
- the evidence needed to declare the strategy implemented

Prefer a small high-signal suite over a large shallow checklist. Do not duplicate
the same assurance at every layer unless the layers expose distinct risks. A
strategy is not complete merely because test cases were listed; every critical
risk needs a credible oracle, execution location, and owner.
