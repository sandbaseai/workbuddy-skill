# WorkBuddy Skill Hub

![WorkBuddy Skill Atlas — 10,000+ public Agent Skills with immutable provenance](site/social-preview.png)

Discover public Agent Skills, assess them before installation, and adapt high-value workflows for WorkBuddy. The repository also ships reviewed, production-ready Skills with bilingual metadata and immutable provenance.

[![Validate skill](https://github.com/sandbaseai/workbuddy-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/sandbaseai/workbuddy-skill/actions/workflows/validate.yml)
[![Latest release](https://img.shields.io/github/v/release/sandbaseai/workbuddy-skill)](https://github.com/sandbaseai/workbuddy-skill/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/sandbaseai/workbuddy-skill?style=flat)](https://github.com/sandbaseai/workbuddy-skill/stargazers)

[中文](#中文) · [English](#english)

## Start here · 从这里开始

1. **Search · 搜索：** Open the [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) or [中文目录](https://sandbaseai.github.io/workbuddy-skill/zh-CN.html). Results are deduplicated and ranked by WorkBuddy compatibility by default.
2. **Inspect · 审核：** Open the immutable GitHub source and review its license, instructions, bundled files, network behavior, and permissions. Static signals are triage aids, not guarantees.
3. **Adapt · 适配：** Copy the catalog ID and follow the [English](docs/adapting-skills.md) or [中文](docs/adapting-skills.zh-CN.md) guide to create a reviewable WorkBuddy ZIP.

Try local search in about a minute, without installing dependencies:

```bash
git clone https://github.com/sandbaseai/workbuddy-skill.git
cd workbuddy-skill
python3 scripts/query_catalog.py research --security no-static-flags --source-context primary-looking --min-score 80 --unique --sort score --limit 5
python3 scripts/review_skill.py --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

Search terms also match review metadata such as `prompt-injection`, `flagged`,
or `description_zh`, which makes security and compatibility triage searchable
without downloading third-party Skill bodies.

If the Atlas or adapter saves you time, [star the repository](https://github.com/sandbaseai/workbuddy-skill) so other WorkBuddy users can find it.

## 中文

这是一个面向 WorkBuddy 的开放 Skill 索引与适配仓库，目标是持续索引不少于 10,000 个公开 Skills，并把其中高价值条目经过来源、许可证、安全和兼容性检查后适配给 WorkBuddy。仓库首个精选成品是 SandBase Skill。

> **重要：** 被索引不代表安全或推荐。目录默认只保存 GitHub 元数据与原始链接，不执行第三方脚本；安装前必须检查许可证、指令、网络行为和权限。

```text
你：找一个适合中文发票 OCR 的 API，比较价格后处理这些图片。
WorkBuddy：发现候选 → 读取实时 schema 和价格 → 选择能力 → 执行 → 交付结果
```

### 为什么使用它

- 按需求发现能力，而不是猜工具名
- 执行前检查参数、价格和同步/异步模式
- 只传必要参数，避免无效调用和意外费用
- 对视频等异步任务持续查询，直到成功或失败
- 缺少 SandBase 工具时明确降级，不伪造结果

### 安装

1. 从 [Releases](https://github.com/sandbaseai/workbuddy-skill/releases/latest) 下载 `sandbase-workbuddy-skill.zip`。
2. 在 WorkBuddy 中打开 **专家 · Skills · Connectors → Skills → 添加 Skill**。
3. 上传 ZIP，并确保工作区已配置 SandBase MCP 服务。

也可以直接克隆：

```bash
git clone https://github.com/sandbaseai/workbuddy-skill.git
```

### 示例

- “找一个能提取网页结构化数据的 API，先告诉我价格再执行。”
- “用 SandBase 找适合中文 OCR 的模型，比较前三个候选。”
- “生成一段 5 秒产品视频，并等待最终结果。”

复制下面这句话完成安装后的首次验收：

```text
使用 SandBase 搜索一个网页提取 API。只比较候选、参数和价格，不要执行付费调用。
```

完整步骤见 [5 分钟快速开始](docs/quickstart.zh-CN.md)，更多可复制任务见 [使用场景](docs/use-cases.md)。

## English

This WorkBuddy skill turns SandBase capability discovery into a safe, repeatable workflow: discover, inspect, run, and poll asynchronous jobs when needed.

```text
You: Find an API for Chinese invoice OCR, compare prices, then process these images.
WorkBuddy: discover → inspect live schemas and pricing → select → run → deliver
```

### Install

1. Download `sandbase-workbuddy-skill.zip` from [Releases](https://github.com/sandbaseai/workbuddy-skill/releases/latest).
2. In WorkBuddy, open **Experts · Skills · Connectors → Skills → Add Skill**.
3. Upload the ZIP and make sure the SandBase MCP service is configured in your workspace.

Then verify it without spending credits:

```text
Use SandBase to find a web extraction API. Compare candidates, schemas, and pricing only; do not run a paid call.
```

For hosts supporting the open Agent Skills convention, install a reviewed
workflow directly by exact path:

```bash
gh skill install sandbaseai/workbuddy-skill skills/oss-review --dir .workbuddy/skills
```

For broader discovery, GitHub CLI can search public `SKILL.md` files, preview
one without installing it, and then install the exact path. Pin a tag or SHA
when reproducibility matters:

```bash
gh skill search incident --limit 10
gh skill preview owner/repository skills/path/to/skill
gh skill install owner/repository skills/path/to/skill --pin v1.2.0 --dir .workbuddy/skills
gh skill update --all
```

See the [English quickstart](docs/quickstart.md) and [copy-ready use cases](docs/use-cases.md).

## Capability map

| Need | SandBase workflow | Example output |
|---|---|---|
| Find a live API | Discover → inspect | Ranked candidates with current inputs and pricing |
| Run a model | Discover → inspect → run | Model response plus material limitations |
| Generate media | Discover → inspect → run → poll | Completed image, audio, or video result |
| Diagnose access | Account check + error guidance | Clear authorization, balance, or schema next step |

The skill does not bundle credentials, silently run paid calls when the user only asks for comparison, or bypass WorkBuddy permissions.

## Curated WorkBuddy Skills

| Skill | Use it for | Provenance |
|---|---|---|
| [SandBase](skills/sandbase/) | Discover, compare, and run live APIs and models | Repository-native |
| [Inspect Runtime Evidence](skills/inspect-runtime-evidence/) | Distinguish authoring, static, headless, native, and failed runtime evidence without overclaiming support | [MIT source](skills/inspect-runtime-evidence/SOURCE.json) |
| [Respec](skills/respec/) | Revise feature specifications from implementation evidence with traceable acceptance, compatibility, approval, and handoff | [MIT source](skills/respec/SOURCE.json) |
| [Documentation](skills/documentation/) | Create evidence-backed, executable, accessible, and maintainable project documentation | [MIT source](skills/documentation/SOURCE.json) |
| [Code Reviewer](skills/code-reviewer/) | Review diffs for correctness, regressions, scope, maintainability, security, and release safety | [MIT source](skills/code-reviewer/SOURCE.json) |
| [Debugging Methodology](skills/debugging-methodology/) | Reproduce, isolate, explain, fix, and verify software failures with controlled evidence and regression protection | [MIT source](skills/debugging-methodology/SOURCE.json) |
| [Security Audit](skills/security-audit/) | Audit trust boundaries, controls, vulnerabilities, compliance evidence, remediation, and residual risk within an authorized scope | [MIT source](skills/security-audit/SOURCE.json) |
| [Accessibility Review](skills/accessibility-review/) | Review semantics, keyboard and focus behavior, ARIA, screen-reader feedback, contrast, and accessible interaction states | [MIT source](skills/accessibility-review/SOURCE.json) |
| [Test Runner](skills/test-runner/) | Run fast or full repository verification with safe command selection, failure evidence, and reproducible reporting | [MIT source](skills/test-runner/SOURCE.json) |
| [Regression Risk Review](skills/regression-risk-review/) | Review behavior changes against existing contracts, failure modes, compatibility paths, and production impact | [MIT source](skills/regression-risk-review/SOURCE.json) |
| [Release Planner](skills/release-planner/) | Plan deployment order, migrations, rollout waves, risk gates, rollback, observability, and release communication | [MIT source](skills/release-planner/SOURCE.json) |
| [Architecture Decision](skills/architecture-decision/) | Make evidence-backed architecture choices with alternatives, trade-offs, fitness functions, migration, and review triggers | [MIT source](skills/architecture-decision/SOURCE.json) |
| [Performance Engineering](skills/performance-engineering/) | Measure and improve latency, capacity, CPU/memory/I/O, responsiveness, cost, and regressions with controlled evidence | [MIT source](skills/performance-engineering/SOURCE.json) |
| [Data Governance](skills/data-governance/) | Govern cross-system data with contracts, ownership, consent, identity, lineage, quality monitoring, safe fallbacks, and change management | [MIT source](skills/data-governance/SOURCE.json) |
| [Feature Flags](skills/feature-flags/) | Design safe runtime gates, gradual rollouts, experiments, kill switches, targeting, audit controls, and expiry cleanup | [MIT source](skills/feature-flags/SOURCE.json) |
| [AI Governance](skills/ai-governance/) | Govern AI systems with risk classification, lifecycle gates, human oversight, responsible-AI evidence, monitoring, exceptions, and accountable decisions | [MIT source](skills/ai-governance/SOURCE.json) |
| [Site Reliability Engineering](skills/site-reliability/) | Define SLOs, error budgets, toil reduction, incident learning, on-call health, capacity, graceful degradation, and progressive delivery | [MIT source](skills/site-reliability/SOURCE.json) |
| [Design Systems](skills/design-systems/) | Build accessible token foundations and component libraries with stable APIs, documentation, governance, migration, and adoption evidence | [MIT source](skills/design-systems/SOURCE.json) |
| [Mobile Development](skills/mobile-development/) | Build reliable iOS, Android, React Native, Flutter, SwiftUI, and Jetpack Compose apps with offline, performance, accessibility, security, testing, and release guidance | [MIT source](skills/mobile-development/SOURCE.json) |
| [Privacy Engineering](skills/privacy-engineering/) | Translate privacy requirements into data classification, consent, subject-rights, retention, vendor, deletion, and breach evidence | [MIT source](skills/privacy-engineering/SOURCE.json) |
| [FinOps](skills/finops/) | Manage cloud cost visibility, allocation, forecasting, commitments, optimization, unit economics, anomalies, and governance | [MIT source](skills/finops/SOURCE.json) |
| [Playwright Component Testing](skills/playwright-component-testing/) | Test isolated React and Vue components with story galleries, observable state, stable locators, traces, and CI evidence | [Apache-2.0 source](skills/playwright-component-testing/SOURCE.json) |
| [MCP Security](skills/mcp-security/) | Secure MCP tools and multi-agent pipelines with trust boundaries, authorization, privacy, side-effect controls, and auditable operations | [MIT source](skills/mcp-security/SOURCE.json) |
| [AI Agent Evaluation Engineering](skills/agent-evaluation-engineering/) | Build reproducible capability, trust, safety, trajectory, regression, latency, and cost evaluations | [MIT source](skills/agent-evaluation-engineering/SOURCE.json) |
| [Product Analytics](skills/product-analytics/) | Define event taxonomies, funnels, cohorts, retention, experiments, privacy boundaries, and evidence-backed product decisions | [MIT source](skills/product-analytics/SOURCE.json) |
| [dbt Patterns](skills/dbt-patterns/) | Design layered dbt models, contracts, tests, incremental workflows, lineage, and safe production delivery | [MIT source](skills/dbt-patterns/SOURCE.json) |
| [RAG Evaluation](skills/rag-evaluation/) | Build leakage-resistant datasets and measure retrieval, grounding, citations, refusal, latency, cost, and regressions | [Apache-2.0 source](skills/rag-evaluation/SOURCE.json) |
| [Browser Automation](skills/browser-automation/) | Navigate sites, fill forms, extract bounded data, capture artifacts, and verify browser flows safely | [MIT source](skills/browser-automation/SOURCE.json) |
| [API Resilience Engineering](skills/api-resilience-engineering/) | Design and diagnose deadlines, retries, idempotency, rate limits, breakers, backpressure, and ambiguous outcomes | [Apache-2.0 source](skills/api-resilience-engineering/SOURCE.json) |
| [AWS Resilience Assessment](skills/aws-resilience-assessment/) | Map failure paths, validate RTO/RPO and recovery evidence, prioritize risks, and design safe experiments | [MIT-0 source](skills/aws-resilience-assessment/SOURCE.json) |
| [GitHub Actions Engineering](skills/github-actions-engineering/) | Build, secure, optimize, and diagnose CI, releases, reusable workflows, artifacts, and deployments | [MIT source](skills/github-actions-engineering/SOURCE.json) |
| [Kafka Event Streaming Engineering](skills/kafka-engineering/) | Design and diagnose event contracts, delivery semantics, consumers, schemas, replay, and production changes | [MIT source](skills/kafka-engineering/SOURCE.json) |
| [Cache Engineering](skills/cache-engineering/) | Prove cache value and preserve key isolation, freshness, invalidation, degradation, and rollout safety | [MIT source](skills/cache-engineering/SOURCE.json) |
| [Container Image Engineering](skills/container-image-engineering/) | Build, secure, optimize, inspect, and diagnose Docker/OCI images | [MIT source](skills/container-image-engineering/SOURCE.json) |
| [Kubernetes Production Operations](skills/kubernetes-operations/) | Diagnose and safely change workloads, rollouts, networking, RBAC, resources, and stateful services | [MIT source](skills/kubernetes-operations/SOURCE.json) |
| [Terraform and OpenTofu Engineering](skills/terraform-engineering/) | Review modules, plans, state, tests, drift, upgrades, and infrastructure changes safely | [Apache-2.0 source](skills/terraform-engineering/SOURCE.json) |
| [PostgreSQL Database Engineering](skills/postgres-engineering/) | Design, query, secure, tune, maintain, and recover PostgreSQL safely | [MIT source](skills/postgres-engineering/SOURCE.json) |
| [OAuth and OIDC Troubleshooting](skills/oauth-debugging/) | Diagnose redirect, state, PKCE, token, session, and authorization failures safely | [MIT source](skills/oauth-debugging/SOURCE.json) |
| [GraphQL API Design and Review](skills/graphql-expert/) | Design and review schemas, resolvers, authorization, pagination, performance, and evolution | [MIT source](skills/graphql-expert/SOURCE.json) |
| [Monitoring and Observability Design](skills/monitoring-observability/) | Define service objectives, telemetry, dashboards, alerts, and end-to-end validation | [MIT source](skills/monitoring-observability/SOURCE.json) |
| [MySQL Database Operations](skills/mysql/) | Inspect schemas, write safe queries, analyze plans, and bound production changes | [MIT source](skills/mysql/SOURCE.json) |
| [Evidence-based Data Analysis](skills/data-analysis/) | Profile, analyze, challenge, and communicate structured-data evidence reproducibly | [MIT source](skills/data-analysis/SOURCE.json) |
| [Applying Differential Privacy](skills/differential-privacy/) | Define and verify privacy mechanisms, budgets, composition, utility, and release claims | [MIT source](skills/differential-privacy/SOURCE.json) |
| [OpenAPI Contract Review](skills/openapi-review/) | Validate structure, semantics, security, compatibility, and consumer usability | [MIT source](skills/openapi-review/SOURCE.json) |
| [Code Security Review](skills/security-review/) | Trace exploitable regressions through changed code and report evidence-backed findings | [MIT source](skills/security-review/SOURCE.json) |
| [Threat Modeling](skills/threat-model/) | Trace plausible abuse paths through real assets and boundaries into verifiable controls | [MIT source](skills/threat-model/SOURCE.json) |
| [User Research Synthesis](skills/user-research-synthesis/) | Turn mixed research evidence into traceable insights, conflicts, gaps, and actions | [MIT source](skills/user-research-synthesis/SOURCE.json) |
| [Product Roadmap Planning](skills/product-roadmap/) | Connect outcomes, evidence, dependencies, capacity, and uncertainty across planning horizons | [MIT source](skills/product-roadmap/SOURCE.json) |
| [Data and Schema Migration](skills/data-and-schema-migration/) | Migrate persisted formats through compatibility, idempotent backfills, and verified recovery | [MIT source](skills/data-and-schema-migration/SOURCE.json) |
| [Project Pre-mortem](skills/pre-mortem/) | Expose plausible failure paths and turn them into owned mitigations | [MIT source](skills/pre-mortem/SOURCE.json) |
| [Architecture Decision Record](skills/architecture-decision/) | Compare consequential technical choices and record verifiable tradeoffs | [MIT source](skills/architecture-decision/SOURCE.json) |
| [Incident Response and Triage](skills/incident-triage/) | Triage production incidents, contain harm, verify recovery, and preserve learning | [MIT source](skills/incident-triage/SOURCE.json) |
| [Prioritization Matrix](skills/prioritization-matrix/) | Rank options transparently with evidence, confidence, dependencies, and sensitivity | [MIT source](skills/prioritization-matrix/SOURCE.json) |
| [Requirements Grounding](skills/requirements-grounding/) | Turn mixed evidence into traceable, solution-free requirements with explicit confidence | [MIT source](skills/requirements-grounding/SOURCE.json) |
| [Email Drafting](skills/email-drafting/) | Draft accurate, actionable messages with recipient, attachment, privacy, and send checks | [MIT source](skills/email-drafting/SOURCE.json) |
| [Research with Sources](skills/web-researcher/) | Answer current questions with authoritative evidence, citations, and explicit uncertainty | [MIT source](skills/web-researcher/SOURCE.json) |
| [Software Release](skills/release-software/) | Prepare, verify, stage, publish, monitor, and roll back releases | [MIT source](skills/release-software/SOURCE.json) |
| [Meeting Notes](skills/meeting-notes/) | Extract supported decisions, action items, owners, risks, and open questions | [MIT source](skills/meeting-notes/SOURCE.json) |
| [CLI Testing](skills/test-cli/) | Verify arguments, streams, exit codes, configuration, signals, and side effects | [MIT source](skills/test-cli/SOURCE.json) |
| [Performance Improvement](skills/improve-performance/) | Measure, profile, optimize, and verify real system bottlenecks | [MIT source](skills/improve-performance/SOURCE.json) |
| [Work Handoff](skills/handoff/) | Preserve verified state, decisions, risks, and an executable restart point | [MIT source](skills/handoff/SOURCE.json) |
| [Test Strategy Design](skills/design-test-strategy/) | Turn product and system risks into a traceable, layered test portfolio | [MIT source](skills/design-test-strategy/SOURCE.json) |
| [Accessibility Review](skills/review-accessibility/) | Find keyboard, screen-reader, low-vision, cognitive, and motion barriers | [MIT source](skills/review-accessibility/SOURCE.json) |
| [Dense Writing](skills/dense-writing/) | Remove filler while preserving evidence, nuance, and constraints | [Apache-2.0 source](skills/dense-writing/SOURCE.json) |
| [Spreadsheet Operations](skills/excel-ops/) | Inspect, clean, analyze, convert, and create Excel/CSV files | [MIT source](skills/excel-ops/SOURCE.json) |
| [Open Source License Review](skills/oss-review/) | Review dependency licenses, obligations, and release risks | [Apache-2.0 source](skills/oss-review/SOURCE.json) |
| [Systematic Debugging](skills/systematic-debugging/) | Reproduce failures, trace root causes, and verify minimal fixes | [Apache-2.0 source](skills/systematic-debugging/SOURCE.json) |

Each curated directory is installable source: `SKILL.md` contains the WorkBuddy instructions, referenced resources are kept beside it, and externally adapted Skills include a machine-readable `SOURCE.json` plus their source license. Tagged releases publish one ready-to-upload ZIP per curated Skill.

### Validate locally

```bash
python3 scripts/validate_skill.py
./scripts/package_skill.sh
```

The validator also checks the standard Agent Skills installation invariants:
each skill's `name` matches its directory and uses the strict lowercase-hyphen
form, and `allowed-tools` remains a space- or comma-separated string. The adapter
also preserves the standard optional `compatibility` requirement when present
and validates its 500-character limit, including folded YAML values.
It also requires the declared `license` to
match `SOURCE.json` when provenance metadata is present. This keeps curated Skills compatible with
`gh skill publish --dry-run` and exact-path installation.

## Repository layout

```text
skills/sandbase/
├── SKILL.md
└── references/
    ├── execution.md
    └── troubleshooting.md
skills/rag-evaluation/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/agent-evaluation-engineering/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/playwright-component-testing/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/api-resilience-engineering/
├── SKILL.md
├── SOURCE.json
├── NOTICE
└── LICENSE
skills/aws-resilience-assessment/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/github-actions-engineering/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/kafka-engineering/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/cache-engineering/
├── SKILL.md
├── SOURCE.json
├── LICENSE
└── references/
    ├── contract.md
    ├── rollout-proof.md
    ├── runtime.md
    └── value.md
skills/container-image-engineering/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/kubernetes-operations/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/terraform-engineering/
├── SKILL.md
├── SOURCE.json
├── NOTICE
└── LICENSE
skills/postgres-engineering/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/oauth-debugging/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/graphql-expert/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/monitoring-observability/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/mysql/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/data-analysis/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/differential-privacy/
├── SKILL.md
├── SOURCE.json
├── LICENSE
└── references/
    ├── privacy-accounting.md
    └── release-statement.md
skills/openapi-review/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/security-review/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/threat-model/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/user-research-synthesis/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/product-roadmap/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/data-and-schema-migration/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/pre-mortem/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/architecture-decision/
├── SKILL.md
├── SOURCE.json
├── LICENSE
└── references/
    └── adr-template.md
skills/incident-triage/
├── SKILL.md
├── SOURCE.json
├── LICENSE
└── references/
    ├── incident-evidence.md
    └── logs-metrics-traces.md
skills/prioritization-matrix/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/requirements-grounding/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/email-drafting/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/web-researcher/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/release-software/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/meeting-notes/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/test-cli/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/improve-performance/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/handoff/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/design-test-strategy/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/review-accessibility/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/dense-writing/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/excel-ops/
├── SKILL.md
├── SOURCE.json
└── LICENSE
skills/systematic-debugging/
├── SKILL.md
├── SOURCE.json
├── LICENSE
└── references/
scripts/validate_skill.py
scripts/crawl_github_skills.py
catalog/skills.jsonl
```

## 10,000+ Skill catalog

The catalog is generated from public GitHub `SKILL.md` results with resumable, rate-limit-aware collection. Every record keeps its repository, path, blob SHA, source links, WorkBuddy review state, and security review state. See [catalog documentation](catalog/README.md).

<!-- CATALOG-METRICS:START -->
| Metric | Current snapshot |
|---|---:|
| Indexed GitHub paths | 12,258 |
| Unique content SHAs | 7,741 |
| Source repositories | 6,267 |
<!-- CATALOG-METRICS:END -->

Browse the catalog in the [English WorkBuddy Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) or [中文 Atlas](https://sandbaseai.github.io/workbuddy-skill/zh-CN.html), or query the JSONL directly. If it helps you discover a useful workflow, a star or a short review helps other WorkBuddy users find it.

需要人工筛选的 WorkBuddy 文档、MCP、工作流、评测与 Skills？浏览 [Awesome WorkBuddy](https://github.com/sandbaseai/awesome-workbuddy)。

For a manually curated index of WorkBuddy documentation, MCP integrations, workflows, benchmarks, and Skills, browse [Awesome WorkBuddy](https://github.com/sandbaseai/awesome-workbuddy).

<!-- CATALOG-ANALYSIS:START -->
The current static analysis successfully inspected 12,258 paths: 9,864 are structurally adaptable to WorkBuddy, 903 need manual review, 0 are currently WorkBuddy-ready, and 404 contain at least one conservative security signal.
<!-- CATALOG-ANALYSIS:END -->
A clean static scan is never a security guarantee.

```bash
GH_TOKEN="..." python3 scripts/crawl_github_skills.py --target 10000
python3 scripts/analyze_catalog.py
python3 scripts/validate_catalog.py --minimum 10000 --require-analysis
python3 scripts/query_catalog.py invoice --limit 10
```

Only metadata is committed by default. Third-party content remains at its original source until a maintainer deliberately reviews and adapts it.

Search results are provenance links, not installation approvals. For machine-readable output, add `--json`; combine terms to require all words to match repository names, paths, or inferred skill names.

To turn a reviewed entry into a WorkBuddy-compatible ZIP, use
`scripts/adapt_skill.py`. It normalizes frontmatter, keeps immutable provenance,
requires a source-license declaration, and refuses flagged or incomplete input
by default. See the [English adaptation guide](docs/adapting-skills.md) or
[中文适配指南](docs/adapting-skills.zh-CN.md).

## Compatibility

| Environment | Status | Notes |
|---|---|---|
| WorkBuddy | Primary | Uses the official WorkBuddy skill package layout |
| Other MCP-capable agents | Portable instructions | Frontmatter extensions may require adaptation |
| Chat-only assistants | Guidance only | Cannot discover or execute SandBase tools |

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
To help turn the catalog into a trusted shortlist, nominate a public Skill in
the [community review queue](https://github.com/sandbaseai/workbuddy-skill/issues/5)
with its exact source, license, permissions, and a concrete user problem. Please
never commit API keys, access tokens, private prompts, or customer data.

For help, see [SUPPORT.md](SUPPORT.md); for responsible vulnerability reports,
see [SECURITY.md](SECURITY.md).

See the [changelog](CHANGELOG.md) for release history.

## License

[MIT](LICENSE)
