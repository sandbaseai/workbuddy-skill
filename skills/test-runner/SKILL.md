---
name: "test-runner"
display_name: "测试执行器"
display_name_en: "Test Runner"
description: "Use when running repository tests and reporting concise, reproducible results in fast or full mode."
description_zh: "用于以快速或完整模式执行仓库测试，并输出简洁、可复现且可操作的结果。"
description_en: "Select repository-native test entry points, bound the scope safely, run fast or full verification, diagnose failures without masking them, and report commands, exit codes, and actionable evidence."
category: "development"
version: "0.1.0"
author: "jpiedrafita; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Repository checkout, project documentation, test scripts, package manager, and CI configuration"
---

# Test Runner

Run tests with the smallest appropriate scope while preserving trustworthy evidence. Use this skill for local verification, change validation, and release checks; do not claim a test passed when it was skipped, flaky, or not actually run.

## Choose the mode and scope

- **Fast:** the smallest deterministic suite that exercises the changed area and gives rapid feedback.
- **Full:** the repository-defined unit, integration, end-to-end, static, and packaging checks required for a release or broad change.

Determine the root and target from the user request, changed files, and repository conventions. If no target is specified, use the repository root and fast mode unless the change or release gate requires full mode. Do not silently expand into unrelated repositories or production systems.

## Select commands safely

Prefer, in order:

1. `PROJECT.md` or equivalent contributor documentation;
2. repository entry points such as `make`, `task`, `just`, package scripts, or checked-in CI commands;
3. the language/framework test runner only when the repository has no clearer entry point.

Inspect the relevant script before running it. Preserve required environment setup, fixtures, seed data, and working directory. Never install packages, contact external services, mutate production data, or run destructive migrations merely to guess how a test works; stop and report the missing prerequisite when authorization or safety is unclear.

Bound expensive tests with the documented timeout, worker count, project, path, or test name. Keep test data isolated and redact credentials, tokens, personal data, and proprietary output from reports.

## Execute and diagnose

Record the commit, mode, root, command, environment assumptions, start/end time, and exit code. Run the selected command exactly once unless a documented retry or flake policy applies. A timeout, crash, missing dependency, collection error, skipped test, and assertion failure are different outcomes.

When a test fails:

1. Preserve the first useful failure and the relevant traceback or log excerpt.
2. Map it to the changed file, fixture, dependency, environment, or known flake.
3. Reproduce with the narrowest safe test command when useful.
4. Check whether the failure is an actual regression, a pre-existing failure, or an invalid test environment; require evidence for the classification.
5. Suggest the next smallest action and owner. Do not weaken assertions, delete tests, increase retries, or mark a failure flaky just to obtain green output.

For parallel or nondeterministic tests, capture worker count, seed, ordering, retries, and relevant service versions. Treat a pass after retry as conditional and report the original failure.

## Report results

Return:

- mode and target;
- exact commands and exit codes;
- passed, failed, skipped, timed-out, and not-run counts when available;
- concise failure evidence with file/test locations;
- environment or prerequisite limitations;
- whether the result is suitable for the requested gate;
- the next authorized action.

For full verification, summarize every check category and link to durable artifacts or CI logs. For fast verification, state what it does not cover. If no tests exist, report that fact and identify safer static or packaging checks rather than implying success.

