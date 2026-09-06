# Starter packs

Use this page when you want a sensible first package without searching the full
catalog. Every item is an existing reviewed package in the latest Release; this
page does not add catalog records or imply that a package is safe for every
environment.

| Goal | Start with | What it helps with |
|---|---|---|
| Review application changes | [code-review-excellence](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/code-review-excellence-workbuddy-skill.zip) | Evidence-based review findings and risk prioritization |
| Debug a difficult failure | [debugging-strategies](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/debugging-strategies-workbuddy-skill.zip) | Reproduction, hypotheses, experiments, and regression checks |
| Build reliable tests | [python-testing-patterns](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/python-testing-patterns-workbuddy-skill.zip) | Fixtures, mocks, async control, and risk-driven coverage |
| Test a web application | [webapp-testing](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/webapp-testing-workbuddy-skill.zip) | Browser flows, responsive behavior, and failure evidence |
| Design a backend | [architecture-patterns](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/architecture-patterns-workbuddy-skill.zip) | Boundaries, dependencies, ports, adapters, and invariants |
| Work with APIs | [api-design-principles](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/api-design-principles-workbuddy-skill.zip) | HTTP contracts, authorization, idempotency, and pagination |
| Research with sources | [deep-research](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/deep-research-workbuddy-skill.zip) | Structured research, source comparison, and uncertainty |
| Use MCP safely | [mcp-security-audit](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/mcp-security-audit-workbuddy-skill.zip) | Credentials, command injection, dependencies, and permissions |
| Prepare a release | [github-release](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/github-release-workbuddy-skill.zip) | Versioning, release evidence, checksums, and asset checks |
| Write maintainable docs | [documentation-writer](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/documentation-writer-workbuddy-skill.zip) | Tutorials, how-to guides, reference, and explanation |

For the exact package asset, pinned source, ready-to-copy download command, and
the matching `SHA256SUMS`, use the [no-JavaScript reviewed package index](https://sandbaseai.github.io/workbuddy-skill/packages.html)
before importing a package.

## A safe first run

1. Download the ZIP from the link above, or use the [quickstart](quickstart.md)
   for a command-line download and checksum verification.
2. Read the package's `SKILL.md`, source link, license, permissions, and any
   referenced scripts before importing it.
3. Ask WorkBuddy for a read-only plan first. Do not provide production data or
   credentials until the required tools and side effects are understood.

```text
Explain the plan, tools, permissions, inputs, external side effects, and cost.
Run a read-only check with public or synthetic data only. Cite the evidence for
each conclusion and stop if an authorization or required input is missing.
```

The catalog is a review-oriented snapshot. For product behavior, use the [official
WorkBuddy documentation](https://www.workbuddy.ai/docs/workbuddy/Quickstart).
