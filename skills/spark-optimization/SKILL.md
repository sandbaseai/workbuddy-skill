---
name: "spark-optimization"
display_name: "Spark 性能优化"
display_name_en: "Spark Optimization"
description: "Use when diagnosing or optimizing Apache Spark jobs, partitioning, shuffles, skew, caching, memory, or distributed data processing cost."
description_zh: "用于诊断或优化 Apache Spark 作业、分区、shuffle、数据倾斜、缓存、内存和分布式数据处理成本。"
description_en: "Optimize Spark jobs from measured baselines using execution plans, partition sizing, AQE, skew handling, memory and shuffle controls, and safe before/after validation."
category: "data"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized Spark UI/event logs, isolated test data, and a bounded compute target; production job reruns, configuration changes, and writes require separate authorization"
---

# Spark Optimization

以可重复的运行基线定位 Spark 的真实瓶颈，再用单变量实验验证收益。Spark 性能问题通常来自 shuffle、数据倾斜、分区粒度、扫描范围、序列化、GC 或下游写入；先判断瓶颈所在阶段，再决定配置或代码变化。

## 使用边界

- 开始前确认 Spark/Scala/Python 版本、集群类型、输入快照、分区布局、作业提交、owner、SLA、预算和目标环境。
- 默认只读分析 Spark UI、event log、SQL plan、executor 指标和代码；验证使用隔离集群、合成/脱敏快照及有界数据量。
- 不擅自重跑生产作业、修改集群配置、扩容、覆盖/删除输出、改变 checkpoint 或清理缓存；这些操作需要明确授权。
- 日志、event log、样本和计划可能含 SQL、路径、租户或敏感列名；报告保存聚合指标并脱敏资源标识。

## 先建立基线

记录输入行数/字节、过滤选择性、分区数、stage/task 时长分布、shuffle read/write、spill、峰值内存、GC、失败重试、输出大小、executor 数量、wall time 和成本。标记观察窗口、代码/配置/数据 hash 与缓存状态；没有基线时只能提出假设，不能声称优化完成。

从 DAG 和 SQL plan 定位 action、stage 边界和宽依赖。区分扫描慢、shuffle 慢、单个长尾 task、executor OOM、driver 压力和写入瓶颈；不要用总耗时掩盖 stage 级回归。

## 分区与 shuffle

- 尽量在读取端做列裁剪、谓词下推和分区裁剪，避免无必要的 `mergeSchema` 和全表扫描。
- 依据数据量、文件大小、task 时长和集群并行度调整分区；“每分区 128–256 MB”只是实验起点，不是通用保证。
- 减少不必要的 `repartition`、`distinct`、全局 `orderBy` 和重复 action；需要重分区时说明 key、基数和 shuffle 成本。
- 开启并验证 Adaptive Query Execution（AQE）对 coalesce、skew join 和动态分区的实际效果；配置改变可能因 Spark 版本而异。

```python
from pyspark.sql import functions as F

# Push filters and projection close to the read; inspect the plan before running.
events = (spark.read.format("parquet").load(input_path)
          .where(F.col("event_date") == logical_date)
          .select("entity_id", "event_type", "amount"))

result = (events.groupBy("event_type")
          .agg(F.sum("amount").alias("total_amount")))
result.explain(mode="formatted")
```

## 倾斜、连接与缓存

先用 key 频率和 task 分布证明倾斜，再选择 AQE skew join、广播小表、预聚合、拆分热点 key 或受控 salting。广播必须以实际大小、executor 内存和版本为依据；不要盲目 `broadcast` 大表。连接前检查 key 类型、空值、重复和基数，避免意外笛卡尔积。

缓存只用于会被重复消费且重算成本高的中间结果；确认存储级别、命中率和 eviction，任务结束释放不再需要的缓存。不要用 cache 掩盖低效 plan，也不要把 driver `collect()`、`toPandas()` 或大数组广播到 executor。

## 内存、序列化与可靠性

根据 executor 峰值、spill、GC、序列化时间和失败日志调整 partition、并行度和 memory overhead；优先减少对象数量、使用列式格式和内置表达式，谨慎使用 Python/Scala UDF。区分 driver OOM、executor OOM、shuffle fetch、磁盘不足和外部服务限流，分别验证修复。

输出写入应使用临时位置或事务/版本表，完成行数、schema、分区和质量检查后再发布；优化实验不能覆盖真实输出。checkpoint、重试和提交模式的改变要评估幂等性、重复写入和恢复路径。

## 验证与交付

一次只改变一个主要变量，固定输入快照、代码、数据格式、缓存状态和并发条件，至少重复足够次数以说明波动。比较 stage 级指标而非只看 wall time，同时检查结果 hash/行数、schema、空值、重复和下游兼容性。记录未验证的成本模型、环境差异和未知项。

交付报告包含：问题假设、基线、plan/DAG 证据、改动变量、前后指标、结果等价性、资源/成本变化、失败与回滚方式、生产授权状态和后续观测窗口。

## 质量门禁

- [ ] 输入、代码、Spark 版本、配置、缓存状态和运行环境已固定并可追溯。
- [ ] 已用 SQL plan、stage 指标和 executor 证据定位瓶颈，而不是猜测配置。
- [ ] 分区、shuffle、AQE、倾斜、连接、缓存、UDF 和内存策略有适用性理由。
- [ ] 实验使用隔离/有界数据，单变量前后对比且结果质量与 schema 未回归。
- [ ] 生产重跑、扩容、配置变更、checkpoint/缓存清理和写入均有明确授权。
- [ ] 报告脱敏并包含成本、可靠性、回滚和未覆盖范围。
