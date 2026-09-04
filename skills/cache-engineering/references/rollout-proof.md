# Cache Rollout and Proof

Use this reference when a change introduces mixed versions, a migration, rollout, rollback or performance claim.

Version key and serializer meaning across rolling deployments, or introduce a new namespace with explicit read/write transition and cleanup. Define cold-fill demand, canary scope, ramp thresholds, bypass or no-cache rollback, and retirement of old keys and invalidators. Rollback must tolerate data and in-flight fills produced by the newer version.

Test both key directions through the real retrieval path: equivalent requests reuse one entry, while any tenant, authorization, policy, locale, representation or other response-changing difference cannot retrieve another variant. Key-string inequality alone does not prove isolation.

Exercise update during fill, negative then create, slow or failed fill, cache timeout and outage, eviction, cold fleet, mixed versions and rollback where those paths apply. Verify bounded origin load during both failure and recovery.

Measure the same workload before and after. Report distributions and origin request rate, concurrency and resource load alongside hit, miss, fill, stale, error and eviction rates, value age, skew and recovery time. A performance win is valid only when user and origin targets improve without violating correctness, freshness, isolation, availability or rollback.
