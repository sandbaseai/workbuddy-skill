---
name: "network-troubleshooting"
display_name: "网络故障排查"
display_name_en: "Network Troubleshooting"
description: "Use when diagnosing network failures such as connection refusals, timeouts, TLS errors, DNS problems, or intermittent connectivity across local, cloud, container, or cluster environments."
description_zh: "用于排查连接拒绝、超时、TLS 错误、DNS 故障，或本机、云端、容器与集群之间的间歇性网络问题。"
description_en: "Isolate failures layer by layer across DNS, TCP, TLS, HTTP, routing, policy, and resource limits; collect evidence from the failing environment and produce a verified remediation."
category: "development"
version: "0.1.0"
author: "nimadorostkar/Claude-Skills-collection; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to the failing environment, permission to run safe network diagnostics, and an authorized path for configuration or code changes"
---

# Network Troubleshooting

## Purpose

Locate a network failure at the narrowest layer supported by evidence instead of guessing. Preserve the original error, test from the environment where it fails, and stop escalation when a lower layer has not been proven healthy.

## Safety and scope

- Begin with read-only diagnostics and a single reproducible symptom.
- Do not scan unrelated hosts, capture payloads, change firewall rules, restart production services, or alter kernel/network settings without explicit authorization.
- Redact credentials, tokens, private payloads, and internal topology before saving or sharing evidence.
- Use bounded timeouts and low request counts; record the source environment, timestamp, resolver, destination, and command exit status.
- Treat a successful test from a laptop as weak evidence when the failure occurs in a pod, worker, VPC, or customer network.

## Inputs and outputs

Capture the exact error and client, destination and port, failing and succeeding locations, frequency, recent deploy/config changes, and whether the issue is size- or load-dependent.

Produce a short report containing:

1. symptom and impact window;
2. tested path and environment;
3. evidence for each layer;
4. failing layer and confidence, or an explicit unknown;
5. smallest authorized fix;
6. verification from the original failing location; and
7. rollback and follow-up telemetry if a change was made.

## Layer-by-layer workflow

1. **Preserve the symptom.** Distinguish refused, reset, timeout, name resolution, certificate, HTTP status, and client-pool errors. Keep one representative sanitized trace.
2. **Check DNS from the failing host.** Use the configured resolver and query the exact name. Compare address, latency, search-path expansion, split-horizon records, and TTL with a known-good environment.
3. **Check routing and policy.** Verify the route, proxy, service discovery target, security group, NACL, network policy, and service-mesh policy that apply to the source identity. Check both directions for stateless ACLs.
4. **Open TCP/UDP deliberately.** For a TCP service, test the destination port with a bounded socket probe. A refusal generally proves reachability to a host that sent a reset; a timeout only proves that no response arrived and needs correlation with policy or packet evidence.
5. **Complete TLS.** Validate SNI, certificate dates and chain, trust store, protocol/cipher negotiation, and hostname. Never disable verification as a production fix.
6. **Make the smallest HTTP/application request.** Use a health endpoint or harmless request with a deadline. Compare proxy behavior, redirects, status, headers, response size, and server logs.
7. **Investigate intermittent or load-only failures.** Check connection reuse, pool limits, ephemeral ports/TIME_WAIT, conntrack, file descriptors, DNS cache, retries, load-balancer backend health, rate limits, and saturation.
8. **Test payload size and MTU when indicated.** If small requests work but large ones stall after handshake, inspect fragmentation, path MTU, MSS, tunnels, and proxy limits.
9. **Correlate and verify.** Align client timestamps with DNS, load-balancer, firewall, mesh, and server telemetry. Apply only an authorized change, rerun the original failing test, and document residual uncertainty.

## Safe diagnostic examples

```bash
# Run from the failing pod/host; keep output sanitized and bounded.
dig +short api.internal.example.com
getent ahosts api.internal.example.com
nc -vz -w 5 api.internal.example.com 443
openssl s_client -connect api.internal.example.com:443 \
  -servername api.internal.example.com -brief </dev/null
curl --fail-with-body --max-time 5 --connect-timeout 3 \
  -sS -o /dev/null -D - https://api.internal.example.com/healthz
ss -s
```

Interpret evidence carefully: a timeout is not proof of a firewall, a TCP success is not proof that the application is healthy, and a TLS success does not prove that the request body fits an intermediary limit.

## Common patterns

- **Works on laptop, fails in cluster:** compare resolver, route, egress identity, proxy, network policy, and trust store from the failing workload.
- **Fixed-rate intermittent errors:** inspect a bad load-balancer backend, uneven DNS answers, pool exhaustion, or a per-instance limit.
- **Cannot assign requested address under load:** inspect client creation and TIME_WAIT/ephemeral-port pressure before tuning kernel settings; reuse a bounded keep-alive client where appropriate.
- **TLS works, large POST hangs:** test payload thresholds and path MTU before changing application retries.
- **Kubernetes name lookup is slow:** inspect the cluster resolver, search path, and `ndots` behavior; validate any change against the cluster's naming conventions.

## Handoff checklist

- [ ] Original symptom, impact, and frequency are recorded.
- [ ] Tests ran from the failing environment with bounded timeouts.
- [ ] DNS, route/policy, transport, TLS, and application evidence are separated.
- [ ] Sensitive data and unnecessary topology are redacted.
- [ ] Root cause is labeled confirmed, probable, or unknown.
- [ ] Fix is authorized, minimal, reversible, and verified against the original symptom.
- [ ] Monitoring or a follow-up experiment is assigned for unresolved risk.
