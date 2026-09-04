---
name: "product-roadmap"
display_name: "产品路线图规划"
display_name_en: "Product Roadmap Planning"
description: "Use when creating or revising a product or program roadmap that must connect outcomes, evidence, dependencies, capacity, and uncertainty; distinguish direction and sequencing from an execution plan or fixed promise."
description_zh: "基于目标、证据、约束、依赖和团队容量构建可复审的产品路线图，明确当前、下一步、后续、阻塞与拒绝事项。"
description_en: "Build reviewable product roadmaps from outcomes, evidence, constraints, dependencies, and capacity, with explicit now, next, later, blocked, and rejected work."
category: "business"
version: "0.1.0"
author: "David Victor; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Product Roadmap Planning

Use this skill to express durable direction and sequencing before detailed implementation plans. A roadmap is a decision aid, not a backlog dump, release calendar, or guarantee. Preserve the user's planning horizon and method when supplied.

## Ground the roadmap

Collect the strategy, target users, problems and evidence, desired outcomes, current baseline, non-goals, constraints, dependencies, committed obligations, capacity assumptions, existing decisions, active work, and prior roadmap. Label facts, estimates, assumptions, and unresolved choices separately.

If information is missing, proceed with clearly marked assumptions when they do not materially change direction. Escalate only decisions that change scope, sequencing, investment, or commitments; do not fabricate stakeholder agreement.

## Shape outcome-oriented items

Each roadmap item should state:

- target user or system and problem evidence;
- intended outcome and observable success measure;
- why it matters now and its link to strategy;
- dependencies, prerequisites, constraints, and affected teams;
- confidence in problem, solution direction, effort, and timing;
- leading signal, review trigger, and accountable owner;
- what is explicitly outside the item.

Do not convert an unvalidated feature request directly into a commitment. Separate discovery, validation, enabling work, delivery, migration, and adoption when their uncertainty or dependencies differ.

## Sequence transparently

Use horizons that match the available evidence:

- **Now:** active or ready work with a clear outcome, owner, and capacity.
- **Next:** validated direction whose prerequisites or capacity are not yet ready.
- **Later:** strategically relevant opportunities with material uncertainty.
- **Blocked:** valuable work with a named unresolved dependency or decision.
- **Rejected or paused:** considered work, the reason, and the condition for reconsideration.

Apply a consistent prioritization method when ranking is needed, but keep its inputs and sensitivity visible. Respect dependency order and realistic capacity; do not fill every team to 100% or hide operational, quality, support, compliance, and migration work. Use dates only for genuine commitments or time-bound constraints, and identify the authority behind them.

## Test coherence

- Every item should advance a stated outcome or obligation.
- The Now horizon should fit declared capacity and expose conflicting commitments.
- Dependencies must point to an owner or external condition, not vague “alignment.”
- Success measures should be observable and resistant to vanity metrics.
- High-uncertainty items should have learning milestones before delivery commitments.
- Removed, delayed, and rejected work should retain rationale so it is not silently reintroduced.

Call out tradeoffs, opportunity cost, concentration risk, and where sequencing changes under plausible capacity or evidence shifts.

## Deliver and maintain

Return the roadmap, material changes from the previous version, assumptions, blocked decisions, capacity or dependency risks, and the next review trigger. Link supporting requirements, research, architecture decisions, plans, and risk records where they exist.

Do not start implementation, assign people, change external planning systems, or communicate commitments unless the current request authorizes those actions. A roadmap remains current only while its evidence and assumptions hold; review it after material learning, capacity changes, incidents, strategic shifts, or at the declared cadence.
