---
name: "agent-discoverability"
display_name: "Agent 可发现性"
display_name_en: "Agent Discoverability"
description: "Use when publishing or auditing an MCP or agent endpoint so third-party agents can find it, understand its capabilities, and complete its authorized authentication flow."
description_zh: "用于发布或审计 MCP/Agent 端点，让第三方 Agent 能发现服务、理解能力并完成授权认证流程。"
description_en: "Make an operated agent endpoint discoverable and connectable through consistent registry metadata, OAuth discovery, capability manifests, and optional DNS-backed trust."
category: "integration"
version: "0.1.0"
author: "ever-just/agentskills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "An operator-owned HTTPS agent or MCP endpoint with authorized access to its registry, deployment, and DNS configuration"
---

# Agent Discoverability

Use this Skill when a team owns an Agent/MCP endpoint and wants other agents
and users to find and connect to it. This covers the publish/serve side, not
driving a third party's MCP as a client and not ordinary search-engine SEO.

## Establish ownership and scope

Confirm the exact endpoint, domain, transport, public tools, audience,
authentication model, and operator authorization before changing anything.
Inventory the canonical registry entry, community listings, deployment routes,
well-known documents, DNS zone, certificate owner, and current versions. Never
invent a domain-ownership proof, capability, OAuth URL, DNS record, or token.
Use placeholders in examples and keep real credentials in the authorized
secret store or environment.

## Keep the four discovery surfaces consistent

An agent typically needs four surfaces. They may be delivered incrementally,
but all values must describe the same endpoint:

1. **Registry listing:** canonical name, repository, version, transport, HTTPS
   remote, and capability/manifest URL. Mirror only after the canonical record
   is verified; record each listing's owner and update path.
2. **OAuth discovery:** an unauthenticated protected request returns `401` and
   a `WWW-Authenticate: Bearer` header with a `resource_metadata` URL; the
   protected-resource metadata names the resource and authorization server; the
   authorization-server metadata exposes the actual authorize/token endpoints.
3. **Capability manifest:** serve a small HTTPS JSON document such as
   `/.well-known/agent/mcp.json` with protocol, transport, endpoint, auth
   metadata, version, and public tool names/descriptions. Do not expose secrets
   or internal-only tools.
4. **DNS-backed discovery (optional):** where the operator explicitly supports
   it, publish the provider's documented service-binding/capability records,
   index records, DNSSEC, and TLSA/DANE data. Verify the provider's exact syntax
   and delegation; do not hand-wave a green result from an unsigned zone.

The registry remote, manifest endpoint, OAuth `resource`, transport, and DNS
capability pointer must agree. Treat a mismatch as a release blocker.

## Publish safely

Prepare the canonical server metadata from the endpoint's source of truth.
Prove a reverse-DNS or domain namespace only with the value returned by the
official publisher and a DNS record the operator can actually control. Submit
community directory mirrors only with the same URL, version, transport, and
manifest. Scope credentials to the minimum registry/DNS operations and record
the resulting listing IDs and timestamps.

For DNS-backed trust, establish DNSSEC delegation before relying on DNS data.
If a TLSA/DANE digest pins a certificate, connect certificate renewal and DNS
record update or add a tested post-renewal monitor. A stale digest can reject a
healthy endpoint. Never make an unverified endpoint public merely to improve a
directory score.

## Verify the connection path

Run read-only checks before and after publication:

- fetch the registry record and compare endpoint, transport, version, and
  manifest URL;
- request the protected endpoint without credentials and inspect status plus
  `WWW-Authenticate` (do not print authorization headers or tokens);
- fetch and parse both OAuth metadata documents and verify issuer/resource
  relationships and HTTPS origins;
- fetch the capability manifest, validate its schema, and compare its tool list
  with the intentionally public server surface;
- when DNS discovery is enabled, verify DNSSEC/authenticated data, service
  target, capability digest, and TLSA/certificate match from an authorized
  network vantage point;
- perform a real authorized client handshake in a disposable or least-privilege
  account and confirm tool listing, expected denial, logout/revocation, and
  audit events.

Classify each result as observed, configured, tested, or unverified. A curl or
registry hit alone does not prove that a client can finish authentication.
Capture response status, document hashes, versions, timestamps, and redacted
diagnostics; never store bearer tokens, cookies, private keys, or personal data.

## Failure analysis and handoff

If connection fails, trace the chain in order: DNS/HTTPS reachability, registry
remote, `401` challenge, protected-resource metadata, authorization-server
metadata, client registration/redirect policy, token scope/audience, transport,
then tool authorization. Do not “fix” an auth failure by opening the endpoint,
disabling TLS verification, broadening scopes, or granting repository-wide
permissions.

Return the ownership/authorization boundary, four-surface inventory, exact
changes, immutable versions and hashes, verification evidence, redacted
failures, residual risks, rollback path, and the next certificate/registry/DNS
review trigger. Stop when endpoint ownership, domain proof, auth authority, or
public capability scope is ambiguous.
