---
name: "vector-index-tuning"
display_name: "向量索引调优"
display_name_en: "Vector Index Tuning"
description: "Use when tuning vector search latency, recall, memory, index build time, quantization, or scaling strategy."
description_zh: "用于调优向量搜索延迟、召回率、内存、索引构建时间、量化策略或扩展方案。"
description_en: "Tune vector indexes from measured recall, latency, memory, build, and update baselines while preserving tenant isolation, deletion, and rollback guarantees."
category: "ai"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized vector index metrics, a versioned evaluation corpus, isolated benchmark infrastructure, and a safe rebuild target; production reindexing, configuration changes, and data writes require separate authorization"
---

# Vector Index Tuning

在召回、延迟、内存、构建和更新成本之间做可测取舍。索引类型和参数没有通用最优值；先锁定查询分布、向量维度、过滤条件、更新频率、租户/删除语义和 SLO，再用固定数据和查询集做基线。

## 使用边界

- 开始前确认 embedding 模型/维度/版本、索引实现、数据量、字段过滤、硬件、数据区域、owner、SLO 和预算。
- 默认只读检查索引配置、查询 trace、召回标注、内存/CPU、构建日志和版本 manifest；基准使用合成、脱敏或授权语料。
- 不擅自重建/删除生产索引、切换 embedding、改变租户过滤、扩容或修改副本；生产变化必须有授权、双写/回滚和删除证明。
- 向量 metadata、query、路径和结果可能含敏感信息；日志只保留哈希、聚合分布和不可逆的样本标识。

## 基线与指标

固定索引版本、数据快照、查询集、过滤条件、并发、warm/cold 状态和硬件，记录 Recall@k、MRR/nDCG、过滤后召回、p50/p95/p99 延迟、QPS、内存、CPU、构建时间、更新/删除延迟和成本。区分近似搜索的召回损失、网络/序列化耗时、过滤耗时和重排耗时。

查询集要覆盖精确术语、短 query、长 query、多语言、空/无结果、热门向量、租户过滤、时间范围、删除后查询和分布漂移。没有标注或可靠的 exact-search 对照时，只能报告相对趋势，不能声称召回保持不变。

## 索引与参数选择

小数据集先用 flat/exact 作为质量基线；规模扩大后再比较 HNSW、IVF/PQ、DiskANN 或 provider-specific 索引。HNSW 的 `M`、`efConstruction` 和 `efSearch` 通常分别影响内存/构建质量/查询质量，但参数必须在目标硬件和过滤模式下实测。IVF 的分桶数、探测数和 PQ 压缩也需与向量分布、更新模式共同评估。

```python
def benchmark(config, queries, exact_reference):
    index = build_index(config)
    results = search_all(index, queries)
    return {
        "recall_at_k": recall(results, exact_reference),
        "p95_ms": percentile(results.latencies_ms, 95),
        "memory_mb": index.memory_mb,
        "build_seconds": index.build_seconds,
        "config": config,
    }
```

只改一个主要变量，固定其他条件并重复运行；将参数、库/硬件版本和随机种子写入 manifest。先以默认值建立对照，再按 SLO 排序实验，不要仅因内存下降就接受不可接受的召回、删除延迟或过滤错误。

## 量化、过滤与生命周期

比较 FP32、FP16、INT8、PQ 或 binary 时验证距离近似、语言/领域差异、尾部 query、重排需求和模型版本兼容性。量化索引保留少量高精度重排候选可能改善质量，但增加延迟和成本；所有取舍必须有分层结果。

ACL、租户、发布状态、删除和时间范围过滤应作为索引查询的硬边界，不可交给相似度或模型判断。验证过滤前后召回、空结果和越权回归；删除请求要覆盖主索引、副本、缓存和备份的 retention 证明。

采用新索引版本离线构建、校验 schema/维度/计数/抽样结果和权限，再原子切换。保留旧版本、回滚窗口、增量更新队列、失败重试和重建成本；embedding 变更通常需要完整重建，不能静默混用不同空间。

## 交付质量门禁

- [ ] 数据快照、embedding/索引/硬件版本、查询分层和基线指标可复现。
- [ ] index 类型、HNSW/IVF/PQ 参数、量化和重排选择有召回、延迟、内存、构建和成本证据。
- [ ] ACL、租户、删除、时间过滤和缓存边界在索引查询中强制执行并通过回归。
- [ ] 实验只改变声明变量，覆盖 warm/cold、并发、无结果、漂移和尾部查询。
- [ ] 新旧索引切换、增量更新、失败恢复、回滚和删除证明已设计并隔离验证。
- [ ] 生产重建、模型/参数切换、扩容和写入均有授权，报告已脱敏且区分未知项。
