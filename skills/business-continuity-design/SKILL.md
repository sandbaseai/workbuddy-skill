---
name: "business-continuity-design"
display_name: "业务连续性设计"
display_name_en: "Business Continuity Design"
description: "Design and validate business continuity through impact analysis, critical dependencies, recovery objectives, resilient operating modes, exercises, and accountable recovery plans."
description_zh: "通过影响分析、关键依赖、恢复目标、韧性运行模式、演练和责任闭环设计并验证业务连续性。"
description_en: "Design and validate business continuity through impact analysis, critical dependencies, recovery objectives, resilient operating modes, exercises, and accountable recovery plans."
category: "development"
version: "0.1.0"
author: "Hermes Agent; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Business Continuity Design

Use this skill when a product or organization must continue critical work
during outages, supplier loss, cyber incidents, facility disruption, staffing
shortages, or degraded dependencies. Continuity includes people, processes,
technology, data, communications, and decisions; a backup or disaster-recovery
runbook alone is not a continuity plan.

## Establish the continuity contract

Identify critical services and user outcomes, owners, stakeholders, regions,
legal or contractual duties, planning horizon, and assumptions. Perform a
bounded business-impact analysis covering minimum acceptable service, priority
tiers, time-to-harm, maximum tolerable downtime, data-loss tolerance, and the
impact of interruption on customers, safety, revenue, operations, compliance,
and reputation.

Inventory critical people, facilities, suppliers, systems, data, communication
paths, and operator access. Map dependencies, single points of failure,
concentration risk, and manual fallback capacity. Separate stated RTO/RPO goals
from measured capability; a policy does not prove a recovery objective is met.

## Design resilient operating modes

For each critical service define normal, degraded, manual, and recovery modes.
Document entry criteria, declaration authority, allowed functionality, customer
and staff communications, data consistency rules, security controls, capacity
limits, and exit criteria. Graceful degradation must not silently weaken
identity, authorization, privacy, audit, or safety controls.

Map failure behavior for dependencies such as identity providers, DNS,
certificates, payment paths, queues, caches, replicas, third parties, and
operator access. Assess alternate suppliers for capacity, data handling,
jurisdiction, compatibility, and ownership. Manual procedures must name people,
tools, inputs, volume limits, quality checks, and sustainable duration.

## Prepare and test recovery

1. Inventory authoritative data, backups, replicas, configuration, secrets,
   images, runbooks, contacts, and access required for recovery.
2. Define backup frequency, retention, separation, encryption, restore order,
   integrity checks, and ownership.
3. Make recovery steps ordered, bounded, reversible where possible, and include
   preconditions plus stop and rollback conditions.
4. Exercise representative restore, failover, dependency substitution,
   degraded mode, communications, and access-revocation paths in a controlled
   scope.
5. Measure elapsed time, data loss, correctness, capacity, operator load,
   alerting, and user-visible behavior against declared objectives.
6. Convert failed assumptions into owned actions with due dates and retest
   triggers.

Never delete evidence, overwrite the only copy, expose secrets, or test against
production without explicit authorization and a recovery plan. A tabletop
proves decision and communication readiness, not technical restore; automated
failover proves neither data correctness nor business acceptance without
independent validation.

## Governance and handoff

Assign service, technical recovery, business decision, communications, and
vendor owners. Keep contact data, dependency inventories, and runbooks fresh
without putting sensitive details in broadly accessible documents. Review after
material system, supplier, staffing, regulatory, or threat changes and after
every exercise or incident. Classify gaps by impact, time to harm, likelihood,
detectability, concentration risk, and evidence confidence.

```text
Service / owner / scope / planning assumptions:
Business impact and priority tier:
Minimum service / MTD / RTO / RPO and evidence:
People, process, technology, data, supplier, and facility dependencies:
Normal / degraded / manual / recovery modes:
Recovery steps, authority, stop conditions, and communications:
Exercise or incident results and measured gaps:
Actions / owners / due dates / retest triggers:
Residual risk, approvals, and next review:
```

State what was exercised, what was merely documented, and what remains
unverified. A continuity plan is ready when outcomes, dependencies, authority,
safe fallbacks, and recovery evidence are explicit and owned.
