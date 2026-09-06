---
name: "eval-driven-dev"
display_name: "评测驱动开发"
display_name_en: "Eval-Driven Development"
description: "Use when improving a Python LLM application with reproducible evaluation criteria, golden datasets, instrumentation, run evidence, and a prioritized quality plan."
description_zh: "用于为 Python LLM 应用建立可复现的评测标准、黄金数据集、运行证据和改进计划；评测真实应用行为，不把猜测当成质量结论。"
description_en: "Improve a Python LLM application with reproducible eval criteria, golden datasets, instrumentation, run evidence, and prioritized actions."
category: "evaluation"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with a Python 3.10+ project, an authorized evaluation environment, and an explicitly bounded model/API budget"
---

# 评测驱动开发

为 Python LLM 应用建立端到端质量反馈回路：定义评测标准，固定黄金样例，保留运行输入/输出证据，分析失败并形成可执行的改进清单。被测对象是应用的请求处理、上下文组装、路由和响应格式，而不是只测试一个孤立的模型调用。

## 何时使用

- 需要评估或回归 LLM、RAG、Agent 或工具编排行为。
- 需要把“回答变差了”转化为可复现样例、指标和失败分类。
- 需要比较提示词、检索、路由或输出格式的变更影响。

## 工作流程

1. 记录应用版本、模型/参数、数据来源、环境和预算；明确不采集的秘密与个人数据。
2. 将用户目标拆成可观察指标，例如事实依据、引用完整性、任务成功率、拒答正确性、延迟和成本。
3. 创建覆盖正常、边界、对抗和已知回归的黄金数据集；每条样例说明期望行为和允许的不确定性。
4. 通过隔离的数据库、缓存和第三方 API 测试数据控制外部输入，同时保留真实应用的路由、提示组装和响应处理。
5. 使用固定评测集运行基线和候选版本，保存模型标识、输入摘要、输出、评分器版本、失败原因和时间戳。
6. 对失败分类、抽样复核评分器、分析分数与用户目标的偏差，并输出按影响/成本排序的改进行动。
7. 只在满足门槛且证据可复现时晋级；否则标记为不确定或阻断，不用一次成功运行掩盖回归。

## 评测原则

- 真实模型调用可能产生非确定结果；使用分层阈值、重复运行、置信区间和人工校准，不依赖单次分数。
- 评测替身只控制外部数据，不伪造被测应用的核心模型结果；若因成本使用离线替身，必须明确其覆盖边界。
- 将事实、来源、推断和未知状态分开保存；引用校验失败应成为独立失败类别。
- 记录失败样例和最小复现上下文，避免把完整秘密、访问令牌或客户数据写入日志和数据集。

## WorkBuddy 安全边界

- 默认只读和离线分析；不得自动部署、修改生产数据、发送外部消息或发起付费调用。
- 运行前确认目标项目、模型、区域、预算、数据处理范围和停止条件；到达预算或错误率阈值立即停止。
- 只使用用户授权的脱敏数据；对外部工具和网络依赖分别记录权限、失败和副作用。
- 输出必须说明数据集覆盖、评分器局限、未验证项和证据新鲜度；不要把评测分数包装成普遍质量保证。
