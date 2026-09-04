---
name: "github-actions-engineering"
display_name: "GitHub Actions 工程"
display_name_en: "GitHub Actions Engineering"
description: "Use when authoring, reviewing, securing, optimizing, migrating, or diagnosing GitHub Actions workflows, reusable workflows, custom actions, CI gates, artifacts, caches, releases, or deployments."
description_zh: "编写、审查、加固、优化、迁移和诊断 GitHub Actions 工作流、复用工作流、自定义 Action、CI 门禁、缓存、制品、发布与部署。"
description_en: "Author, review, secure, optimize, migrate, and diagnose GitHub Actions workflows, reusable workflows, custom actions, CI gates, caches, artifacts, releases, and deployments."
category: "development"
version: "0.1.0"
author: "Don Artkins; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# GitHub Actions Engineering

Use this skill for files under `.github/workflows`, reusable workflows, repository-local custom actions, CI policies, release automation, and GitHub-hosted or self-hosted runners. Inspect repository languages, package managers, lockfiles, existing local commands, branch protection, environments, runner constraints, and GitHub Enterprise or Actions feature versions before editing. Preserve the project's chosen build and deployment systems unless replacement is requested.

## Define the workflow contract

For every workflow, record its triggering events and filters, trusted and untrusted inputs, required checks, job dependencies, runner and permissions, secrets or identity path, produced artifacts, external side effects, concurrency policy, timeouts, retry behavior, and success evidence.

Keep CI checks runnable locally through documented project commands where practical. The workflow should orchestrate those commands rather than hide critical validation in opaque YAML-only shell fragments. Pin runtime and package-manager versions consistently with the repository.

Use explicit job dependencies and conditions. A deployment or release should depend on every required gate and run only for the intended immutable commit or tag. Do not confuse a skipped gate with a passed gate; verify branch-protection behavior for conditional jobs.

## Treat event context as a security boundary

Code from forks and pull requests is untrusted. Prefer `pull_request` for testing contributor code because secrets are not exposed. Do not check out or execute untrusted head code in a privileged `pull_request_target`, `workflow_run`, issue-command, or repository-dispatch context. If a privileged follow-up workflow consumes an artifact or identifier from an untrusted run, validate its provenance, exact commit, producer workflow, conclusion, content, and size before use.

Treat branch names, commit messages, issue text, PR titles, matrix values, workflow inputs, artifact filenames, and API results as untrusted data. Pass values through environment variables or structured action inputs instead of interpolating expressions directly into shell source. Quote shell variables, use safe temporary files, and reject unexpected formats.

Set top-level `permissions: {}` or the narrowest read permission, then grant only the capabilities each job needs. Separate build/test jobs from jobs that write contents, packages, deployments, attestations, pull requests, or issues. Never expose broad tokens to steps that execute repository-controlled hooks, build scripts, test fixtures, or third-party code unnecessarily.

## Pin dependencies and identities

Pin third-party actions to immutable full commit SHAs and retain a readable version comment or dependency-update mechanism. Tags and branches can move. Review action source, transitive runtime, permissions, inputs, output handling, and network behavior before adding it. Prefer GitHub-maintained primitives where they satisfy the requirement, but still pin them according to project policy.

Use OpenID Connect with short-lived, audience- and repository-scoped cloud roles instead of long-lived deployment credentials when supported. Restrict trust by repository, branch or tag, workflow, and environment claims. Grant `id-token: write` only to the job that exchanges it. Masking is not access control: avoid printing, transforming, or placing secrets in command arguments, artifacts, caches, job summaries, outputs, debug logs, or matrix values.

Self-hosted runners may retain processes, files, credentials, network reachability, and caches. Do not run untrusted fork code on persistent privileged runners. Define isolation, ephemeral lifecycle, egress, labels, patching, cleanup, capacity, and incident ownership before selecting them.

## Build deterministic jobs

Use lockfile-enforced dependency installation and fail when the lockfile is inconsistent. Avoid globally mutable tool state and floating container tags. Set `timeout-minutes` proportionally; a hung job should release capacity. Add `concurrency` when superseded runs or simultaneous deployments would waste resources or violate correctness, and choose `cancel-in-progress` based on whether interruption is safe.

Use matrices for genuinely independent supported variants. Name dimensions clearly, bound expansion, decide whether `fail-fast` hides useful failures, and make experimental entries explicit. Avoid multiplying expensive end-to-end tests when a smaller compatibility matrix proves the contract.

Service containers need image/version pinning, health checks, isolated credentials, and readiness—not just process start. Make ports and network assumptions explicit. Collect sanitized logs on failure without leaking service passwords or production data.

## Handle caches and artifacts deliberately

A cache accelerates reproducible inputs; it is not a source of truth or a deployment artifact. Include OS, architecture, toolchain and lockfile hashes in keys, use constrained restore prefixes, and ensure untrusted changes cannot poison a privileged cache consumer. Do not cache credentials, signing material, repository tokens, generated secrets, or mutable production state. A cache miss must remain correct.

Artifacts cross job and workflow boundaries. Give them unique, collision-resistant names; constrain paths to intended files; set retention; verify size and contents; and preserve source commit, build configuration, checksums, SBOM or provenance as required. Promote the same verified artifact to later environments rather than rebuilding mutable source.

## Design releases and deployments

Use protected GitHub environments for sensitive targets and scope environment secrets to the deployment job. Define commit/tag eligibility, approval or policy gates, artifact identity, migration ordering, concurrency, canary or staged rollout, health evidence, rollback, and post-deploy verification. Do not infer permission to deploy from permission to edit workflow code.

Make releases idempotent around reruns: detect existing tags, releases, assets, deployments, and package versions; distinguish safe reconciliation from conflicting content; and verify checksums before overwriting or replacing anything. Avoid force-moving release tags or deleting published assets without explicit authorization.

Use environments and job summaries to expose what commit and artifact reached which target, without exposing secrets. Bind cloud identity and attestations to the exact repository, workflow, ref, and artifact digest.

## Diagnose by the earliest failing layer

Locate the first failure among trigger/filter selection, expression evaluation, permissions, checkout, runner provisioning, tool setup, dependency restore, cache, service readiness, build/test, artifact transfer, environment policy, identity exchange, API rate limit, deployment, or cleanup.

Capture the workflow and run URL, event, ref and immutable SHA, attempt, job and step, runner image or labels, action SHAs, sanitized logs, permissions, relevant input presence—not secret values—and recent workflow or dependency changes. Compare a rerun against the original attempt; reruns may use changed mutable action tags unless dependencies are pinned.

Use debug logging only when needed and review it for secret exposure. Do not “fix” authorization failures by granting repository-wide write permissions, switching to a privileged event, or placing secrets in fork-triggered jobs. Do not repeatedly rerun flaky workflows without bounding attempts and preserving evidence.

## Validate and hand off

Validate YAML and expressions, then exercise each meaningful event and condition: trusted push, fork PR, internal PR, tag, manual input, scheduled run, cancellation, timeout, cache miss, failed dependency, matrix failure, deployment gate, rerun, and concurrent invocation as applicable. Confirm required checks appear with stable names and failure blocks protected merges or deployments.

Test scripts through their local entry points. Verify least-privilege permissions, immutable action pins, secret isolation, artifact provenance, cache boundaries, shell quoting, retention, failure diagnostics, cancellation and rollback. For a proposed workflow, use a branch or isolated repository before affecting production targets.

Return changed files, trigger and trust model, job graph, permissions, dependency pins, local-equivalent commands, validation runs, artifact and cache contracts, cost or duration impact, deployment evidence, rollback path, and unresolved runner, security, or availability risks.
