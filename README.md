# WorkBuddy Skill Hub

Discover public Agent Skills, assess them before installation, and adapt high-value workflows for WorkBuddy. The repository also ships a production-ready SandBase integration as its first curated skill.

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

See the [English quickstart](docs/quickstart.md) and [copy-ready use cases](docs/use-cases.md).

## Capability map

| Need | SandBase workflow | Example output |
|---|---|---|
| Find a live API | Discover → inspect | Ranked candidates with current inputs and pricing |
| Run a model | Discover → inspect → run | Model response plus material limitations |
| Generate media | Discover → inspect → run → poll | Completed image, audio, or video result |
| Diagnose access | Account check + error guidance | Clear authorization, balance, or schema next step |

The skill does not bundle credentials, silently run paid calls when the user only asks for comparison, or bypass WorkBuddy permissions.

### Validate locally

```bash
python3 scripts/validate_skill.py
./scripts/package_skill.sh
```

## Repository layout

```text
skills/sandbase/
├── SKILL.md
└── references/
    ├── execution.md
    └── troubleshooting.md
scripts/validate_skill.py
scripts/crawl_github_skills.py
catalog/skills.jsonl
```

## 10,000+ Skill catalog

The catalog is generated from public GitHub `SKILL.md` results with resumable, rate-limit-aware collection. Every record keeps its repository, path, blob SHA, source links, WorkBuddy review state, and security review state. See [catalog documentation](catalog/README.md).

<!-- CATALOG-METRICS:START -->
| Metric | Current snapshot |
|---|---:|
| Indexed GitHub paths | 10,400 |
| Unique content SHAs | 6,688 |
| Source repositories | 5,292 |
<!-- CATALOG-METRICS:END -->

Browse the catalog in the [English WorkBuddy Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) or [中文 Atlas](https://sandbaseai.github.io/workbuddy-skill/zh-CN.html), or query the JSONL directly. If it helps you discover a useful workflow, a star or a short review helps other WorkBuddy users find it.

需要人工筛选的 WorkBuddy 文档、MCP、工作流、评测与 Skills？浏览 [Awesome WorkBuddy](https://github.com/sandbaseai/awesome-workbuddy)。

For a manually curated index of WorkBuddy documentation, MCP integrations, workflows, benchmarks, and Skills, browse [Awesome WorkBuddy](https://github.com/sandbaseai/awesome-workbuddy).

<!-- CATALOG-ANALYSIS:START -->
The current static analysis successfully inspected 10,400 paths: 9,169 are structurally adaptable to WorkBuddy, 885 need manual review, 0 are currently WorkBuddy-ready, and 259 contain at least one conservative security signal.
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
