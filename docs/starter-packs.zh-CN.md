# Starter Packs 入门包

如果你不想先搜索完整目录，可以从下面按任务选择一个起点。每一项都是
最新 Release 中已经审阅过的包；本页不会新增目录记录，也不表示任何包适合
所有环境。

| 目标 | 推荐起点 | 适合处理 |
|---|---|---|
| 审查代码变更 | [code-review-excellence](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/code-review-excellence-workbuddy-skill.zip) | 基于证据整理评审发现并排序风险 |
| 排查复杂故障 | [debugging-strategies](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/debugging-strategies-workbuddy-skill.zip) | 复现、假设、实验和回归检查 |
| 构建可靠测试 | [python-testing-patterns](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/python-testing-patterns-workbuddy-skill.zip) | fixture、mock、异步控制和风险驱动覆盖率 |
| 测试 Web 应用 | [webapp-testing](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/webapp-testing-workbuddy-skill.zip) | 浏览器流程、响应式行为和失败证据 |
| 设计后端架构 | [architecture-patterns](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/architecture-patterns-workbuddy-skill.zip) | 边界、依赖、端口、适配器和不变量 |
| 设计 API | [api-design-principles](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/api-design-principles-workbuddy-skill.zip) | HTTP 契约、授权、幂等和分页 |
| 做有来源的研究 | [deep-research](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/deep-research-workbuddy-skill.zip) | 结构化研究、来源比较和不确定性说明 |
| 安全使用 MCP | [mcp-security-audit](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/mcp-security-audit-workbuddy-skill.zip) | 凭据、命令注入、依赖和权限边界 |
| 准备发布 | [github-release](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/github-release-workbuddy-skill.zip) | 版本、发布证据、校验和资产核对 |
| 编写可维护文档 | [documentation-writer](https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/documentation-writer-workbuddy-skill.zip) | 教程、操作指南、参考和解释 |

## 安全试运行

1. 点击上面的 ZIP 链接下载，或按[快速开始](quickstart.zh-CN.md)中的命令行
   方式下载并校验 SHA256。
2. 导入前阅读包内 `SKILL.md`、来源链接、许可证、权限和引用的脚本。
3. 先让 WorkBuddy 给出只读计划。确认工具和副作用前，不要提供生产数据或凭据。

```text
先说明计划、工具、权限、输入、外部副作用和费用。
只使用公开或合成数据做只读检查。每个结论附上依据；缺少授权或必要输入时停止。
```

目录是用于审阅的公开快照。产品行为请以[官方 WorkBuddy 文档](https://www.workbuddy.ai/docs/zh/workbuddy/Quickstart)为准。
