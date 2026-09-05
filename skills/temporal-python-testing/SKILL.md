---
name: "temporal-python-testing"
display_name: "Temporal Python 工作流测试"
display_name_en: "Temporal Python Workflow Testing"
description: "Use when testing Temporal Python workflows or activities with pytest; choose time-skipping, activity isolation, worker integration, and replay tests deliberately, and verify determinism and version compatibility before deployment."
description_zh: "用于使用 pytest 测试 Temporal Python 工作流或 Activity；有意识地选择时间跳过、Activity 隔离、Worker 集成和 replay 测试，并在部署前验证确定性与版本兼容。"
description_en: "Build fast, isolated, and evidence-based Temporal tests with time-skipping environments, ActivityEnvironment, mocked dependencies, task-queue isolation, signal/query/error coverage, replay of authorized redacted histories, safe worker shutdown, and fail-closed CI gates."
category: "testing"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized Temporal Python repository, SDK/Server versions, isolated test namespace or environment, pytest async support, disposable payloads, and retained test evidence; no production execution or history access is implied"
---

# Temporal Python 工作流测试

Temporal 测试需要同时验证工作流确定性、Activity 边界、事件时间、重试/取消、信号/查询和版本兼容。长时间业务流程应通过 time-skipping 获得快速反馈，再用受控 Worker 集成和授权的历史 replay 覆盖运行时差异。

## 环境与安全门禁

开始前记录 repository revision、Python/SDK/Server 版本、namespace/task queue、工作流类型、数据来源、测试副作用、历史访问授权和 artifact 保留策略。

- 默认使用本地 time-skipping 环境、专用测试 namespace、合成 payload 和最小权限凭据；不连接生产 Temporal。
- history、payload、headers、日志、trace 和截图可能含客户数据/秘密，必须脱敏、限制访问并设置保留期；不要把完整 history 提交到仓库。
- Activity 测试禁止真实付款、邮件、删除或外部写入；用 fake/sandbox 并验证调用契约。
- SDK/Server、workflow 版本或历史来源不明，Worker 无法可靠 shutdown，或清理失败时返回 `BLOCKED`。

## 测试层

| 层级 | 验证目标 | 典型环境 |
| --- | --- | --- |
| Workflow unit | 分支、计时器、重试、取消、signal/query 和状态 | `WorkflowEnvironment` time-skipping，mock Activities |
| Activity unit | 输入校验、业务副作用、异常分类和超时 | `ActivityEnvironment` + fake 外部依赖 |
| Worker integration | 注册、序列化、task queue、workflow/activity 协作 | 本地 Temporal/test namespace |
| Replay | 既有事件历史仍可由当前 workflow 确定性重放 | 授权且脱敏的固定 history |
| End-to-end | 少量关键流程和真实 sandbox 集成 | 隔离服务，谨慎使用，明确清理 |

多数逻辑应在前两层快速验证；E2E 不应替代 determinism 或契约测试。

## Time-skipping Workflow 测试

使用 time-skipping 环境让月/日级 timer 在测试中快速推进，但每次推进都要对应业务条件，不要依赖墙上时钟或固定 sleep。

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

@pytest.fixture
async def workflow_env():
    env = await WorkflowEnvironment.start_time_skipping()
    try:
        yield env
    finally:
        await env.shutdown()

@pytest.mark.asyncio
async def test_reminder_fires_after_due_time(workflow_env):
    async with Worker(
        workflow_env.client,
        task_queue="test-reminder-unique",
        workflows=[ReminderWorkflow],
        activities=[send_reminder],
    ):
        handle = await workflow_env.client.start_workflow(
            ReminderWorkflow.run,
            ReminderArgs(...),
            id="test-reminder-unique",
            task_queue="test-reminder-unique",
        )
        await workflow_env.sleep(30 * 24 * 60 * 60)
        assert await handle.result() == "sent"
```

实践要点：

- 每个测试使用唯一 workflow ID/task queue，避免并行碰撞和旧 execution 污染；
- fixture 必须在异常时关闭环境，Worker 使用 `async with` 保证 shutdown；
- 明确 time-skipping 是否影响 Activity、retry backoff、heartbeat 和 external clock；
- 测试 timer、continue-as-new、超时、取消、重试上限和失败补偿，而不只测成功结果。

## Activity 测试

Activity 是副作用边界：使用 `ActivityEnvironment` 或窄 fake 验证输入、结果、异常类型和调用契约。把超时、可重试错误、永久错误、取消和幂等分别测试。

```python
from temporalio.testing import ActivityEnvironment

@pytest.mark.asyncio
async def test_charge_activity_maps_declined_payment():
    env = ActivityEnvironment()
    gateway = FakeGateway(result="declined")

    with pytest.raises(PaymentDeclined):
        await env.run(charge_card, gateway, ChargeRequest(...))

    assert gateway.calls == 1
```

不要让 mock 永远返回成功、吞掉异常或伪造不可能的 payload。真实 gateway/schema/事务语义至少通过一个 sandbox contract/integration 测试验证。Activity 的 token、连接、日志和 payload 不得进入测试输出。

## Signal、Query、更新与状态

为每个公开交互写出状态机和可观察后置条件：

- signal 重复、乱序、并发和在 timer 前后到达；
- query 在初始化、等待、完成和失败状态下的返回；
- update/command 的验证拒绝、幂等和并发冲突；
- workflow cancellation、termination、retry exhaustion 和 continue-as-new；
- Activity heartbeat、心跳超时、取消传播和补偿动作。

断言 workflow result、query/signal 可见状态、Activity 调用和事件后置条件，不读取私有 runtime 状态来制造脆弱测试。

## Replay 与确定性

workflow 代码不能依赖当前时间、随机数、环境变量、网络、文件系统、线程竞态或不可控全局状态。使用 Temporal SDK 提供的时间/随机机制和 Activity 作为外部边界。

Replay 流程：

1. 固定 workflow revision、SDK/Server 版本和 history 来源；
2. 只使用经过授权、脱敏、最小化的历史；
3. 在 CI 中对所有关键 workflow 版本执行 replay；
4. 将 nondeterminism、schema/version 不兼容和 payload 解码失败与产品断言失败分开；
5. 任何历史失败都先阻断部署或进入明确的 versioning/migration 决策，不用跳过掩盖。

历史 replay 成功只证明该历史在当前 runner 上可重放，不证明新分支覆盖所有历史或外部服务可用。

## 版本、Worker 与本地开发

- 记录 workflow versioning/patch、兼容窗口、部署顺序和旧 Worker 排空策略；
- 测试 task queue、workflow/activity 注册、数据序列化和 namespace 隔离；
- 本地 Docker/Temporal Server 只使用固定版本和临时数据，启动健康检查有超时；
- Worker 测试结束后关闭 poller、连接和临时服务，验证无后台 task 遗留；
- 不把本地 dev namespace、凭据或 compose 中的默认秘密当成生产配置。

## Coverage 与 CI

覆盖率按 workflow 分支、Activity 分支、错误/重试/取消和版本路径统计，而不是只看行数。可设置项目阈值（例如关键 workflow/Activity 以 80% 作为起点），但阈值必须结合风险和基线，不能替代 determinism/replay 证据。

推荐 CI 分层：

1. 快速静态检查、类型和 workflow sandbox unit；
2. Activity unit 与契约测试；
3. Worker integration + time-skipping；
4. 授权历史 replay；
5. 少量 sandbox E2E，明确副作用和清理。

报告必须区分测试失败、Temporal 服务不可用、history 缺失、版本不匹配、未运行和未知状态。unknown 不得变绿；`skip`/`xfail` 需要原因、owner、链接和复查日期。

## 失败诊断模板

```markdown
# Temporal Test Report

Target: <repository, commit, workflow type/version>
Environment: <Python/SDK/Server/namespace, no secrets>
Layer: Workflow unit | Activity | Worker integration | Replay | Sandbox E2E
Result: Passed | Failed | Blocked | Unknown
Time model: <time-skipping or wall-clock; advancement>
Failure: <event/step, expected vs actual, classification>
History: <authorized redacted ID/hash, never raw payload>
Evidence: <sanitized logs, metrics, trace, test ID>
Unverified: <versions, external dependency, concurrency, cleanup>
Next action: <smallest safe reproduction or migration decision>
```

禁止用增加 timeout、无限 retry、跳过 replay、删除 history 断言或关闭 determinism 检查处理失败。修复必须有最小复现和回归测试。

## 质量门槛

- workflow、Activity、Worker integration 和 replay 的职责边界清晰；
- time-skipping、唯一 ID/task queue、async cleanup 和外部副作用隔离可靠；
- retry、timeout、cancel、signal/query/update、continue-as-new 和版本兼容有证据；
- replay history 已授权、脱敏、固定来源且失败会阻断或进入明确决策；
- coverage、skip、环境故障和 unknown 状态可追踪；
- 生产 namespace、秘密、客户 history、数据清理或版本边界无法确认时返回 `BLOCKED`。

## Related Skills

- `python-testing-patterns` - 通用 pytest、fixture、mock 和 CI 测试策略
- `workflow-orchestration-patterns` - 设计重试、补偿和跨步骤工作流
- `e2e-testing-patterns` - 覆盖少量高价值用户旅程
- `regression-risk-review` - 评估部署前回归范围和证据
