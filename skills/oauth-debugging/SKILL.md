---
name: "oauth-debugging"
display_name: "OAuth 与 OIDC 故障诊断"
display_name_en: "OAuth and OIDC Troubleshooting"
description: "Use when an OAuth 2.0 or OpenID Connect flow fails, loops, loses session state, rejects a token, or grants the wrong access; reconstruct the exact protocol exchange without exposing credentials or live tokens."
description_zh: "安全诊断 OAuth 2.0 与 OpenID Connect 的重定向、状态校验、PKCE、令牌、会话、授权和提供方集成问题。"
description_en: "Safely diagnose OAuth 2.0 and OpenID Connect redirect, state, PKCE, token, session, authorization, and provider-integration failures."
category: "security"
version: "0.1.0"
author: "ssrjkk; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# OAuth and OIDC Troubleshooting

Use this skill to diagnose a concrete OAuth 2.0 or OpenID Connect failure. First identify the protocol, grant/flow, client type, provider, library and versions, deployment environment, redirect path, and expected user outcome. Do not treat OAuth authorization, OIDC authentication, application sessions, and resource authorization as interchangeable layers.

## Protect evidence

Never request or reproduce client secrets, authorization codes, refresh tokens, access tokens, session cookies, private keys, PKCE verifiers, or complete ID tokens. Redact values while preserving field presence, length where useful, timestamps, issuer, audience, algorithm, key ID, scope names, HTTP status, and correlation IDs. Prefer provider audit events, sanitized server logs, browser network metadata, configuration, and a controlled test account.

Do not paste live bearer material into decoders or third-party tools. Decode only synthetic, expired, or locally redacted token structures. Do not disable signature, issuer, audience, nonce, state, or TLS checks as a fix.

## Reconstruct the failing exchange

Write the expected and observed sequence with a timestamp and actor for each hop:

1. application creates an authorization request;
2. browser reaches the authorization endpoint;
3. provider authenticates and obtains required consent;
4. provider redirects to the exact registered URI;
5. application validates `state` and, for OIDC, `nonce` as applicable;
6. confidential server or public client exchanges the code using the correct client authentication and PKCE values;
7. client validates returned tokens and establishes its own session;
8. resource server validates the access token and authorizes the requested action.

Locate the earliest divergence rather than debugging the final symptom. Record sanitized request parameters, response/error fields, cookie attributes, host/proxy headers, and which component generated each value. Account for multiple tabs, retries, clock skew, load balancing, and different public versus internal origins.

## Check boundaries by failure stage

For authorization-request or redirect failures, compare the redirect URI byte-for-byte after the same canonicalization rules as the provider. Check scheme, host, port, path, case, trailing slash, URL encoding, response type/mode, scope, tenant or policy, and registered application/environment. Avoid wildcard redirect URIs.

For `state`, `nonce`, or loop failures, verify generation uses sufficient entropy, each value is bound to the initiating browser transaction, single-use expiry is enforced, and validation state survives the redirect. Inspect `Secure`, `HttpOnly`, `SameSite`, domain, path, proxy trust, HTTPS termination, session affinity, and shared session storage. Do not “fix” a mismatch by skipping validation.

For code exchange and PKCE failures, verify the code is unused and unexpired, the redirect URI matches the authorization request, the same client is used, and the verifier belongs to that transaction. Public clients should use PKCE and must not depend on a distributable secret. Distinguish `invalid_client`, `invalid_grant`, and provider-specific errors using the provider's versioned documentation.

For token validation, inspect metadata from the configured issuer and use the provider's supported algorithms and current keys. Validate signature, issuer, intended audience, time claims with bounded skew, token type/use, nonce where required, and authorized party when applicable. A JWT that merely decodes is not valid. Do not assume every access token is a JWT or that an ID token authorizes an API.

For scope and authorization failures, compare requested, consented, issued, and resource-required scopes or permissions. Then inspect application roles, tenant/resource policies, object ownership, and token-to-session mapping. Authentication success does not prove the caller may perform the action.

For refresh or logout failures, identify rotation, reuse detection, revocation, session expiry, concurrency, and provider logout semantics. Preserve a recoverable sign-in path; never log refresh tokens to diagnose rotation.

## Test the hypothesis

State one falsifiable cause at a time and the least invasive check that distinguishes it. Reproduce in a controlled environment when possible, changing one variable per run. Use a fresh browser profile or cleared test session only when stale client state is part of the hypothesis; do not destroy user sessions or revoke production credentials without explicit authorization.

After a fix, verify the successful path plus denied consent, expired state/code, mismatched PKCE, invalid issuer/audience, missing scope, multi-tab flow, refresh rotation, logout, and a deployment behind the real proxy/domain shape. Confirm logs remain redacted and that the change did not weaken a protocol guarantee.

## Handoff

Return the exact failing stage, sanitized evidence, provider/library/version, expected versus observed behavior, ruled-out causes, confirmed root cause or remaining hypotheses, minimal change, security impact, tests performed, rollback, and residual risks. If evidence is insufficient, say what observable data is missing rather than guessing from a generic provider error.
