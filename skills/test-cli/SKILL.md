---
name: "test-cli"
display_name: "命令行测试"
display_name_en: "CLI Testing"
description: "Test CLIs across arguments, streams, exit codes, files, environment, signals, and interaction."
description_zh: "在隔离环境中验证命令行工具的参数、流、退出码、配置、文件副作用、信号和交互行为。"
description_en: "Test command-line tools in isolation across arguments, streams, exit codes, configuration, filesystem effects, signals, and interaction."
category: "development"
version: "0.1.0"
author: "skills contributors; adapted for WorkBuddy by SandBase AI"
---

# Test CLI

Verify the CLI contract from a user's perspective, including behavior that is
easy to miss when only calling internal functions. Use this Skill for new
commands, regression testing, packaging checks, release readiness, or diagnosis
of shell- and platform-specific failures.

## Establish the contract

Identify the exact installed artifact, version, entry point, supported operating
systems, shell assumptions, and documented command behavior. Record:

- commands, subcommands, arguments, defaults, aliases, and incompatible options
- configuration files, environment variables, and precedence rules
- stdin formats and stdout/stderr contracts
- exit codes, files, network calls, and other observable side effects
- interactive prompts, TTY requirements, signals, and cancellation semantics

Test the built or installed artifact when release behavior matters; running a
source module directly may bypass packaging, launchers, or bundled resources.

## WorkBuddy test workflow

1. Create an isolated temporary directory with disposable fixtures. Set an
   explicit working directory and only the environment variables needed by the
   scenario.
2. Check help, version, unknown-command, and no-argument behavior before a
   minimal successful invocation.
3. Exercise required, optional, repeated, mutually exclusive, and ordered
   arguments. Include spaces, quotes, glob-like characters, Unicode, empty
   values, leading hyphens, long paths, and platform path separators where
   supported.
4. Test stdin as a pipe and file redirection, including empty input, missing
   terminators, binary or invalid encoding, and large bounded payloads when
   relevant.
5. Assert exit code, stdout, and stderr separately. Parse stable JSON or other
   machine-readable formats instead of snapshotting volatile text.
6. Verify configuration precedence without reading unrelated user-level config.
   Test missing files, malformed config, denied permissions, and unwritable
   destinations.
7. Inspect filesystem and network effects, partial outputs, cleanup, idempotency,
   retries, and repeated execution. Confirm dry-run modes do not mutate state.
8. Compare interactive TTY behavior with piped or non-interactive execution.
   Where safe and supported, verify interrupt, termination, timeout, and broken
   pipe handling without leaving child processes behind.

Avoid timing-only sleeps when an observable readiness condition is available.
Bound every wait, payload, retry, and spawned process so failures terminate.

## Safety boundaries

Do not test against real user data, credentials, home-directory configuration,
production services, or irreversible destinations when a disposable fixture is
possible. Never print secret values in commands, snapshots, or failure reports.
Stub or sandbox paid and state-changing network operations unless the user has
explicitly authorized the real effect.

Do not construct destructive test paths from an unresolved variable, wildcard,
home directory, repository root, or filesystem root. Confirm the exact temporary
target before cleanup.

## Failure report

For each failure, report the exact artifact version, platform, shell, working
directory, sanitized environment inputs, command, exit code, stdout, stderr,
filesystem/network effects, and minimal reproduction. Separate observed facts
from likely causes.

Finish with covered contract areas, untested platform or interaction gaps, and
the commands needed to rerun the suite. A passing internal unit test is not
evidence that packaging, stream behavior, or process semantics work correctly.
