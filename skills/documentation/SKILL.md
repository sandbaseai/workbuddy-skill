---
name: "documentation"
display_name: "技术文档"
display_name_en: "Documentation"
description: "Use when creating, auditing, or upgrading READMEs, API references, developer guides, docstrings, PR descriptions, or related project documentation."
description_zh: "用于创建、审计或改进 README、API 参考、开发者指南、文档字符串、PR 描述及相关项目文档。"
description_en: "Create accurate, scannable, maintainable documentation from repository evidence, with executable commands, audience-aware structure, portability, accessibility, and explicit handling of unknowns."
category: "documentation"
version: "0.1.0"
author: "SWE-pro-Agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Repository source, manifests, tests, CI, configuration, existing documentation, and verifiable project context"
---

# Documentation

Turn a real repository into accurate, useful, scannable documentation. Inspect the project before writing. Source code, manifests, lockfiles, tests, CI, configuration, existing docs, and license files are evidence; guesses are not.

## Determine the documentation task

Classify the work as create, upgrade, audit, rewrite, or focused section. Identify the audience: end user, contributor, developer, package consumer, reviewer, or a mix. For a multi-document change, list the surfaces first and keep their terminology and commands consistent.

## Build an evidence map

Inspect the tree, project type, manifests and lockfiles, entry points, scripts, configuration, environment examples, tests, CI/CD, containers, license and security files, and relevant source behavior. Map each factual claim to evidence and confidence. If a fact is missing or contradictory, omit it or label it as unknown and investigate rather than inventing it.

Never fabricate commands, features, supported platforms, versions, metrics, links, screenshots, badges, roadmap items, coverage, or production-readiness claims. Do not silently document behavior that conflicts with the implementation; record the discrepancy and its owner.

## Write for scanning and action

For a README, answer quickly: what is this, why use it, what can it do, can it be trusted, how is it installed, how is it used, and where is deeper documentation? Prefer this order when justified:

1. value proposition and verified proof;
2. capabilities and supported use cases;
3. prerequisites and installation;
4. shortest working quick start and expected result;
5. configuration and examples;
6. development, testing, contribution, security, and license links.

Move long API references, architecture internals, and tutorials to `docs/` when appropriate. Use short sections, meaningful headings, focused tables, and repository-relative links. Avoid filler, hype, badge spam, decorative markup, and a parallel vocabulary that the codebase does not use.

## Make commands executable

Derive every install, build, test, lint, format, and run command from manifests, scripts, contributor docs, CI, or configuration. Verify the dependency manager, runtime version, working directory, required environment, and expected output. State prerequisites and platform differences. If a command cannot be verified, do not present it as copy-ready.

Keep examples minimal but real. For APIs document request/response contracts, errors, authentication, limits, and versioning only when the repository supports those claims. For configuration document required variables, safe defaults, allowed values, secret handling, and failure behavior. Never expose credentials or private data in examples.

## Maintain quality

Keep docs next to the behavior they describe and update them in the same change. Check links, headings, code fences, paths, examples, spelling, accessibility, and narrow-screen readability. Give images meaningful alt text and prefer relative assets. Do not rely on color alone. Use badges only for verifiable, useful metadata.

For an audit, report each issue with location, evidence, impact, severity, and a concrete fix. Distinguish stale documentation, missing documentation, incorrect claims, broken commands, and style suggestions. For an update, report the evidence inspected, claims changed, commands checked, limitations, and remaining unknowns.

## Handoff

Deliver the intended audience and scope, changed documentation surfaces, evidence sources, verified commands, known limitations, unresolved inconsistencies, and next owner/action. Revisit docs when interfaces, configuration, workflows, dependencies, or operational guarantees change.

