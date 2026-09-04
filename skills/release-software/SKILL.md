---
name: "release-software"
display_name: "软件发布"
display_name_en: "Software Release"
description: "Prepare, verify, publish, and monitor a release with artifacts, migrations, rollout, and rollback."
description_zh: "准备、验证、分阶段发布并监控软件版本，覆盖构建产物、迁移、供应链、停止条件和回滚。"
description_en: "Prepare, verify, stage, publish, and monitor a software release across artifacts, migrations, supply chain, stop conditions, and rollback."
category: "development"
version: "0.1.0"
author: "skills contributors; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Release Software

Prepare and execute a release as a controlled state transition, not merely a tag
or upload. Use this Skill for libraries, applications, services, containers,
plugins, datasets, or infrastructure bundles.

## Confirm scope and authority

Record the target version, channel, source revision, release destination,
supported environments, intended audience, and person or policy authorized to
publish. Distinguish preparation, dry run, staging, and production publication.

Never infer permission to publish from a request to prepare, review, package,
or write release notes. Do not bypass required reviews, protected environments,
signing controls, or deployment approvals.

## Release workflow

1. Compare the exact source revision with the previous release. Classify user
   impact, breaking changes, deprecations, security fixes, dependency changes,
   configuration changes, data migrations, and operational requirements.
2. Establish preflight checks and stop conditions. Confirm clean source,
   required CI results, credentials by name, destination, capacity, maintenance
   window, backups, observability, and on-call ownership.
3. Build from a clean, reproducible checkout. Verify tests, dependency locks,
   generated files, package contents, checksums, signatures, attestations,
   software bill of materials, and provenance when the project supports them.
4. Exercise install, upgrade, downgrade, and rollback paths in a representative
   disposable environment. For database or schema changes, verify forward and
   backward compatibility, backup restoration, transaction boundaries, and the
   point after which rollback is no longer safe.
5. Write user-facing notes with behavior changes, upgrade steps, migration
   commands, known issues, compatibility, security impact, and rollback advice.
   Do not expose embargoed vulnerabilities or secret values.
6. Sequence irreversible operations last. Prefer staged rollout, canary,
   percentage or region gates, and explicit pauses where the platform allows.
7. At every stage, compare health signals to a recorded baseline. Include error
   rate, latency, saturation, queue depth, data integrity, business events, and
   support signals relevant to the release.
8. Stop or roll back when a defined threshold is crossed. Do not continue a
   failing rollout merely because some steps already succeeded.
9. Independently verify the published artifact and deployed behavior from the
   consumer path; do not treat a successful upload command as proof of release.

## Safety rules

- Keep secrets out of commands, logs, release notes, and artifacts.
- Resolve the exact repository, registry, environment, region, and version
  before any state-changing action.
- Do not overwrite an existing immutable version. Investigate a collision and
  publish a new version when required by the ecosystem.
- Prefer recoverable actions and preserve evidence needed for incident review.
- If rollback would cause data loss or is untested, state that before rollout
  and use a safer forward-fix or restore plan approved for the system.
- Do not announce availability until the release is actually accessible to the
  intended audience.

## Completion record

Record the final version, commit, artifact URLs or digests, checksums, target
environments, migration outcome, rollout stages, health evidence, known issues,
and rollback status. Clearly mark skipped, failed, pending, and unverified
checks.

A release is complete only when the intended consumer can retrieve or use the
verified version and critical signals remain healthy for the defined observation
window. If monitoring must continue beyond the current session, leave a named
owner, stop condition, and executable handoff.
