---
name: "python-testing-patterns"
display_name: "Python 测试模式"
display_name_en: "Python Testing Patterns"
description: "Use when writing or restructuring Python tests with pytest, fixtures, mocks, async code, database boundaries, or CI gates; choose the smallest test layer that proves behavior and preserve diagnostic evidence."
description_zh: "用于使用 pytest、fixture、mock、异步代码、数据库边界或 CI 门禁编写/重构 Python 测试；选择能证明行为的最小测试层，并保留可诊断证据。"
description_en: "Build isolated and meaningful Python tests with clear Arrange-Act-Assert structure, explicit fixtures, contract-aware mocks, deterministic time and concurrency controls, coverage tied to risk, and fail-closed CI handling without hiding failures."
category: "testing"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized Python repository, pytest environment, disposable dependencies/data, test configuration, and CI artifact policy; tests do not authorize production access or data mutation"
---

# Python 测试模式

Python 测试的目标是证明行为、边界和失败处理，而不是堆积断言或追求一个漂亮的覆盖率百分比。先选择测试层，再用 pytest 的 fixture、参数化、mock、异步支持和标记建立可重复的证据。

## 范围与安全门禁

开始前记录 Python/pytest 版本、目标模块、需求/不变量、依赖服务、测试数据来源、允许的副作用、秘密处理和 CI 门禁。

- 默认使用合成数据、隔离数据库和最小权限测试账号；不读取或写入生产数据。
- 日志、失败输出、coverage、快照和 CI artifact 不得包含 token、密码、个人数据或完整连接字符串。
- 数据库、队列、邮件、付款和外部 API 使用 sandbox、fake 或可回滚 fixture；边界不明时返回 `BLOCKED`。
- 测试代码不自动修改实现、关闭门禁、批准发布或扩大访问权限。

## 选择测试层

| 层级 | 证明什么 | 典型工具/边界 |
| --- | --- | --- |
| Unit | 单个函数、值对象、领域规则和错误 | 纯输入、少 fixture、无真实网络/数据库 |
| Component | 模块内协作、应用用例和端口契约 | fake/内存适配器、受控 fixture |
| Integration | ORM、事务、消息、HTTP 和真实 schema 交互 | 隔离依赖、迁移和清理证据 |
| Functional/E2E | 完整用户或服务旅程 | 专用环境，少量高价值路径 |
| Performance | 延迟、吞吐、资源和退化 | 固定数据/环境，独立基线 |

一个单元测试不应伪装成集成测试；mock 通过不代表真实依赖契约、事务或性能通过。

## 基本结构

每个测试尽量遵循 Arrange-Act-Assert，并让测试名描述输入、场景和可观察结果：

```python
def test_create_user_with_duplicate_email_returns_conflict(user_repo):
    # Arrange
    user_repo.save(User(email="a@example.test"))

    # Act
    result = create_user(user_repo, email="a@example.test")

    # Assert
    assert result.error_code == "conflict"
    assert user_repo.count() == 1
```

避免 `test_1`、`test_function` 这类无法表达行为的名称，也避免只断言实现细节。优先断言返回值、状态变化、公开事件、错误类型/代码和用户可见结果。

## Fixture 与隔离

- fixture 只提供一个清晰资源或前置条件，作用域越短越容易推理；
- 默认 function scope，较宽作用域必须证明没有可变共享状态或顺序依赖；
- 每个测试创建自己的对象、目录、队列消息和数据库行，并在成功/失败后清理；
- 并行运行时使用 worker/租户/临时目录唯一命名空间；
- fixture 失败应清晰显示是环境前置条件失败，而非业务断言失败。

```python
@pytest.fixture
def user_repo(tmp_path):
    repo = InMemoryUserRepository(path=tmp_path / "users.json")
    yield repo
    repo.close()
```

不要在 fixture 中偷偷调用真实生产端点、创建永久账号或吞掉清理异常。数据库 fixture 应显式说明事务回滚、截断、迁移版本和并发限制。

## 参数化与边界

使用参数化表达同一行为的输入集合，给每个案例有意义的 ID；不要用几十个相似断言掩盖真正不同的风险。

```python
@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("alice@example.test", True, id="valid"),
        pytest.param("", False, id="empty"),
        pytest.param("not-an-email", False, id="malformed"),
    ],
)
def test_email_validation(raw, expected):
    assert validate_email(raw) is expected
```

为边界测试写出为什么重要：空值、极值、重复、时区、编码、权限、超时、重试、并发和部分失败。不要为了提高 coverage 率机械测试不可达或无业务意义的行。

## Mock、patch 与外部边界

mock 应替代不可控的外部边界，而不是替代被测逻辑。优先 patch 被测模块实际查找的位置，使用 `spec`/autospec 或协议约束，验证关键调用参数、次数、超时和错误映射。

- 对网络、时钟、随机数、队列和文件系统建立窄接口；
- 不 mock 私有方法链、所有内部对象或返回值实现细节；
- mock 的成功路径之外必须覆盖超时、可重试错误、永久错误和部分响应；
- 至少用一个契约/集成测试验证 mock 所代表的真实协议。

```python
def test_retry_stops_after_limit(api_client):
    api_client.fetch.side_effect = TimeoutError("temporary")

    with pytest.raises(TimeoutError):
        fetch_with_retry(api_client, attempts=3)

    assert api_client.fetch.call_count == 3
```

不要让 mock 把异常吞掉、返回不可能的数据或让测试永远通过。第三方库升级后，失效的 spec 应让 CI 失败。

## 时间、异步与并发

- 将时钟注入或冻结在测试边界，明确时区和精度；不要依赖机器当前时间；
- 异步测试使用项目认可的 `pytest-asyncio`/anyio 配置，等待 task 完成并检查异常；
- 测试取消、超时、重试、重复消息和幂等，而不是只测最终成功；
- 并发测试固定资源、屏障和随机性，记录环境限制；不能稳定复现时标记 `Unknown`，不凭一次通过宣称安全。

```python
@pytest.mark.asyncio
async def test_expired_token_is_rejected(clock, token_service):
    clock.set("2026-01-15T10:00:00Z")
    token = token_service.issue(expires_in=60)
    clock.advance(seconds=61)

    with pytest.raises(TokenExpired):
        await token_service.verify(token)
```

## 数据库与服务集成

集成测试应固定 schema/migration 版本，使用专用数据库或临时 schema，并验证：事务提交/回滚、唯一约束、并发冲突、分页、时区、序列化和连接释放。只用内存 fake 时明确它没有证明真实索引、锁、隔离级别或查询计划。

服务测试要区分：

- 应用层返回的业务错误；
- 依赖超时/限流/不可用；
- 输入校验和权限拒绝；
- 可重试与不可重试故障。

## 标记、覆盖率与 CI

为 `unit`、`integration`、`e2e`、`slow`、`network` 等标记建立项目注册表，CI 明确每个 job 的范围。`skip`/`xfail` 必须有责任人、链接、原因和复查日期，不能永久隐藏失败。

覆盖率用于发现盲区，不是质量的唯一指标：

- 关注高风险路径、分支、错误和权限，而非只看行覆盖率；
- 阈值应基于基线逐步提高，下降时给出差异；
- 排除项有可审计理由，不用于隐藏未实现代码或死代码；
- CI 将测试失败、环境不可用、收集错误和未运行分开；未知状态不得变绿。

推荐 CI 顺序：快速静态检查 → unit → component → 集成/契约 → 少量 E2E/性能。每层保存脱敏摘要、版本、命令和失败 artifact 保留策略。

## 失败诊断

1. 固定 commit、Python/依赖/平台和测试选择；
2. 单独运行失败案例，再按相同 seed 和并发度重复；
3. 读取完整 traceback、fixture 生命周期、日志和外部响应摘要；
4. 分类为产品回归、测试缺陷、环境故障或未知；
5. 用最小复现和回归测试验证修复，记录未验证范围。

禁止用无限重试、增大 timeout、随机 sleep、无条件 `xfail` 或删除断言解决 flaky。重试可作为诊断信号，但必须报告首次失败和重试结果。

## 测试报告模板

```markdown
# Python Test Report

Target: <repository, commit, scope>
Environment: <Python/pytest/platform, no secrets>
Command: <exact bounded command>
Result: Passed | Failed | Blocked | Unknown
Coverage: <risk-relevant summary and baseline delta>
Failures: <test IDs, expected/actual, classification>
Skipped/xfail: <reason, owner, review date>
Evidence: <redacted logs/artifacts and retention>
Unverified: <dependencies, concurrency, production parity>
Next action: <smallest safe verification>
```

## 质量门槛

- 测试层与要证明的行为匹配，名称、AAA 结构和断言可读；
- fixture、数据、时钟、随机性和异步任务隔离且可清理；
- mock 有窄边界并有真实契约/集成证据，未掩盖异常或副作用；
- coverage、skip、xfail、重试和 flaky 处理均有原因与可追溯记录；
- CI 能区分失败、环境问题、未运行和未知状态，artifact 已脱敏；
- 生产访问、秘密、数据清理、关键依赖或副作用边界无法确认时返回 `BLOCKED`。

## Related Skills

- `test-driven-development` - 用 RED-GREEN-REFACTOR 先固定行为再实现
- `e2e-testing-patterns` - 设计少量高价值浏览器用户旅程
- `python-code-style` - 统一 Python 可读性、类型和 lint 约定
- `regression-risk-review` - 评估变更影响和回归证据
