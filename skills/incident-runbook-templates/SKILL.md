---
name: "incident-runbook-templates"
display_name: "事件响应运行手册"
display_name_en: "Incident Runbook Templates"
description: "Use when creating or reviewing an incident runbook with detection, triage, authorized mitigation, escalation, verification, rollback, and communication boundaries."
description_zh: "用于创建或审阅事件响应运行手册，覆盖检测、分诊、获授权缓解、升级、验证、回滚和沟通边界。"
description_en: "Turn service failure modes into bounded, evidence-driven runbooks with explicit preconditions, safe read-only checks, approval gates, stop conditions, rollback, and freshness ownership."
category: "operations"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized service documentation, observability references, ownership data, and a controlled runbook repository; production actions require independent approval"
---

# 事件响应运行手册

运行手册应帮助人在压力下稳定服务，而不是把未经审查的命令复制到生产环境。每一步都要说明目的、前置条件、预期证据、失败处理、授权要求、停止条件和回滚路径；无法安全验证时宁可升级，也不猜测或扩大影响。

## 安全前置门禁

编写或执行前确认服务、环境、事件范围、责任角色、数据处理规则、最后验证时间和审批边界：

- 默认先做只读、低风险检查；任何写入、重启、回滚、扩容、流量切换、数据库变更、通知或凭据动作都需要独立授权；
- 命令、路径、集群、租户、区域和账号必须由运行时上下文明确绑定，禁止使用模糊的 `prod`、通配符或复制粘贴的默认目标；
- 不在手册中保存密码、token、私钥、客户数据或个人信息；使用安全引用、角色名和脱敏示例；
- 对破坏性动作提供 dry-run/预览、影响上限、审批人、双人确认、回滚和停止条件；没有回滚或证据不足时标记 `BLOCKED`；
- 事件仍在进行时，手册只是受授权响应的辅助材料，不替代事件指挥、变更管理、取证保全或安全升级。

## 编写工作流

1. **定义故障模式**：描述用户影响、触发信号、可能范围、严重度和不适用场景；不要把一个症状写成唯一根因。
2. **列出责任与升级**：服务 owner、事件指挥、沟通角色、依赖 owner、备用路径和升级时限；只放可访问的角色/队列引用。
3. **写快速检查表**：按“确认影响 → 建立责任 → 只读观察 → 假设分支 → 获批缓解 → 验证 → 交接/复盘”排列，允许每项记录结果。
4. **为每一步补元数据**：目的、前置条件、精确目标、权限、命令/界面引用、预期结果、超时、失败处理和证据保存位置。
5. **隔离动作等级**：把观察、可逆缓解、不可逆变更和外部沟通分开；动作前显示授权和影响提示。
6. **加入分支与停止条件**：结果不符合预期、影响扩大、数据完整性不确定、权限不匹配或证据冲突时停止并升级。
7. **定义恢复验证**：检查用户旅程、错误率、延迟、容量、数据一致性和告警恢复；不要只看单个进程变绿。
8. **加入回滚与退出**：回滚触发条件、最小安全步骤、负责人、观察窗口和无法回滚时的升级路径。
9. **定期验证新鲜度**：每次事件、重大变更、依赖升级或环境变化后复核；标记 owner、最后验证时间、下次复查和过期状态。

## 运行手册模板

```markdown
# <Service> — <Failure mode>

Status: Draft | Verified | Expired | Blocked
Owner: <team/role>
Last verified: <timestamp and timezone>
Next review: <date or trigger>
Scope: <environment, region, tenant boundary>

## Impact and detection
- User impact: <observable effect and estimated scope>
- Trigger signals: <alert/metric/log reference>
- Severity policy: <link or role-owned rule>
- Not this runbook when: <similar symptoms with different scope>

## Roles and escalation
| Role | Responsibility | Route | Escalate after |
| --- | --- | --- | --- |

## Quick checklist
- [ ] Confirm scope and establish incident owner
- [ ] Capture evidence before changing state
- [ ] Run approved read-only checks
- [ ] Select a bounded, reversible mitigation
- [ ] Verify user impact and dependencies
- [ ] Document result, next check, and rollback decision

## Procedure
### Step N — <purpose>
- Preconditions: <access, target binding, health and approval>
- Action level: Observe | Reversible | Irreversible | Communication
- Exact target: <explicit environment/region/resource; no wildcard>
- Command or UI reference: <controlled reference, not embedded secrets>
- Expected evidence: <output, threshold, time window>
- If it fails: <safe fallback or escalation>
- Stop when: <condition>
- Record: <evidence ID and redacted location>

## Verification and rollback
- Recovery signals: <user journey, SLO, data, dependency checks>
- Monitoring window: <duration and owner>
- Rollback trigger: <threshold or contradiction>
- Rollback plan: <authorized, bounded, reversible steps>

## Communication
- Audience: <role/channel reference>
- Update cadence: <interval>
- Template: status, impact, action, next update, residual risk

## Unknowns and safety notes
- <missing evidence, incompatible version, access gap, or data concern>
```

## 动作安全要求

对每个非只读动作使用以下确认句式，并让执行者在动作前填入实际值：

> I have authorization `<approval reference>` for target `<exact resource>` in environment `<exact environment>`. The expected impact is `<bounded impact>`, the stop condition is `<condition>`, and rollback is `<reference>`. I will record evidence `<location>`.

缺少审批引用、精确目标、影响上限、停止条件、回滚或证据位置时，结果为 `BLOCKED`。运行手册本身不授予权限，也不应自动调用外部系统执行动作。

## 质量门槛

- 值班人员能在不依赖口头背景的情况下理解影响、下一步和升级路径；
- 每个步骤能通过预期证据判断成功或失败，失败不会静默继续；
- 破坏性动作有 dry-run、双人/独立审批、影响边界、回滚和验证；
- 手册注明版本、目标范围、最后验证时间和过期责任；
- 示例没有秘密、真实客户数据、模糊生产目标或未经授权的操作细节；
- 未运行的命令、未验证的回滚和未观察到的恢复不得被写成已完成；
- 目标、权限、证据或数据完整性不确定时返回 `BLOCKED`，而不是继续猜测。

## Related Skills

- `incident-triage` - 对事件分级、稳定、恢复和升级
- `on-call-handoff-patterns` - 在责任切换时传递活动事件和风险
- `postmortem-writing` - 将已结束事件整理为证据驱动的无责复盘
