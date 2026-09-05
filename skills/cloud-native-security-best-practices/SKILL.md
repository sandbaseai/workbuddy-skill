---
name: "cloud-native-security-best-practices"
display_name: "云原生安全实践"
display_name_en: "Cloud-Native Security Best Practices"
description: "Design and review cloud-native security across workloads, images, identities, networks, secrets, supply chains, runtime controls, and recovery."
description_zh: "从工作负载、镜像、身份、网络、密钥、供应链、运行时控制和恢复等方面设计并审查云原生安全。"
description_en: "Design and review cloud-native security across workloads, images, identities, networks, secrets, supply chains, runtime controls, and recovery."
category: "security"
version: "0.1.0"
author: "Hermes Agent; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Cloud-Native Security Best Practices

Use this skill when reviewing or designing security for containerized,
orchestrated, serverless, or otherwise distributed cloud workloads. Start from
assets, trust boundaries, and likely failure or abuse paths rather than from a
vendor checklist. The skill provides a review method; it does not claim access
to a cluster, cloud account, image registry, or policy engine unless an
authorized read-only integration actually supplied evidence.

## Define the security contract

Record the application, environment, cluster or account boundary, workload
owners, data sensitivity, compliance obligations, deployment model, and review
commit. Map:

- identities for users, workloads, nodes, controllers, CI, and operators;
- image, dependency, build, registry, admission, and deployment supply chain;
- network ingress, egress, service-to-service, control-plane, and data-plane
  boundaries;
- secrets, keys, certificates, config, persistent data, and backup paths;
- runtime capabilities, host access, namespaces, tenancy, and blast radius;
- detection, response, recovery, and evidence-retention ownership.

Separate observed platform facts from assumptions. A cloud provider default,
manifest example, or dashboard green state is not proof that the deployed
workload has the intended control.

## Apply layered controls

Review controls in this order, keeping each control tied to an abuse path and
an owner:

1. **Identity and authorization:** use short-lived, audience-bound identities,
   least privilege, explicit workload separation, default deny, and auditable
   administrative or break-glass access.
2. **Build and supply chain:** pin and verify dependencies and base images,
   produce provenance and signed artifacts where supported, isolate builders,
   scan before release, and define how critical findings block or are accepted.
3. **Workload and image:** use minimal trusted images, non-root execution,
   read-only filesystems where feasible, dropped capabilities, seccomp or
   equivalent profiles, resource bounds, and explicit privilege exceptions.
4. **Network and tenancy:** restrict ingress and egress, authenticate service
   calls, segment namespaces or tenants, protect metadata and control-plane
   paths, and verify that shared caches and queues preserve isolation.
5. **Secrets and data:** use an authorized secret manager, avoid secrets in
   images, logs, manifests, URLs, and crash artifacts, rotate and revoke with
   bounded propagation, and encrypt data according to its classification.
6. **Runtime and recovery:** detect anomalous behavior, preserve tamper-aware
   evidence, limit blast radius, test rollback and restore, and define safe
   containment without destroying forensic data.

Do not recommend a control without stating its compatibility, performance,
availability, cost, and failure-mode trade-offs. Do not disable admission,
authentication, network policy, encryption, or monitoring as a troubleshooting
shortcut.

## Verify safely

Use non-production identities and synthetic workloads where possible. Prefer
read-only inspection of rendered manifests, effective policy, image digest,
identity bindings, network rules, secret references, audit events, and runtime
configuration. When controlled testing is authorized, verify:

- a compromised or misconfigured workload cannot cross its intended identity,
  filesystem, network, namespace, or tenant boundary;
- denied operations fail closed without leaking sensitive existence or policy
  details;
- image and dependency changes are traceable from source to deployed digest;
- revocation, rotation, policy updates, rollout, rollback, and restore behave
  within their declared time and safety bounds;
- alerts contain enough sanitized context for response and do not expose
  credentials, personal data, or exploit-enabling details.

Never probe an unrelated account or tenant, exfiltrate data to prove a control,
create privileged access, delete evidence, or mutate production infrastructure
without explicit authorization and a rollback plan. If evidence is unavailable,
label the control unverified instead of inferring it from intent.

## Findings and handoff

Classify each finding by demonstrated impact, exploitability, affected scope,
control strength, evidence confidence, and remediation urgency. Keep severity,
priority, confidence, and effort separate. Include the smallest safe corrective
action, owner, dependency, rollout guard, rollback or containment condition,
and retest evidence.

```text
Scope / commit / environment / authority boundary:
Assets, identities, data, and trust boundaries:
Supply-chain, workload, network, secret, and runtime controls:
Observed evidence / freshness / unverified assumptions:
Abuse path and user or system impact:
Finding severity / confidence / owner:
Remediation / rollout / rollback / recovery:
Retest and monitoring evidence:
Residual risk, approvals, and next review:
```

Return facts, hypotheses, and recommendations separately. A review is complete
only when high-risk boundaries have reproducible evidence and every remaining
gap has an accountable owner and a safe next step.
