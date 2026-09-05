---
name: "distributed-tracing"
display_name: "分布式追踪"
display_name_en: "Distributed Tracing"
description: "Use when instrumenting or diagnosing distributed requests, service dependencies, latency, retries, failures, or trace-to-log correlation."
description_zh: "用于埋点或诊断跨服务请求、依赖关系、延迟、重试、故障和 trace 与日志关联。"
description_en: "Implement privacy-safe OpenTelemetry tracing with context propagation, sampling, semantic spans, trace-log correlation, bottleneck analysis, and bounded overhead."
category: "observability"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized telemetry access, an OpenTelemetry-compatible collector/backend, and a non-production validation target; instrumentation changes and telemetry retention require separate authorization"
---

# Distributed Tracing

用 trace 重建一次请求跨服务、队列、数据库和外部 API 的路径，回答“哪里慢、哪里失败、哪次变更影响了它”。追踪是抽样的诊断证据，不是完整审计日志；必须同时管理上下文、隐私、采样、保留、成本和证据局限。

## 使用边界

- 开始前确认服务拓扑、协议、OpenTelemetry/SDK 版本、collector、采样策略、保留周期、数据区域和访问权限。
- 默认只读检查 instrumentation、trace、span、日志、指标和部署变更；先在本地/预发布或脱敏流量验证。
- 不擅自修改生产采样率、collector 路由、保留策略、网络策略或重启服务；这些变更需要明确授权与回滚计划。
- span attributes、events、baggage 和日志不得写入 token、密码、完整请求/响应、原始 query、邮件、手机号或稳定的用户标识。需要关联时使用短期、不可逆、受控的 correlation ID。

## 追踪契约

统一服务名、环境、版本、区域和 operation 名称；span 名称描述动作而不是动态值，例如 `GET /orders/{id}`，不要把订单号放入名称。每个跨进程边界传播 W3C Trace Context；队列要区分 producer/consumer，异步任务保留 parent/links 的语义。

为关键 span 规定必需字段、允许枚举、敏感字段清单、错误语义、超时和采样规则。HTTP、数据库、消息和 RPC 优先使用 OpenTelemetry 语义约定，避免同一事实在不同服务使用不同名称。

```python
from opentelemetry import trace

tracer = trace.get_tracer("orders-service")

def process_order(order_ref: str):
    # Keep only a non-sensitive operation reference; never attach raw payloads.
    with tracer.start_as_current_span("process order") as span:
        span.set_attribute("app.operation", "order.process")
        try:
            result = reserve_inventory(order_ref)
            span.add_event("inventory.reserved", {"item_count": result.count})
            return result
        except TimeoutError as exc:
            span.record_exception(exc)
            span.set_status(Status(StatusCode.ERROR, "dependency timeout"))
            raise
```

## 采样与成本

头部采样适合控制基础成本，尾部采样可保留错误、慢请求和特定业务路径，但要评估 collector 内存、决策延迟和丢失风险。生产采样率应由流量、SLO、诊断目标、存储成本和隐私要求共同决定；“1–10%”只是起点，不能当作普遍正确值。

使用 batch span processor、队列上限、export timeout 和 backpressure；telemetry 发送失败不能阻断业务请求。测量 instrumentation 的 CPU、内存、网络和 p95/p99 延迟开销，设定可告警阈值，并为高基数 attributes 设置白名单。

## 传播、日志与指标关联

检查 HTTP/RPC headers、消息 metadata、线程/异步 context、重试和跨进程边界。不要把来自请求的 baggage 当作可信授权信息，也不要无条件把 baggage 复制到下游；只传播经过验证、最小化和有保留策略的字段。

日志使用 trace ID/span ID 做关联，但日志内容仍需独立脱敏和访问控制。用 metrics 发现总体 SLO 变化，用 traces 解释单次路径，用 logs 补充离散错误；不要用单条 trace 推断全体用户或全部请求的可靠性。

## 故障与性能诊断

先确认 trace 完整性：采样、时钟偏差、collector 丢弃、上下文断裂、重试和 fan-out 是否造成误读。沿 critical path 对比同类成功/失败和变更前后 trace，区分应用耗时、队列等待、连接池、DNS/TLS、数据库、下游限流和重试放大。

没有 trace 时按层排查 exporter endpoint、TLS/权限、collector pipeline、采样和 SDK 配置；不要通过提高采样率无限期解决丢失。高开销时先减少 payload 和高基数属性、启用批处理与限流，再验证采样变化的诊断损失。

## 验证与交付

在隔离环境生成带固定 correlation 的成功、超时、异常、重试、异步和取消流量，验证每个边界的 parent/child/link、span 状态、错误事件、日志关联和敏感字段清理。对 trace 缺失、部分采样、collector 不可用和服务重启测试降级行为。

交付报告记录代码/SDK/collector 版本、拓扑、采样与保留策略、完整性缺口、基线与开销、查询时间范围、代表性 trace、日志/指标证据、隐私审查、成本和回滚步骤；把 observed、derived、unknown 分开。

## 质量门禁

- [ ] 服务、协议、operation、版本和环境命名符合统一追踪契约。
- [ ] HTTP/RPC/队列/异步边界传播 context，重试、取消、fan-out 和跨线程语义已验证。
- [ ] 采样、尾部决策、批处理、队列上限、超时、丢弃和成本有明确依据。
- [ ] span/log/metric 关联可用，且无 secret、原始 payload、用户标识或高基数泄露。
- [ ] 成功、失败、慢请求、重试、collector 故障和部分采样均有隔离测试。
- [ ] 生产 instrumentation、采样、路由、保留和网络变更均有授权和回滚方案。
