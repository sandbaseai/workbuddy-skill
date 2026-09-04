---
name: "data-analysis"
display_name: "证据化数据分析"
display_name_en: "Evidence-based Data Analysis"
description: "Use when analyzing tabular or structured data for trends, distributions, comparisons, relationships, anomalies, or decisions; establish data quality and statistical limits before drawing conclusions."
description_zh: "对表格数据进行可复现的质量检查、探索分析、统计比较和结论验证，明确假设、不确定性与行动建议。"
description_en: "Analyze tabular data through reproducible quality checks, exploration, statistical comparisons, and validated conclusions with explicit assumptions and uncertainty."
category: "data"
version: "0.1.0"
author: "Gaurav Datar; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Evidence-based Data Analysis

Use this skill for structured datasets, including CSV, JSON, spreadsheets, query results, and data frames. Preserve the user's requested output format. Analysis should be reproducible and decision-relevant, not a collection of charts or unsupported “insights.”

## Frame the question

State the decision or question, target population, unit of analysis, measures, comparison groups, time window, expected grain, and what would change based on the result. Separate exploratory questions from pre-specified tests. Record the source, extraction time, filters, joins, and transformations needed to reproduce the input.

Do not access additional systems, query production data, or expose sensitive records unless authorized. Prefer aggregates and redacted samples; avoid placing secrets or personal identifiers in code, logs, charts, or deliverables.

## Profile before interpreting

Inspect:

- rows, columns, types, units, grain, keys, duplicates, and referential integrity;
- missingness by field and segment, distinguishing unknown, absent, zero, and not applicable;
- ranges, distributions, cardinality, impossible values, encoding and parsing failures;
- outliers, censoring, truncation, survivorship, sampling and instrumentation changes;
- time zones, partial periods, late-arriving data, seasonality, and denominator changes;
- coverage of the intended population and any excluded records.

Never silently coerce, drop, impute, winsorize, deduplicate, or replace data. Explain the rule, quantify affected records, preserve the original where practical, and show whether the conclusion changes under reasonable alternatives.

## Analyze with appropriate evidence

Start with counts, denominators, distributions, and uncertainty. Compare like with like and normalize only when the denominator is meaningful. For grouped results, report sample size and surface segments hidden by the aggregate.

Use statistical tests or models only when their assumptions and the question justify them. Report effect size and interval estimates alongside p-values when applicable. Correct or disclose multiple comparisons. Keep training/evaluation leakage, repeated observations, confounding, and selection effects visible.

Use “associated with” for observational relationships. Claim causation only when the identification strategy, treatment assignment, timing, interference assumptions, and robustness evidence support it. Forecasts and model outputs must include evaluation window, baseline, error measure, and known regime limits.

## Challenge the result

- Recompute important metrics independently or through an alternate aggregation.
- Trace surprising values back to source rows or groups without exposing sensitive data.
- Check sensitivity to filters, time windows, missing-data treatment, outliers, and definitions.
- Look for Simpson's paradox, denominator errors, leakage, duplicated joins, and partial periods.
- Distinguish evidence that contradicts the conclusion from data that is merely noisy.

If the data cannot answer the question, say what is missing and propose the smallest useful collection or experiment. Do not manufacture precision or recommendations from inadequate coverage.

## Deliver

Lead with the supported answer and decision implication. Include:

- question, scope, data version, and reproducible method;
- key numbers with denominators, units, time windows, and uncertainty;
- tables or charts only where they materially clarify the evidence;
- assumptions, robustness checks, conflicting signals, and limitations;
- data-quality notes that could change the conclusion;
- concrete next actions tied to evidence and an owner or validation signal when known.

Make generated files easy to inspect and preserve source-to-output traceability. Do not overwrite source data or publish results unless the current request authorizes those actions.
