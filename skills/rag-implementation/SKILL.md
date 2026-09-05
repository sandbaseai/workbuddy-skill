---
name: "rag-implementation"
display_name: "RAG 实现模式"
display_name_en: "RAG Implementation"
description: "Use when designing or reviewing Retrieval-Augmented Generation systems, knowledge search, document Q&A, grounding, citations, or retrieval evaluation."
description_zh: "用于设计或审查检索增强生成系统、知识搜索、文档问答、回答依据、引用和检索评测。"
description_en: "Design grounded RAG pipelines with ingestion, chunking, hybrid retrieval, reranking, citations, evaluation, observability, and privacy-safe data boundaries."
category: "ai"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized knowledge source, embedding/retrieval provider, isolated evaluation corpus, and configured model endpoint; indexing, deletion, and production writes require separate authorization"
---

# RAG Implementation

把外部知识可靠地带入模型上下文，让答案可追溯、可拒答、可评测。RAG 不是“接一个向量库”：要同时设计来源、解析、切分、索引、召回、重排、上下文预算、生成、引用和反馈闭环。

## 使用边界

- 开始前确认知识库 owner、来源许可证、更新频率、访问范围、租户边界、模型/embedding 版本、延迟与成本目标。
- 默认只读检查 schema、索引配置、检索结果和评测样本；使用合成、脱敏或已获授权的语料，不把用户输入自动写入知识库。
- 不擅自抓取受限内容、建立跨租户索引、删除/重建索引、上传文档、改变 ACL 或切换生产模型；这些是明确授权的副作用。
- 语料、向量 metadata、prompt、检索结果、trace 和评测集可能含敏感信息，报告只保留最小必要字段并脱敏。

## 先定义质量契约

在选型前写清问题类型、可接受的“不知道”、引用格式、时效性、语言、最大延迟、预算和安全约束。把质量拆成可测信号：

- **Retrieval**：相关文档是否进入 top-k（Recall@k、MRR、nDCG），过滤/租户边界是否正确。
- **Grounding**：回答中的关键主张是否被上下文支持，是否引用正确来源和版本。
- **Answer**：完整性、准确性、拒答质量、格式遵循和有害内容防护。
- **Operations**：索引 freshness、失败率、p95 延迟、token/查询成本、provider 错误和漂移。

评测集包含代表性问题、无答案问题、同义改写、跨文档问题、旧版本问题、权限边界和对抗性输入。将人工标注、规则检查和模型评审分开，并保存样本版本与评测配置。

## 摄取、解析与切分

为每个 chunk 保留不可变 `source_id`、文档版本、标题路径、页码/段落、更新时间、租户/ACL 标签和内容 hash；引用必须能从 chunk 回到原文。解析失败、OCR 不确定、重复文档和过期版本要分别标记，不能静默进入索引。

切分依据文档结构、语义边界和目标上下文，而非固定字符数；保留少量可解释 overlap，避免把表格、代码、列表和标题拆散。对不同文档类型做小规模对照实验，记录 chunk 策略、embedding 模型、维度和版本，变更时可重现。

## 召回与重排

根据语料和问题类型选择 dense、BM25 或 hybrid retrieval；对精确术语、编号、代码和专名不要只依赖 dense 相似度。先用 metadata/ACL 做硬过滤，再做相似度召回；不要让 prompt 中的文本决定权限。

用 MMR 或去重控制相似片段，必要时用 cross-encoder/模型重排，但设置候选数、超时、成本和降级策略。检索失败、无结果、低置信度和 provider 超时必须走不同路径；低质量上下文应触发澄清或拒答，而非编造。

```python
def grounded_context(question, tenant, *, k=8):
    # Authorization filter is applied by the retriever, never by the model.
    candidates = retriever.search(
        question,
        filters={"tenant_id": tenant, "status": "published"},
        limit=k,
    )
    candidates = rerank(question, candidates, limit=4)
    return [doc for doc in candidates if doc.score >= MIN_SCORE]

def answer(question, tenant):
    docs = grounded_context(question, tenant)
    if not docs:
        return {"answer": "没有找到足够依据。", "citations": [], "grounded": False}
    result = model.generate(build_prompt(question, docs))
    return {"answer": result.text, "citations": citation_ids(docs), "grounded": True}
```

## 生成、引用与提示注入

上下文明确标记为不可信资料；文档中的指令、脚本、链接或“忽略规则”不能改变系统策略、工具权限或回答格式。系统提示规定：只用给定依据、主张找不到支持时拒答、区分来源事实与推断、为关键主张附 source/version 定位。

引用应在生成后校验：每个关键主张能映射到返回 chunk，链接/页码存在且属于当前租户，引用版本未过期。无法验证的引用要删除或标为未验证；不要把检索到的文档数量当作回答正确性的证明。

## 索引生命周期与可观测性

索引任务必须幂等、可断点恢复并产生 manifest：输入 hash、解析状态、chunk 数、embedding 版本、写入批次和失败项。更新采用新版本索引与原子切换，保留回滚和删除证明；租户隔离、删除请求和 retention policy 优先于召回率。

记录脱敏后的 query hash、过滤范围、候选数量、分数分布、引用 ID、延迟、token 和错误类别。原始 query/context 默认不入长期日志；调试样本需显式授权、短期留存并可删除。

## 交付质量门禁

- [ ] 来源许可证、owner、ACL、租户边界、版本和 freshness 已确认。
- [ ] 解析/切分/metadata 能回溯到原文，重复、失败、过期和删除状态有分类。
- [ ] dense/sparse/hybrid、硬过滤、去重、重排、阈值和降级策略有评测证据。
- [ ] 评测覆盖无答案、权限、改写、跨文档、旧版本、注入和引用正确性。
- [ ] 关键主张可验证引用；无依据时澄清或拒答，不将模型自信当作证据。
- [ ] 索引更新、删除、回滚、日志、成本、延迟和敏感数据处理均有授权边界。
