# Differential Privacy Release Statement

Use this template for a model card, dataset note, analytic release, or internal approval record. Replace every bracketed field; do not omit unknowns silently.

## Claim

This release was produced by **[mechanism and implementation/version]** and satisfies **(epsilon = [value], delta = [value])-differential privacy** under **[add/remove or replace-one adjacency]** for **[protected unit]**. The guarantee covers **[outputs and composition scope]** over **[time/query/training scope]**. Cumulative privacy loss was computed with **[accountant and settings]** from **[executed parameters]**.

## Configuration and evidence

- Population and contribution bounds:
- Sensitivity or clipping bound:
- Sampling model:
- Noise parameter:
- Steps/releases included in composition:
- Budget ledger or reproducible calculation:
- Utility evaluation and affected segments:
- Verification owner and date:

## Limitations

The guarantee does not cover **[raw-data access, side channels, excluded artifacts, non-DP releases, unsupported threat models, or other boundaries]**. Material assumptions are **[list]**. Remaining budget and future composition obligations are **[state]**. Reassess when **[data population, adjacency, mechanism, parameters, outputs, threat model, or deadline changes]**.
