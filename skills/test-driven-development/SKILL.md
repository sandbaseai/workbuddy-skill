---
name: "test-driven-development"
display_name: "测试驱动开发"
display_name_en: "Test-Driven Development"
description: "Use before implementing a feature or bug fix to drive a small, observable change through the RED-GREEN-REFACTOR cycle."
description_zh: "用于实现功能或修复缺陷前，以可观察的小步变更执行 RED-GREEN-REFACTOR 测试驱动开发循环。"
description_en: "Translate a behavior into a failing regression test, implement the smallest change that makes it pass, run the relevant and full verification, then refactor without losing evidence or scope control."
category: "development"
version: "0.1.0"
author: "a5c-ai/babysitter; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Repository checkout, existing test framework, repository-native commands, and permission to edit code and tests"
---

# Test-Driven Development

Use a short RED–GREEN–REFACTOR loop when implementing a feature or bug fix. The test is an executable statement of behavior and a durable regression guard, not a ceremony. Keep each loop narrow enough that a failure has one plausible cause.

## RED: specify the behavior first

1. Inspect the request, current implementation, nearby tests, public contracts, and repository conventions.
2. State the observable behavior, inputs, outputs, errors, and important boundary cases. Separate required behavior from implementation preference.
3. Add the smallest deterministic test that would fail before the change. Prefer a focused unit or contract test; use an integration or end-to-end test when the behavior crosses a real boundary.
4. Run that test and confirm it fails for the intended reason. A test that passes immediately is not proof that the new behavior is covered; inspect whether it exercises the changed path.

Record the exact command, exit code, failure, and environment assumptions. Do not weaken an assertion, skip a test, or rewrite the requirement merely to obtain a red result.

## GREEN: implement the smallest behavior

Make the minimum production change that satisfies the failing test and preserves existing contracts. Avoid speculative abstractions, unrelated cleanup, hidden fallbacks, and broad rewrites. Reuse repository-native APIs and patterns, and make invalid or unsafe inputs fail explicitly where the contract requires it.

Run the focused test again and verify GREEN. If it still fails, classify the failure as a product misunderstanding, test defect, implementation defect, or environment issue; gather evidence and correct the cause instead of masking it. Then run adjacent tests that cover callers, serializers, persistence, permissions, or other affected boundaries.

## REFACTOR: improve without changing behavior

Only refactor after the behavior is green. Simplify duplication, names, control flow, and test fixtures while keeping the new test and relevant suite green after each meaningful change. Preserve public behavior, error semantics, observability, and migration safety. If refactoring changes the contract, return to RED with a new test rather than smuggling the change into cleanup.

## Close the loop

Before handoff, run the repository's appropriate fast and full verification. Report the focused test, adjacent checks, full-suite result, skipped or flaky checks, changed files, and remaining limitations. Confirm that the test fails on the pre-change revision when practical, passes on the final revision, and would detect the original regression. Commit or hand off only after the evidence is reproducible; never claim a test passed when it was not run.
