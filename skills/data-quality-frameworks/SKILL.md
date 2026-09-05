---
name: "data-quality-frameworks"
display_name: "数据质量框架"
display_name_en: "Data Quality Frameworks"
description: "Use when implementing data-quality checks, data contracts, validation pipelines, freshness monitoring, or CI/CD gates for analytical and operational datasets."
description_zh: "用于实现数据质量检查、数据契约、验证流水线、新鲜度监控，或为分析与业务数据建立 CI/CD 门禁。"
description_en: "Define contract-backed completeness, uniqueness, validity, accuracy, consistency, and timeliness checks with bounded samples, baselines, privacy-safe evidence, and fail-closed pipeline decisions."
category: "data"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized data-schema access and an approved test/staging dataset or read-only warehouse connection; production writes, alerts, quarantines, and contract changes require separate authorization"
---

# Data Quality Frameworks

为数据管道建立可解释、可重复、隐私安全的质量验证。围绕数据契约和业务关键字段检查完整性、唯一性、有效性、准确性、一致性和时效性，并将失败转化为有证据的阻断、告警或人工复核决定。

## 范围和安全边界

- 开始前确认数据集、版本/分区、来源、时区、schema、业务负责人、允许的样本范围和质量目标。
- 默认只读检查 schema、元数据、统计摘要和授权测试数据；不写入生产表、不删除/隔离记录、不触发真实告警或重跑高成本全量任务。
- 采样必须有界并记录方法、覆盖率、偏差和查询成本；抽样通过不能推断全量通过。
- 记录聚合值、计数、比例和脱敏示例，不保存 PII、支付信息、秘密、完整原始行或可还原的用户标识。
- 质量失败不自动等同于业务事故；区分数据问题、契约变更、上游延迟、采集缺失、规则过时和验证器故障。

## 数据契约

为每个关键数据集建立版本化契约，至少包含：字段名/类型/可空性、允许值或范围、主键/唯一性、关系约束、分区/时区、新鲜度目标、敏感级别、所有者、兼容性策略和失败处置。契约变更必须说明新增、删除、收窄、放宽和迁移窗口；没有批准版本时标记 `unknown`，不从当前样本反推契约。

## 质量维度与检查

按风险选择检查，不盲目测试每一列：

| 维度 | 典型问题 | 证据 |
|---|---|---|
| 完整性 | 关键字段空值、分区缺失 | null ratio、分区计数 |
| 唯一性 | 主键或业务键重复 | distinct/duplicate count |
| 有效性 | 枚举、格式、范围非法 | 合法值比例、越界摘要 |
| 准确性 | 与可信源不一致 | 对账差异、抽样交叉核对 |
| 一致性 | 跨字段/跨表矛盾 | 关系失败计数、约束摘要 |
| 时效性 | 数据延迟或陈旧 | 最大事件时间、延迟分布 |

每条规则写清字段、谓词、单位、适用分区、空集行为、允许误差、严重性和失败动作。`null`、未知枚举、重复键、无数据和验证器错误不能混为一个 0 分。

## 基线、阈值和增量验证

优先在源数据进入转换前检查，再逐层检查关键转换和跨表关系。阈值以历史基线、业务 SLA 或契约为依据，记录窗口、样本量、统计方法和置信限制；不要硬编码没有来源的阈值。增量检查覆盖新增/变更分区，并定期抽查历史分区，避免旧数据永久逃逸。动态基线必须设置上下限、冷启动、季节性和异常缺失策略。

检查计算失败率和“未执行”状态，避免把空输入或查询超时当成全通过。高风险字段、跨系统对账、权限/租户隔离和金额等规则应设置阻断级别；低风险漂移可以告警但仍需记录。

## 流水线和报告

在 CI/CD 或编排中把质量检查作为有界步骤：固定数据版本/分区，输出机器可读结果和人类摘要，保留规则版本、运行时间、查询 ID、样本统计和脱敏证据。失败报告至少包含 dataset、partition、rule、expected、observed、severity、coverage、baseline、owner、下一动作和是否阻断发布。

失败处置分为：阻断下游、重试上游读取、延迟等待 freshness、进入人工复核、发布兼容变更或登记已批准例外。重试要有次数和总时限；例外必须有负责人、理由、范围、到期日和补偿检查，不得永久吞掉失败。

## 监控与演进

跟踪通过率、失败率、新鲜度、规则覆盖、误报/漏报反馈和上游责任。规则和契约随 schema/业务变化评审，删除过时规则前先查历史影响。准确性通常只能用抽样或可信源验证，报告其成本和不确定性；工具版本、connector 和 SQL 方言也要固定并记录。

## 质量门禁

- [ ] 数据集、版本/分区、schema、时区、所有者和授权范围明确。
- [ ] 契约版本化，字段、关系、freshness、敏感级别和兼容策略可追溯。
- [ ] 检查覆盖关键质量维度，规则含谓词、单位、空集行为、阈值和严重性。
- [ ] 采样/增量范围、基线、样本量、冷启动和缺失数据状态明确。
- [ ] 失败与未执行、数据问题与验证器故障分开，处置有界且例外会过期。
- [ ] 报告可机器解析、证据脱敏，没有未授权写入、告警或高成本全量操作。
