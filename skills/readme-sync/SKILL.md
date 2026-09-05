---
name: "readme-sync"
display_name: "README 同步校对"
display_name_en: "README Synchronization"
description: "Use after changes to features, commands, configuration, dependencies, APIs, project structure, or deployment workflows to keep README documentation aligned with the current repository and remove unsupported claims."
description_zh: "在功能、命令、配置、依赖、API、项目结构或部署流程变化后使用，确保 README 与当前仓库一致，并移除没有事实依据的描述。"
description_en: "Synchronize README content with code and configuration by checking commands, prerequisites, examples, structure, APIs, and limitations against repository sources of truth."
category: "content"
version: "0.1.0"
author: "hnidboubker/readme-async; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized repository with a README and discoverable source-of-truth files; repository-native checks when available"
---

# README Synchronization

Use this skill after a change that can affect user-facing or developer-facing documentation. The code, configuration, manifests, scripts, tests, and deployed contract are the sources of truth; the README describes the current state, not an intended or historical state. Keep the edit bounded and preserve the document's established tone and structure.

## Establish scope and baseline

Identify the target README, changed files, public audience, supported platforms, and the exact change that may have made documentation stale. Read the complete README before editing. Inspect only files that exist, such as manifests and lockfiles, environment examples, build/deploy files, source directories, scripts, docs, tests, and API definitions. Do not assume a package manager, framework, path, command, version, or feature.

Record repository status, diff/stat, recent commits, baseline validation failures, and relevant source paths. Treat uncommitted user work as part of the current context. Do not expose secrets, private paths, tokens, credentials, or production data while documenting configuration.

## Verify each documentation claim

Check the README against the repository's actual evidence:

- installation prerequisites, runtime versions, package manager, setup steps, and supported platforms;
- commands and arguments against scripts, Makefiles, task runners, and CI workflows;
- configuration keys, defaults, required/optional status, and safe placeholder values against config and examples;
- features and behavior against implementation, tests, API contracts, and flags;
- project structure against meaningful current directories, without generating a noisy full tree;
- API routes, parameters, response/error behavior, and examples against the authoritative contract;
- build, test, release, deployment, limitations, and recovery instructions against executable workflows;
- links, anchors, images, code fences, tables, and examples for existence and rendering hazards.

Classify every discrepancy as confirmed stale, likely stale, missing documentation, intentionally historical, or unknown. Never claim a feature exists because a TODO, old README paragraph, branch, or plan mentions it. Never remove a limitation or safety warning merely to make the project look complete.

## Update surgically

Make the smallest edit that makes the README truthful. Preserve headings, badges, links, images, tone, Markdown conventions, and useful examples unless they are themselves inaccurate. Add a feature only when the current code/config supports it; remove or revise obsolete commands, paths, prerequisites, flags, and screenshots. Prefer human-readable examples with placeholders such as `YOUR_API_KEY` and avoid copying real values.

When a claim cannot be verified, state the limitation or omit the claim. Do not rewrite the entire README, add generated inventories, expose internal workflow details, or silently alter unrelated documentation. If code and README disagree on intended behavior, report the conflict rather than choosing the more attractive version.

## Verify the result

Re-read the changed README and compare its claims against the same sources. Validate Markdown structure, internal links, code fences, table rendering risks, command names, and examples. Run the repository's native docs/build/lint/test checks that apply, plus safe read-only command discovery or help output when available. Record exact commands, working directory, exit codes, tool versions, and checks not executed.

Do not run installation, deployment, data mutation, or destructive “fix” commands merely because the README suggests them. A command's existence does not prove it succeeds in every environment. Separate syntax/link evidence from runtime evidence, and label network or browser checks as unverified when unavailable.

## Handoff

Return the changed README path, source-of-truth files consulted, corrected claims, removed/added sections, link and command checks, baseline limitations, remaining discrepancies, and rollback note. For review-only mode, leave files unchanged and report findings. Stop when README ownership, target scope, authoritative behavior, or the difference between current and intended state is ambiguous.
