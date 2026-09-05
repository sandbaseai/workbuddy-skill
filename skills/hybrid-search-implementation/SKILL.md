---
name: "hybrid-search-implementation"
display_name: "混合检索实现"
display_name_en: "Hybrid Search Implementation"
description: "Use when combining vector and keyword search for RAG or search systems, especially for exact terms, codes, names, and domain-specific vocabulary."
description_zh: "用于为 RAG 或搜索系统组合向量检索与关键词检索，尤其适合精确术语、编号、名称和领域词汇。"
description_en: "Design measurable hybrid retrieval with dense and sparse candidates, rank fusion, reranking, ACL filtering, query routing, fallbacks, and latency/cost controls."
category: "ai"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized vector/keyword indexes, versioned evaluation data, tenant-aware filters, and an isolated test target; indexing changes and production experiments require separate authorization"
---

# Hybrid Search Implementation

将语义召回与精确匹配结合起来：向量检索理解含义，关键词检索保留名称、代码、错误号和专有术语。混合检索的目标是提升可测的召回与回答质量，同时控制延迟、成本、权限和索引生命周期。

## 使用边界

- 开始前确认语料来源、许可证、租户/ACL、字段权重、索引版本、embedding/分词器版本、延迟和成本目标。
- 默认只读检查查询、索引配置、候选结果、分数和评测数据；验证使用脱敏或合成语料及隔离索引。
- 不擅自抓取受限内容、改变 ACL、重建/删除索引、上传用户数据或进行生产 A/B；这些操作需要明确授权与回滚方案。
- query、候选文本、metadata 和点击日志可能含敏感信息；长期证据只保存最小字段、哈希和聚合结果。

## 架构与权限

典型流程为 `query → dense + sparse candidates → hard filters → fusion → optional rerank → threshold/dedup → results`。租户、ACL、发布状态和数据保留条件必须在候选返回前作为硬过滤执行；模型不能决定用户权限，也不能通过 query 或 metadata 绕过过滤。

为每个结果保留 source/version/chunk ID、dense rank/score、sparse rank/score、融合分数、过滤原因和索引版本。分数来自不同检索器，不能未经校准直接相加；先记录排序和分布，再选择融合方法。

```python
def hybrid_retrieve(query, tenant_id, *, limit=20):
    filters = {"tenant_id": tenant_id, "status": "published"}
    dense = vector_index.search(query, filters=filters, limit=limit)
    sparse = keyword_index.search(query, filters=filters, limit=limit)
    fused = reciprocal_rank_fusion([dense, sparse], k=60)
    fused = remove_duplicate_sources(fused)
    return rerank(query, fused[:limit], limit=8)
```

## 融合与查询路由

- **RRF**：按各列表名次融合，适合没有可靠跨检索器分数校准的初始基线。
- **加权融合**：在固定评测集上校准 dense/sparse 权重，并按查询类型验证；不要把权重硬编码成通用真理。
- **级联**：先用便宜的硬过滤/关键词缩小候选，再进行向量或 cross-encoder 重排；记录漏召回风险。
- **查询路由**：精确 ID/代码、自然语言问题、短词、拼写变体和多语言查询可采用不同候选数或权重，但路由规则需可解释、可回归。

对空 query、单词 query、长 query、拼写错误、同义改写、数字/代码、无结果、重复结果、跨语言和注入文本分别测试。结果不足时返回低置信度或澄清，不以增加 top-k 或编造内容掩盖召回失败。

## 重排、阈值与上下文

重排器只处理已授权候选，设置候选上限、超时和成本预算；观察其对 Recall、nDCG、引用正确性、p95 延迟和 token 的影响。用版本化标注集校准阈值，区分“相关但旧”“相关但无权限”“相似但不能支持主张”。

去重按不可变 source/chunk/版本判断，避免同一段内容占满上下文；保留多样性时使用 MMR 或分组上限。传给生成模型的上下文应携带来源定位和可信边界，文档里的指令不能改变检索或工具策略。

## 评测与运维

建立 query 分层和金标准：测 dense、sparse、RRF、加权、级联和重排的 Recall@k、MRR/nDCG、precision、coverage、无答案拒答、ACL 正确性、引用支持率、p50/p95 延迟、错误率和每查询成本。候选与基线固定语料、索引、模型、过滤和参数，只改变声明变量。

监控各检索器空结果率、候选重合度、分数漂移、过滤拒绝、重排超时、索引 freshness 和查询成本。索引更新采用新版本构建、抽样校验、原子切换和可回滚 manifest；删除请求必须能证明所有副本和缓存均处理完毕。

交付报告记录查询/语料/索引版本、融合方法与权重依据、过滤和权限证据、前后质量、延迟、成本、失败分类、隐私处理、未覆盖查询和回滚条件。线上效果与离线评测冲突时保留冲突并重新调查。

## 质量门禁

- [ ] dense/sparse 索引、版本、来源、ACL、租户和删除策略可追溯。
- [ ] 硬过滤在召回结果返回前执行，不能由模型或 query 决定权限。
- [ ] RRF/加权/级联/路由/重排选择有分层评测、阈值和成本延迟证据。
- [ ] 空结果、精确术语、改写、多语言、重复、旧版本和提示注入均有测试。
- [ ] 结果可回溯到来源版本，去重、引用和低置信度拒答行为已验证。
- [ ] 索引更新、删除、缓存、生产 A/B 和配置变更均有授权、回滚与隐私边界。
