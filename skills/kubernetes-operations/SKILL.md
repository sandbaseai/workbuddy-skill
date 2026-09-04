---
name: "kubernetes-operations"
display_name: "Kubernetes 生产运维"
display_name_en: "Kubernetes Production Operations"
description: "Use when designing, reviewing, deploying, or diagnosing Kubernetes manifests, Helm charts, Kustomize overlays, policies, workloads, or cluster behavior; establish the real cluster context and require a reviewed diff before production mutation."
description_zh: "安全设计、审查和诊断 Kubernetes 工作负载、发布、网络、RBAC、资源、状态服务和集群变更。"
description_en: "Safely design, review, and diagnose Kubernetes workloads, rollouts, networking, RBAC, resources, stateful services, and cluster changes."
category: "development"
version: "0.1.0"
author: "Lukas Niessen; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Kubernetes Production Operations

Use this skill for Kubernetes workloads and cluster-facing configuration. Establish the target context, cluster version and distribution, namespace, environment criticality, deployment controller, rendering method, CNI, ingress, storage classes, admission policies, service mesh, autoscaling, and workload ownership before generating commands or manifests.

Treat repository configuration and read-only cluster evidence as separate sources. Identify whether GitOps, Helm, Kustomize, an operator, or another controller owns each object; editing or applying the rendered object directly may be overwritten or create configuration drift.

## Diagnose the failure mode

Start with the user-visible symptom and classify the likely boundary: API/schema mismatch, scheduling or quota, image/configuration, probe or rollout, service discovery, network policy or ingress, identity/RBAC, storage, node/runtime, autoscaling, controller reconciliation, or dependency failure. Build a timestamped path from desired state through admission, scheduling, startup, readiness, routing, and application behavior.

Prefer bounded, read-only evidence: object YAML and events, conditions, rollout history, owner references, logs for the affected container and prior instance, endpoints, resource usage, policy decisions, controller status, and relevant node state. Do not dump all secrets, environment values, tokens, or cluster-wide objects. Redact sensitive data and use the narrowest namespace, selector, and time range.

Do not infer root cause from a final status such as `CrashLoopBackOff`, `Pending`, `ImagePullBackOff`, or HTTP 503. These describe a stage; correlate the earliest failing condition with events and application evidence.

## Author workload contracts

Select the controller that matches lifecycle semantics: Deployment for replaceable replicas, StatefulSet for stable identity/storage ordering, DaemonSet for node-scoped agents, Job for finite work, and CronJob for scheduled work. Make labels and selectors immutable and consistent; include ownership and app/version labels used by policy and observability.

Set CPU and memory requests from measured usage and scheduling needs, then set limits according to workload behavior and platform policy. Avoid arbitrary equal requests/limits, missing requests, or CPU limits that create unexplained throttling. Define quotas and limit ranges at the tenancy boundary when appropriate.

Design startup, readiness, and liveness probes for different questions. Readiness controls traffic; liveness should detect unrecoverable process failure, not dependency slowness; startup protects slow initialization. Choose thresholds from observed startup and latency distributions and ensure probe endpoints do not create expensive work.

Use immutable image digests or a controlled immutable tag policy. Define termination grace, signal handling, `preStop` only when justified, disruption budgets, topology spread/anti-affinity, and rollout surge/unavailability from availability and capacity constraints. A PDB does not prevent every voluntary or involuntary outage and cannot compensate for a single replica.

## Enforce security at boundaries

Use a dedicated ServiceAccount and least-privilege namespace-scoped RBAC unless a cluster scope is proven necessary. Review verbs, resources, subresources, API groups, resource names, and impersonation. Do not grant wildcard permissions or bind broad built-in roles to workloads for convenience.

Use restricted workload defaults where supported: non-root execution, explicit user/group policy, read-only root filesystem when compatible, dropped capabilities, seccomp, no privilege escalation, and no host namespaces, host paths, privileged mode, or unrestricted device access without documented necessity. Confirm image behavior rather than adding a security context that prevents startup.

Secrets encoded in base64 are not encrypted. Prefer external secret delivery or encryption-at-rest and tightly scoped read access. Never place credentials in manifests, Helm values committed to source, command history, logs, annotations, or generated debug bundles.

NetworkPolicy is effective only when the installed CNI enforces it. Define ingress and egress from observed flows, include DNS and control-plane dependencies, test allowed and denied paths, and avoid claiming isolation from YAML alone. Review externally exposed Services, ingresses, gateways, source ranges, TLS termination, and forwarded identity.

## Render and validate before mutation

Render the exact artifact using the repository's tool and pinned versions. Validate YAML, API schemas against the target Kubernetes version, deprecated APIs, policy/admission, labels/selectors/ports, references, namespace, image provenance, resources, RBAC, security contexts, and controller ownership. Client-side validation cannot prove admission, CRD schemas, defaults, or webhook behavior.

For a reachable target, use server-side dry run and a diff with the exact context and namespace. Review creates, updates, deletions, immutable-field replacements, prune behavior, generated names, and controller-driven side effects. Treat rendered output and diffs as potentially sensitive.

Never apply, delete, scale, restart, drain, cordon, evict, patch finalizers, change RBAC, rotate secrets, or alter cluster policy in production without explicit authorization for that action and target. A user asking for a manifest or diagnosis has not authorized deployment.

## Roll out and recover

Define preconditions, owner, observation window, stop conditions, and rollback before a risky rollout. Observe desired/current/ready/available replicas, conditions, events, error rate, latency, saturation, restarts, and dependent services. A rollout reported complete does not prove the user-visible path works; verify a representative request.

Rollback depends on data and compatibility. `rollout undo` changes the pod template but does not reverse database migrations, external side effects, CRD conversion, persistent-volume changes, or deleted objects. For stateful changes, coordinate schema compatibility, backup/recovery evidence, ordered updates, quorum, fencing, and replication health.

When cleanup or deletion is authorized, resolve owner references, finalizers, volumes, load balancers, DNS, and retained data first. Do not use force deletion or remove finalizers until the responsible controller and recovery impact are understood.

## Handoff

Return the exact cluster/context/namespace and versions, ownership path, symptom timeline, evidence and assumptions, proposed artifacts, rendered diff summary, policy/security/resource impact, authorization boundary, validation performed, rollout and recovery plan, user-visible verification, and remaining risks. Clearly distinguish offline validation, server dry run, applied state, controller convergence, and observed service recovery.
