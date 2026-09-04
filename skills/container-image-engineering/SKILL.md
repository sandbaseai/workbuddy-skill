---
name: "container-image-engineering"
display_name: "容器镜像工程"
display_name_en: "Container Image Engineering"
description: "Use when authoring, reviewing, optimizing, or diagnosing Dockerfiles, build contexts, Compose services, or OCI images; preserve application behavior while improving reproducibility, supply-chain integrity, caching, size, and runtime isolation."
description_zh: "安全设计、审查和诊断 Dockerfile、构建上下文、多架构镜像、缓存、供应链、运行时权限与容器启动问题。"
description_en: "Safely design, review, and diagnose Dockerfiles, build contexts, multi-platform images, caching, supply chain, runtime privileges, and container startup failures."
category: "development"
version: "0.1.0"
author: "Mukesh Murugan; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Container Image Engineering

Use this skill for Dockerfiles, Docker/BuildKit builds, Compose development environments, and OCI-compatible images. Inspect the application runtime, build system, repository layout, target platforms, deployment runtime, registry, network constraints, and existing CI before writing a container recipe. Preserve the user's chosen language, base distribution, and orchestrator unless a change is part of the request.

## Define the image contract

Record the build inputs, output artifact, entrypoint and arguments, listening interface and port, writable paths, user identity, environment/configuration, signal and shutdown behavior, health semantics, CPU/memory expectations, supported architectures, and required certificates or native libraries. Distinguish build-time dependencies from runtime dependencies and local-development conveniences from production requirements.

Do not assume an image that builds will start correctly, handle termination, pass a health probe, or run under the target security policy. Validate those behaviors explicitly.

## Make builds reproducible and reviewable

Use a narrow build context and a `.dockerignore` based on actual repository needs. Exclude version-control data, local caches, test results, credentials, `.env` files, editor state, package stores, and unrelated artifacts; do not blindly exclude files required by compilation or runtime.

Prefer multi-stage builds when they keep compilers, package managers, source, and temporary credentials out of the runtime image. Copy dependency manifests before frequently changing source when the build system supports a correct cached restore. Use cache mounts and bind mounts only with a documented BuildKit/version floor and without making the output depend on undeclared local state.

Pin language dependencies through their native lock files. Choose base-image tags intentionally and record the resolved digest for production reproducibility; digest pinning also requires a defined update process for security fixes. Keep build arguments for non-sensitive configuration only. A secret passed through `ARG`, `ENV`, a copied file, command text, or ordinary layer can remain in image history or cache.

Use BuildKit secret or SSH mounts for authorized private dependency access, then verify the secret is absent from the final filesystem, history, metadata, attestations, and logs. Never ask for or print live registry tokens, private keys, package credentials, or application secrets.

## Minimize without breaking compatibility

Select the smallest runtime base that satisfies libc, CA certificate, time-zone, locale, native library, debugging, and operational requirements. Alpine, distroless, scratch, and chiseled images have real compatibility and observability tradeoffs; do not recommend them from size alone.

Combine commands when it prevents package-index or temporary-file residue, but do not collapse unrelated build steps so aggressively that caching and diagnosis become worse. Copy only runtime artifacts with explicit ownership and permissions. Avoid `ADD` when `COPY` is sufficient, and do not fetch mutable remote content without integrity verification.

Measure compressed image size, unpacked size, layer composition, build duration, and cache reuse before claiming an optimization. Confirm the new image preserves cold start, throughput, memory, and application behavior when those outcomes matter.

## Reduce runtime privilege

Create or use a stable non-root user and group, ensure required directories are writable before switching users, and avoid broad `chmod 777` fixes. Prefer a read-only root filesystem, dropped capabilities, no privilege escalation, constrained mounts, and a minimal writable temporary area when the deployment platform supports them.

Do not bake configuration or credentials into the image. Inject runtime secrets through the target platform's secret mechanism with least-privilege access. Treat labels, environment variables, build metadata, SBOMs, and error output as potentially public.

Use exec-form `ENTRYPOINT`/`CMD` or a deliberate init wrapper so the application receives signals as PID 1 and reaps children when required. Verify graceful shutdown under the actual stop signal and timeout. Expose documentation ports only as metadata; publishing a port is a separate runtime decision.

## Preserve supply-chain evidence

Use trusted registries and scoped CI identities. Scan the final image and its dependencies, but report scanner database time, severities, fix availability, reachability limits, and accepted exceptions. A clean scan is not proof of safety.

Generate an SBOM and provenance/attestation where the build platform supports them. Sign artifacts only through the project's established identity and key policy. Promote the same immutable digest between environments instead of rebuilding from a mutable source reference. Record base digest, source commit, build configuration, target platforms, and output digest.

## Review Compose and local orchestration

Treat Compose as an environment contract, not production hardening by default. Verify build context, dependency readiness, networks, volumes, restart behavior, port collisions, platform selection, and persistent-data ownership. `depends_on` ordering alone does not prove a service is ready. Avoid real credentials in checked-in Compose files or example connection strings that train users to reuse weak secrets.

Named-volume removal, bind-mount writes, and `down -v` can destroy data. Require explicit authorization and identify the exact volumes before destructive cleanup.

## Diagnose by stage

Locate the earliest failing stage: context transfer, Dockerfile parse, base resolution, dependency download, compilation, export, registry push/pull, runtime creation, entrypoint, health, networking, storage, or shutdown. Capture the exact command, builder/engine version, target platform, sanitized error, stage, cache status, image digest, exit code, and runtime configuration.

For architecture errors, compare image manifests, host/node platform, and native binaries. For startup failures, inspect effective entrypoint/arguments, user, working directory, permissions, dynamic libraries, environment presence—not values—and prior logs. For networking, distinguish build network, container network, published host ports, DNS, proxy, and application bind address.

Do not resolve TLS or registry errors by disabling certificate verification, and do not run privileged containers or mount the container engine socket merely to bypass permissions.

## Validate

Build from a clean checkout with the intended builder and target platforms. Run the image as non-root with production-like read-only and resource constraints, test startup, a representative request, health, termination, filesystem writes, configuration failure, and architecture compatibility. Inspect history and contents for excluded files and secrets, scan the final—not only builder—stage, and verify the published digest can be pulled and run in an isolated test environment.

Return the Dockerfile or findings, assumptions, build/runtime versions, image and base digests, size and timing evidence, cache behavior, security/supply-chain results, functional tests, deployment constraints, rollback image digest, and unresolved risks. Distinguish local build success, registry publication, deployment, and observed application health.
