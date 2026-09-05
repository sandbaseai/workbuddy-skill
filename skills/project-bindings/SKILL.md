---
name: "project-bindings"
display_name: "项目绑定清单"
display_name_en: "Project Bindings"
description: "Use when authoring or changing a repository's project-specific bindings such as module ownership, workspace roots, database locations, gate keys, namespaces, palettes, registry contracts, or release values; keep facts in one authoritative declaration."
description_zh: "用于创建或修改仓库的项目专属绑定，例如模块归属、工作区根目录、数据库位置、阶段键、命名空间、调色板、注册契约或发布值，将事实集中在唯一权威声明中。"
description_en: "Maintain one auditable repository bindings document for project-specific values consumed by otherwise project-neutral standards, without turning rules, design, behavior, or secrets into mutable configuration."
category: "development"
version: "0.1.0"
author: "iamthenop/infurnet-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Repository with governance entry point, project-neutral standards, and an authorized place for committed configuration declarations"
---

# Project Bindings

Use this skill when a repository needs to declare project-specific values that generic Skills and standards consume. A binding is a value that two repositories could change while both still follow the same rule: a package owner, workspace root, database/test directory, closed namespace, palette asset, release set, or registry identifier. Keep one authoritative bindings document at the repository root or the location named by governance.

## Separate values from rules

Bindings declare values; they do not create obligations. Put “the approved compute module is X” in bindings, but keep “only the approved compute module may do Y” in the standard that owns that rule. Do not put architecture decisions, workflow behavior, explanatory doctrine, or current runtime behavior into bindings. Code is the authority for current behavior; architecture documents own boundaries and contracts.

Never store secrets, tokens, passwords, private endpoints, environment credentials, or ephemeral deployment values as bindings. Use safe references or environment-owned configuration and document only the interface needed by consumers.

## Discover consumers before editing

Before adding, changing, renaming, or retiring a binding, identify every consumer: Skills, standards, build files, source code, tests, API documents, migrations, workflows, and generated projections. Verify the current declaration, ownership, value type, scope, default/undefined status, and evidence for the proposed change. A binding change is a consumer event; a partial update creates silent drift.

Do not invent a value because a consumer wants one. If a value is not decided, state `not yet defined` in the appropriate form and keep the consuming path blocked or explicitly fallback-only. Do not use a realistic placeholder that tools or agents could mistake for an approved value.

## Use a machine-readable declaration

Organize declarations by class, such as package/module ownership, workspaces, databases, namespaces, assets, release, and external contracts. Each entry should provide a stable name, value, and owning scope when it is not repository-global. Use tables or key/value forms that tools can parse; avoid narration between declarations that becomes a second source of truth.

Keep names stable and unambiguous. Closed sets belong in one declared table or list. Paths should be repository-relative where possible, validated to stay inside the workspace, and explicit about whether they are source, generated, test, or deployment paths. Distinguish a single value, a list, a closed vocabulary, and a per-service/per-database map rather than encoding all of them as opaque strings.

## Enforce consumer discipline

Consumers dereference a binding by its stable name; they do not copy its value into another Skill, standard, or document. Every binding should have a known consumer. Unused declarations are dead vocabulary and should be retired through the same impact review. Duplicate or contradictory declarations are not admitted: identify the existing authority and escalate the conflict before adding another.

Do not let a bindings file become a general settings dump. Build flags, secrets, runtime state, product behavior, and design content belong to their owning systems. A binding may name where those authorities live, their identifier, or the selected contract, but should not restate their contents.

## Change safely

Make one coherent binding change at a time. For a rename or move, create a consumer inventory, update all authorized consumers together, validate references and generated outputs, and preserve a migration/rollback path. For a split or merge, document the old/new names, scope mapping, compatibility window, and removal criteria. Review the diff for hidden copies, stale paths, unexpected generated files, and accidental secret exposure.

Treat binding edits as configuration changes with ownership and review, not as harmless text cleanup. Existing values may be mutable by design, but mutability does not reduce their authority: every consumer can break when a value moves.

## Validate and hand off

Run repository-native schema, link, path, build, configuration, and relevant test checks. Verify each declaration parses, each path exists or is explicitly deferred, each closed value is valid, each consumer resolves the intended name, and no undeclared duplicate is used. Record exact commands, exit codes, baseline failures, generated artifacts, environment assumptions, and checks not run.

Return the binding inventory, owners, consumer map, changed values, evidence, unresolved decisions, compatibility/migration impact, rollback plan, and next review gate. Stop when ownership, source-of-truth precedence, value approval, consumer coverage, or secret handling is ambiguous.
