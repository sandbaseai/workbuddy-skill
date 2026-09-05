---
name: "llm-evaluation"
display_name: "LLM 评测"
display_name_en: "LLM Evaluation"
description: "Use when evaluating LLM or RAG applications, comparing models/prompts, detecting regressions, designing benchmarks, or validating safety and quality improvements."
description_zh: "用于评测 LLM 或 RAG 应用、比较模型和提示、发现回归、设计基准，或验证安全与质量改进。"
description_en: "Build reproducible LLM evaluations with task-specific datasets, automated and human metrics, judge calibration, regression thresholds, privacy-safe evidence, and release gates."
category: "ai"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized model endpoint, versioned evaluation corpus, isolated test target, and reviewer process; production experiments, user-data collection, and model changes require separate authorization"
---

# LLM Evaluation

把“看起来更好”变成可复现、可解释、能发现回归的证据。评测应围绕任务风险和用户目标组合自动指标、人工判断、对抗样本、线上信号与成本/延迟，而不是追求一个脱离场景的总分。

## 使用边界

- 开始前锁定模型/provider、版本、系统提示、工具、检索器、参数、数据快照、随机性、语言、时区和评测 owner。
- 默认使用合成、公开或脱敏样本；不得将真实用户输入、反馈或完整模型输出写入长期评测集，除非有明确授权、最小化和删除路径。
- 不擅自执行生产 A/B、收集用户画像、切换模型、改变安全策略或发布评测结论；这些操作需要独立授权。
- prompt、context、答案、grader 输出和 trace 可能含敏感信息；报告使用哈希、聚合和最小引用，保留失败样本需单独审批。

## 评测契约与数据集

先定义任务、受众、成功标准、不可接受错误、拒答条件、SLO、成本上限和版本范围。数据集按真实分布分层：常见、边界、长上下文、多语言、无答案、歧义、工具失败、权限、注入和安全样本；保留训练/评测隔离，避免泄漏。

每个 case 记录稳定 ID、输入类别、期望行为/参考答案（可选）、允许证据、风险等级、数据版本和评分规则。对随机模型运行固定 seed 或多次重复，报告样本量、缺失、置信区间和异常，而非只报告均值。

## 指标组合

- **任务结果**：分类用 precision/recall/F1 与混淆矩阵；结构化输出验证 schema、类型、必填字段和业务不变量。
- **文本质量**：BLEU/ROUGE 等重叠指标只适合相应任务；事实性、相关性、完整性和可读性需要语义或人工评审。
- **RAG**：分别测 retrieval Recall@k/MRR/nDCG、context relevance、claim groundedness、citation correctness 和无依据拒答。
- **安全与可靠性**：越权、提示注入、敏感信息泄露、危险建议、工具滥用、超时、重试和 graceful refusal 必须作为独立门禁。
- **运营**：p50/p95/p99 延迟、token、错误率、缓存命中、provider 成本和可用性与质量一起看。

不要把不同风险、不同任务或不同语言简单平均；按预先声明的权重和分层报告，保留逐 case 结果。

## 人工评审与 LLM-as-Judge

评分 rubric 写出 0/1/2 或等级的可观察锚点、必错条件和“不确定/不适用”。人工评审使用盲评、随机顺序、双评审和分歧仲裁，计算一致性并抽查 grader 漂移。pairwise 比较需平衡顺序和位置偏差。

LLM judge 只能作为可校准的测量工具：固定 judge 版本/提示，提供 rubric 与必要证据，先用人工金标准校准偏差，检查长度、风格、位置和自我偏好。judge 分数不能单独证明事实、安全或生产改进；关键样本必须人工复核。

```python
async def evaluate_case(case, system):
    output = await system.run(case.input)
    return {
        "case_id": case.id,
        "schema_ok": validate_schema(output),
        "task_score": score_task(output, case.reference),
        "grounded": check_claims_against_context(output, case.context),
        "citation_ok": validate_citations(output, case.allowed_sources),
        "unsafe": safety_check(output),
        "latency_ms": output.latency_ms,
        "tokens": output.usage.total_tokens,
    }
```

## 回归、比较与发布门禁

比较 prompt/model/retriever 时只改变一个主要变量，保持数据、工具、参数和评测器一致；记录候选与基线的完整配置。阈值应按业务风险设定：关键安全/权限项不能被平均分抵消，质量提升若伴随成本、延迟、拒答或引用正确性回退则不能直接发布。

对多次运行使用 bootstrap 或其他适合的区间/显著性方法，预先声明最小实际改进，避免在看到结果后挑选指标。出现数据分布、模型版本、评测器或 provider 变化时，标记不可直接比较并重新建立基线。

发布报告包含版本和 hash、数据分层、指标定义、逐层结果、失败样例分类、人工一致性、成本/延迟、安全测试、统计不确定性、已知偏差、未覆盖范围和回滚条件。线上监控与离线结果冲突时保留冲突，不将未知解释成成功。

## 质量门禁

- [ ] 任务、风险、成功/失败标准、模型配置、数据版本和评测器均可复现。
- [ ] 评测集覆盖常见、边界、无答案、权限、注入、多语言和工具/服务失败场景。
- [ ] 任务、grounding、引用、安全、可靠性、成本和延迟指标分层报告。
- [ ] 人工 rubric、盲评、一致性、judge 校准和关键样本复核已完成。
- [ ] 基线/候选只改变声明变量，报告样本量、区间、偏差和不可比条件。
- [ ] 未经授权不收集生产用户数据、不执行线上实验、不切换模型或发布安全策略。
