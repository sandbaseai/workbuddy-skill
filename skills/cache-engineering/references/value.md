# Cache Value Decision

Use this reference before introducing or retaining a cache whose value is uncertain.

1. Pin the operation, environment, cache state, representative workload and time window.
2. State correctness, isolation, freshness, availability and cost invariants before optimizing latency.
3. Measure end-to-end latency distributions, throughput and errors together with origin request rate, concurrency, latency and constrained resource.
4. Identify repeated work the proposed layer can remove. Separate compute, database, network and serialization costs rather than attributing the whole request to the cacheable segment.
5. Estimate cold-start, invalidation, eviction, outage and operational costs. Include memory, network, replication and on-call complexity.
6. Define a falsifier such as insufficient hit rate, unchanged user latency, excessive stale serves, increased error rate or origin overload during bypass.

Reject caching when the removable work cannot repay its correctness and operational surface. If measurement is missing, specify the minimum instrumentation and experiment instead of presenting modeled savings as observed results. Reopen the decision when workload shape, origin cost, protected invariants or product targets change materially.
