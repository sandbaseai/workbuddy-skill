---
name: "python-observability"
display_name: "Python 可观测性"
display_name_en: "Python Observability"
description: "Use when instrumenting Python services with structured logs, metrics, traces, correlation IDs, dashboards, or production diagnostics."
description_zh: "用于为 Python 服务增加结构化日志、指标、追踪、关联 ID、仪表盘或生产诊断能力。"
description_en: "Instrument Python services with privacy-safe structured logs, golden-signal metrics, trace correlation, bounded cardinality, alerting, and tested diagnostic evidence."
category: "observability"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized application telemetry, a non-production validation target, and configured log/metrics/trace backends; instrumentation, retention, and alert changes require separate authorization"
---

# Python Observability

让服务在出问题时回答“发生了什么、影响在哪里、证据有多可靠”，同时控制隐私、成本和噪声。可观测性代码应独立于业务逻辑、可测试、可降级，不能因为 telemetry 失败而阻断业务。

## 使用边界

- 开始前确认 Python/SDK 版本、服务边界、环境、数据分类、日志/指标/trace 后端、保留周期、owner、SLO 和访问权限。
- 默认只读检查现有日志、指标、trace、配置和错误；先在本地/预发布用合成或脱敏流量验证。
- 不擅自修改生产采样、路由、告警、保留策略、网络或服务重启；这些变更需要授权、变更记录和回滚方案。
- 禁止记录 token、密码、cookie、完整请求/响应、原始 prompt、支付数据、邮箱/手机号和稳定用户标识。关联用户时使用短期、不可逆、低基数的受控 ID。

## 观测契约

统一 `service.name`、环境、版本、区域、operation 和 correlation/trace ID。日志使用 JSON 和稳定字段，指标 label 只使用有限枚举（method、route template、status class、dependency），绝不使用 user ID、request ID、URL 原文或任意输入作为 label。

四大黄金信号分别是 latency、traffic、errors、saturation；每个服务边界说明单位、窗口、聚合、采样和告警阈值。日志、metrics 和 traces 各自回答不同问题：不要用日志计数替代可靠指标，也不要把一条 trace 当作全局结论。

```python
import logging
import structlog
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")
logger = structlog.get_logger()

def configure_logging(level: str = "INFO") -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level)),
    )

def log_request_done(route: str, status_class: str, duration_ms: int) -> None:
    # Route is a template; no raw path, payload, or identity is logged.
    logger.info("request.completed", route=route, status_class=status_class,
                duration_ms=duration_ms, correlation_id=correlation_id.get())
```

## 日志级别与脱敏

`DEBUG` 用于短期开发诊断，`INFO` 记录正常生命周期，`WARNING` 记录已处理异常，`ERROR` 只记录需要调查的失败。错误事件保留异常类型、稳定错误码、边界和 correlation ID；原始异常消息需经过 allowlist 脱敏，不能把下游响应或输入直接拼入日志。

在 logger/handler 出口做 schema 校验、字段 allowlist、递归脱敏、长度上限和采样；不要依赖调用方“记得不打印秘密”。结构化日志解析失败、后端不可用或队列满时，采用限量本地降级并计数，不能无限重试或阻塞请求。

## 关联 ID 与追踪

在 ingress 生成或验证 correlation ID，响应和下游请求只传播经过验证的值。跨服务优先使用 W3C Trace Context/OpenTelemetry；异步消息记录 producer/consumer 关系。Correlation ID 是诊断键，不是认证凭据，不应放入高基数 metrics label 或可公开的业务字段。

检查 contextvars 在 async task、线程池、重试和后台任务中的生命周期，避免跨请求泄露；请求结束清理绑定上下文。span attributes 使用有限枚举和 route template，敏感 payload 只记录摘要或完全省略。

## 指标、告警与仪表盘

按服务/route template/dependency 建立请求量、错误率、延迟分位数、饱和度、队列长度、连接池、缓存命中和外部调用超时指标。为每个告警写出症状、阈值、窗口、runbook、抑制/恢复条件和 owner；避免每个异常都创建告警造成疲劳。

采样、聚合、retention 和 label cardinality 以成本预算验证。对长尾延迟、突发错误、静默服务、telemetry 丢弃和后端延迟做演练，并区分观测系统故障与业务故障。

## 验证与交付

测试日志字段、脱敏规则、级别、异常路径、关联传播、context 清理、metrics label 上限、trace parent/child 和 exporter 降级。用固定合成请求比较 instrumentation 前后 CPU、内存、网络、延迟和日志量；不要用一次本地运行推断生产开销。

交付报告记录 SDK/collector/agent 版本、契约、采样与保留、四大信号、告警、脱敏测试、成本/性能基线、已知丢失、查询时间范围和回滚方式，并区分 observed、derived、unknown。

## 质量门禁

- [ ] 日志、metrics、trace 字段和 route/operation 命名符合版本化观测契约。
- [ ] 无 secret、原始 payload、个人标识和无界输入进入日志、span 或 metrics label。
- [ ] correlation/trace context 在 async、线程、重试、下游和消息边界正确传播并清理。
- [ ] latency、traffic、errors、saturation 及观测系统自身健康均可查询和告警。
- [ ] 脱敏、字段校验、降级、采样、cardinality、性能和成本均有测试/基线。
- [ ] 生产埋点、采样、路由、告警、保留和网络改动均有授权与回滚方案。
