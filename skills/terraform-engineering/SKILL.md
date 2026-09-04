---
name: "terraform-engineering"
display_name: "Terraform 与 OpenTofu 工程"
display_name_en: "Terraform and OpenTofu Engineering"
description: "Use when writing, reviewing, testing, or diagnosing Terraform/OpenTofu modules, plans, state, CI, imports, refactors, drift, or provider upgrades; inspect the real runtime and plan before any infrastructure mutation."
description_zh: "安全设计、审查和诊断 Terraform/OpenTofu 模块、计划、状态、测试、CI、漂移和基础设施变更。"
description_en: "Safely design, review, and diagnose Terraform/OpenTofu modules, plans, state, tests, CI, drift, and infrastructure changes."
category: "development"
version: "0.1.0"
author: "Anton Babenko; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
---

# Terraform and OpenTofu Engineering

Use this skill for Terraform or OpenTofu infrastructure-as-code work. Establish the runtime and exact version, providers and lock file, backend and workspace/state key, execution path, target account/project/region, environment criticality, and authorization before proposing commands. Read the repository's modules, variables, state conventions, CI policy, and existing plans rather than assuming a layout.

## Classify the risk first

Identify the dominant failure mode: unintended create/update/delete, resource-address churn, secret exposure, state or lock corruption, configuration drift, dependency cycles, provider upgrade, import/refactor, excessive blast radius, policy failure, or insufficient testing. State unsupported assumptions and the evidence needed to resolve them.

Never treat `terraform plan` as approval to apply. Planning may refresh remote objects, invoke data sources, expose sensitive values in artifacts, or differ from a later run. Production apply, import, state mutation, lock force-unlock, taint/replacement, or destroy requires explicit authorization for the exact environment and reviewed plan.

## Write stable configuration

Model reusable modules around a cohesive lifecycle and a narrow contract. Give variables explicit types, descriptions, validation, intentional nullability, and safe defaults. Marking a value `sensitive` only masks display; it can still enter state. Prefer workload identity and secret-manager references, and keep secret material out of configuration, variable files, logs, plans, and state whenever the provider supports that design.

Use stable resource identity. Choose `for_each` with meaningful keys when collection order can change; use `count` for a true optional singleton or when index identity is intentional. Do not convert between them or rename resource addresses without `moved` blocks or an explicit state migration verified by a no-destroy plan.

Make dependencies arise from references when possible. Add `depends_on` only for a real hidden ordering contract and document it. Avoid provisioners as a default orchestration mechanism; they are hard to model, retry, secure, and destroy. Pin the runtime, providers, and production modules according to the repository's upgrade policy, commit the lock file intentionally, and isolate dependency upgrades from unrelated infrastructure changes.

Do not hardcode a specific cloud, backend, naming scheme, directory layout, or workspace strategy unless the existing system requires it. Separate states by ownership, lifecycle, permissions, and blast radius—not an arbitrary resource count alone.

## Review the plan as the change artifact

Run formatting and initialization in a context that cannot silently rewrite production state. Validate configuration, then create a saved plan using the same variables, credentials class, backend, runtime, provider lock file, and commit that the authorized apply will use. Treat plan files and JSON as sensitive artifacts.

Review all actions, including replacements, data-source reads, moved/imported/forgotten resources, provisioners, unknown values, dependencies, and outputs. For every delete or replacement, identify the cause and dependent effects. A targeted plan can hide unrelated drift and is not proof that the whole stack is safe.

Summarize the reviewed artifact by create/change/destroy/import/move counts, identity and data-loss risks, externally visible impact, expected cost direction, policy results, rollback limits, and unresolved unknowns. Apply the reviewed saved plan where the workflow supports it; do not generate a fresh unreviewed plan during the apply stage.

Never run or recommend an unreviewed `destroy`, `-auto-approve` destructive action, or `-target` as a routine deployment mechanism. If destroy is explicitly requested, generate and inspect a destroy plan, enumerate implicit dependents, confirm backups and recovery, and require authorization immediately before execution.

## Handle state and drift carefully

Before state operations, confirm the backend, workspace/key, caller identity, locking, encryption, versioning, audit trail, and a recoverable backup or backend version. Do not edit a state file by hand. Prefer declarative `import`, `moved`, and `removed` blocks when supported by the actual runtime; otherwise document exact addresses and verify a before/after plan.

For a stuck lock, prove no live writer owns it using CI, remote-run, process, and backend evidence. Force-unlock only with explicit authorization and the exact lock ID. For backend migration, preserve the source, test credentials and locking, serialize writers, migrate with the supported command, and verify lineage, resource addresses, and a no-change plan before normal operations resume.

Diagnose drift by separating authorized out-of-band changes, provider normalization, volatile data, failed applies, and unmanaged resources. Decide whether code should adopt reality or infrastructure should return to code; do not automatically overwrite either. Record ownership and prevent recurrence.

## Test in layers

Select tests by risk and supported runtime:

- format and validate for syntax and provider schemas;
- lint, security, cost, and policy checks for organizational rules;
- saved-plan assertions for proposed actions and invariants;
- native tests or mocks for module logic when the version supports them;
- isolated real-provider integration tests for lifecycle and computed behavior;
- post-apply checks for the user-visible infrastructure outcome.

Mock tests cannot prove provider permissions, API behavior, quotas, eventual consistency, or real destroy cleanup. Plan-only tests cannot reliably assert values known only after apply. Use short-lived, uniquely named test infrastructure with budget and cleanup ownership; destructive test cleanup still needs the authority granted for that environment.

## Upgrade and refactor safely

Read the selected runtime and provider release notes and migration guides. Change runtime/provider/module constraints and the lock file intentionally. Test representative stacks, review schema changes and replacements, and separate the upgrade from functional changes when possible. Do not emit newer features such as native tests, import/moved/removed blocks, write-only attributes, or backend locking options without verifying the version floor and OpenTofu compatibility.

For module contract changes, preserve callers with additive inputs/outputs and deprecation where feasible. Find all call sites and state addresses before renaming. Validate that a refactor produces moves or no changes—not destroy/create—across every supported environment.

## Diagnose failures from evidence

Capture the exact command, sanitized error, runtime/provider versions, phase, resource address, backend/workspace, and whether partial remote or state changes occurred. Check state and provider/API reality independently before retrying. A retry can duplicate objects or deepen a partial apply; make it only when the operation is demonstrably idempotent or a reconciliation plan is understood.

Never expose credentials, plan contents containing secrets, state snapshots, or sensitive outputs in diagnostics. Do not disable TLS, policy, locking, or validation to bypass an error.

## Handoff

Return the execution context, risk category, changed artifacts, reviewed plan summary, assumptions, security and cost implications, validation evidence, authorization boundary, rollout, rollback or recovery limits, and unresolved risks. Distinguish configuration authored, plan verified, apply executed, and outcome observed; none implies the next without evidence.
