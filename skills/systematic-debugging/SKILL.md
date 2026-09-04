---
name: "systematic-debugging"
display_name: "系统化调试"
display_name_en: "Systematic Debugging"
description: "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes"
description_zh: "在修复前复现、定位并追踪根因，然后用最小改动验证结果。"
description_en: "Reproduce, localize, and trace root causes before making the smallest verified fix."
category: "development"
version: "0.1.0"
author: "GuicedEE; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
---

# Systematic Debugging

Always investigate root cause before proposing fixes.

## WorkBuddy operating contract

- Start by restating the observed failure and the evidence needed to reproduce it.
- Inspect before editing. Read relevant logs, tests, configuration, and recent changes with the tools available in the current workspace.
- Separate confirmed facts, hypotheses, and unknowns. Do not present a plausible cause as proven.
- Ask for input only when missing information changes the safe course of action; otherwise continue with bounded diagnostics.
- Do not expose credentials or private data from logs and environment output.
- Make changes only when the user requested a fix. For diagnosis-only requests, stop after an evidence-backed cause and recommended next step.
- After a fix, rerun the smallest failing check and then the relevant broader checks. Report anything that remains unverified.

## Core Rule
No fixes without root-cause investigation.

## Workflow

1) **Reproduce**: capture exact steps and error output.
2) **Localize**: find the smallest failing scope (file, test, input).
3) **Trace**: follow data and control flow to the first wrong state.
4) **Fix**: smallest change that addresses the root cause.
5) **Verify**: re-run the failing test/flow and any related checks.

## When stuck

- Add diagnostic logging at component boundaries.
- Create a minimal reproduction case.
- Use bisect to isolate the introduction point.

## References

- Root-cause tracing: `references/root-cause-tracing.md`
- Defense-in-depth fixes: `references/defense-in-depth.md`
- Condition-based waiting: `references/condition-based-waiting.md`
- Extended examples: `references/examples.md`
