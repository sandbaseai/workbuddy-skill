# Incident Evidence

## Intake

- Symptom: what is broken, who is affected, and how the user or dependent service sees it.
- Time: first detection, likely start, last known good state, deploy/config/migration/change window.
- Scope: service, route, tenant, region, queue, job, dependency, browser, device, or data segment.
- Severity: active user impact, data risk, security risk, revenue/operational impact, and workaround availability.

## Containment First

- If impact is active, consider rollback, feature flag disablement, traffic shift, rate limit, queue pause, cache bypass, or maintenance mode before root-cause depth.
- Keep changes reversible and small during mitigation.
- Avoid speculative fixes that broaden blast radius.
- Record what was changed, when, and how recovery will be judged.

## Investigation

- Build a timeline from alerts, deploys, config changes, migrations, dependency incidents, queue depth, and error-rate shifts.
- Compare affected and unaffected segments to narrow the boundary.
- Check whether retries, backpressure, cache behavior, rate limits, or downstream timeouts are amplifying the symptom.
- Preserve evidence before log retention, pod restart, queue drain, or cleanup removes it.

## Handoff

- Current status, impact, owner, next action, and rollback/mitigation state.
- Evidence links or portable paths only; do not paste secrets or personal machine paths.
- Follow-up items: tests, monitors, runbook updates, alerts, dashboards, data repair, and customer-facing notes when applicable.
