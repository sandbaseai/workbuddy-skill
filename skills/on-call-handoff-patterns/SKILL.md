---
name: "on-call-handoff-patterns"
display_name: "值班交接模式"
display_name_en: "On-Call Handoff Patterns"
description: "Use when transferring on-call responsibility, an active incident, or an investigation so the incoming responder receives verified context, current risk, escalation paths, and explicit next actions."
description_zh: "用于交接值班责任、进行中的事件或排查工作，确保接班人获得已核验的上下文、当前风险、升级路径和明确下一步。"
description_en: "Create concise, evidence-linked handoffs with active-state summaries, watch items, decision history, ownership, and acceptance checks without silently changing alerts or production state."
category: "operations"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized incident records, service ownership data, alert references, and a controlled handoff destination; production changes and alert tests require separate authorization"
---

# 值班交接模式

值班交接是风险转移，不是把链接堆在一起。交接文档应让接班人在有限时间内回答：什么正在发生、影响谁、当前假设是什么、下一次检查何时进行、谁有决策权，以及哪些动作绝不能未经授权执行。

## 交接前门禁

确认交接双方、责任窗口、时区、事件/服务范围、文档访问权限和事件状态。默认只读整理：

- 只引用已授权的事件记录、告警、日志、指标、变更和工单；每个高影响判断注明时间、来源和置信度；
- 不在交接过程中重启服务、修改配置、触发告警、发送通知、轮换凭据或执行生产命令；
- 不把 token、密码、客户数据、个人信息或内部秘密写入交接文档；使用安全引用或脱敏标识；
- 事件仍在升级、影响范围不明或接班人未确认时，状态为 `BLOCKED`，不能宣称交接完成；
- “无事项”也要明确写成 `None confirmed`，不能用空白字段掩盖未知。

## 交接工作流

1. **锁定窗口**：写明交出时间、接班时间、重叠时间、时区和责任切换的明确时刻。
2. **汇总当前状态**：服务、用户影响、严重度、事件状态、最近一次已验证指标和恢复目标。
3. **列出活动事项**：每个事件/调查包含现象、证据、当前假设、已尝试动作、结果、风险、下一检查点和负责人。
4. **记录决策上下文**：保留已做决定、当时可见信息、未采用方案、审批边界和回滚条件；不要只写“按惯例处理”。
5. **标明监控与阈值**：引用已有告警和 Dashboard，说明哪些信号要观察、阈值意味着什么、误报/漏报限制是什么。
6. **确认升级路径**：列出服务 owner、事件指挥、技术专家、业务联系人和备用路径；不要在文档中暴露私人联系方式或秘密。
7. **列出近期变更**：部署、配置、依赖、维护和外部事件，注明已验证影响或仍待核对的关联。
8. **完成接班验收**：接班人复述当前风险、下一动作、停止条件和升级路径；双方记录 `Accepted`、`Accepted with gaps` 或 `Blocked`。
9. **关闭旧责任**：交出人确认未遗留私下上下文，保留短暂可联系窗口（若已授权），并记录交接后的首个复查时间。

## 交接模板

```markdown
# On-Call Handoff — <service/window>

Handoff status: Draft | Accepted | Accepted with gaps | Blocked
Outgoing: <role, not unnecessary personal data>
Incoming: <role>
Responsibility switch: <timestamp and timezone>
Overlap: <window>

## Current status
- Overall: <Healthy | Degraded | Incident | Investigating | Unknown>
- User/system impact: <scope and duration>
- Last verified evidence: <time, source, result>
- Residual risk: <...>

## Active incidents and investigations
| ID | State | Impact | Evidence | Hypothesis | Next check | Owner |
| --- | --- | --- | --- | --- | --- | --- |

## Recent changes and watch list
- Change: <what, when, evidence, rollback condition>
- Signal: <metric/alert/reference and threshold>

## Decisions and boundaries
- Decisions already made: <...>
- Do not do without approval: <production or external actions>
- Escalate when: <condition, role/path, deadline>

## Gaps and questions
- Unknown: <evidence needed and safe source>
- Disputed: <views and owner for resolution>

## Acceptance
- Incoming summary/check: <result>
- Access verified: <yes/no; no secrets>
- Next review: <time>
- Handoff result: <Accepted | Accepted with gaps | Blocked>
```

## 交接质量检查

- 每个字段有内容或明确的 `None confirmed`；
- 当前影响、事件状态、证据时间和责任切换时间一致；
- 接班人能在不依赖口头隐藏信息的情况下找到活动事项、下一检查和升级路径；
- 下一步动作有负责人、截止/检查时间、停止条件和所需授权；
- 未知、争议和假设没有被写成事实；
- 文档没有凭据、客户数据、无关个人信息或不可审计的私聊结论；
- 未经授权的生产、通知、告警或凭据动作没有被自动执行；
- 事件仍未稳定、关键访问缺失或接班未确认时返回 `BLOCKED`。

## Related Skills

- `incident-triage` - 进行事件稳定、分级、恢复和升级
- `postmortem-writing` - 将已结束事件整理为无责复盘和可验证行动项
- `verify-agent-action` - 在高影响动作前核验目标、授权和证据
