---
name: "python-background-jobs"
display_name: "Python 后台任务"
display_name_en: "Python Background Jobs & Task Queues"
description: "Use when moving long-running work out of request handlers, designing Python task queues/workers, or handling asynchronous jobs and events."
description_zh: "用于将长任务移出请求处理器、设计 Python 任务队列/Worker，或处理异步任务与事件。"
description_en: "Design observable Python background jobs with durable state, at-least-once delivery, idempotency, bounded retries, deadlines, backpressure, DLQs, cancellation, and graceful shutdown."
category: "backend"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized durable queue, job store, isolated worker tests, and configured telemetry; production enqueue, replay, deletion, and side-effect changes require separate authorization"
---

# Python Background Jobs & Task Queues

把耗时、易失败或可异步的工作从请求生命周期中解耦。可靠的后台任务不是简单调用 `.delay()`：必须定义持久状态、投递语义、幂等性、重试预算、取消、死信、可观测性和副作用边界。

## 使用边界

- 开始前确认 Python/queue/worker 版本、任务 owner、输入输出 schema、租户边界、SLA、保留周期、并发、成本和目标环境。
- 默认只读检查队列、job store、worker 配置、代码、指标和日志；在本地/预发布使用合成数据与受控故障。
- 不擅自向生产队列 enqueue/replay/purge、修改 worker 并发、重放死信、变更保留或执行副作用任务；这些操作需要授权和回滚方案。
- payload、job metadata 和错误日志不得含 token、完整用户输入、个人数据或支付信息；任务日志保存脱敏摘要与 correlation ID。

## 任务契约与状态机

每个任务声明稳定 `task_type`、schema/version、owner、最大运行时间、资源类别、幂等键、可重试错误、输出保留和取消语义。API 对长任务只持久化最小输入并返回不可猜测的 job ID；状态接口只允许授权租户读取。

状态至少包括 `pending → running → succeeded/failed`，并明确 `cancel_requested`、`retrying`、`dead_letter` 和过期状态。状态转换使用条件更新/版本号防止两个 worker 同时“成功”；状态存储和消息投递采用 outbox、事务或可证明的一致性策略。

```python
from dataclasses import dataclass
from enum import StrEnum

class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"

@dataclass(frozen=True)
class JobRequest:
    job_id: str
    schema_version: int
    idempotency_key: str

async def submit_export(request, tenant_id):
    job = await jobs.create_if_absent(
        tenant_id=tenant_id, request=request.safe_fields(),
        idempotency_key=request.idempotency_key,
    )
    await outbox.publish_once("export.v1", job.id, tenant_id)
    return {"job_id": job.id, "status": job.status, "poll_url": f"/jobs/{job.id}"}
```

## 投递、幂等与副作用

多数队列是至少一次投递：worker 崩溃、ack 丢失、超时或网络分区都会造成重复。任务 handler 必须使用幂等键、唯一约束、upsert、处理记录或事务边界安全重跑；“检查后写入”要防并发竞态。副作用完成后再 ack，或使用可证明的 outbox/去重协议。

发送邮件、扣款、webhook、发布事件和文件覆盖等操作必须有服务端幂等语义与未知结果处理；不能因客户端超时自动再次扣款。租户、权限和任务版本在 worker 侧重新验证，不能信任队列 payload 中的授权字段。

## 重试、超时与死信

只重试暂时性网络、限流和依赖可用性错误；参数、schema、权限、业务拒绝和代码 bug 进入快速失败或死信。每项任务设置 attempt 上限、总 deadline、指数退避+jitter、响应/日志大小和资源上限，并遵守下游 `Retry-After`。

超过预算后将最小化的失败摘要、版本和 attempt 信息写入 DLQ，保护原始 payload；DLQ replay 是有副作用的运维动作，需要授权、筛选、幂等证明和回滚/补偿。不要用无限重试掩盖队列积压或下游故障。

## 队列、背压与资源隔离

按任务类型、优先级、租户或资源类别隔离队列/并发，设置可见性超时、prefetch、队列上限和最大 in-flight 数。监控 queue depth、oldest age、吞吐、失败率、重试放大、执行时长分布、worker 饱和和 DLQ 数量；积压时降低生产、拒绝低优先级或返回明确状态，而非无限堆积。

任务 payload 尽量只包含版本化引用；大文件放在授权对象存储并校验 hash/权限。worker 资源限制要防单个任务耗尽 CPU、内存、磁盘或连接池；敏感任务不能与不同租户共享未隔离的缓存/临时目录。

## 取消、恢复与优雅停机

取消是协作信号，不等于强杀：任务在安全检查点停止，标记取消结果并清理临时资源。worker 停机先停止取新任务，等待有界时间，延长/释放 lease，确保未完成任务可重投；重复启动必须不会破坏幂等状态。

恢复验证覆盖 worker 丢失、ack 丢失、数据库不可用、队列不可用、依赖超时、部分输出、schema 版本不兼容和部署中断。恢复成功不只看任务状态，还要检查业务结果、重复副作用、积压和下游一致性。

## 测试与交付

隔离测试验证状态转换、重复消息、并发 claim、重试分类、deadline、jitter、DLQ、replay 授权、取消、租户读取、payload 脱敏、outbox、幂等副作用和优雅停机。用固定时钟、随机源和 fake queue，避免依赖真实生产服务。

报告记录任务 schema/version、投递语义、幂等策略、状态证据、并发/资源参数、失败矩阵、队列指标、恢复测试、成本、隐私处理、授权状态和未覆盖范围，并区分 observed、derived、unknown。

## 质量门禁

- [ ] 任务 schema/version、owner、租户、状态机、SLA、deadline、资源和保留策略已定义。
- [ ] 至少一次投递、重复消息、并发 claim、ack/lease 和幂等副作用已有证明。
- [ ] 重试仅覆盖暂时性错误，有界次数/时间/资源、退避+jitter 和 DLQ 策略已验证。
- [ ] 队列深度、老化、吞吐、失败/重试放大、worker 饱和和 DLQ 可观测并有告警。
- [ ] 取消、故障恢复、版本兼容、优雅停机、部分输出和重放均有隔离测试。
- [ ] 生产 enqueue/replay/purge、worker/并发、保留和副作用变更均有授权与回滚方案。
