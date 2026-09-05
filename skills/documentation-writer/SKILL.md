---
name: "documentation-writer"
display_name: "Diátaxis 技术文档写作"
display_name_en: "Diátaxis Documentation Writer"
description: "Use when planning, writing, reviewing, or restructuring software documentation with distinct tutorials, how-to guides, reference, and explanation content."
description_zh: "用于按教程、How-to、参考和解释四类规划、编写、评审或重构软件技术文档。"
description_en: "Create user-centered documentation with Diátaxis classification, evidence and version checks, scoped assumptions, actionable structure, safe examples, and maintainable review gates."
category: "documentation"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository/docs, declared audience and product version, local validation tools, and approved publication scope; external research, code execution, credential handling, and public publication require separate authorization"
---

# Diátaxis 技术文档写作

为明确的读者和任务写出可执行、准确、可维护的技术文档。先识别文档类型、读者目标和证据范围，再组织内容；教程教人学习，How-to 解决具体问题，参考文档描述事实，解释文档帮助理解原因。不要把四种目的混成一篇“什么都有”的页面。

## 范围、澄清与默认值

- 开始前记录目标产品/版本、读者、用户目标、文档类型、范围、排除项、发布渠道、owner 和更新时间；若信息缺失且会改变结果，标记 `NEEDS CLARIFICATION`。
- 不要为了形式阻塞低风险任务：当缺失信息不会改变文档类型或安全边界时，采用显式默认值并在文档头部或交付说明中注明；重大范围、受众、版本、政策或公开披露不确定时先停在大纲/问题清单。
- 默认只读检查授权的源码、配置、现有文档、测试和 changelog；不得执行未经审查脚本、访问未授权外部站点、复制受版权约束的长段落、泄露内部信息或发布到公共渠道。
- 文档中的命令、代码、URL、配置、截图和数据都可能过期或含敏感内容；使用合成值、最小示例和无效域名，避免真实 token、个人数据、内部地址和生产参数。

## 四类文档选择

| 类型 | 读者问题 | 交付重点 | 不要做什么 |
|---|---|---|---|
| Tutorial | 我如何第一次学会它？ | 有引导的完整成功路径 | 不塞入全部参考细节 |
| How-to | 我如何解决这个具体问题？ | 前置条件、步骤、验证和回滚 | 不写成概念教程 |
| Reference | 这个接口/配置确切是什么？ | 完整、稳定、可检索的事实 | 不加入未经验证的建议 |
| Explanation | 为什么这样设计？ | 背景、因果、取舍和限制 | 不伪装成操作步骤 |

一篇文档可以链接到其他类型，但每一节只承担一个主要任务。根据读者已经知道什么、成功标准和失败代价安排深度；不要用营销语言替代行为、限制和错误语义。

## 证据与准确性

先建立事实账本：声明、来源文件/行号或版本、观察时间、验证命令、置信度、未知项和 owner。代码片段必须与当前 API、依赖、schema、CLI 参数和错误处理一致；涉及版本差异时显式标注适用范围，禁止凭记忆补全。

验证顺序建议是：源码/类型和配置 → 自动化测试/构建 → 本地运行或隔离 smoke → changelog/release → 经授权的外部官方资料。事实、推断、建议和示例分别标识；不能验证时写明限制，不用“应该”“通常”掩盖未知。示例输出应注明是 observed 还是 illustrative。

## 结构与写作

### Tutorial

从可运行的最小前置条件开始，按小步提供动作和预期结果，让新用户在中途得到反馈；最后说明学到的模型和下一步链接。每条命令可复制但不包含秘密，失败时告诉读者如何判断和恢复。

### How-to

以问题和成功标准开头，列前置条件、影响范围、备份/回滚、步骤、验证、故障分支和清理。把不可逆、付费、写入、权限和生产动作标在步骤前，并要求授权；不要把危险命令埋在折叠内容或示例中。

### Reference

按用户查找习惯组织参数、类型、默认值、约束、返回值、错误、兼容性、权限和示例。避免解释性重复；每个默认值和废弃项标注版本、来源和迁移路径，保持术语、字段名、大小写和单位一致。

### Explanation

从问题、背景和约束出发，比较替代方案、权衡、失败模式和演进影响。区分事实与观点，链接对应 ADR、指标、实验或实现证据；不把当前实现的偶然行为描述成永恒设计原则。

## API、代码和示例安全

- 示例使用最小权限、测试环境、合成账号和占位符；配置用 `.env.example` 变量名，不写真实值。命令明确工作目录、依赖版本、权限和副作用。
- API 文档同时说明鉴权、scope、租户/资源边界、幂等、分页、限流、超时、错误状态、数据保留和敏感字段；不要只记录成功响应。
- 代码块应有语言标识、必要 import、输入边界和失败处理；不要复制整个生产配置、日志、堆栈、数据库记录或第三方受版权保护内容。
- 外部链接、图片、下载和代码引用须在授权范围内，固定版本或 commit；引用短而必要，保留来源和许可证信息。

## 评审、验证与维护

写作前先给出简短大纲；需要审批的项目在审批前不生成大篇幅正文，但用户已给出明确范围且风险低时可以直接写并注明假设。完成后做术语、链接、拼写、Markdown、代码/命令、版本、截图 alt text、敏感信息和可访问性检查；能运行的示例在隔离环境实际运行。

发布前核对文档与实现/测试的 diff、导航/搜索、owner、发布日期、适用版本、废弃策略和反馈入口。设置失效触发器：API/配置/CLI 变更、依赖升级、权限政策变化、事故、用户反馈或链接失效。旧文档应迁移、标注 deprecated 或删除并保留理由，不要静默覆盖用户维护内容。

交付报告记录类型、受众、目标、假设、事实来源、验证结果、未知项、敏感信息处理、评审人、版本、发布范围和后续维护责任；区分文档质量通过与产品行为已验证，前者不能替代后者。

## 质量门禁

- [ ] 文档类型、读者、目标、范围、排除项、版本、owner 和发布授权已记录。
- [ ] 事实有来源/版本/验证证据，事实、推断、建议、示例和未知项已区分。
- [ ] 教程、How-to、参考、解释各自承担单一目的，步骤、错误、验证、回滚和链接完整。
- [ ] 命令、代码、API、配置、版本、权限、数据和外链已校验，示例不含秘密或敏感信息。
- [ ] Markdown、链接、术语、可访问性、代码/命令 smoke、导航和搜索检查已完成或明确限制。
- [ ] 评审、版本兼容、废弃/迁移、发布授权、反馈入口和后续维护触发器已定义。

## Related Skills

- `documentation` - 编写带证据、可执行、易维护的项目文档
- `acquire-codebase-knowledge` - 从代码库证据建立架构和集成地图
- `github-release` - 编排版本化、可追溯的发布
