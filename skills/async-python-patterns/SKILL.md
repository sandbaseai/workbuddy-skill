---
name: "async-python-patterns"
display_name: "Python 异步模式"
display_name_en: "Async Python Patterns"
description: "Use when building or reviewing Python asyncio services, concurrent I/O, async APIs, background tasks, cancellation, or event-loop performance."
description_zh: "用于构建或审查 Python asyncio 服务、并发 I/O、异步 API、后台任务、取消处理或事件循环性能。"
description_en: "Design correct async Python with bounded concurrency, non-blocking I/O, structured cancellation, deadlines, resource cleanup, backpressure, and deterministic tests."
category: "backend"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized async runtime, dependency contracts, isolated load/failure tests, and configured telemetry; production concurrency, timeout, and traffic changes require separate authorization"
---

# Async Python Patterns

用 `asyncio` 管理 I/O 并发，同时保持事件循环可响应、资源可回收、取消可传播、并发有上限。异步不是越多越好：CPU 密集任务、低并发脚本或阻塞 SDK 应选择同步、线程池或进程池，并用基线证明收益。

## 使用边界

- 开始前确认 Python/框架/依赖版本、调用链、并发量、deadline、资源配额、owner、SLO 和目标环境。
- 默认只读检查 coroutine、task、连接池、队列、超时、trace 和错误；在本地/预发布使用合成负载与受控故障。
- 不擅自修改生产并发、超时、线程/进程池、连接池、限流、流量或重启服务；这些变更需要授权和回滚方案。
- 日志、task 参数、异常和 trace 不得包含 token、完整 payload、个人信息或原始响应；使用脱敏摘要和受控 correlation ID。

## 同步/异步边界

多网络/数据库调用适合 asyncio；CPU 密集工作使用 `asyncio.to_thread`（阻塞但可释放事件循环）或进程池，并限制 worker。一个调用路径应有清晰的 sync/async 边界，不能在事件循环中执行 `time.sleep`、同步 HTTP/数据库客户端、重型序列化或无界文件操作。

每个外部调用都要有连接、读和总 deadline；每个 task 都说明 owner、结果、异常、取消和资源清理语义。优先使用 `async with`、`async for` 和结构化并发（如 `TaskGroup`，按 Python 版本确认行为）。

```python
import asyncio

async def fetch_bounded(items, client, *, limit=20):
    semaphore = asyncio.Semaphore(limit)

    async def one(item):
        async with semaphore:
            # The caller supplies a request deadline; no unbounded await.
            return await client.fetch(item, timeout=5.0)

    # Keep the result order and make the concurrency bound explicit.
    return await asyncio.gather(*(one(item) for item in items))
```

## 并发、背压与结果

`gather`、task 集合、队列和连接池都必须有上限；不要一次为不受控输入创建百万个 task。生产者速度超过消费者时使用 `asyncio.Queue(maxsize=...)`、信号量或流式 `async for`，队列满时暂停、丢弃低优先级或快速失败，并返回明确状态。

决定失败策略：默认一个失败是否取消同组任务、是否收集部分结果、是否允许继续。不要用 `return_exceptions=True` 后静默过滤异常；逐项分类、记录受控上下文并为部分成功定义业务语义。对外部调用结合限流、指数退避+jitter、幂等键和总 deadline，避免并发重试放大。

## 取消、超时与清理

取消是控制流，不应被普通 `except Exception` 吞掉。捕获 `asyncio.CancelledError` 后在 `finally` 中关闭连接、释放 semaphore、取消子任务、提交/回滚事务和删除临时资源，再重新抛出。区分调用方取消、超时、依赖错误和服务关闭。

超时应包住完整工作范围，并验证子任务不会在父请求结束后泄漏。任务完成、失败、取消和超时均要有可查询状态；后台 `create_task` 必须保存引用、处理异常和在 shutdown 时 await。

```python
async def run_with_cleanup(operation, resource):
    try:
        async with asyncio.timeout(10):
            return await operation(resource)
    except asyncio.CancelledError:
        await resource.abort_safely()
        raise
    finally:
        await resource.close()
```

## 资源与事件循环健康

使用有界连接池、请求体/响应体上限和复用 client；不要每个请求创建未关闭的 client。监控 event-loop lag、task 数、队列深度、连接池等待、超时/取消、错误率、p95/p99 延迟、CPU、内存和线程/进程池饱和。

阻塞调用放到受限 executor 并测量上下文切换；不要用 `asyncio.run` 嵌套现有事件循环。关闭时停止接收新工作、设置有界 grace period、取消并等待子任务、关闭 async generators/clients，然后报告未完成任务。

## 测试与交付

测试覆盖并发上限、顺序/部分结果、阻塞检测、超时、取消传播、子任务泄漏、队列背压、连接池耗尽、依赖失败、重试预算、shutdown 和资源关闭。使用 fake clock、fake client、受控 scheduler 和合成数据；负载测试需固定输入、版本、并发、warm 状态和硬件，比较事件循环延迟与资源成本。

报告记录 sync/async 选择、调用/资源契约、并发/队列/timeout 参数、基线、失败与取消语义、泄漏检查、负载结果、观测和回滚，并区分 observed、derived、unknown。

## 质量门禁

- [ ] sync/async/线程/进程边界有依据，事件循环无未经审查的阻塞调用。
- [ ] task、并发、队列、连接池、请求体和 executor 均有硬上限与背压策略。
- [ ] deadline、超时、异常分类、取消传播、子任务生命周期和幂等重试已定义。
- [ ] `async with`/`finally` 清理连接、锁、文件、事务和临时资源，shutdown 无 task 泄漏。
- [ ] 失败、部分结果、超时、取消、过载和依赖故障有确定性测试及性能基线。
- [ ] 生产并发、timeout、池、限流、流量和服务重启变更均有授权与回滚方案。
