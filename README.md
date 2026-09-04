# SandBase for WorkBuddy

Give WorkBuddy access to the right SandBase model or API without memorizing provider names, request schemas, or polling details.

[![Validate skill](https://github.com/sandbaseai/workbuddy-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/sandbaseai/workbuddy-skill/actions/workflows/validate.yml)
[![Latest release](https://img.shields.io/github/v/release/sandbaseai/workbuddy-skill)](https://github.com/sandbaseai/workbuddy-skill/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[中文](#中文) · [English](#english)

## 中文

这是一个面向 WorkBuddy 的 SandBase Skill。它把“找能力 → 查看参数与价格 → 执行 → 获取异步结果”固化成可靠工作流，适合搜索、数据提取、多模态生成、嵌入和模型调用等任务。

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

## English

This WorkBuddy skill turns SandBase capability discovery into a safe, repeatable workflow: discover, inspect, run, and poll asynchronous jobs when needed.

### Install

1. Download `sandbase-workbuddy-skill.zip` from [Releases](https://github.com/sandbaseai/workbuddy-skill/releases/latest).
2. In WorkBuddy, open **Experts · Skills · Connectors → Skills → Add Skill**.
3. Upload the ZIP and make sure the SandBase MCP service is configured in your workspace.

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
```

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Please never commit API keys, access tokens, private prompts, or customer data.

## License

[MIT](LICENSE)
