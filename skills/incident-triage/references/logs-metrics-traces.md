# Logs Metrics Traces

## Logs

- Prefer structured fields, correlation/request IDs, tenant/account IDs when safe, route/job names, error class, and dependency name.
- Separate first error from repeated downstream noise.
- Check log sampling, retention, clock skew, redaction, and deployment version labels before drawing conclusions.
- Never paste secrets, tokens, personal data, or full noisy logs into durable docs.

## Metrics

- Compare rate, ratio, and saturation signals: error rate, request rate, latency percentiles, queue depth, retries, CPU, memory, disk, connection pools, and external dependency latency.
- Align metric windows with deploy/change windows and user reports.
- Watch for denominator traps: a low count can make a high percentage misleading, and aggregate health can hide one impacted segment.
- Confirm whether alerts fire on symptoms, causes, or synthetic checks.

## Traces

- Use traces to identify slow spans, failing dependencies, retries, fan-out, cold starts, and missing context propagation.
- Compare successful and failed traces for the same route/job.
- Treat missing spans as evidence about instrumentation gaps, not proof that a dependency was not involved.

## Verification

- Recovery should be judged by the signal that represented impact, not only by a green deploy.
- After mitigation, check logs, metrics, traces, queues, jobs, and synthetic or user-path smoke checks.
- Record residual uncertainty and follow-up instrumentation gaps.
