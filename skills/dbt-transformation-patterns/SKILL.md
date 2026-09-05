---
name: "dbt-transformation-patterns"
display_name: "dbt 转换模式"
display_name_en: "dbt Transformation Patterns"
description: "Use when organizing dbt analytics projects, designing source/staging/intermediate/mart models, adding tests and documentation, building incremental models, or reviewing lineage and transformation risk."
description_zh: "用于组织 dbt 分析项目、设计分层模型、增加测试与文档、构建增量模型，或审查 lineage 与转换风险。"
description_en: "Design layered dbt models with versioned sources, explicit contracts, tests, documentation, lineage, incremental boundaries, freshness, cost controls, and isolated validation."
category: "data"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized dbt project metadata and an isolated development/CI target; production model runs, writes, backfills, seeds, and contract changes require separate authorization"
---

# dbt Transformation Patterns

以可追溯分层、版本化契约和自动质量检查构建 dbt 转换。让 sources → staging → intermediate → marts 的责任清晰，控制增量边界、回溯成本、freshness、敏感数据和生产写入风险。

## 范围和安全边界

- 开始前确认 dbt 版本、adapter、项目/target、仓库提交、数据集/分区、所有者、SLA、成本预算和敏感级别。
- 默认只读审查 `dbt_project.yml`、models、sources、macros、tests、docs、manifest/catalog 和 CI 配置；验证优先使用 dev/CI target、合成或脱敏数据。
- 不在生产执行 `run`、`build`、`seed`、`snapshot`、`full-refresh`、回填、删除或权限/契约变更；这些是单独授权的外部副作用。
- SQL、样本、manifest、编译结果和日志不得包含 PII、secret、完整客户行或可还原标识；报告只保存聚合和脱敏证据。

## 模型分层与职责

采用适合项目的分层并记录偏离理由：

```text
sources/       原始来源、freshness 与来源契约
    ↓
staging/       与来源近似的一对一清洗、类型和命名规范化
    ↓
intermediate/  可复用业务逻辑、连接、去重和聚合
    ↓
marts/         面向分析/产品的稳定维度、事实和服务模型
```

Staging 不隐藏业务规则；intermediate 不成为无法复用的“垃圾抽屉”；marts 明确消费者、粒度、主键、更新频率和数据所有权。每个模型只承担一个清晰责任，重复逻辑提取为经测试的 macro，并考虑 adapter 方言差异。

## 命名、契约与来源

保持项目既有规则；无规则时可使用 `stg_<source>__<entity>`、`int_<purpose>`、`dim_<entity>`、`fct_<event>`，但需在项目文档确认。Source 定义记录表、列、加载时间、唯一标识、分区/时区、freshness、敏感级别和所有者。模型契约记录列类型、可空性、枚举/范围、粒度、关系、语义、版本和兼容策略；改变含义、删除/收窄字段或改变粒度必须有消费者影响与迁移计划。

## 测试和文档

关键模型至少检查 not-null、unique、accepted values、relationships、粒度/重复、跨字段一致性和业务关键不变量。测试写明适用分区、空集行为、严重性、抽样/全量范围和失败动作；避免只测 schema 而不测结果。模型和列文档说明来源、转换、粒度、更新时间、消费者和敏感性，生成的 lineage 必须能追溯到 source；不能从命名推断 lineage。

质量检查应结合 [Data Quality Frameworks](../data-quality-frameworks/) 的契约、基线和脱敏原则。Freshness 失败、新增 schema、模型测试失败、编译失败和验证器故障分别分类，不能把未执行当成通过。

## 增量模型与回溯

增量策略只在数据规模、更新模式、唯一键、事件时间、迟到数据、删除/更新语义和成本证据支持时采用。定义 watermark、lookback 窗口、merge/append 行为、去重、分区、并发、重跑和 late-arriving 数据处理；不要硬编码无来源的起始日期。超过窗口的修复需要有界回填计划、影响分区、成本、锁/并发、校验和回滚策略，默认在隔离 target 演练。

## 性能、依赖和 CI

检查 DAG 依赖、循环、过宽选择、重复扫描、笛卡尔积、不可下推过滤、物化方式和 full-refresh 风险。为高成本模型记录预估扫描量、执行基线、缓存/分区假设和 owner。CI 按变更选择受影响模型，同时保留 source freshness、契约、关键 mart 和安全门禁；选择性测试不能声称全项目通过。锁定 dbt/adapter/package 版本，审查 macro/package 权限和许可证。

## 交付报告

报告包含项目/提交/target、分层和 DAG、source/模型契约、粒度与 lineage、测试/文档/freshness、增量与回溯、性能/成本、敏感数据、CI 证据、未覆盖范围和迁移/回滚授权。区分 `observed`、`derived`、`unknown`；模型设计或静态检查不等于已在生产执行。

## 质量门禁

- [ ] dbt 版本、adapter、target、数据范围、所有者和授权边界明确。
- [ ] sources/staging/intermediate/marts 职责、粒度、主键、契约和 lineage 可追溯。
- [ ] 关键模型测试覆盖 schema、质量维度、关系、不变量和失败分类。
- [ ] 文档、freshness、增量 watermark、迟到数据、重跑和回溯策略有证据。
- [ ] DAG、物化、分区、成本、full-refresh、package 和 CI 门禁已审查。
- [ ] 验证使用隔离 target/安全数据，未执行未授权生产 run、写入、回填或契约变更。
