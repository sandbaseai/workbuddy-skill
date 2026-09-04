# Differential Privacy Accounting

Use this reference to review mechanism selection and cumulative privacy loss. Calculations must match the implementation and its documented assumptions.

## Mechanism checklist

| Workload | Common mechanism | Required evidence |
|---|---|---|
| Bounded counts or sums | Laplace or Gaussian | Unit, contribution bound, sensitivity, noise calibration |
| Bounded means | Noisy sum and count or a proven mean mechanism | Value bounds, contribution bounds, denominator behavior |
| Repeated analytics | Budgeted DP query system | Total scope, per-query allocation, composition accountant |
| Gradient training | DP-SGD or equivalent proven optimizer | Per-example clipping, sampling model, noise multiplier, steps |
| Private selection | Exponential or noisy-max family | Utility sensitivity, candidate set, selection proof |

Do not infer sensitivity from typical data. Enforce bounds in code before the mechanism sees the data.

## Accounting record

Capture enough information to reproduce the accountant result:

- neighboring relation and protected unit;
- population and sampling assumptions;
- mechanism and library/version;
- clipping or contribution bounds;
- noise scale or multiplier;
- number and adaptivity of steps/releases;
- accountant family and orders or parameters;
- target delta and resulting cumulative epsilon;
- rounding, approximation, and conversion choices.

Basic composition is conservative but transparent: epsilon and delta add across mechanisms. Tighter composition such as Rényi DP can be appropriate only when the accountant's mechanism and sampling assumptions match execution. Never compare epsilon values with different adjacency definitions or composition scopes as if they were equivalent.

## Operational checks

- Reserve budget atomically before producing a release.
- Count retries and partial failures unless the proof shows they reveal nothing.
- Persist accountant state consistently with model or query-system checkpoints.
- Reconcile the ledger with actual artifacts and published outputs.
- Fail closed at the budget boundary and test concurrent requests.
- Recalculate after changes to batch size, epochs, sampling, clipping, or releases.
