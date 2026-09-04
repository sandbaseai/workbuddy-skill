# Execution guide

## Candidate selection

Compare only fields returned by `sandbase_inspect`: capability fit, required inputs, output shape, price, latency mode, and vendor. Do not infer undocumented quality guarantees.

## Asynchronous runs

When `sandbase_run` returns a `run_id`:

1. Preserve the exact ID.
2. Call `sandbase_run_get` with that ID.
3. If status is queued or running, continue polling at a reasonable interval supported by the host.
4. Stop on `completed` or `failed`. Never present an in-progress response as the final artifact.
5. If the user asked for the result in a file, download or transform it only when the returned data and host permissions allow it.

Avoid starting a duplicate paid run merely because an asynchronous run is slow.

## Reporting

Lead with the delivered result. Mention the selected capability and material cost only when useful. Keep raw provider metadata out of the response unless the user requested it or it helps diagnose a failure.

