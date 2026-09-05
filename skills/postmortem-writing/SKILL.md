---
name: "postmortem-writing"
display_name: "事件复盘写作"
display_name_en: "Postmortem Writing"
description: "Use after an incident, near miss, or reliability event to produce a blameless, evidence-grounded postmortem with a timeline, contributing conditions, actions, owners, and follow-up verification."
description_zh: "用于在事件、险情或可靠性故障后编写无责、证据驱动的复盘，形成时间线、促成条件、行动项、负责人和后续验证。"
description_en: "Turn incident evidence into a psychologically safe learning artifact, separating facts from hypotheses, tracing systemic conditions, assigning bounded actions, and verifying whether risk actually decreased."
category: "operations"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized incident records, logs, metrics, change history, and a controlled document destination; do not infer blame or disclose sensitive data"
---

# 事件复盘写作

复盘的目标是改进系统，而不是寻找替罪羊。把事件材料整理成可审阅、可行动、可追踪的学习文档：明确发生了什么、哪些条件共同促成了结果、哪些证据仍缺失，以及如何验证改进确实降低了风险。

## 安全与范围门禁

开始前确认事件编号、时间窗口、读者、授权材料、保留期限和发布范围。默认最小披露：

- 只使用获授权的日志、指标、变更、工单、告警和访谈记录；未知内容标记 `Unknown`，不补写细节；
- 不点名羞辱个人，不把一次操作失误写成个人品格判断，不根据职位或相关性推断责任；
- 报告中脱敏 token、密码、个人信息、客户内容、内部地址、漏洞利用细节和不必要的供应商数据；
- 区分事实、推断、争议和估算；每个高影响结论绑定时间、来源或可复核查询；
- 事件仍在进行时，先服务稳定和安全处置；复盘不得替代值班升级、取证保全或正式事故响应。

证据不足、授权不明、事件尚未稳定或报告目标不清时，返回 `BLOCKED`，先列出缺口和安全的补证动作。

## 复盘工作流

1. **定义影响**：记录开始/结束时间、受影响用户或系统、错误预算/服务目标、数据完整性、恢复方式和置信度；事实与估算分栏。
2. **建立证据账本**：为日志查询、指标面板、变更记录、告警、部署、沟通和工单记录引用编号、时间范围、时区、保存位置和脱敏结果。
3. **重建时间线**：按统一时区排列“发生、发现、判断、缓解、恢复、验证”事件；标出观察间隔、矛盾时间和缺失数据。
4. **描述故障链**：从触发器、系统状态、失效机制、扩大因素到用户影响建立因果假设；避免把相关性直接写成根因。
5. **分析促成条件**：检查设计、依赖、容量、部署、监控、流程、权限、文档和沟通等系统条件；允许多个根因和未知项共存。
6. **记录响应决策**：说明当时已知信息、可选方案、为何选择、结果和未采用方案；不要用事后信息指责当时决策。
7. **生成行动项**：每项行动针对明确风险，指定负责人、截止时间、完成证据、优先级、依赖、回滚/退出条件和复查日期。
8. **进行复盘审阅**：让受影响团队核对事实、隐私和可执行性；异议保留为异议，不强行合并成单一叙述。
9. **验证学习结果**：到期检查测试、告警、演练、变更或指标证据，标记 `Verified`、`Partially Verified`、`Overdue` 或 `Rejected`，并更新残余风险。

## 证据状态与因果纪律

使用下列状态，避免把推测包装成事实：

| 状态 | 含义 |
| --- | --- |
| `Observed` | 可由原始记录直接复核的现象 |
| `Inferred` | 有多个证据支持但仍存在替代解释 |
| `Disputed` | 团队对事实、解释或影响存在分歧 |
| `Unknown` | 当前材料不能可靠回答 |
| `Verified` | 行动或假设已通过约定测试/指标复核 |

“根因”应描述可改变的系统条件，不应停留在“某人犯错”“操作不当”或“缺乏注意力”。如果存在多个必要条件，列出它们的关系；如果只能证明相关性，明确写出尚未证明的因果链。

## 复盘模板

```markdown
# <Incident title>

Status: Draft | Reviewed | Published | Superseded
Severity: <policy-defined level>
Incident window: <start/end with timezone>
Impact: <users, systems, duration, data integrity>
Confidence: High | Medium | Low

## Executive summary
<what happened, impact, recovery, and current residual risk>

## Timeline
| Time | Event | Evidence ID | State | Confidence |
| --- | --- | --- | --- | --- |

## Failure chain and contributing conditions
- Trigger: <Observed/Inferred>
- Mechanism: <Observed/Inferred/Unknown>
- Amplifiers: <conditions and evidence>
- Missing safeguards: <detection, prevention, mitigation, or recovery>

## Response and decisions
| Decision | Information available then | Alternative | Result |
| --- | --- | --- | --- |

## What went well / what hurt
- Went well: <system or team capability>
- Hurt: <system condition, not person>

## Actions
| Action | Risk addressed | Owner | Due | Completion evidence | Status |
| --- | --- | --- | --- | --- | --- |

## Unknowns and dissent
- <unresolved question, evidence needed, or disagreement>

## Data handling
- Sources and retention: <...>
- Redactions: <...>
- Audience and access: <...>
```

## 行动项质量门槛

行动项必须能回答“降低了哪一个风险、如何知道完成、如何知道有效”。优先选择测试、限流、回滚、告警、容量边界、权限、运行手册、演练或架构改进等可验证控制；避免“加强注意”“提高意识”“继续关注”这类无法验收的表述。高风险行动应有独立复核、分阶段发布和失败回滚方案。

## 发布前检查

- 影响、时间线和恢复结论与证据一致；
- 事实、推断、未知和争议已分开，未隐藏反证；
- 无责语言描述系统条件，未公开个人或客户敏感信息；
- 每个行动项有风险、负责人、期限和完成证据；
- 事件编号、查询、附件和链接在目标读者权限内可复核；
- 复盘不声称验证了尚未运行的测试或已完成的行动；
- 未稳定事件、缺少授权或关键事实冲突时返回 `BLOCKED`，不发布草稿。

## Related Skills

- `incident-triage` - 进行事件稳定、分级、恢复和交接
- `changelog-automation` - 从已确认变更生成可追溯的发布记录
- `grounded-vault` - 保存带来源和漂移检查的长期知识
