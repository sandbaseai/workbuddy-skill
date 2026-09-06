---
name: "microsoft-docs"
display_name: "Microsoft 官方文档检索"
display_name_en: "Microsoft Docs Research"
description: "Use when researching Microsoft technologies with official documentation search, code samples, and page retrieval, keeping citations, version context, and uncertainty explicit."
description_zh: "用于检索 Microsoft 官方文档、代码示例和完整页面，回答 Azure、.NET、GitHub、VS Code、Agent Framework 等技术问题，并保留引用与版本上下文。"
description_en: "Research Microsoft technologies through official docs, code samples, and page retrieval while preserving citations, version context, and uncertainty."
category: "research"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized Microsoft Learn/MCP or public web access; external tool availability must be verified before use"
---

# Microsoft 官方文档检索

优先使用 Microsoft Learn 和产品官方文档回答 Microsoft 技术问题，必要时检索官方代码示例和完整页面。输出把来源事实、版本假设、推断和未知项分开，避免用搜索摘要替代完整文档。

## 工作流程

1. 明确产品、版本/区域、任务目标、运行环境和用户需要的证据类型。
2. 先搜索官方文档概念、教程、参考和代码样例；对关键结论再获取完整页面。
3. 对照页面的发布日期、适用版本、前置条件、权限、费用和弃用提示。
4. 提取最小可执行示例，保留官方 URL、标题、访问时间和相关段落的语义证据。
5. 回答时区分官方明确说明、基于文档的推断和未验证信息；出现冲突时列出版本差异。

## WorkBuddy 边界

- 默认只读检索；不得因为文档示例而部署资源、修改订阅、发送消息或产生付费操作。
- 不复制密钥、租户数据、私有链接或完整客户内容；对输入和工具返回先脱敏。
- MCP/CLI 工具名称、Schema 和返回值都需运行时核验；工具不可用时明确说明并使用公开来源替代。
- 代码示例使用占位符，列出身份、网络、区域、权限和清理前提；不把文档存在当成运行成功证据。
