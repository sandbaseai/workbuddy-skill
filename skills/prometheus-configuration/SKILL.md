---
name: "prometheus-configuration"
display_name: "Prometheus 配置"
display_name_en: "Prometheus Configuration"
description: "Use when configuring Prometheus scraping, metric schemas, relabeling, recording rules, alerting, service discovery, retention, or monitoring HA."
description_zh: "用于配置 Prometheus 抓取、指标 schema、relabel、记录规则、告警、服务发现、保留或高可用监控。"
description_en: "Configure Prometheus with consistent metric contracts, bounded cardinality, safe scraping, recording/alert rules, HA and retention planning, self-monitoring, and validated rollout."
category: "observability"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized metrics endpoints, Prometheus-compatible targets, isolated config validation, and a retention/storage policy; production scrape, query, alert, and retention changes require separate authorization"
---

# Prometheus Configuration

让指标采集、查询、记录规则和告警成为可验证的可靠性基础。配置 Prometheus 前先定义指标语义、目标范围、访问权限、数据保留、高可用、成本和 Prometheus 自身的健康门禁。

## 使用边界

- 开始前确认 Prometheus/agent 版本、target、网络/TLS、认证、数据区域、抓取频率、存储、保留、owner、SLO 和告警接收人。
- 默认只读审查配置、targets、规则、series、存储和告警；在隔离实例验证，不向未授权 endpoint 发送查询或探测。
- 不擅自修改生产 scrape、relabel、remote write、保留、告警路由、服务发现或删除时序数据；变更需要授权、备份/回滚和容量证据。
- metric labels、target metadata 和 exporter 响应不得含 secret、完整请求、个人标识或无界输入。

## 指标契约与 cardinality

命名使用稳定前缀、对象、动作和单位，例如 `http_request_duration_seconds`、`queue_depth`；统一 counter/gauge/histogram/summary 语义、帮助文本、bucket 和 label。label 只允许有限枚举（route template、method、status class、region），禁止 user ID、request ID、原始 URL、trace ID 和任意错误消息。

每个自定义指标记录 owner、来源、单位、采样/聚合、保留、告警消费者和废弃计划。上线前估算 active series、抓取字节、样本速率、规则计算、远程写入和存储成本；通过 cardinality 预算和自监控告警防止租户/版本/异常字符串爆炸。

## Scrape、发现与 relabel

按 target 类型设置合理 interval、timeout（必须小于 interval）、TLS/认证、honor labels、协议和失败处理；批量 target 用服务发现，避免静态清单漂移。relabel 只做可解释的 allow/drop/rename，防止把 secret、内部路径或高基数字段带入 labels；先在隔离配置上检查最终 target 与 label 集。

```yaml
scrape_configs:
  - job_name: api
    scrape_interval: 30s
    scrape_timeout: 10s
    metrics_path: /metrics
    static_configs:
      - targets: ["api.example.invalid:8080"]
        labels:
          environment: staging
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: "debug_.*"
        action: drop
```

生产 target 不应暴露在公开网络；使用 TLS、最小读取权限、网络 allowlist 和 collector/agent 隔离。检查 `up`、scrape duration、sample limit、parse error、target churn、丢样和 exporter 自身依赖，区分 endpoint 故障与 Prometheus 故障。

## Recording 与 alerting rules

高成本、重复使用或跨窗口查询用 recording rules，命名表达聚合和单位；规则 evaluation interval、依赖顺序、标签继承和重启行为要验证。告警规则处理零分母、低流量、缺失、NaN、counter reset 和数据延迟，设置 `for`、severity、owner、runbook、影响和恢复条件。

```yaml
groups:
  - name: api-sli
    interval: 30s
    rules:
      - record: api:http_error_ratio:rate5m
        expr: |
          sum(rate(http_requests_total{status_class="5xx"}[5m]))
          /
          clamp_min(sum(rate(http_requests_total[5m])), 1)
      - alert: ApiErrorBudgetBurn
        expr: api:http_error_ratio:rate5m > 0.01
        for: 10m
        labels:
          severity: page
          owner: api-team
        annotations:
          summary: "API error ratio is consuming the reliability budget"
          runbook_url: "https://runbooks.example.invalid/api-errors"
```

规则表达式通过 `promtool check rules`/`test rules` 或等价隔离验证，并用历史/合成时序回放触发、恢复和误报场景。告警路由、抑制、维护窗口和升级链路单独测试；Prometheus 能计算不等于通知一定送达。

## 存储、HA 与远程写入

保留窗口由查询需求、容量、压缩、恢复时间和隐私/删除政策决定；估算 samples/day、retention、WAL、磁盘水位和 compaction。高可用实例避免同一数据重复计数，使用 external labels、去重和一致的规则版本；remote write、federation、Thanos/Cortex 等扩展需验证背压、延迟、成本、权限和故障降级。

监控 Prometheus 自身：target 可用性、规则评估、TSDB/WAL、磁盘、内存、查询耗时、remote write 队列、scrape 样本/标签限制、配置 reload 和 alertmanager 投递。观测系统异常时明确数据缺口，不把未知当作服务健康。

## 验证与交付

在隔离实例验证 YAML/schema、target/TLS、最终 labels、抓取超时、规则、告警、容量、查询权限和 reload；对 target 下线、指标 schema 变化、网络分区、存储满、规则错误、远程写入故障和时间序列删除做演练。发布采用版本化配置、canary、回滚和变更 hash。

报告记录指标契约、targets、interval/timeout、relabel、series/成本基线、规则/告警证据、HA/保留、权限、数据缺口、runbook 和回滚，并区分 observed、derived、unknown。

## 质量门禁

- [ ] 指标类型、单位、命名、label allowlist、owner、生命周期和 cardinality 预算已定义。
- [ ] target、TLS/认证、发现、interval/timeout、relabel、sample limit 和失败语义已验证。
- [ ] recording/alert rules 处理零分母、缺失、低流量、reset、NaN 和数据延迟，且有回放测试。
- [ ] 存储、保留、WAL、容量、HA、remote write/federation、删除和成本有依据。
- [ ] Prometheus、target、规则、通知、权限和观测系统自身均可监控并有 runbook。
- [ ] 生产抓取、规则、路由、保留、远程写入和数据删除变更均有授权与回滚方案。
