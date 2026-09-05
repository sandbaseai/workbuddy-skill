---
name: "repository-formatting"
display_name: "仓库格式化"
display_name_en: "Repository Formatting"
description: "Use when a repository needs source formatting, import normalization, or formatter verification before review or release."
description_zh: "用于代码仓库需要源代码格式化、导入规范化或在审查/发布前验证格式时。"
description_en: "Run the repository's declared formatter from the correct root with bounded dependency handling, recover once from known transient formatting failures, inspect the resulting diff, and report reproducible formatting evidence without overwriting unrelated work."
category: "development"
version: "0.1.0"
author: "Microsoft TypeSpec; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized repository checkout, package manifests and workspace files, declared formatter, installed dependencies or permission to install them, and a cleanly reviewable worktree"
---

# Repository Formatting

Format code using the repository's own command and configuration. Formatting is a controlled source change, not a license to rewrite unrelated files or hide semantic changes. Preserve existing user edits, inspect the diff afterward, and never claim a clean result when the formatter was skipped or failed.

## Establish the root and command

1. Identify the repository root from version-control metadata and the manifest/workspace files that define the project. Do not run a formatter from an arbitrary subdirectory.
2. Read contributor and CI documentation, package scripts, formatter configuration, lockfiles, and ignore rules. Prefer the exact command used by CI or the project maintainers (`pnpm format`, `npm run format`, `cargo fmt`, `gofmt`, `rustfmt`, or equivalent).
3. Inspect `git status` and the target diff before starting. Do not overwrite unrelated modifications; narrow the formatter scope if the repository supports it, or record the pre-existing state.
4. Confirm the formatter and dependency versions. Use the lockfile and repository package manager. Installing dependencies is a state-changing action: do it only in the authorized checkout, with the declared manager, and do not execute untrusted post-install code merely to inspect formatting.

## Run with bounded recovery

Run the formatter from the root and capture command, version, scope, duration, exit code, and changed paths. If the package manager reports that dependencies or the importer manifest are missing, correct the root or perform the documented dependency setup. If a formatter exits non-zero while clearly reporting changed files, re-run it once as the repository guidance permits; do not retry indefinitely or treat a second failure as success. For other errors, stop and classify the failure rather than applying broad fixes.

Do not cancel a bounded formatter run without recording the interruption. Respect workspace scripts, network policy, resource limits, generated-file conventions, and user changes. Never format secrets, vendored code, build output, or generated artifacts unless repository configuration explicitly includes them.

## Review the result

Inspect `git diff --stat`, `git diff --check`, and representative diff hunks. Confirm that changes are formatting-only and confined to the intended scope. If imports, generated files, snapshots, or line endings change, determine whether that is expected from project configuration and report it. If the formatter changes semantics or conflicts with a user edit, revert only the formatter's exact changes when safely identifiable and stop for a scoped decision; do not use destructive broad resets.

Run the repository's fast lint or format-check command after formatting, then the relevant tests or full verification required by CI when the change is headed for review or release. A formatter passing does not prove compilation or behavior. Report warnings, unavailable tools, ignored files, pre-existing changes, and any remaining nonconformance.

## Handoff

The final handoff includes root and command, tool and dependency versions, scope, files changed, recovery attempts, diff review result, format-check and test results, limitations, and the next safe action. Leave a reproducible worktree and make the formatting change separately reviewable from semantic edits.
