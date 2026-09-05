---
name: "grafana-dashboards"
display_name: "Grafana 仪表盘"
display_name_en: "Grafana Dashboards"
description: "Use when designing Grafana dashboards for Prometheus metrics, service health, infrastructure, SLOs, or business KPIs."
description_zh: "用于设计 Grafana 仪表盘，呈现 Prometheus 指标、服务健康、基础设施、SLO 或业务 KPI。"
description_en: "Design production-ready Grafana dashboards with information hierarchy, RED/USE views, variables, thresholds, alerts, provisioning, and evidence-backed validation."
category: "observability"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized Grafana/Prometheus metadata and isolated dashboard-as-code validation; production dashboard, datasource, alert, provisioning, or notification changes require separate authorization"
---

# Grafana Dashboards

设计能帮助值班人员快速判断状态、趋势和行动的 Grafana 仪表盘。先明确受众、决策、数据源、时间范围和指标语义，再组织面板；仪表盘是观测入口，不应替代 runbook、告警路由或未经授权的生产操作。

## 使用边界

- 开始前确认 Grafana/数据源版本、目标受众、服务与环境范围、时区、刷新频率、数据保留、owner、SLO 和 runbook。
- 默认只读检查现有仪表盘、查询、变量、权限、告警和 provisioning；只在隔离环境导入或验证 JSON/YAML，不向未授权数据源查询或写入。
- 不擅自修改生产仪表盘、数据源、告警规则、通知联系人、文件 provisioning、Terraform state 或删除面板；变更需要授权、评审、备份和回滚方案。
- 查询、面板标题、变量值、标签和截图不得泄露 secret、token、完整请求、个人标识或租户隔离信息。

## 信息层级与信号

按从“是否需要行动”到“如何定位”的顺序布局：顶部放关键状态和 SLO/错误预算，随后是趋势，再放表格、分布和诊断细节。服务面板优先使用 RED：请求速率（Rate）、错误率（Errors）、延迟分位数（Duration）；资源面板使用 USE：利用率（Utilization）、饱和度（Saturation）、错误（Errors）。每个面板说明单位、聚合、时间窗口、数据缺失含义和行动链接。

API 示例查询（指标名必须与实际契约一致）：

```promql
sum(rate(http_requests_total{environment=~"$environment",service=~"$service"}[5m])) by (service)
sum(rate(http_requests_total{status_class="5xx",service=~"$service"}[5m]))
  / clamp_min(sum(rate(http_requests_total{service=~"$service"}[5m])), 1)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service=~"$service"}[5m])) by (le, service))
```

不要把 `user_id`、request ID、原始 URL、任意错误文本等高基数或敏感值作为 dashboard 变量或 series 维度。零流量、缺失数据、counter reset、NaN 和低采样量必须有明确的显示语义，不能用“绿色”掩盖未知状态。

## 面板、变量与阈值

- Stat 适合单值状态，但同时展示时间范围、计算方式和 `lastNotNull` 等 reduce 语义；不要把单点值误当趋势。
- Time series 展示速率、错误率和 P50/P95/P99；统一单位、legend、颜色、排序和对数/线性轴选择。
- Table 适合实例、服务、版本和健康状态；Heatmap 适合延迟或大小分布，确认 Prometheus bucket 与 Grafana 数据格式匹配。
- 变量只提供有限 allowlist；查询变量要绑定授权的数据源和范围，依赖变量按 namespace/environment 等安全顺序刷新，多选时使用正确的正则匹配。
- 阈值来自 SLO、容量基线或业务约定，并记录单位、窗口和 owner；不要复制社区阈值而不说明依据。

## 告警与 SLO

仪表盘告警应与集中式告警规则、通知和 runbook 一致。检查告警表达式、`for`、无数据/执行错误状态、抑制、维护窗口、severity、owner 和升级链路；验证触发、恢复、延迟、重复通知和通知失败。SLO 面板至少区分目标、当前 SLI、错误预算余额和 burn rate，并链接到用户影响和处置步骤。

## Dashboard as Code 与 provisioning

将 JSON、YAML、Terraform 或 Ansible 文件纳入版本控制，固定 Grafana/API schema、数据源 UID、文件路径、folder、权限、刷新策略和导入覆盖行为。提交前执行 JSON/schema、PromQL、变量展开、权限边界和快照渲染检查；预览确认没有空面板、遮挡、截断 legend、错误单位或跨环境数据混用。部署采用评审、canary、版本化导入和可验证回滚，禁止把凭据写入 dashboard 文件。

## 验证与交付

用代表性的时间范围和低流量、无数据、目标下线、指标 schema 变化、数据源超时、权限拒绝、告警触发/恢复等场景验证。报告记录目标、数据源 UID、查询与变量、面板语义、阈值依据、截图/JSON hash、权限、数据缺口、告警证据、owner、回滚点，并区分 observed、derived、unknown。

## 质量门禁

- [ ] 受众、决策、环境、时区、刷新、保留、owner 和 runbook 已定义。
- [ ] RED/USE/SLO 面板的指标契约、单位、聚合、窗口、变量和缺失数据语义已验证。
- [ ] 变量有 allowlist 和权限边界；查询不会泄露 secret、个人标识或无界高基数。
- [ ] 阈值、告警状态、通知链路、无数据处理和恢复行为有依据并已测试。
- [ ] Dashboard as Code/provisioning 通过 schema、查询、渲染、权限和回滚检查。
- [ ] 生产仪表盘、数据源、告警、通知和 provisioning 变更均有授权与回滚方案。

## Related Skills

- `prometheus-configuration` - 设计指标、抓取、规则和 Prometheus 自监控
- `slo-implementation` - 定义 SLI、SLO、错误预算和 burn-rate 告警
