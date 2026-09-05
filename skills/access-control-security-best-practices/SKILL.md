---
name: "access-control-security-best-practices"
display_name: "访问控制安全实践"
display_name_en: "Access Control Security Best Practices"
description: "Design, review, implement, and verify least-privilege access controls across users, services, tenants, resources, and administrative workflows."
description_zh: "围绕用户、服务、租户、资源和管理流程设计、审查、实现并验证最小权限访问控制。"
description_en: "Design, review, implement, and verify least-privilege access controls across users, services, tenants, resources, and administrative workflows."
category: "security"
version: "0.1.0"
author: "Hermes Agent; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Access Control Security Best Practices

Use this skill when designing or reviewing authentication-to-authorization
boundaries, RBAC or ABAC policies, tenant isolation, service identities,
administrative actions, or permission regressions. Authentication proves who or
what is acting; authorization decides whether that principal may perform this
action on this resource in this context. Never treat a login, client-side flag,
hidden UI control, or predictable identifier as authorization evidence.

## Map the authorization contract

Start with the protected assets, operations, principals, trust boundaries,
tenants, environments, and policy owners. For each operation document:

- subject and authenticated identity source;
- resource and authoritative ownership or tenant relation;
- action, context, and required decision point;
- allowed, denied, missing, expired, and degraded behavior;
- policy version, audit event, and decision owner.

Separate human, service, background-job, support, and break-glass identities.
Use server-side authoritative identifiers and derive tenant scope from trusted
session or service context, never from an unverified request field. Make
cross-tenant access an explicit, narrow policy rather than an accidental result
of a shared query or cache.

## Design for least privilege

Default to deny and grant only the actions and fields required for the task.
Prefer resource- and action-level checks over broad roles when risk or tenancy
requires it. If using RBAC, define role inheritance and separation-of-duties
constraints. If using ABAC, define trusted attributes, freshness, provenance,
combination rules, and behavior when an attribute is absent or stale.

Review service-to-service credentials, delegated authority, token audience and
expiry, session invalidation, admin impersonation, and emergency access. Keep
authorization checks close to the protected operation and repeat them after
untrusted transitions such as queue consumption, file retrieval, or background
jobs. Do not rely on the UI to enforce policy, and do not log secrets or full
policy inputs containing personal data.

## Verify implementation and boundaries

1. Trace each sensitive route or job from identity extraction to the final data
   read or side effect.
2. Check object-level, field-level, function-level, and tenant-level decisions.
3. Test same-tenant allow cases and cross-tenant, unauthenticated, wrong-role,
   expired-session, missing-attribute, and tampered-identifier deny cases.
4. Test indirect paths: bulk export, search, downloads, webhooks, caches,
   asynchronous jobs, retries, admin tools, and error responses.
5. Confirm denial is fail-closed, does not leak resource existence, and is
   consistently represented in API, UI, logs, and metrics.
6. Verify policy changes, role grants, revocations, and break-glass use are
   authorized, auditable, bounded in time, and tested for propagation delay.

Use non-production identities and synthetic records. Never probe another
tenant, bypass a control, alter production permissions, or create a privileged
account without explicit authorization. A successful endpoint response is not
proof of correct authorization unless the principal, resource scope, action,
and decision evidence are all shown.

## Operational safeguards

Define policy ownership, review cadence, stale-role cleanup, access-request
approval, revocation SLA, audit retention, and alerting for unusual grants or
denials. Keep policy evaluation deterministic and versioned where practical.
Make caches, replicas, and asynchronous consumers respect revocation and tenant
boundaries; document bounded residual risk when immediate propagation is not
possible. Emergency access must have an expiry, reason, approver, and post-use
review.

## Handoff format

```text
Scope / commit / environment / policy version:
Assets, principals, actions, tenants, and trust boundaries:
Authorization contract and ownership evidence:
Allow and deny matrix:
Implementation paths and data-flow checks:
Tests, fixtures, and observed decisions:
Audit, revocation, cache, and operational controls:
Findings / severity / confidence / owner:
Required remediation, rollout, rollback, and retest:
Open unknowns and approval boundaries:
```

State facts, assumptions, and recommendations separately. A complete review
ends with reproducible deny evidence for the highest-risk boundaries and an
accountable owner for every remaining gap.
