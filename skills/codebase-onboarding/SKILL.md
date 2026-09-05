---
name: "codebase-onboarding"
display_name: "代码库上手指南"
display_name_en: "Codebase Onboarding"
description: "Use when onboarding engineers or contractors, rebuilding stale architecture docs, or preparing a repeatable technical handoff for an unfamiliar repository."
description_zh: "用于新工程师或承包商上手、重建过时架构文档，或为陌生代码库准备可复用技术交接资料。"
description_en: "Gather repository facts, map architecture and setup paths, inventory key files and boundaries, validate common commands, and produce audience-specific living onboarding documentation."
category: "development"
version: "0.1.0"
author: "alirezarezvani/claude-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to the target repository, documented setup/test commands, a clean or disposable validation environment, and an authorized documentation output path"
---

# Codebase Onboarding

## Purpose

Produce an evidence-backed onboarding packet for an unfamiliar repository. The packet should help a new contributor build a correct mental model, reach a passing baseline, perform common tasks safely, and know where ownership and integration boundaries lie. It is a living operational asset, not a prose tour or a substitute for repository instructions.

## Scope and authority

Default to read-only discovery. Define target revision, audience, output path, time budget, and exclusions before inspection. Do not modify application code, install arbitrary dependencies, run production commands, expose secrets, or infer undocumented permissions. Documentation edits require an authorized path and a reviewable diff.

## Step 1: gather facts

Inspect repository instructions, branch/status, top-level structure, manifests, build/test/lint configuration, CI workflows, deployment descriptors, ownership files, and recent history. Record exact revision and tool versions. Inventory:

- languages, frameworks, runtimes, package managers, and generated artifacts;
- entry points, service/module boundaries, public interfaces, storage, queues, and external integrations;
- configuration and environment variables by sensitivity (names only for secrets);
- setup, build, test, lint, debug, release, and rollback commands;
- key directories/files a contributor should read first;
- architectural decisions, compatibility constraints, and known hotspots;
- owners, contribution/review rules, and protected paths.

Separate observed facts, documented policy, and inference. Cite each important fact with a file, line/section, command result, commit, or CI link. If a signal cannot be verified, label it unknown rather than smoothing it into an authoritative sentence.

## Step 2: establish a clean baseline

Prefer a disposable or clean environment. Run only repository-native setup and verification commands that are documented and authorized. Record command, working directory, tool/version, duration, exit status, and safe diagnostic. Check that setup instructions actually work; do not publish a command that was merely copied from an old README.

Classify failures as pre-existing, environment/dependency, documentation drift, or task-owned. Never hide a baseline failure behind “setup complete,” and never claim a clean build when only a narrow check ran.

## Step 3: tailor by audience

| Audience | Emphasize |
|---|---|
| junior engineer | prerequisites, setup, first safe change, tests, guardrails, glossary |
| senior engineer/tech lead | architecture, contracts, trade-offs, operations, failure modes, decisions |
| contractor | bounded ownership, inputs/outputs, integration points, access limits, handoff and acceptance evidence |

Keep a common fact base and vary depth, not truth. Lead with the shortest path to a successful first contribution, then link deeper architecture and operational sections progressively.

## Document contract

Generate sections appropriate to the audience:

1. **What this repository does:** purpose, users/consumers, scope and non-goals.
2. **Fast path:** prerequisites, setup, baseline checks, and expected output.
3. **Repository map:** key directories/files and generated-versus-owned boundaries.
4. **Architecture:** components, data/control flow, external dependencies, trust boundaries, and failure containment.
5. **Common tasks:** exact commands for test, lint, debug, local run, migration, release, and rollback where verified.
6. **Contribution path:** smallest safe change, tests, review/ownership rules, branch policy, and handoff format.
7. **Troubleshooting:** symptom→diagnostic→likely cause→safe recovery, with known limitations.
8. **Decisions and vocabulary:** links to ADRs, policies, glossary, and unresolved questions.
9. **Freshness record:** source revision/date, validation commands/results, owner, and next review trigger.

Each command must state prerequisites and expected evidence. Each architecture assertion must identify its source or be marked inference. Do not include secret values, private logs, or copied source passages beyond what the documentation license permits.

## Drift and quality checks

Before delivery, compare the draft against current manifests, CI, scripts, ownership, and recent changes. Search for dead links, renamed paths, stale commands, missing environment variables, contradictory instructions, undocumented generated files, and architecture claims unsupported by code. Re-run the fast path after documentation changes when feasible. Flag unverified setup, missing access, and clean-environment differences visibly.

The guide is ready only when:

- a new reader can identify the first safe action and expected result;
- setup/test commands are reproducible or clearly marked unavailable;
- architecture and ownership boundaries are navigable;
- troubleshooting includes failure evidence and safe recovery;
- scope, secrets, permissions, revision, and freshness are explicit;
- the full documentation diff is reviewable and free of unrelated edits.

## WorkBuddy handoff

Report target revision, audience, inspected paths, exact commands/results, baseline limitations, generated document paths, evidence links, drift findings, unresolved unknowns, owner/review status, and next freshness trigger. If the repository cannot be safely inspected or setup cannot be validated, deliver a clearly labeled partial onboarding report instead of inventing certainty.
