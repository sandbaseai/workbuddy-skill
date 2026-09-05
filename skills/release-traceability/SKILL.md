---
name: "release-traceability"
display_name: "发布可追溯性"
display_name_en: "Release Traceability"
description: "Use when changing or auditing CI/CD, build artifacts, deployment contracts, runtime release identity, or any build-to-deploy-to-verify path."
description_zh: "用于变更或审计 CI/CD、构建产物、部署契约、运行时版本标识，或任何从构建到部署再到验证的发布链路。"
description_en: "Keep a release auditable from source commit through immutable build artifact, deployment, runtime identity, and verification; detect provenance gaps, mixed versions, rebuilds, and unverifiable gates; and produce evidence-backed release decisions."
category: "development"
version: "0.1.0"
author: "ai-workspace-services/portal; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
compatibility: "Authorized repository, CI/CD configuration, build metadata, artifact registry, deployment target, runtime health or release endpoint, and verification access"
---

# Release Traceability

Audit and improve the chain from source commit to deployed runtime. The central invariant is that the artifact tested, the artifact published, and the artifact running are the same intended release—or any difference is explicit, bounded, and approved. Do not rebuild silently on a target host, overwrite an immutable tag, or call a deployment verified from a control-plane success message alone.

## Map the release chain

Inventory source revision, branch/tag, build workflow, dependency and tool versions, generated files, image/package/artifact digest, registry or storage location, signing/attestation, deployment manifest, environment, rollout mechanism, runtime release identity, health endpoint, verification job, and rollback artifact. Identify who owns each transition and which metadata is propagated. Record absent links and mutable identifiers as risks.

## Preserve the required invariants

Verify that:

- build output carries an immutable or commit-derived release identity and enough metadata to locate its source;
- the deployment consumes the published artifact or digest selected by policy, rather than rebuilding from an ambiguous checkout;
- target hosts do not compile or mutate the release artifact outside the approved build boundary;
- runtime health or release metadata exposes the active identity without leaking secrets;
- validation compares source/build metadata, published artifact, deployed configuration, and runtime output;
- promotion, rollback, migration, and mixed-version behavior are observable and have explicit abort criteria.

Check image/package tags, digests, lockfiles, generated manifests, environment overrides, caches, artifact retention, signatures, SBOM/provenance, deployment logs, and release notes. Follow the identity through asynchronous jobs and multiple services. Treat a mutable `latest`-style reference, missing digest, stale cache, host-side rebuild, or runtime endpoint without version evidence as a traceability gap even if the service is healthy.

## Validate with evidence

Use repository-native CI checks, artifact inspection, deployment metadata, read-only runtime endpoints, logs, metrics, traces, and synthetic probes within the approved scope. Compare expected and observed commit/artifact/runtime identities, timestamps, environment, configuration, and health. Record exact commands, workflow/run IDs, artifact digest, target, endpoint, tool versions, evidence locations, and limitations. Never expose credentials, tokens, private URLs, or sensitive runtime data.

Classify each gate as **pass**, **pass with follow-up**, **fail**, **not run**, or **unknown**. Separate build, registry, deployment, runtime, and verification failures. A passing build does not prove deployment; a reachable endpoint does not prove it runs the intended artifact; and a matching version string without independently checked provenance is weak evidence.

## Handle gaps and releases

For each finding record severity, transition and location, expected identity, observed identity, evidence, impact, owner, remediation, acceptance criteria, and retest. Prefer immutable digests, signed or attestable metadata, explicit propagation, fail-closed verification, and a single source of release identity. Define rollout waves, promotion gates, rollback artifact and data compatibility, recovery owner, alerting, and cleanup of superseded artifacts.

Before sign-off, validate source→build→publish→deploy→runtime→verify as a complete path and state any unverified link. The handoff includes the release graph, identities and digests, commands and run IDs, environment, gate results, deviations, rollback readiness, residual risk, approvals, and exact next action. Re-run the traceability check after CI, artifact, deployment, runtime, or verification changes.
