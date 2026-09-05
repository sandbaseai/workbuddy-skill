---
name: "acquire-codebase-knowledge"
display_name: "代码库知识获取"
display_name_en: "Acquire Codebase Knowledge"
description: "Use when the user asks to map, document, or onboard into an existing codebase and needs evidence-backed architecture, structure, conventions, integrations, testing, and concerns documentation."
description_zh: "用于用户要求梳理、记录或熟悉现有代码库，并需要有证据支撑的架构、结构、约定、集成、测试和风险文档。"
description_en: "Produce an evidence-backed codebase map covering stack, structure, architecture, conventions, integrations, testing, and concerns without inferring undocumented intent."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized read-only repository, git, and terminal access; writing documentation, running scans, and publishing findings require scoped workspace authorization"
---

# Acquire Codebase Knowledge

将陌生代码库转换为可上手、可评审、可排障的证据地图。默认只读检查源码、配置、Git 历史和测试入口，输出结构、技术栈、架构、约定、集成、测试和风险；不把 README 中的意图当成当前事实。

## 输出契约

默认输出 `docs/codebase/` 下七份文档：`STACK.md`、`STRUCTURE.md`、`ARCHITECTURE.md`、`CONVENTIONS.md`、`INTEGRATIONS.md`、`TESTING.md`、`CONCERNS.md`。每份文档必须包含：

- 结论与适用范围；
- 可复核的证据清单（具体文件、配置键、命令输出或提交）；
- 未能确认的事项标记 `[TODO]`；
- 需要团队意图才能决定的事项标记 `[ASK USER]`；
- 事实、推导和假设的明确区分。

如果用户只要求某个领域，仍建立其他文档的最小骨架并标记未知项，不伪造完整分析。

## 安全与授权边界

- 扫描前确认仓库路径、提交/分支、允许读取的目录和输出位置；不默认读取父目录、私有密钥目录或外部挂载。
- 不执行项目安装脚本、应用启动脚本、迁移、部署、网络请求或任意源码；如确需命令，先列出命令及副作用并使用最小授权。
- 排除 `.git` 内部对象、`dist`、`build`、`generated`、`.next`、`out`、缓存和虚拟环境，除非用户明确要求审计生成物。
- 不将 `.env`、凭据、客户数据、授权头或完整日志写入文档；只记录变量名、脱敏摘要和证据路径。
- 文档写入、提交、发布和外部分享是独立动作；交付分析不等于自动发布。

## 阶段一：扫描和读取意图

先记录仓库提交、目录清单、语言文件、包管理清单、CI/CD、容器/编排、测试配置和安全策略。再读取 README、PRD、设计、路线图、规范和贡献指南，并将其中的“应该如此”与源码中的“实际如此”分开。

建立发现表：`area`、`source`、`observed`、`confidence`、`unknowns`。不因目录命名或变量名推断框架、数据库、部署平台或业务意图。

## 阶段二：分域调查

按以下问题调查并保留证据：

- STACK：生产依赖与开发工具分别是什么？运行时和入口在哪里？
- STRUCTURE：源码、测试、脚本、配置和生成物边界如何？有哪些入口？
- ARCHITECTURE：调用流、层次、模块边界、状态/数据所有权能由哪些文件证明？
- CONVENTIONS：命名、导入、错误处理、日志、格式化和分支约定实际是什么？
- INTEGRATIONS：外部 API、数据库、身份、队列、监控和配置入口在哪里？失败边界是什么？
- TESTING：测试框架、组织方式、fixture/mock、覆盖缺口和可安全运行的命令是什么？
- CONCERNS：高变更文件、陈旧文档、TODO、依赖/安全/性能风险分别有什么证据？

使用 Git 历史只作为变更频率和演进线索，不能把提交信息当成当前行为证明。大型仓库按模块分批调查，记录未覆盖范围。

## 阶段三：生成和校验

文档中的每个非平凡结论至少链接一个具体证据。若证据冲突，保留冲突并写出“意图 vs 现实”差异；若没有证据，使用 `[TODO]` 而不是补全常识。校验：七个文件齐全、必需章节非空、路径存在、命令不会隐式产生副作用、敏感值已脱敏。

## 交付格式

最终摘要包含：调查提交和范围、七份文档链接、关键发现、覆盖缺口、所有 `[ASK USER]` 问题，以及意图与现实的差异。明确哪些内容是 `observed`、`derived`、`inferred` 或 `unknown`，并建议安全的下一步，而不是声称已完成未执行的动作。

## 质量门禁

- [ ] 七份文档存在且覆盖范围明确。
- [ ] 每个重要结论有具体证据引用。
- [ ] 事实、推导、假设和未知分离；未知使用 `[TODO]`。
- [ ] 团队意图缺口使用 `[ASK USER]`，没有猜测。
- [ ] 生产依赖、开发工具、生成物和测试债务分类正确。
- [ ] 没有执行未授权代码、读取或发布敏感数据。
- [ ] 意图与现实差异、未覆盖区域和限制已交付。
