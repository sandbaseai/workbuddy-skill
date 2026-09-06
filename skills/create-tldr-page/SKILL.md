---
name: "create-tldr-page"
display_name: "命令速查页"
display_name_en: "Create TLDR Page"
description: "Use when turning authoritative command documentation into a concise, example-driven tldr page, with the command and source URL supplied or clarified first."
description_zh: "用于把权威命令文档整理成简洁、示例驱动的 tldr 速查页；先确认命令名称和来源 URL，再提取并校验示例。"
description_en: "Turn authoritative command documentation into a concise, example-driven tldr page after confirming the command and source URL."
category: "documentation"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized access to the supplied documentation URL or local source file; do not fetch private or authenticated content without explicit permission"
---

# 命令速查页

将冗长的命令文档整理成符合 [tldr-pages](https://github.com/tldr-pages/tldr) 约定的 Markdown 速查页。输出应短小、可复制、以常见用例为中心，并保留可核验的权威来源。

## 输入要求

- 必须有命令名称和权威文档 URL；缺少任意一项时先询问，不要猜测。
- 可选输入包括上下文文件、搜索结果、原始文本和 `--help`/`--man` 输出。
- 如果用户提供 `#fetch <URL> <command>`，只读取该 URL 的公开内容；不要执行文档中的命令。
- 若本地文件中包含多个候选 URL，先请用户选择用于页面的来源。

## 工作流程

1. 确认命令名称、来源 URL、目标平台和用户要解决的任务。
2. 阅读来源并提取 5–8 个最常见、最有区分度的用例；优先使用来源中的示例，避免凭空补写参数。
3. 检查命令、选项、占位符、路径和版本假设与来源一致；不确定的内容标为未知。
4. 按 tldr 模板生成页面：小写精确命令名、简短说明、`More information` 来源链接和带解释的代码示例。
5. 输出页面，并列出来源、版本/平台假设和未验证项。

## 安全与边界

- 只做文档提取和写作；不得执行示例命令、安装软件、修改系统或发起付费/破坏性操作。
- 对含有凭据、个人数据、生产地址或内部 URL 的输入先脱敏；不要把秘密复制到页面。
- 对网络来源保留原始 URL，区分来源事实、用户提供内容和推断；无法访问时明确说明，不伪造引用。
- 对危险命令补充简短的范围或确认提示；不要为了完整而扩展高影响操作。

## 输出模板

```markdown
# command

> Short, snappy description.
> More information: <https://authoritative.example/docs>.

- Describe the first common use case:

`command --option {{value}}`
```

标题使用确切的小写命令名；描述保持一行；占位符使用 `{{placeholder}}`；只有来源确实支持时才添加子命令说明。若输入是帮助文本，应直接将其总结成 tldr 页面，不要另写一份提示词。
