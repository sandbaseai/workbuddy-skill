# Changelog

All notable changes to this project are documented here.

## Unreleased

- Added the MIT Python Background Jobs Skill with durable job state, at-least-once delivery, idempotency, bounded retries/deadlines, DLQs, backpressure, tenant reauthorization, cancellation, graceful shutdown, and recovery verification.
- Added the MIT Python Resilience Patterns Skill with transient/permanent failure classification, deadline budgets, jittered bounded retries, idempotency, circuit breaking, rate limits, backpressure, safe fallbacks, fault injection, and recovery verification.
- Added the MIT Python Observability Skill with structured logging, golden signals, correlation and trace propagation, bounded metric cardinality, privacy-safe schemas, telemetry failure isolation, alerting, retention, and measured overhead validation.
- Added the MIT Vector Index Tuning Skill with measured recall/latency/memory/build baselines, flat/HNSW/IVF/PQ selection, quantization, hard ACL filters, deletion lifecycle, versioned rebuilds, atomic cutover, rollback, and authorized production changes.
- Hardened release asset publication with sequential rate-limited uploads and retry-friendly GitHub CLI steps after a large-release API limit event.
- Added the MIT Hybrid Search Implementation Skill with dense/sparse retrieval, RRF and weighted fusion, query routing, reranking, ACL-before-return, score calibration, edge-case handling, index lifecycle, privacy, cost/latency baselines, and authorized experiment gates.
- Added the MIT LLM Evaluation Skill with versioned task corpora, automated and human metrics, RAG grounding/citation checks, judge calibration, bias and uncertainty reporting, regression thresholds, privacy-safe evidence, and production-experiment authorization gates.
- Added the MIT Distributed Tracing Skill with OpenTelemetry context propagation, semantic spans, sampling, trace-log correlation, tail-latency diagnosis, collector backpressure, privacy-safe attributes, bounded overhead, and authorized telemetry changes.
- Added the MIT Spark Optimization Skill with measured execution baselines, plan/stage diagnosis, partition and shuffle tuning, AQE, skew and join handling, cache and memory controls, result-equivalence checks, cost limits, and isolated production-write boundaries.
- Added the MIT RAG Implementation Skill with ingestion and chunk provenance, ACL-before-retrieval, dense/sparse/hybrid search, reranking, citation verification, prompt-injection handling, refusal thresholds, evaluation, index lifecycle, privacy, cost, and authorization boundaries.
- Added the MIT Airflow DAG Patterns Skill with idempotent and observable DAG design, logical-date scheduling, dependency sensors, bounded retries, branching, failure classification, testing, safe backfills, and production-side-effect boundaries.
- Added the MIT dbt Transformation Patterns Skill with layered source/staging/intermediate/mart design, versioned contracts, tests, documentation and lineage, incremental watermark and late-data controls, cost-aware CI, isolated targets, and production-write boundaries.
- Added the MIT Workflow Orchestration Patterns Skill with deterministic workflow/activity boundaries, idempotent activities, bounded retries and timeouts, payload limits, version compatibility, Saga compensation, human approval gates, and recovery testing.
- Added the MIT Error Handling Patterns Skill with failure taxonomy, typed error contracts, safe context propagation, resource cleanup, async cancellation, bounded retries, circuit breakers, fail-closed degradation, observability, and synthetic fault validation.
- Added the MIT Secrets Management Skill with provider-agnostic storage, workload identity, least-privilege CI/CD injection, fork/PR trust controls, rotation and revocation, scanning, auditability, value-free evidence, and explicit mutation authorization.
- Added the MIT API Design Principles Skill with resource and HTTP semantics, schema-first GraphQL, pagination, idempotency, concurrency, authorization, versioning, consumer migration, query-cost, rate-limit, contract-test, and rollback boundaries.
- Added the MIT Data Quality Frameworks Skill with versioned data contracts, six quality dimensions, bounded sampling, incremental validation, evidence-backed baselines, failure classification, expiry-aware exceptions, privacy-safe reports, and cost-controlled read-only boundaries.
- Added the MIT Screen Reader Testing Skill with declared browser/assistive-technology matrices, landmark and keyboard checks, ARIA/form validation, dynamic announcements, automation-versus-manual evidence separation, and safe testing boundaries.
- Added the MIT Test-Driven Development Skill with RED/GREEN/REFACTOR, expected-failure verification, real-behavior assertions, minimal implementation, mock limits, full regression gates, explicit exceptions, and safe fixture boundaries.
- Added the MIT Subagent-Driven Development Skill with isolated plan-task execution, fresh scoped workers, task-level specification and quality reviews, bounded fix loops, recovery ledgers, final whole-branch review, and explicit merge/release authority boundaries.
- Added the MIT Writing Implementation Plans Skill with scope checks, file/interface maps, bite-sized testable tasks, global constraints, dependency and rollback gates, placeholder self-review, and explicit planning-versus-implementation boundaries.
- Added the MIT Systematic Debugging Skill with red-capable feedback loops, boundary evidence, backward data-flow tracing, working-versus-broken comparisons, falsifiable hypotheses, one-variable tests, regression gates, and architecture escalation after repeated failed fixes.
- Added the MIT Chrome DevTools Diagnostics Skill with snapshot-first interaction, console/network correlation, bounded script evaluation, authorized emulation, performance traces, side-effect classification, and redaction-safe browser evidence.
- Added the MIT Acquire Codebase Knowledge Skill with seven-document evidence contracts, intent-versus-reality checks, stack and integration mapping, history-aware concerns, explicit TODO/ASK USER states, generated-artifact exclusions, and read-only redaction boundaries.
- Added the MIT Bug Reproduction Brief Skill with fact/assumption separation, environment capture, one-variable minimization, repeatability evidence, safe isolated fixtures, stop-before-repair boundaries, and redaction-aware handoffs.
- Added the MIT Agent Supply Chain Integrity Skill with deterministic manifests, file-drift classification, dependency pinning audits, provenance chains, fail-closed promotion gates, symlink/root containment, and read-only evidence boundaries.
- Added the MIT AWS CloudWatch Investigation Skill with bounded Logs Insights and metric queries, alarm/deployment correlation, blast-radius narrowing, timeline reconstruction, baseline validation, counterevidence, and read-only redaction-safe evidence handoffs.
- Added the MIT GitHub Release Skill with immutable diff classification, SemVer rationale, changelog preparation, repository-native gates, PR/direct authority modes, tag and asset reconciliation, failure handling, rollback, and evidence-bounded completion.
- Added the MIT Architectural Decision Record Skill with decision-question framing, fact/assumption/unknown ledgers, evidence-backed alternatives, coded consequences, immutable ADR lifecycle links, approval-state integrity, and validation/review handoffs.
- Added the MIT Agent Governance Skill with composable least-privilege policies, pre-tool intent checks, exact approval binding, bounded delegation and rate limits, fail-closed behavior, privacy-safe audit trails, trust-score safeguards, and enforcement verification.
- Added the MIT Dependabot Management Skill with ecosystem and directory inventory, monorepo and multi-ecosystem grouping, schedule and cooldown controls, security/version-update separation, triage safeguards, least-noise policies, and owner/expiry-aware handoffs.
- Added the MIT Incident Post-Mortem Skill with blameless evidence contracts, UTC timeline reconstruction, impact reconciliation, systemic causal analysis, counterevidence, accountable dated actions, redaction, and publication gates.
- Added the MIT AWS Well-Architected Review Skill with six-pillar evidence contracts, IaC/live-state reconciliation, architecture mapping, risk calibration, trade-off handling, report-first remediation, and explicit issue-publication and rollback boundaries.
- Added the MIT Azure Deployment Preflight Skill with Bicep/azd detection, syntax and parameter validation, identity and RBAC boundaries, read-only what-if previews, change classification, secret-safe reports, approval gates, and rollback evidence.
- Added the MIT AWS Resource Query Skill with strict read-only command boundaries, intent and scope parsing, account/region confirmation, service query mappings, pagination completeness, bounded execution, sensitive-output redaction, and observed-versus-inferred handoffs.
- Added the MIT GitHub Actions Efficiency Skill with measured CI baselines, runner-minute versus wall-clock analysis, cache/concurrency/path/matrix reviews, required-check guardrails, safe optimization ranking, rollback-aware validation, and measured-versus-modeled impact reporting.
- Added the MIT GitHub Actions Hardening Skill with trigger trust mapping, expression-injection review, least-privilege permissions, secret and output boundaries, immutable action supply-chain checks, runner exposure analysis, and evidence-linked remediation reports.
- Added the MIT Agentic Evaluation Skill with explicit evaluation contracts, deterministic-first checks, reflection and evaluator-optimizer patterns, bounded refinement, convergence detection, judge calibration, privacy-safe evidence, and human-review gates.
- Added the MIT Code Tour Skill with persona-targeted narrative paths, verified repository anchors, CodeTour step guidance, manual validation fallbacks, secret-safe output, and explicit limits on commands and unsupported navigation behavior.
- Added the MIT Cloud Resource Health Skill with exact-resource scoping, control-plane/data-plane separation, bounded metric and log diagnosis, dependency correlation, confidence states, privacy-safe reports, and authorized reversible remediation verification.
- Added the MIT Technical Spike Skill with one-question framing, evidence and confidence tracking, bounded prototypes, explicit stop conditions, safe synthetic-data defaults, cleanup verification, actionable recommendations, and unresolved-risk handoffs.
- Added the MIT Cloud Design Patterns Skill with problem-first pattern selection, reliability/performance/messaging/security/deployment maps, explicit trade-offs, bounded contracts, anti-pattern checks, validation gates, and retirement criteria.
- Added the MIT Microservices Architect Skill with evidence-backed boundary discovery, contract and data ownership design, sync/async trade-offs, bounded failure behavior, tracing, migration compatibility, rollback, and modular-monolith alternatives.
- Added the MIT Database Query Optimizer Skill with safe baselines, plan evidence, PostgreSQL/MySQL guidance, single-variable changes, execution-risk controls, lock/replication/write-amplification checks, rollback, and before/after verification.
- Added the MIT Cloud Architect Skill with evidence-backed multi-cloud discovery, decision criteria, security and reliability boundaries, cost and quota checks, migration waves, disaster-recovery proof, rollback gates, and implementation handoff.
- Added the MIT Cloud Cost Optimization Skill with measured cost-driver ranking, utilization and trade-off checks, current-price assumptions, reversible savings plans, commitment sequencing, attribution, budgets, anomaly alerts, and authorization gates for financial or destructive changes.
- Simplified the public README to focus on WorkBuddy usage, discovery, installation, curated capabilities, provenance, compatibility, and contribution guidance while removing internal catalog-building and maintenance constraints.
- Added the MIT Chaos Engineer Skill with authorized experiment contracts, measurable steady-state hypotheses, blast-radius caps, dry-run preflight, tested abort paths, secret-safe evidence, recovery verification, and tracked learning follow-ups.
- Added the MIT Network Troubleshooting Skill with layer-by-layer DNS, routing, transport, TLS, HTTP, policy, resource-limit, and MTU isolation, bounded diagnostics, secret-safe evidence, explicit authorization gates, and verified remediation.
- Added the MIT Parallel Agent Dispatch Skill with independence proofs, isolated assignments, bounded concurrent orchestration, result review, conflict-aware integration, full verification, and secret/authority boundaries.
- Added the MIT Plan Execution Skill with canonical-plan review, task ledgers, ordered checkpoints, focused and integrated verification, recovery boundaries, authority controls, deviation tracking, and durable handoffs.
- Added the MIT Git Worktree Isolation Skill with isolation detection, safe path and ignore checks, baseline verification, branch and Agent boundaries, conflict recovery, ownership-safe cleanup, and direct-work exceptions for authorized automation.
- Added the MIT Review Feedback Triage Skill with complete review intake, evidence ledgers, reproduction and consumer checks, YAGNI and compatibility decisions, item-level verification, factual pushback, and inline-thread hygiene.
- Added the MIT Audit Integrity Gate Skill with evidence contracts, anti-rationalization checks, mandatory second passes, bounded retry handling, coverage-gap states, calibrated quality scoring, safe lessons, and fail-closed WorkBuddy handoffs.
- Added the MIT Evidence Map Builder Skill with falsifiable decision framing, bounded source regions, typed reasoning nodes and edges, preserved counterevidence, explicit unknowns, portable JSON, honest validation labels, and authorized source verification.
- Added the MIT Agent Decision Receipts Skill with action-before-side-effect binding, receipt decision criteria, canonical manifests, secret-safe input hashes, offline signature verification, key isolation, explicit unsigned states, and policy-scoped handoffs.
- Added the MIT Document-to-Skill Pipeline Skill with rights gates, bounded extraction, incremental fold-in, progressive-disclosure budgets, structure-first synthesis, authority non-expansion, link and provenance validation, and safe WorkBuddy packaging.
- Added the MIT Checkpointed Agent Loop Skill with a packaged dependency-free checkpoint tool, bounded attempt budgets, legal state transitions, atomic persistence, evidence requirements, resumable recovery, malformed-state protection, and explicit approval boundaries.
- Added the CC0-1.0 Memory Discipline Skill with bounded recall, durable single-fact saves, provenance, supersession instead of deletion, contradiction handling, evidence/policy separation, no-memory fallback, and safe WorkBuddy memory boundaries.
- Added the MIT Agent Session Audit Skill with local discovery, capability-level reporting, cost/token/failure/retry/latency signals, missing-data safeguards, privacy boundaries, reproducible CI gates, and partial/unavailable outcomes.
- Added the MIT Codebase Onboarding Skill with revision-bound fact gathering, clean-baseline validation, audience-specific guidance, architecture and ownership mapping, executable task paths, troubleshooting evidence, drift checks, and safe partial handoffs.
- Added the MIT Evidence Before Claims Skill with claim-to-proof mapping, fresh full-scope verification, regression evidence, remote-state checks, deletion safeguards, partial-evidence classification, redaction, and authority-aware handoff.
- Added the MIT Agent Document Design Skill with context-pointer contracts, progressive disclosure, information hierarchy, exhaustive completion criteria, leading-word guidance, positive instructions, pruning, trigger evaluations, and safe WorkBuddy boundaries.
- Added the MIT Architecture Friction Scan Skill with history-based hot-spot selection, deep-module/deletion-test analysis, seam and test-friction evidence, candidate ledgers, ADR-aware ranking, structured report guidance, and read-only WorkBuddy boundaries.
- Added the MIT Tight Bug Loop Skill with red-capable symptom tests, deterministic feedback loops, minimization, falsifiable hypothesis ranking, selective instrumentation, seam-level regression tests, redaction, and cleanup evidence.
- Added the MIT Git Guardrails Skill with effect classification, command normalization, repository-scoped policy, explicit exceptions, protected-ref safeguards, secret-safe diagnostics, disposable-worktree verification, and recovery maintenance.
- Added the MIT Merge Conflict Resolution Skill with exact operation-state inspection, primary-intent tracing, hunk ledgers, semantic resolution, native validation, protected-branch safeguards, and recoverable completion/abort boundaries.
- Added the MIT Wayfinding Skill with destination-first scope, canonical decision maps, frontier/dependency tracking, research/prototype/task classification, evidence-backed resolution, local-tracker fallback, and safe cross-session handoff.
- Added the MIT Specification Synthesis Skill with evidence-led problem framing, user stories, highest-seam planning, implementation/testing decisions, explicit scope, consistency checks, and gated external publication.
- Added the MIT Domain Modeling Skill with canonical vocabulary, glossary challenges, concrete scenario stress tests, code/evidence cross-checks, consumer mapping, implementation-free context files, selective ADRs, and safe WorkBuddy handoff boundaries.
- Added the MIT Codebase Design Skill with deep-module vocabulary, smallest-honest interfaces, evidence-based seams, adapter discipline, test-surface design, safe refactoring, and explicit WorkBuddy execution boundaries.
- Added the MIT Context Retrieval Skill with bounded query decomposition, semantic/keyword/hybrid search selection, access-before-context filtering, provenance and coverage ledgers, freshness/conflict handling, calibrated retrieval metrics, and explicit empty-result safeguards.
- Added the MIT Skill Supply Chain Audit Skill with immutable provenance, read-only inspection, archive hazard checks, instruction and capability inventory, least-privilege disposition, version comparison, evidence labels, safe verification, and owner-led recovery.
- Added the MIT Multi-Agent Orchestration Skill with bounded decomposition, acyclic dependency graphs, minimum-authority scopes, structured handoffs, single-writer safety, approval references, failure accounting, integration verification, and explicit residual risk.
- Added the MIT Tool Schema Design Skill with intent boundaries, bounded JSON Schema guidance, explicit effects and authority, confirmation/idempotency/error contracts, contrastive selection tests, provider limitations, and implementation-drift verification.
- Added the MIT MCP Server Building Skill with bounded capabilities, explicit effects and data classes, structural tool contracts, independent authorization, token audience safeguards, protocol-version verification, interoperability tests, and reversible operations guidance.
- Added the MIT Human in the Loop Skill with risk-tiered oversight, immutable approval binding, quorum and separation-of-duties controls, timeout/escalation handling, execution-time reauthorization, redacted decision records, compensation, and recovery verification.
- Added the MIT Agent Red Teaming Skill with target-specific authorization, rules of engagement, privilege mapping, safe synthetic test matrices, traceable findings, bounded execution, cleanup, remediation retesting, and explicit residual risk.
- Added the MIT Context Optimization Skill with auditable context budgets, conservative deduplication, relevance and information-density scoring, provenance-preserving ordering, coverage validation, exclusion ledgers, and sensitive-domain safeguards.
- Added the MIT Prompt Injection Defense Skill with trust-boundary mapping, enforceable authority invariants, least-privilege tool controls, safe synthetic adversarial tests, provenance preservation, incident containment, and explicit residual-risk reporting.
- Added the MIT Agent Observability Skill with trace and event contracts, content-free telemetry defaults, metric and alert definitions, sampling and retention controls, trace-graph verification, privacy safeguards, and partial-evidence handoff.
- Added the Apache-2.0 Sev1 First 15 Minutes Skill with explicit incident roles, read-first diagnosis, authorized reversible stabilization, redacted evidence, communication cadence, escalation boundaries, and auditable handoff.
- Added the MIT Video Transcript Research Skill with bounded video/channel discovery, provider authorization and quota boundaries, timestamp provenance, caption-quality uncertainty, batch monitoring, and copyright/privacy safeguards.
- Added the MIT Study Materials Kit Skill with source manifests, chapter modeling, original-question provenance, bounded generation, dependency-aware knowledge graphs, offline/print validation, and extraction-limitation reporting.
- Added the MIT Recurring Process Capture Skill with repeat-pattern evidence, readiness classification, bounded backlog/skeleton outputs, planned-versus-active state, secret exclusion, and authoring handoff.
- Added the MIT Skill Authoring Skill with intent and trigger contracts, executable-first design, representative evaluation, safe capability declarations, context-aware disclosure, packaging, and quality gates.
- Added the MIT Skill Progressive Refactor Skill with contract freezing, core/detail separation, bounded reference extraction, rollback preservation, behavior checks, and complete post-refactor quality re-audit.
- Added the MIT Skill Quality Audit Skill with complete read-only structure, UX, procedure, model metadata, capability, security, license, provenance, and context-budget checks.
- Added the MIT Durable Work Ledger Skill with verified execution boundaries, stable task state, claims and leases, checkpoints, owner attention routing, bounded search, secret exclusion, and auditable handoffs.
- Added the MIT Agent Discoverability Skill with four-surface registry/OAuth/manifest/DNS modeling, consistency checks, least-privilege publication, certificate-pinning safeguards, redacted diagnostics, and real-client verification.
- Added the MIT Multi-Source Knowledge Library Skill with source manifests, one-reference-per-source structure, master routing, structure-over-summary extraction, coverage ledgers, conflict handling, and incremental maintenance safeguards.
- Added the MIT Deep Evidence Research Skill with scoped research briefs, multi-angle retrieval, atomic claim ledgers, independent corroboration, citation audits, disagreement handling, and reproducible handoff.
- Added the MIT Project Bindings Skill with single-source project values, rule/value separation, consumer inventories, secret exclusion, conflict detection, migration safety, and reference validation.
- Added the MIT API Documentation Skill with source-of-truth discipline, stable operation structure and anchors, precise request/response/error tables, route/type conventions, safe examples, surgical contract changes, and verification gates.
- Added the MIT GitHub Research Skill with search-surface selection, candidate ranking, immutable provenance, license/security checks, rate-limit handling, and reproducible research reports.
- Added the MIT Database Schema Design Skill with authority boundaries, initialization strata, database-enforced integrity, least privilege, migration safety, approved seeds, catalog-level tests, and rollback evidence.
- Added the MIT README Synchronization Skill with source-of-truth checks for commands, configuration, features, APIs, structure, links, limitations, and surgical documentation updates.
- Added the MIT Workflow State Modeling Skill with stable lineage, gate-as-state modeling, bounded statuses, transition and replay semantics, architecture-multiplication checks, and migration evidence.
- Added the MIT Java Service Coding Standards Skill with repository-aligned layering, API/error contracts, authorization, transaction and idempotency boundaries, safe persistence, operations, testing, and handoff gates.
- Added the MIT Modern CSS Pro Tips Skill with semantic tokens, cascade ownership, intrinsic responsive layout, accessible states, progressive enhancement, motion safeguards, and browser-evidence verification.
- Added the MIT Confidence-Gated Task Routing Skill with per-unit tier assignment, objective escalation, independent verification, bounded handoffs, and post-run calibration.
- Added the MIT Agent Quality Grading Skill with evidence-bounded task, speed, tool, message, asset, and prompt/config evaluation plus privacy-safe reporting and retest guidance.
- Added the MIT Skill Sunset Audit Skill with bounded read-only discovery, deterministic drift checks, conservative verdicts, reversible remediation, experiment safeguards, and evidence-based handoff.
- Added the MIT Premium UI Craft Skill with evidence-driven hierarchy, semantic tokens, complete interaction states, responsive navigation, accessibility, restrained motion, and visual verification.
- Added the MIT Data Engineering Pipeline Best Practices Skill with data contracts, delivery semantics, idempotent processing, quality and reconciliation gates, lineage, privacy, observability, replay, backfill, and recovery handoff.
- Added the MIT Business Continuity Design Skill with business-impact analysis, critical dependency mapping, degraded and manual operating modes, RTO/RPO evidence, recovery exercises, communications, governance, and accountable retest handoff.
- Added the MIT Modular Design Principles Skill with boundary rationale, state ownership, public contracts, consistency and failure semantics, isolation testing, coupling diagnostics, and safe migration handoff.
- Added the MIT Multi-Format Document Analysis Skill with bounded file discovery, format-aware extraction, page and line provenance, OCR and parser limitations, numerical reconciliation, privacy-safe reporting, and non-execution safeguards.
- Added the MIT Cloud-Native Security Best Practices Skill with asset and trust-boundary mapping, workload identity, supply-chain integrity, network and tenant isolation, secret handling, runtime safeguards, safe verification, and recovery handoff.
- Added the MIT Access Control Security Best Practices Skill with authorization-contract mapping, least privilege, RBAC/ABAC safeguards, tenant isolation, indirect-path testing, revocation and cache considerations, and auditable handoff.
- Added the MIT Deep Project Primer Skill with instruction precedence, repository and architecture mapping, evidence pointers, safe reconnaissance, contract and rollback awareness, and reproducible context-restoration handoff.
- Added the MIT Playwright Web App QA Skill with critical-path contracts, isolated test contexts, visible-state assertions, console/network diagnostics, responsive and negative-state coverage, redacted artifacts, and flaky-test transparency.
- Added the MIT Bug Triage and Fix Analysis Skill with evidence-bounded intake, stack-trace analysis, hypothesis testing, duplicate and regression assessment, severity/priority separation, safe fix proposals, and verification handoff.
- Added the MIT Log Monitoring and Pattern Detection Skill with bounded log evidence, normalized pattern detection, cross-source correlation, privacy-safe alert design, missing-data handling, and reproducible reporting.
- Added the Apache-2.0 Release Traceability Skill with source-to-runtime identity mapping, artifact and digest invariants, host-rebuild detection, deployment and rollback evidence, fail-closed verification, and auditable release handoff.
- Added the MIT Migration Validation Skill with baseline capture, layered post-cutover health and data checks, performance and integration validation, observability and backup gates, authoritative platform-fact verification, rollback readiness, and sign-off evidence.
- Added the MIT Frontend Review Skill with state and interaction coverage, responsive and browser checks, accessibility, data and error handling, performance, frontend security, evidence-based findings, and retest handoff.
- Added the MIT Backend Review Skill with input and authorization checks, contract and error semantics, transaction and consistency boundaries, dependency/resource safety, persistence and migration review, failure behavior, and regression handoff.
- Added the MIT Breaking Change Review Skill with contract-surface mapping, bidirectional compatibility analysis, mixed-version checks, schema and migration risk, consumer evidence, versioning, rollout, rollback, and deprecation gates.
- Added the MIT Compliance Review Skill with diff-first control inspection, purpose and minimization, consent and retention, auditability, access segregation, financial controls, regulatory traceability, evidence classification, and retest handoff.
- Added the MIT Escalation Policy Skill with explicit trigger and non-trigger checks, authority boundaries, sensitive-context transfer, policy-backed timing, emergency routing, audit trails, and accountable closure.
- Added the MIT Repository Formatting Skill with repository-root detection, declared formatter selection, dependency and scope safety, bounded recovery, formatting-only diff review, post-format checks, and reproducible handoff.
- Added the Apache-2.0 Launch Risk Review Skill with scoped input and destination checks, AI detection, cross-functional risk categories, evidence calibration, blocker classification, specialist routing, rollout gates, and accountable handoff.
- Added the Apache-2.0 Integration Health Check Skill with read-only connection validation, credential and scope checks, authorized target resolution, capability discovery, ambiguity handling, redaction, and safe continuation rules.
- Added the Apache-2.0 Go Testing Skill with package-boundary decisions, `require` versus `assert` guidance, deterministic fixtures, race-aware diagnostics, scoped verification, and reproducible handoff.
- Added the MIT LLM Application Security Skill with trust-boundary mapping, input and retrieval isolation, tenant authorization, tool-side-effect controls, output safeguards, abuse prevention, and safe remediation evidence.
- Added the MIT Test-Driven Development Skill with behavior-first RED tests, smallest-change GREEN implementation, evidence-preserving REFACTOR loops, adjacent boundary checks, and reproducible handoff.
- Added the MIT Accessibility Review Skill with evidence-first UI inspection, semantic and keyboard checks, focus and ARIA validation, assistive-technology limitations, severity-based findings, and retest handoff.
- Added the MIT Inspect Runtime Evidence Skill with exact capability mapping, read-only inspection, evidence provenance and freshness, platform-level execution statuses, stale/crossed evidence detection, and uncertainty-aware support reports.
- Added the MIT Respec Skill for evidence-driven specification revisions, explicit scope and non-goals, observable acceptance contracts, compatibility and migration checks, approval traceability, and safe delivery handoff.
- Added the MIT Documentation Skill with repository reconnaissance, evidence mapping, executable-command verification, audience-aware structure, accessibility and portability guidance, documentation audits, and uncertainty-aware handoff.
- Added the MIT Code Reviewer Skill with diff-first review, correctness and regression checks, scope control, security and operational checkpoints, actionable severity-based findings, and explicit build/merge recommendations.
- Added the MIT Debugging Methodology Skill with safe reproduction, minimized cases, boundary isolation, causal hypotheses, controlled experiments, durable fixes, regression verification, and uncertainty-aware handoff.
- Increased scheduled public Skill catalog refreshes from daily to every six hours while retaining bounded crawling, rate-limit backoff, validation, and automatic publication safeguards.
- Added the MIT Security Audit Skill with bounded scope, trust-boundary mapping, control verification, safe tool use, risk classification, compliance evidence, remediation ownership, retesting, and residual-risk handoff.
- Added the MIT Test Runner Skill with fast/full modes, repository-native command selection, safe scope and environment handling, failure classification, flake transparency, and reproducible test reporting.
- Added the MIT Regression Risk Review Skill with diff-first evidence gathering, compatibility-path analysis, high-risk behavior checks, prioritized machine-readable findings, regression-test guidance, rollout safeguards, and accountable handoff.
- Added the MIT Release Planner Skill with deployment sequencing, expand-and-contract migrations, rollout waves, blast-radius controls, measurable go/no-go gates, rollback and recovery, observability, communication, and post-release cleanup.
- Added the MIT Architecture Decision Skill with decision framing, measurable quality attributes, alternative comparison, ADR recording, fitness functions, migration and rollback safeguards, operational handoff, and review triggers.
- Added the MIT Performance Engineering Skill with representative baselines, load/stress/soak/spike testing, profiling, bottleneck evidence, performance budgets, capacity boundaries, safe optimization, and regression gates.
- Added the MIT Data Governance Skill with flow mapping, ownership, enforceable data contracts, consent and suppression, identity resolution, lineage, quality monitoring, safe fallbacks, and reversible change management.
- Added the MIT Feature Flags Skill with typed flag contracts, deterministic evaluation, safe defaults, progressive rollout, experimentation evidence, administration controls, emergency mitigation, and lifecycle cleanup.
- Added the MIT AI Governance Skill with lifecycle gates, risk classification, NIST AI RMF mapping, human oversight, fairness/privacy/security evidence, transparency, exceptions, incident handling, and accountable handoffs.
- Added the MIT Site Reliability Engineering Skill with user-centered SLI/SLO design, error budgets, toil reduction, blameless incident learning, sustainable on-call, capacity, graceful degradation, and progressive delivery.
- Added the MIT Design Systems Skill with semantic token layers, accessible component contracts, executable documentation, versioning and migration, governance, visual evidence, and adoption metrics.
- Added the MIT Mobile Development Skill with platform selection, offline-first behavior, lifecycle-safe architecture, performance budgets, accessibility, secure storage, real-device testing, and staged delivery.
- Added the MIT Privacy Engineering Skill with data classification, minimization, purpose and consent controls, subject-rights workflows, retention and vendor governance, DPIA inputs, and breach-ready evidence.
- Added the MIT FinOps Skill with the Inform/Optimize/Operate cycle, allocation, unit economics, anomaly investigation, commitment and rightsizing safety, forecasting, maturity, governance, and evidence-based handoffs.
- Added the MIT FinOps Skill with the Inform/Optimize/Operate cycle, allocation, unit economics, anomaly investigation, commitment and rightsizing safety, forecasting, maturity, governance, and evidence-based handoffs.
- Added the MIT MCP Security Skill with tool provenance, trust boundaries, five-layer validation, server-side authorization, side-effect controls, tenant isolation, secret handling, audit telemetry, and incident containment.

## [0.50.0] - 2026-09-05

- Added Microsoft's official Apache-2.0 Playwright component-testing source to the Atlas with immutable commit and blob provenance; its conservative credential-path signal remains disclosed after review.
- Added the Playwright Component Testing Skill with application-owned story galleries, observable callback state, configuration-preserving setup, deterministic visual checks, isolation proof, incremental migration, and trace-first diagnosis.

- Added the MIT Product Analytics Skill with privacy-aware event contracts, funnel and cohort definitions, data-quality checks, statistically defensible experiments, guardrails, and reproducible handoffs.

## [0.48.0] - 2026-09-05

## [0.47.0] - 2026-09-05

- Added Microsoft's MIT-licensed eval-guide generator source to the Atlas with immutable commit and blob provenance.
- Added the platform-independent AI Agent Evaluation Engineering Skill covering capability versus trust and safety, representative and adversarial cases, observable trajectories, calibrated graders, paired comparisons, failure recovery, regression gates, latency, and cost.

## [0.46.0] - 2026-09-05

- Added the MIT dbt Patterns Skill with layered models, explicit grains and contracts, incremental and snapshot safety, data quality tests, lineage, bounded validation, and production handoff guidance.

## [0.45.0] - 2026-09-05

- Added the MIT Browser Automation Skill with bounded navigation, stable selectors, safe side-effect handling, privacy controls, bounded extraction, and reproducible end-to-end verification.

## [0.44.0] - 2026-09-05

- Added NVIDIA's official Apache-2.0 RAG evaluation source to the Atlas with immutable commit and blob provenance; its conservative credential-path and dynamic-eval signals remain disclosed after review.
- Added the tool-independent RAG Evaluation Skill with leakage-resistant datasets, stage-level retrieval and context metrics, grounded-answer and citation review, permission and prompt-injection gates, calibrated judges, paired comparisons, latency and cost evidence, and reproducible failure diagnosis.

## [0.43.0] - 2026-09-05

- Added the Apache-2.0 API contract source from the 29k-star `simstudioai/sim` repository to the Atlas, with its immutable commit, blob SHA, static analysis, license, and NOTICE provenance.
- Added the API Resilience Engineering Skill with end-to-end deadline budgets, safe retries, honest idempotency semantics, fair rate and concurrency limits, bounded queues, circuit breakers, bulkheads, ambiguous-outcome reconciliation, and attempt-level proof.

## [0.42.0] - 2026-09-05

- Curated the existing MIT-0 AWS resilience source from `aws-samples/sample-aws-resilience-skill` without inflating Atlas discovery counts.
- Added the AWS Resilience Assessment Skill with critical-journey dependency maps, shared-fate and failure-mode analysis, target-versus-evidence RTO/RPO review, restore and failover proof, cost-aware risk prioritization, read-only inspection boundaries, and safely bounded resilience experiments.

## [0.41.0] - 2026-09-05

- Curated the existing MIT GitHub Actions source from `DonArtkins/griot` without inflating Atlas discovery counts.
- Added the GitHub Actions Engineering Skill with event trust boundaries, least-privilege jobs, immutable dependencies, OIDC identities, deterministic matrices, safe caches and artifacts, idempotent releases, protected deployments, and reproducible diagnosis.

## [0.40.0] - 2026-09-05

- Curated the existing MIT Kafka source from `ssrjkk/claude-skills` without inflating Atlas discovery counts.
- Added the Kafka Event Streaming Engineering Skill with explicit event and partition contracts, honest end-to-end delivery semantics, idempotent effects, consumer lifecycle controls, schema compatibility, poison-record handling, replay safety, and evidence-based diagnosis.

## [0.39.0] - 2026-09-05

- Curated the existing MIT Cache Engineering source from `Dankosik/go-service-template-rest` without inflating Atlas discovery counts.
- Added the Cache Engineering Skill with evidence-based value decisions, complete multi-tenant key contracts, freshness and invalidation ordering, bounded miss collapse, outage recovery, mixed-version rollout, and falsifiable performance proof.

## [0.38.0] - 2026-09-05

- Added the MIT Docker source from `codewithmukesh/dotnet-claude-kit` to the Atlas, increasing it to 11,104 indexed paths across 5,769 repositories; its static credential-example signal remains disclosed in provenance.
- Added the Container Image Engineering Skill with reproducible multi-stage builds, cache correctness, secret-safe dependency access, runtime isolation, supply-chain evidence, staged diagnosis, and clean-build verification.

## [0.37.0] - 2026-09-05

- Added the MIT KubeShark source to the Atlas, increasing it to 11,003 indexed paths across 5,708 repositories.
- Added the Kubernetes Production Operations Skill with failure-stage diagnosis, workload and probe contracts, least-privilege security, exact rendering and diff review, explicit production authorization, rollout observation, and state-aware recovery.

## [0.36.0] - 2026-09-05

- Added Anton Babenko's official Apache-2.0 Terraform Skill to the Atlas, increasing it to 10,902 indexed paths across 5,632 repositories.
- Added the Terraform and OpenTofu Engineering Skill with execution-context discovery, stable resource identity, reviewed plan artifacts, state and drift controls, layered testing, version-aware upgrades, and explicit infrastructure mutation boundaries.
- Fixed adapter resource discovery so Markdown heading fragments resolve to the referenced file instead of producing false missing-resource failures.

## [0.35.0] - 2026-09-05

- Added the official MIT Supabase PostgreSQL source to the Atlas, increasing it to 10,801 indexed paths across 5,558 repositories.
- Added the PostgreSQL Database Engineering Skill with version-aware schema changes, query-plan evidence, index tradeoffs, lock and connection controls, RLS verification, maintenance safety, and tested recovery.

## [0.34.0] - 2026-09-05

- Added the MIT OAuth and OIDC Troubleshooting Skill with protocol-stage reconstruction, secret-safe evidence handling, redirect and session diagnosis, PKCE and token validation, authorization boundaries, falsifiable hypotheses, and security regression tests.

## [0.33.0] - 2026-09-05

- Added the MIT GraphQL API Design and Review Skill with client-grounded schemas, resolver authorization, robust pagination and errors, operation-cost controls, N+1 verification, subscription boundaries, and evidence-based schema evolution.
- Corrected the monitoring adaptation manifest so its packaged-resource inventory describes the final self-contained WorkBuddy package rather than the temporary source-adapter output.

## [0.32.0] - 2026-09-05

- Added the MIT Monitoring and Observability Design Skill with journey-based SLIs/SLOs, bounded-cardinality telemetry, decision-focused dashboards, actionable alerts, privacy and cost controls, and end-to-end signal-path validation.

## [0.31.0] - 2026-09-05

- Added the MIT MySQL Database Operations Skill with version-aware schema discovery, bounded parameterized queries, execution-plan safety, index tradeoffs, transaction controls, and explicit production authorization.

## [0.30.0] - 2026-09-05

- Added the MIT Evidence-based Data Analysis Skill with explicit analysis units, data-quality profiling, statistical limits, causal-claim discipline, robustness checks, reproducibility, and source-to-output traceability.

## [0.29.0] - 2026-09-05

- Added the MIT Applying Differential Privacy Skill with explicit adjacency, contribution bounds, mechanism selection, reproducible composition accounting, utility checks, budget-ledger controls, and qualified release claims.

## [0.28.0] - 2026-09-05

- Added the MIT OpenAPI Contract Review Skill with structural validation, semantic checks, security-scheme review, baseline compatibility analysis, consumer-path testing, and explicit tool coverage.

## [0.27.0] - 2026-09-05

- Added the MIT Code Security Review Skill with scoped diff analysis, attacker-controlled data-flow tracing, authorization checks, exploitability evidence, calibrated severity, and explicit review limitations.

## [0.26.0] - 2026-09-05

- Added the MIT Threat Modeling Skill with evidence-grounded boundaries, attacker capabilities, end-to-end abuse paths, control validation, residual-risk ownership, and explicit live-system safety limits.

## [0.25.0] - 2026-09-05

- Added the MIT User Research Synthesis Skill with source inventories, privacy controls, atomic evidence coding, contradiction analysis, confidence rationale, decision-linked gaps, and auditable insight traceability.

## [0.24.0] - 2026-09-05

- Added the MIT Product Roadmap Planning Skill with outcome-based items, evidence confidence, capacity-aware horizons, dependencies, explicit rejected work, coherence checks, and review triggers.

## [0.23.0] - 2026-09-05

- Added the MIT Data and Schema Migration Skill with compatibility contracts, expand/migrate/contract staging, idempotent backfills, reconciliation, production stop conditions, and tested recovery.

## [0.22.0] - 2026-09-05

- Added the MIT Project Pre-mortem Skill with evidence-constrained failure paths, cross-functional risk lenses, measurable warning signals, owned mitigations, residual-risk acceptance, and review triggers.

## [0.21.0] - 2026-09-05

- Added the MIT Architecture Decision Record Skill with measurable decision drivers, fair option comparison, evidence confidence, reversible adoption, fitness functions, and explicit review triggers.

## [0.20.0] - 2026-09-05

- Added the MIT Incident Response and Triage Skill with incident command, evidence hygiene, authorization boundaries, reversible containment, recovery verification, and blameless follow-up.

## [0.19.0] - 2026-09-05

- Added the MIT Prioritization Matrix Skill with framework selection, evidence-linked inputs, comparable scales, dependency handling, visible formulas, and sensitivity analysis.

## [0.18.0] - 2026-09-05

- Added the MIT Requirements Grounding Skill with source classification, solution-free problem framing, observable completion, confidence, recovery-mode evidence, and decision records.

## [0.17.0] - 2026-09-05

- Added the MIT Email Drafting Skill with recipient and attachment checks, factual fidelity, privacy controls, phishing awareness, and explicit draft-versus-send authorization.

## [0.16.0] - 2026-09-05

- Added the MIT Research with Sources Skill with primary-source prioritization, recency checks, conflict analysis, claim-level citations, prompt-injection resistance, and explicit uncertainty.

## [0.15.0] - 2026-09-05

- Added the MIT Software Release Skill with supply-chain verification, migration safety, staged rollout, stop conditions, rollback, monitoring, and consumer-path validation.

## [0.14.0] - 2026-09-05

- Added the MIT Meeting Notes Skill with source-grounded decisions, action items, owners, risks, privacy controls, and explicit uncertainty.

## [0.13.0] - 2026-09-05

- Added the MIT CLI Testing Skill with installed-artifact coverage, isolated fixtures, stream and signal verification, bounded processes, and destructive-path safeguards.

## [0.12.0] - 2026-09-05

- Added the MIT Performance Improvement Skill with reproducible baselines, profiling evidence, controlled experiments, production safeguards, and regression protection.

## [0.11.0] - 2026-09-05

- Added the MIT Work Handoff Skill with live-state verification, executable restart steps, and privacy-safe context preservation.

## [0.10.0] - 2026-09-05

- Added the MIT Test Strategy Design Skill with risk traceability, explicit test oracles, execution gates, ownership, and residual-risk reporting.

## [0.9.0] - 2026-09-05

- Added the MIT Accessibility Review Skill with evidence-based severity, manual verification, and honest conformance boundaries.

## [0.8.0] - 2026-09-05

- Added the Apache-2.0 Dense Writing Skill with evidence, nuance, attribution, and safety-preservation rules.
- Added the Apache-2.0 Open Source License Review Skill for dependency and release compliance checks.
- Improved folded YAML frontmatter parsing and preserved `argument-hint` when adapting Skills.

## [0.7.0] - 2026-09-05

- Added the MIT Spreadsheet Operations Skill with WorkBuddy-specific fidelity, safety, and output verification rules.
- Connected the new adaptation to the Atlas as a directly installable WorkBuddy-ready result.

## [0.6.0] - 2026-09-05

- Added the Apache-2.0 Systematic Debugging Skill as the second reviewed WorkBuddy adaptation.
- Fixed adaptation of resource paths written as inline code so referenced files are no longer silently omitted.
- Expanded validation and release packaging to every curated Skill.

## [0.5.0] - 2026-09-04

- Made Atlas results shareable, sortable, deduplicated, and directly usable through copied catalog IDs.
- Added guarded packaging of reviewed catalog entries with immutable provenance.

## [0.4.0] - 2026-09-04

- Added compatibility and conservative static review signals for indexed Skills.
- Added the reviewed-skill adaptation workflow and bilingual guidance.

## [0.3.0] - 2026-09-04

- Published the searchable [WorkBuddy Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/).
- Expanded the provenance-only catalog to 10,100 public `SKILL.md` paths.
- Added dynamic Atlas metrics, local catalog search, and stricter provenance validation.
- Added weekly incremental refreshes with validated snapshots and automated PR handling.
- Added security, support, and community review guidance.

## [0.2.0] - 2026-09-04

- Added the initial searchable catalog and resilient packaging fallback.
- Published the first 10,000-source catalog snapshot.

## [0.1.0] - 2026-09-04

- Released the installable SandBase WorkBuddy Skill package.

[0.3.0]: https://github.com/sandbaseai/workbuddy-skill/releases/tag/v0.3.0
[0.7.0]: https://github.com/sandbaseai/workbuddy-skill/releases/tag/v0.7.0
[0.6.0]: https://github.com/sandbaseai/workbuddy-skill/releases/tag/v0.6.0
[0.5.0]: https://github.com/sandbaseai/workbuddy-skill/releases/tag/v0.5.0
[0.4.0]: https://github.com/sandbaseai/workbuddy-skill/releases/tag/v0.4.0
[0.2.0]: https://github.com/sandbaseai/workbuddy-skill/releases/tag/v0.2.0
[0.1.0]: https://github.com/sandbaseai/workbuddy-skill/releases/tag/v0.1.0
