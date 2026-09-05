---
name: "prd"
display_name: "产品需求文档"
display_name_en: "Product Requirements Document"
description: "Use when turning a product or AI feature idea into a measurable Product Requirements Document with user stories, technical specifications, acceptance criteria, evaluation, risks, and rollout phases."
description_zh: "用于将产品或 AI 功能想法整理为可度量的产品需求文档，包含用户故事、技术规格、验收标准、评测、风险和分阶段发布。"
description_en: "Produce a fact-grounded PRD that separates confirmed decisions from assumptions, defines measurable outcomes, and gives engineering and evaluation teams an actionable contract."
category: "product"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with access to the authorized product context, repository or design evidence, and optional research/evaluation tools; publication, data access, and implementation changes require separate authorization"
---

# 产品需求文档（PRD）

把模糊的产品或 AI 功能想法转换成业务、设计、工程、评测和运营都能执行的需求契约。PRD 的目标不是填满模板，而是让问题、范围、成功标准、约束、风险和决策责任可验证、可追踪。

## 激活与证据边界

适用于新产品/功能启动、需求澄清、AI 能力规格、验收标准设计和实施前统一范围。开始前记录文档受众、决策人、版本和允许使用的资料范围。

- 至少提出两个关键澄清问题；如果用户暂时无法回答，写成 `TBD` 或明确假设，不要猜测技术栈、预算、法规、用户规模或发布日期。
- 将信息分成 `Confirmed`（有来源或用户确认）、`Assumption`（待确认）、`Unknown`（尚无证据）和 `Decision`（需要负责人选择）。不要把推断写成事实。
- 只读取授权的产品、用户研究、分析、设计、代码和政策资料；最小化个人数据，报告中脱敏，不复制客户内容、凭据或私有提示词。
- 工具、API、数据库、实验、付费调用和生产写入必须在需求中标注用途、权限、成本和授权人；PRD 本身不代表已经批准实施。
- 所有指标写明单位、时间窗口、分母、基线、目标、数据来源和统计口径。避免只写“快”“智能”“易用”“现代”。

## Phase 1：发现问题

先询问并记录：

1. 核心用户和具体痛点是什么，为什么现在解决？
2. 成功如何衡量，当前基线和期望改善是多少？
3. 目标市场、平台、地区、语言、时间、预算和技术约束是什么？
4. 已有方案、替代方案和不做这件事的代价是什么？
5. 哪些内容已经决定，哪些需要产品、工程、安全、法务或数据负责人确认？

将答案与来源绑定；把无法回答的问题放入 Assumptions/Unknowns，并说明会阻塞哪项决策。

## Phase 2：分析与定界

- 画出从触发到结果的用户流程，标出成功、空结果、错误、取消、权限不足和恢复路径。
- 定义目标用户、反目标用户、用户故事、非目标和明确的 MVP 边界。每个用户故事都必须有可观察的完成条件。
- 盘点依赖：API、数据集、身份、存储、模型、人工审核、供应商、迁移、运营和支持；为每项标注 owner、状态和替代方案。
- 对 AI 功能额外定义输入/输出、工具调用、引用或来源要求、拒答条件、人工升级、评测集、质量阈值、延迟、成本和漂移监测。
- 用影响/成本/风险或 RICE 等明确方法排序，不以“大家都觉得重要”作为优先级证据。

## Phase 3：按固定 Schema 起草

```markdown
# <产品/功能名称>

Status: Draft | In Review | Approved | Superseded
Owner: <decision owner>
Version: <version/date>

## 1. Executive Summary

### Problem Statement
<具体问题、受影响用户、证据和时机>

### Proposed Solution
<解决方案及其边界；不要把实现猜测写成决定>

### Success Criteria
| KPI | Baseline | Target | Window | Source | Owner |
|---|---:|---:|---|---|---|

## 2. User Experience & Functionality

### Personas
<用户、权限、目标、环境>

### User Stories
- As a <user>, I want to <action>, so that <benefit>.

### Acceptance Criteria
- Given <context>, when <action>, then <observable result>.

### Non-Goals
- <明确不做的事情>

## 3. AI System Requirements (if applicable)

### Inputs, Tools, and Outputs
<schema, permissions, sources, citations, side effects>

### Evaluation Strategy
<dataset, slices, metrics, human calibration, thresholds, regression gate>

## 4. Technical Specifications

### Architecture and Data Flow
<components, boundaries, sequence, failure paths>

### Integrations
<API, database, auth, rate/cost limits, contracts>

### Security & Privacy
<data classification, retention, access, logging, abuse and compliance questions>

## 5. Risks & Roadmap

### Phased Rollout
<MVP -> next phase -> later phase, dependencies and exit criteria>

### Risks and Mitigations
| Risk | Likelihood | Impact | Signal | Mitigation | Owner |
|---|---|---|---|---|---|

## 6. Open Decisions and Evidence
| Item | Type | Evidence/Source | Decision owner | Due/Trigger |
|---|---|---|---|---|
```

## 质量标准

### 需求可验证

将模糊表述改成有范围的结果，例如：

- “搜索很快” → “在 10,000 条数据、P95 口径下响应不超过 200ms”；
- “结果相关” → “离线评测集 Precision@10 ≥ 85%，并单独报告长尾和权限过滤切片”；
- “界面易用” → “目标任务完成率、放弃率、键盘可操作性和无障碍审计均达到预先定义的阈值”。

不要为了让指标好看而改变分母、删除失败样本或把模型评审分数当作真实用户结果。阈值未被负责人批准时标为 Proposed。

### AI 与工具边界

为每个工具写清名称、输入 Schema、最小权限、数据去向、费用、超时、重试、幂等性和副作用。为不确定或高风险输出定义拒答、人工审核和回滚路径。生成式结果必须规定来源/引用、事实核验、提示注入处理、敏感数据过滤和评测回归。

### 迭代与审阅

先交付 Draft，列出最多影响范围的未决问题，再按章节请求反馈。每次修改保留变更摘要、决策理由、来源版本和未解决风险；Approved 只表示负责人批准需求，不表示代码、预算、生产发布或外部沟通已经获批。

## 完成交付前检查

- [ ] 至少两个关键澄清问题已回答，剩余内容均标记 Confirmed/Assumption/Unknown。
- [ ] 问题、目标用户、用户流程、非目标和 MVP 范围相互一致。
- [ ] 每个 KPI 有基线、目标、口径、时间窗口、来源和 owner。
- [ ] 每个用户故事有可观察的验收标准，包含失败和权限路径。
- [ ] AI 功能有输入/输出、工具边界、评测集、质量门槛、拒答和人工升级设计。
- [ ] 技术、数据、隐私、安全、成本、依赖、迁移和回滚风险有证据或明确 owner。
- [ ] 需求状态和批准范围没有被误写成实现或发布授权。

## Related Skills

- `requirements-grounding` - 校验需求与代码、设计、测试和历史证据的一致性
- `launch-risk-review` - 在实现证据具备后进行发布准备度评审
- `agentic-evaluation` - 为 Agent 输出建立可复现评测与回归门禁
