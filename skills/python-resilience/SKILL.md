---
name: "python-resilience"
display_name: "Python 韧性模式"
display_name_en: "Python Resilience Patterns"
description: "Use when adding Python retry logic, timeouts, backoff, circuit breakers, rate limits, fallbacks, or fault-tolerant service calls."
description_zh: "用于为 Python 服务调用增加重试、超时、退避、熔断、限流、降级或故障容错。"
description_en: "Design bounded Python resilience with transient-failure classification, deadlines, jittered retries, idempotency, circuit breakers, backpressure, safe fallbacks, and recovery tests."
category: "backend"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized dependency contracts, isolated failure-injection tests, and configured telemetry; production retry, timeout, traffic, and fallback changes require separate authorization"
---

# Python Resilience Patterns

让依赖短暂失效时系统能受控地恢复，同时避免重试风暴、请求堆积、重复写入和静默数据错误。韧性设计必须先定义失败语义、总 deadline、幂等性、降级质量和恢复证据。

## 使用边界

- 开始前确认 Python/HTTP client 版本、依赖 SLO、错误契约、超时预算、流量、并发、重试成本、owner 和目标环境。
- 默认只读检查调用代码、错误/延迟指标、依赖契约和日志；在本地/预发布使用合成流量与受控故障注入。
- 不擅自修改生产重试/超时、熔断阈值、限流、队列、缓存、fallback、流量或写入；这些变更需要授权和回滚方案。
- 日志不得记录 token、请求 payload、个人信息或完整下游响应；重试上下文使用错误类别、尝试次数、依赖名和 correlation ID。

## 失败分类与 deadline

只重试有证据的暂时性失败：连接重置、DNS/网络瞬态、读超时、服务端 429/502/503/504（遵循 `Retry-After`）。不要重试参数错误、认证/授权失败、schema/代码 bug、资源不存在或不可幂等的副作用请求。区分依赖失败、调用方取消、超时、熔断打开和本地过载。

每次调用从请求级 deadline 分配连接、读、重试和处理预算；重试必须消耗同一个总预算，不能每次重新获得完整 timeout。为重试次数、总时间、响应体、队列和并发设置硬上限。

```python
import asyncio
import random

RETRYABLE_STATUS = {429, 502, 503, 504}

async def get_with_budget(client, url, *, deadline, max_attempts=3):
    for attempt in range(max_attempts):
        remaining = deadline - monotonic()
        if remaining <= 0:
            raise TimeoutError("deadline exhausted")
        try:
            response = await client.get(url, timeout=remaining)
            if response.status_code not in RETRYABLE_STATUS:
                response.raise_for_status()
                return response
        except (TimeoutError, ConnectionError):
            if attempt + 1 == max_attempts:
                raise
        delay = min(2 ** attempt, 10) + random.uniform(0, 0.5)
        await asyncio.sleep(min(delay, max(0, deadline - monotonic())))
    raise RuntimeError("retry budget exhausted")
```

## 重试、jitter 与幂等

使用指数退避和 jitter，避免大量实例同时重试；尊重服务端 `Retry-After` 与限流契约。记录每次重试的受控原因和最终结果，监控 retry rate、attempt 分布、耗时和放大系数；高重试率是依赖健康问题，不是成功指标。

只对安全读取或带幂等键的操作自动重试。创建、扣款、发送消息和状态变更必须使用服务端幂等键/去重语义，并验证超时后的未知结果；不能因客户端未收到响应就再次产生副作用。重试库装饰器要显式列出异常白名单，禁止捕获 `Exception` 后无限重试。

## 熔断、限流与背压

熔断器区分 closed、open、half-open，按依赖、操作和租户设置隔离，使用错误率/慢调用/连续失败与最小样本窗口，避免低流量误判。half-open 探测必须有并发上限和恢复验证，不能所有请求同时放行。

本地并发信号量、队列上限、令牌桶/漏桶和依赖配额共同形成背压；队列满时快速失败或返回明确的可重试结果，不无限排队。限流 key、错误响应和 retry-after 不得泄露租户或内部资源信息。

## 降级与恢复

按业务关键性设计 fallback：短期缓存、只读快照、有限默认值、排队或明确拒答；降级结果必须标记 stale/partial，不把默认值当作真实成功。关键路径宁可 fail closed，也不能返回未经验证的权限、价格或安全判断。

恢复时验证依赖健康、数据新鲜度、积压、重复写入、熔断状态和下游负载，再逐步放量；不要只因一次探测成功就关闭所有保护。所有 fallback、丢弃、补偿和人工介入都应可观测。

## 测试与交付

隔离测试覆盖连接失败、DNS/网络、读写超时、429/5xx、非重试 4xx、认证失败、取消、重复响应、deadline 耗尽、熔断打开/恢复、队列满、部分依赖和 telemetry 故障。验证调用次数、总耗时、幂等键、背压、错误分类和最终数据质量；使用固定时钟/随机源避免 flaky 测试。

报告记录依赖契约、失败矩阵、timeout/retry/circuit 参数、基线、放大与成本、fallback 质量、故障注入结果、告警、回滚和未覆盖场景，并区分 observed、derived、unknown。

## 质量门禁

- [ ] 暂时性/永久性/未知失败分类和重试白名单有依据，deadline、次数、队列和响应大小有硬上限。
- [ ] 退避、jitter、Retry-After、取消和总超时预算已验证，不会造成重试风暴。
- [ ] 所有副作用操作具备幂等键、去重或明确禁止自动重试的边界。
- [ ] 熔断、限流、并发、背压、fallback 和恢复过程可观测且按关键路径隔离。
- [ ] 故障注入覆盖依赖、网络、过载、取消、部分失败和 telemetry 故障，并检查数据质量。
- [ ] 生产韧性参数、流量、缓存、队列、fallback 和写入变更均有授权与回滚方案。
