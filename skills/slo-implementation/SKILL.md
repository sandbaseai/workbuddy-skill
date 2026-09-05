---
name: "slo-implementation"
display_name: "SLO 实施"
display_name_en: "SLO Implementation"
description: "Use when defining or implementing service level indicators, SLOs, error budgets, burn-rate alerts, reliability targets, or SRE policies."
description_zh: "用于定义或实施 SLI、SLO、错误预算、燃烧率告警、可靠性目标或 SRE 策略。"
description_en: "Implement user-centered SLIs and SLOs with valid windows, error budgets, multi-window burn alerts, missing-data handling, ownership, and evidence-backed reliability policy."
category: "observability"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized telemetry, service ownership, versioned SLI/SLO definitions, and a non-production validation target; alert, traffic, and release-policy changes require separate authorization"
---

# SLO Implementation

用用户可感知的 SLI 衡量可靠性，用 SLO 定义目标，用错误预算连接可靠性和交付速度。SLO 不是 SLA，也不是“99.9%”的装饰数字；必须能说明测量对象、分母、窗口、排除项、数据完整性、责任人和行动。

## 使用边界

- 开始前确认用户旅程、服务边界、依赖、SLA/合同、数据区域、owner、业务时段、SLO 窗口、成本和告警接收人。
- 默认只读检查 metrics、logs、traces、告警、部署和历史影响；在隔离/回放数据上验证查询与 burn rate。
- 不擅自修改生产 SLO、采样、告警路由、流量、发布冻结、容量或恢复策略；这些变更需要授权、变更记录和回滚方案。
- 指标 label、请求样本、错误信息和报告不得含 secret、完整 payload、个人标识或无界用户输入。

## SLA / SLO / SLI 与测量契约

SLA 是对外合同，SLO 是内部目标，SLI 是实际测量。每个 SLO 定义：用户/旅程、服务和版本范围、事件分母/分子、成功标准、时间窗口、时区、排除项、数据源、缺失数据处理、owner、review 日期和错误预算策略。

优先从用户结果选择 SLI：可用性是成功请求/有效请求，延迟是低于阈值的用户请求比例，正确性/新鲜度/持久性要使用业务结果或端到端证据。基础设施 CPU、队列和 5xx 可作为诊断信号，不能自动代表用户 SLO。明确健康检查、重试、缓存命中、批处理和部分成功是否进入分母，避免通过改分母“优化”目标。

```yaml
slos:
  - name: checkout_success
    owner: commerce
    target: 0.999
    window: 28d
    sli:
      numerator: "checkout requests with committed order or explicit safe refusal"
      denominator: "valid user checkout attempts"
    evidence: [request_metrics, order_state, trace_correlation]
    missing_data: "unknown; do not count as success"
    review_after: 2026-10-01
```

## 目标与错误预算

错误预算为 `1 - target`，但要结合窗口、流量、业务关键性、依赖、恢复能力和可靠性成本校准。目标应来自用户期望与历史基线，并用分层/地域/版本检查不能被总体平均掩盖的局部故障。记录目标假设和 review 周期，避免永久继承没有证据的 99.9/99.99。

错误预算消耗报告包含已用、剩余、流失速度、受影响用户/旅程、数据延迟和不确定性。预算策略可定义正常发布、风险变更审查、冻结非关键变更、优先修复和恢复验证，但阈值必须绑定明确 owner、例外审批、期限和解除条件，不能自动阻塞所有工程工作。

## Burn rate 与告警

用短/长窗口组合告警以同时降低噪声和漏报：快燃烧用于快速影响，慢燃烧用于持续退化；阈值来自窗口和预算消耗目标，不直接复制示例数字。告警表达式要处理零分母、低流量、指标延迟、NaN、采样和缺失，并将数据源故障与服务故障分开。

告警包含 SLO、窗口、burn rate、预算剩余、用户影响、查询链接、runbook、owner、severity、开始时间和自动恢复条件。告警接收路径、抑制、升级、维护窗口和重复告警应在隔离环境演练；错误预算耗尽不能被静默关闭或改阈值掩盖。

## 数据完整性与实现

Recording rule 和 dashboard 使用版本化定义，固定 label 集和窗口。检查 metrics reset、重复计数、重试/代理上报、时钟、采样、分区、collector 丢失和 cardinality；对 SLI 查询做已知故障回放，确认计算方向与人工样本一致。指标无证据时标为 unknown，不推断“健康”。

把端到端 SLI 与诊断指标关联：错误预算变化触发 trace/log/部署关联，但不要将告警表达式塞入业务代码。报告按用户、版本、地域、依赖和关键旅程分层，注明统计窗口、数据延迟、排除项和不可比条件。

## 验证与治理

测试正常、部分失败、超时、依赖故障、低流量、无数据、采样降低、指标延迟、部署回滚、跨窗口和恢复场景。用历史事件回放验证预算消耗、告警触发/恢复、通知、runbook 和冻结策略；用合成探针补充但不替代真实用户结果。

交付报告记录 SLI/SLO 版本、目标依据、分母/排除项、数据质量、错误预算、burn-rate 结果、告警责任、例外、成本、未覆盖旅程和 review 日期，并区分 observed、derived、unknown。

## 质量门禁

- [ ] SLA/SLO/SLI 层级、用户旅程、分子/分母、窗口、排除项、缺失处理和 owner 已定义。
- [ ] SLI 体现用户结果，基础设施指标仅作为诊断；查询版本、label 和数据源可追溯。
- [ ] 目标/预算有历史、业务、依赖、成本和恢复依据，并有 review/例外/解除条件。
- [ ] 快/慢 burn、多窗口、低流量、零分母、延迟、NaN 和数据源故障均有验证。
- [ ] 告警含影响、owner、runbook、升级、抑制和恢复证据，未用改阈值掩盖消耗。
- [ ] SLO、采样、告警、发布冻结、流量和可靠性政策变更均有授权与回滚方案。
