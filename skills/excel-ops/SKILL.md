---
name: "excel-ops"
display_name: "表格操作"
display_name_en: "Spreadsheet Operations"
description: "Excel/CSV 文件操作技能 — 读取、写入、筛选、排序、公式计算"
description_zh: "安全读取、清洗、分析、转换和创建 Excel/CSV 表格，并验证公式、格式与输出。"
description_en: "Safely inspect, clean, analyze, convert, and create Excel or CSV files with verified formulas, formatting, and outputs."
category: "data"
version: "0.1.0"
author: "xuthreekid; adapted for WorkBuddy by SandBase AI"
---

# Spreadsheet Operations

Use this Skill for `.xlsx`, `.xls`, `.csv`, or `.tsv` inspection, cleanup,
analysis, conversion, and creation. Match the user's language in explanations.

## Tool selection

Use the spreadsheet or artifact tool available in the current WorkBuddy
workspace. Prefer a purpose-built spreadsheet capability that preserves cell
types, formulas, styles, merged ranges, and multiple sheets. Use a code runtime
only when no suitable spreadsheet tool exists, and state any fidelity limits.
Never claim to have recalculated formulas unless the selected tool actually did.

## Workflow

1. **Inspect** — identify file type, sheet names, dimensions, headers, formula
   regions, merged cells, and a small representative sample. Do not dump an
   entire large or sensitive workbook into the conversation.
2. **Confirm the transformation** — translate the request into explicit input
   columns, filters, joins, calculations, output columns, and ordering. Resolve
   only ambiguities that would materially change the result.
3. **Transform** — filter, sort, deduplicate, group, join, calculate, pivot, or
   convert while preserving unaffected workbook structure.
4. **Validate** — reopen the output and verify sheet names, row/column counts,
   headers, formulas or computed values, representative records, and requested
   formatting. Check totals or invariants when available.
5. **Deliver** — save to a new, descriptive filename by default and summarize
   the changes, validation performed, and any unsupported feature.

## Safety and fidelity

- Treat spreadsheet formulas and links as untrusted content; do not execute
  macros, external links, embedded scripts, or data connections.
- Preserve identifiers such as account numbers and postal codes as text when
  leading zeros matter. Do not silently coerce dates, currencies, percentages,
  booleans, or locale-specific decimals.
- Never invent missing values. Mark assumptions and distinguish blanks, zero,
  `null`, and unavailable data.
- Avoid overwriting the source unless the user explicitly requests it. Before
  any destructive replacement, ensure a recoverable original remains.
- For large files, inspect schema and samples first, process in bounded chunks
  when supported, and report incomplete validation honestly.

## Common outputs

- Cleaned workbook with retained formatting
- CSV/TSV conversion with declared encoding and delimiter
- Summary sheet with formulas or materialized values clearly identified
- Pivot or grouped analysis with source scope and filters recorded
