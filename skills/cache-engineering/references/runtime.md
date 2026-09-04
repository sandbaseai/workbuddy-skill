# Cache Runtime

Use this reference for layer selection, concurrent fills, hot keys, outages and recovery.

Request-local and process caches inherit memory limits and deploy cold starts. Distributed caches add network latency, ambiguous failures, partitions, replication and eviction. HTTP and CDN caches require correct audience, `Cache-Control`, validators, `Vary`, key, purge and propagation semantics. Add a layer only when it removes a separately measured cost.

On a miss, bound concurrent origin work, queue length, waiter count and fill deadline. Collapse only requests with interchangeable keys. A single caller cancellation should not normally cancel a shared fill. Before publishing, verify that the result still matches the current authority generation.

Place cache time inside the end-to-end deadline and reserve budget for origin fallback. For timeout, partition, eviction, synchronized expiry or cold fleet, constrain fallback concurrency to origin headroom. Fail open only when stale data is explicitly safe; otherwise bypass, use a permitted stale window or fail closed. Add jitter only within the freshness contract.

Monitor hit classes rather than a single hit ratio: fresh, stale, negative, miss, fill, bypass and error. Track key cardinality, memory, eviction, network and command latency, pool saturation, hot-key skew, fill concurrency and origin fallback. Ramp recovery so returning cache capacity does not create another origin or fill surge.
