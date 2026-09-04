---
name: "differential-privacy"
display_name: "差分隐私应用"
display_name_en: "Applying Differential Privacy"
description: "Use when an analytic release or machine-learning pipeline needs a formal differential-privacy guarantee against inference about individual records; define adjacency, budget, mechanism, composition, utility, and the exact release claim."
description_zh: "为统计查询和机器学习训练定义威胁模型、邻接关系、隐私预算、机制与组合核算，并验证效用和隐私声明。"
description_en: "Apply differential privacy to analytics and machine learning by defining the threat model, adjacency, privacy budget, mechanism, composition accounting, utility, and release statement."
category: "data"
version: "0.1.0"
author: "Rock Lambros; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Applying Differential Privacy

Differential privacy (DP) is a guarantee about a randomized mechanism under a stated neighboring-dataset relation. Never describe a dataset, model, or dashboard as “differentially private” without naming the protected unit, mechanism, total privacy parameters, and composition scope.

Use this skill for statistical releases, repeated query systems, or training pipelines where membership, attribute, or reconstruction inference about protected records is in scope. Do not use DP as a substitute for access control, encryption, deletion, purpose limitation, or secure computation.

## Define the guarantee before implementation

Record:

- adversary, observable outputs, auxiliary knowledge, and inference objective;
- protected unit and adjacency relation, such as add/remove one person or replace one event;
- population size, contribution bounds, clipping/bounding rules, and sensitivity;
- all releases that compose against the same population and unit;
- target total epsilon and delta, their decision owner, and the risk/utility basis for choosing them;
- excluded leakage paths, including raw-data access, logs, debugging artifacts, hyperparameter selection, checkpoints, and non-DP releases.

There is no universal safe epsilon. Do not present a value copied from another deployment as regulatory approval. Delta should be justified relative to the protected population and failure interpretation; never choose it only because a library default exists.

## Choose and implement the mechanism

- Use a mechanism whose privacy proof matches the query sensitivity, adjacency definition, sampling method, and implementation.
- Bound every person's contribution before adding noise. Unbounded sensitivity invalidates the claimed calibration.
- For training, clip per-example contributions and use a maintained DP training/accounting library when available. Confirm whether the accountant assumes Poisson, without-replacement, or another sampling model.
- For repeated or adaptive queries, allocate and enforce a total budget rather than labeling each result independently.
- Use cryptographically appropriate randomness where the implementation requires it, and prevent raw intermediates from escaping the DP boundary.

Read [references/privacy-accounting.md](references/privacy-accounting.md) when selecting a mechanism, composing releases, or validating an accountant.

## Verify privacy and utility

Pin library versions and record the exact accountant settings. Recompute cumulative privacy loss from the executed parameters, not only the planned configuration. Add tests for clipping/contribution bounds, deterministic budget refusal, checkpoint resumption, and no output after budget exhaustion.

Evaluate utility on representative tasks and segments with confidence intervals or repeated runs where randomness matters. Check small groups and tails separately; aggregate accuracy can hide unusable or unfair results. Empirical privacy attacks can reveal implementation leakage, but passing an attack does not prove DP and failing one requires investigation.

Stop rather than issue a misleading guarantee when adjacency, sensitivity, composition scope, sampling assumptions, or executed parameters cannot be established.

## Release and operate

Maintain a budget ledger with release/query identifier, population, protected unit, mechanism, parameters, accountant, consumed and remaining budget, owner, and timestamp. Make exhaustion fail closed. Treat retries, dashboards, model checkpoints, exploratory runs, and correlated publications according to the composition model rather than assuming they are free.

Use [references/release-statement.md](references/release-statement.md) for the final claim and limitations. Have the appropriate privacy, security, legal, or risk owner accept the parameters when organizational policy requires it.

Do not run training, release statistics or models, inspect sensitive records, or change a production privacy budget unless the current request authorizes those actions. A completed analysis reports the guarantee, assumptions, executed configuration, cumulative accounting, utility evidence, residual leakage paths, owners, and review trigger.
