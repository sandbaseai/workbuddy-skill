---
name: "go-testing"
display_name: "Go 测试"
display_name_en: "Go Testing"
description: "Use when writing, running, or debugging Go tests, fixtures, mocks, and coverage while preserving package boundaries and failure evidence."
description_zh: "用于编写、运行或调试 Go 测试、fixture、mock 和覆盖率检查，同时保持包边界与失败证据。"
description_en: "Plan Go tests around observable behavior, choose internal or external package boundaries deliberately, use require for stopping preconditions and assert for independent checks, and report deterministic go test evidence without weakening failures."
category: "development"
version: "0.1.0"
author: "alex-ilgayev/MCPSpy; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
compatibility: "Authorized Go repository, go.mod, repository test conventions, test dependencies, and permission to run go test commands"
---

# Go Testing

Develop and verify Go code with tests that express observable behavior and preserve trustworthy failure signals. Start from the repository's conventions and current diff. Do not expose production APIs merely to make a test convenient, delete a failing test, or claim coverage from a command that was not run.

## Choose the test boundary

1. Inspect `go.mod`, package layout, existing `_test.go` files, build tags, CI commands, fixtures, and the behavior being changed.
2. Use an internal package test when private implementation behavior or package invariants must be exercised; use an external package test when the public API and consumer contract are the subject.
3. Test through existing interfaces and dependency seams. Introduce a test seam only when it improves the production design; never add an externally visible function solely for testing.
4. Select the smallest deterministic scope first, then expand to affected packages and the repository-defined full suite.

## Write useful assertions

Arrange inputs and dependencies explicitly, act once, and assert the externally meaningful result, error, state transition, or side effect. Use `require` for preconditions whose failure makes the remainder meaningless; use `assert` for independent expectations that should all be reported. Check error identity or structured details where the contract requires it, not only the error string. Include table-driven cases for boundaries, invalid input, empty values, concurrency-sensitive paths, and retries when relevant.

Keep tests isolated from wall-clock timing, network availability, global mutable state, and order dependence. Use controlled clocks, deterministic seeds, temporary directories, `t.Cleanup`, and local fakes or mocks. Ensure goroutines terminate and channels, files, servers, and resources are closed. Do not use sleeps to hide races; use synchronization or the race detector.

## Run and diagnose

Run focused checks such as `go test ./path/to/package -run TestName -count=1`, then affected packages and the repository's documented full command. Add `-race` when concurrent behavior or shared state is in scope, and use coverage or benchmarks only when they answer a stated question. Record Go version, command, package scope, exit code, and relevant output.

Classify failures as assertion or implementation defects, fixture or test defects, race/deadlock, compile or dependency failure, environment limitation, or flake. Reproduce a suspected flake repeatedly with a bounded count and preserve the first failure. Do not retry until green without reporting the failure, and do not change assertions to accommodate an unexplained result. Compare failures with the diff and inspect logs, traces, goroutine dumps, and minimal reproductions as appropriate.

## Handoff

Before completion, verify the focused test passes, adjacent behavior remains covered, and the required package or full suite passes. Review coverage gaps rather than chasing a percentage blindly. Report tests added or changed, package boundary choice, commands and versions, pass/fail counts, race or benchmark results, skipped checks, flake evidence, and remaining risks. A durable fix includes a regression test for the original failure and leaves the repository's normal test command reproducible.
