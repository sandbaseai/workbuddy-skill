---
name: "decision-receipts"
display_name: "Agent 决策凭证"
display_name_en: "Agent Decision Receipts"
description: "Use before or during consequential Agent actions such as deploy, delete, pay, export, access grants, or high-risk decisions when later offline verification of what happened and under which policy matters."
description_zh: "用于部署、删除、付款、导出、授权或高风险决策等重大 Agent 行动，在需要离线证明行动内容及其政策依据时使用。"
description_en: "Decide when a receipt is warranted, build a minimal action manifest, sign it with an authorized receipt primitive, and verify its hash and signature offline without trusting a database or issuer."
category: "security"
version: "0.1.0"
author: "alirezarezvani/claude-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized signing primitive, protected key storage, canonical JSON, and a policy/audit workflow; receipt cryptography is an operator-provided dependency"
---

# Agent Decision Receipts

## What a receipt proves

A log describes an event after the fact and may be edited. A decision receipt is created before or at the point of a consequential action, records the actor, operation, target, governing policy, and input digest, and is signed so tampering breaks verification. It is local evidence that can be checked offline; it is not a hosted notary, a replacement for logs, or a legal opinion.

## Decision 1: receipt or ordinary log?

Mint a receipt only when all three conditions hold:

| Condition | Meaning |
|---|---|
| side-effecting | writes, sends, deploys, deletes, pays, exports, grants access, or changes external state |
| consequential | a wrong call could cost money, violate policy, break a service, or harm a person |
| later-provable | an auditor, reviewer, insurer, regulator, or counterparty may ask what happened and why |

High-signal defaults include deploy, delete, pay/refund, access changes, data egress, claim approval/denial, and high-risk model decisions. Read-only, reversible, trivial actions normally need ordinary trace logs; receipt everything and the signal becomes noise. Record the decision and policy used, including why a receipt was not warranted.

## Decision 2: build the action manifest

Create a canonical, ASCII-safe or UTF-8 normalized manifest immediately before the side effect. It must contain:

- `agent_id`: stable identity of the acting Agent;
- `operation`: precise verb, such as `deploy`, `delete`, `grant_access`, or `decide`;
- `target`: bounded resource identifier, never a secret;
- `policy`: rule, change ticket, approval, or control governing the action;
- `inputs_hash`: digest of full inputs rather than cleartext payloads;
- `decision_label`: explicit action classification;
- timestamp, repository/service revision, and correlation ID when the policy requires them.

Hash inputs before signing when they contain credentials, personal data, proprietary content, or large payloads. Do not put raw secrets, private keys, tokens, or unnecessary PII in the manifest or receipt. The target and policy must be specific enough for an independent reviewer to understand scope.

Example shape:

```json
{
  "schema": "workbuddy.decision-receipt/v1",
  "agent_id": "deploy-agent-prod",
  "operation": "deploy",
  "target": "prod/api@<revision>",
  "policy": "change-control:<ticket>",
  "inputs_hash": "sha256:<64 hex chars>",
  "decision_label": "ACTION_GOVERNED",
  "occurred_at": "<UTC timestamp>",
  "correlation_id": "<request id>"
}
```

## Decision 3: sign and verify

Delegate cryptography to an approved, maintained receipt primitive supplied by the operator. The primitive must sign the canonical manifest, return the evidence hash, identify the algorithm/key ID, and fail explicitly when unsigned. Prefer a well-managed modern signature scheme and optional post-quantum legs when the evidence retention period and policy justify them; never claim post-quantum or legal validity unless the installed primitive actually provides it.

Before executing the external action, bind the receipt to the exact manifest and policy. Store signing keys in a protected secret manager or hardware-backed boundary, never beside receipts or in Git. Keep the receipt immutable and retain the manifest or a recoverable digest according to policy.

Verification must work from the certificate and trusted public-key material alone:

1. parse canonical receipt data;
2. recompute the manifest/evidence hash and compare it byte-for-byte;
3. verify every declared signature leg and key identity;
4. confirm operation, target, policy, revision, and time are in scope;
5. return `verified`, `tampered`, `unsigned`, `unsupported`, or `unavailable` with reason.

No database callback, network call, issuer assertion, or log line may be required to establish cryptographic integrity. A missing crypto backend must produce `unsigned`/`unavailable`, never a fabricated signature or a success claim.

## Safety and anti-patterns

- Do not mint a receipt over a post-action log and call it proof of the action.
- Do not execute a consequential action when the required receipt cannot be minted, unless policy explicitly allows a labeled `receipt-unavailable` exception and records who authorized it.
- Do not reuse a receipt across targets, revisions, policies, or requests.
- Do not store private keys with artifacts, commit them, print them, or include raw secrets in errors.
- Do not confuse an intact signature with a correct business decision; policy and authorization still require review.
- Do not claim “admissible,” “compliant,” or “proven safe” from a cryptographic check alone.

## WorkBuddy handoff

Report whether a receipt was warranted, the sanitized manifest identifiers, policy/approval reference, receipt ID and evidence hash, algorithms/key ID, verification result and exact offline check, storage/retention boundary, exceptions, and rollback or incident path. Redact sensitive inputs. If the action was unsigned or verification unavailable, label the handoff plainly and do not present it as signed evidence.
