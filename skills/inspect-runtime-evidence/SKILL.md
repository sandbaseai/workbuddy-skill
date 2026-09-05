---
name: "inspect-runtime-evidence"
display_name: "运行证据审查"
display_name_en: "Inspect Runtime Evidence"
description: "Use when determining whether an adapter, integration, feature, or package is actually executable from read-only runtime evidence."
description_zh: "用于根据只读运行证据判断适配器、集成、功能或软件包是否真正可执行。"
description_en: "Inspect immutable runtime evidence without mutating implementations, map requested capabilities to verified support, distinguish authoring from execution, classify evidence quality, and report gaps without claiming untested paths pass."
category: "development"
version: "0.1.0"
author: "DrHepa; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Read-only access to runtime reports, capability registries, package metadata, logs, traces, and platform-specific evidence"
---

# Inspect Runtime Evidence

Use this skill to answer “does it actually run and support the requested capability?” from evidence, not from labels, configuration, or an optimistic README. Stay read-only: do not mutate logic, assets, packages, evidence, runtime state, or release artifacts.

## Define the inspection

Record the exact adapter, integration, feature set, package, version, platform, environment, and requested capabilities. Use exact identifiers and capability names; never select by product genre, display label, or a similar-looking implementation. State the report identity, evidence time, scope, and out-of-scope paths.

## Map capabilities precisely

For every requested capability, map it to one status:

- **supported:** verified by current execution evidence;
- **extension-verified:** verified only through an explicitly named extension or adapter;
- **authoring-only:** can be configured or authored but has no execution proof;
- **blocked:** evidence shows a missing dependency, incompatible contract, permission, platform, or failure;
- **unknown:** evidence is absent, stale, partial, or contradictory.

Do not collapse unknown into supported. A missing hosted row is not a pass. A fake, recording, or deterministic test backend is local evidence only and must not be described as native or production execution.

## Assess evidence quality

For each claim, capture the exact evidence ID, report or snapshot version, platform, environment, input, observed output, timestamp, and status. Distinguish:

- authoring/configuration validity;
- static or schema validation;
- unit or headless execution;
- sandbox/native execution;
- integration or production-like execution;
- failed, timed-out, skipped, and not-run.

Check freshness, provenance, reproducibility, dependency versions, feature flags, permissions, data shape, and whether the evidence crosses the boundary being claimed. A successful mock does not prove a native dependency works. A package existing on disk does not prove its entry point, assets, or runtime contract works.

## Find crossed or stale evidence

Look for report IDs that do not match the selected version or platform, duplicated or conflicting capability rows, stale snapshots, unsupported fallback behavior, missing dependencies, incorrect package paths, environment drift, and evidence copied from another adapter. Mark the precise mismatch and reason code. Do not repair evidence during inspection.

When useful, use a read-only command to inspect manifests, registry snapshots, package contents, logs, or existing reports. Record the command and exit status, and stop when access, authorization, or data sensitivity makes further inspection unsafe.

## Complete the report

Return the exact support-report identity and status, selected adapter/capabilities, evidence IDs, evidence dimensions, missing-capability reason codes, stale/crossed-evidence findings, and limitations. Include the next authorized action for each unknown or blocked item.

Do not materialize or claim a release from this inspection. Do not claim runtime executability when only authoring or static evidence exists. A trustworthy “not verified” is a complete result when the required evidence is missing.

