---
name: "javascript-testing-patterns"
display_name: "JavaScript/TypeScript 测试模式"
display_name_en: "JavaScript/TypeScript Testing Patterns"
description: "Use when building or repairing JavaScript/TypeScript tests with Jest, Vitest, Testing Library, async services, or CI; select the right test layer, keep mocks contract-aware, and assert public behavior."
description_zh: "用于使用 Jest、Vitest、Testing Library、异步服务或 CI 构建/修复 JavaScript/TypeScript 测试；选择正确测试层，保持 mock 符合契约，并断言公开行为。"
description_en: "Create isolated and meaningful JS/TS tests with typed fixtures, deterministic async control, narrow module mocks, user-facing component assertions, cleanup, risk-driven coverage, and safe CI artifacts without weakening type or failure signals."
category: "testing"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized JavaScript/TypeScript repository, Jest/Vitest runner, disposable dependencies/data, browser or DOM environment when needed, and CI artifact policy; tests do not authorize production access"
---

# JavaScript/TypeScript 测试模式

用 Jest、Vitest 和 Testing Library 建立分层测试：快速单元测试证明纯逻辑，组件/集成测试证明模块协作和协议，少量 E2E 覆盖关键用户旅程。测试应该让失败原因清晰，而不是用大量 snapshot、宽泛 mock 或覆盖率数字制造虚假信心。

## 范围与安全门禁

开始前记录 Node/package manager/runner 版本、目标 revision、需求和不变量、测试环境、外部服务、数据清理、秘密处理和 CI artifact 保留策略。

- 使用合成数据、sandbox 和最小权限账号；不要把 token、cookie、个人数据、环境变量值或完整 URL 写入测试与报告。
- 网络、支付、邮件、队列和数据库使用隔离依赖、fake 或可回滚 fixture；不允许测试默认访问生产。
- 失败截图、DOM、console、网络请求和 coverage 必须脱敏；artifact 访问范围和保留期明确。
- 测试不自动修改实现、关闭 CI 门禁、批准发布或扩大权限；关键环境/清理/副作用未知时返回 `BLOCKED`。

## 测试层选择

| 层级 | 适合验证 | 典型选择 |
| --- | --- | --- |
| Unit | 纯函数、类、解析、业务规则、错误 | Jest/Vitest，无真实网络/数据库 |
| Component | React/Vue 等组件的公开交互和可见状态 | Testing Library + DOM 环境 |
| Integration | API client、模块协作、schema、数据库边界 | MSW/contract harness/隔离依赖 |
| E2E | 登录、结账、关键导航和真实浏览器行为 | Playwright/Cypress，少量高价值路径 |

不要用组件测试断言私有 state，不要用 E2E 覆盖每个分支，也不要把 mock 通过当作真实协议或性能通过。

## AAA 与可读断言

测试名说明场景和结果，结构遵循 Arrange-Act-Assert：

```typescript
it('rejects duplicate email with a conflict error', () => {
  const repo = new InMemoryUserRepo();
  repo.save({ id: '1', email: 'a@example.test' });

  const result = createUser(repo, { email: 'a@example.test' });

  expect(result).toMatchObject({ errorCode: 'conflict' });
  expect(repo.count()).toBe(1);
});
```

优先断言返回值、错误类型/代码、公开事件、可访问名称、URL 和用户可见文本；不要依赖私有字段、调用顺序或 DOM 层级，除非它们本身是公开契约。

## Fixture、类型与隔离

- 每个测试拥有自己的对象、时间、随机种子、临时目录和数据命名空间；
- `beforeEach`/fixture 只准备必要资源，`afterEach` 无论成功失败都清理并报告清理错误；
- 用工厂函数和明确类型创建数据，避免 `as any` 把无效状态藏起来；
- 并行 worker 不共享可变单例、端口、数据库行或全局 mock；
- fake 的行为应符合最小真实契约，必要时用一个 contract/integration test 校验。

```typescript
const user = (overrides: Partial<User> = {}): User => ({
  id: `test-${crypto.randomUUID()}`,
  email: 'user@example.test',
  role: 'member',
  ...overrides,
});
```

不要在全局 setup 中写永久数据、吞掉异常或改变所有测试的时区/网络而不记录。

## 异步、时间和并发

- 每个异步测试 `await` 最终 promise，并断言 rejected path；禁止遗留未等待的 task；
- 用 fake clock 或注入时钟测试过期、轮询、debounce 和重试，明确 timezone/precision；
- 用 MSW 或窄 client mock 控制网络响应，覆盖成功、4xx/5xx、超时、取消、重试和部分响应；
- 用 AbortController、test barrier 或受控 promise 验证竞态、重复提交和幂等，不用任意 sleep；
- 测试结束时清理 timers、subscriptions、event listeners、servers 和 pending requests。

```typescript
it('stops retrying after the configured limit', async () => {
  const request = vi.fn().mockRejectedValue(new TimeoutError());

  await expect(fetchWithRetry(request, { attempts: 3 })).rejects.toThrow(TimeoutError);
  expect(request).toHaveBeenCalledTimes(3);
});
```

## Mock 与模块边界

mock 被测模块依赖的外部边界，而不是被测逻辑本身。优先 `vi.spyOn`/`jest.spyOn`、MSW 或依赖注入；对模块 mock 使用 typed factory 和最小接口。

- patch 被测代码实际查找依赖的位置，避免 mock 错模块导致假通过；
- 验证关键请求的 method、路径、参数、headers、超时和错误映射，但不锁死无关实现；
- `clearAllMocks`、`resetAllMocks` 和 `restoreAllMocks` 的区别要明确，避免测试间污染；
- 不将整个 SDK、时间、随机数和所有内部模块全部 mock；至少保留真实契约/集成证据；
- 不用 `any`、过宽 `object` 或永远成功的 mock 绕过 TypeScript 检查。

## 组件与 Testing Library

以用户行为测试组件：

- 优先 `getByRole`、`getByLabelText`、`getByText`，必要时使用有意设计的 `data-testid`；
- 通过 `userEvent` 模拟真实交互，断言可见状态、焦点、错误、加载和恢复；
- 使用 `findBy*`/`waitFor` 等待明确条件，不用固定延时；
- 验证键盘路径、语义角色、名称和 live region，但不要把自动化结果当成人工屏幕阅读器完整证明；
- 每个测试渲染干净树，清理 portal、timer、订阅和网络 handler。

不要断言 React/Vue 私有 state、组件实例、CSS class 层级或调用了某个内部 helper；这些会让重构变成无意义的测试迁移。

## 参数化、属性与错误

用 table-driven/parameterized 测试表达输入矩阵，并为每个案例提供 ID。对解析器、序列化器和不变量可采用 property-based testing，但必须约束生成范围并在失败时保存 seed。

至少覆盖：空值、边界、重复、Unicode/时区、权限、网络失败、取消、重试上限、过期、并发和部分成功。每个 `catch`、fallback 和 feature flag 路径都要有理由和证据，不为 coverage 机械添加无价值断言。

## Coverage 与 CI

覆盖率是盲区信号，不是质量结论：

- 关注分支、错误、权限和高风险路径，记录基线差异；
- 阈值逐步提高，下降时失败或要求解释；排除项有可审计理由；
- snapshot 只用于稳定的公共输出，避免把时间戳、随机 ID 和整棵 DOM 当作质量；
- CI 分层运行 typecheck/lint → unit → component/integration → 少量 E2E，记录确切命令和版本；
- 测试失败、收集错误、环境不可用、跳过和未运行必须区分，unknown 不得变绿。

`skip`/`todo`/`expected failure` 需要原因、owner、链接和复查日期。禁止用永久 skip、无限 retry、放宽 timeout 或删除断言处理 flaky。

## 失败诊断

固定 commit、Node、lockfile、浏览器/DOM 环境和 seed；单独运行失败案例并保存脱敏日志。按产品回归、测试缺陷、环境故障、资源耗尽或未知分类，记录首次失败与重试结果。修复必须有最小复现和回归测试；不能稳定复现时保留 `Unknown`，不声称已解决。

## 报告模板

```markdown
# JS/TS Test Report

Target: <repository, commit, scope>
Environment: <Node/runner/platform, no secrets>
Command: <exact bounded command>
Result: Passed | Failed | Blocked | Unknown
Failures: <test IDs, expected/actual, classification>
Coverage: <risk-relevant summary and baseline delta>
Skipped/mocked: <reason, owner, review date, contract evidence>
Artifacts: <redacted IDs and retention>
Unverified: <browser, network, database, concurrency or production parity>
Next action: <smallest safe verification>
```

## 质量门槛

- 测试层与风险匹配，断言公开行为，类型检查保持有效；
- fixture、mock、timer、promise、event listener 和 DOM 状态隔离且可清理；
- 外部依赖的 mock 有窄契约，关键协议有真实集成证据；
- coverage、snapshot、skip、retry 和 flaky 处理有可追溯理由；
- CI 能区分失败、环境故障、未运行和未知状态，artifact 已脱敏；
- 生产访问、秘密、数据清理或关键依赖边界无法确认时返回 `BLOCKED`。

## Related Skills

- `python-testing-patterns` - 使用 pytest、fixture、mock 和风险驱动覆盖率
- `e2e-testing-patterns` - 设计少量高价值浏览器用户旅程
- `test-driven-development` - 用 RED-GREEN-REFACTOR 固定行为
- `screen-reader-testing` - 深入验证屏幕阅读器和键盘行为
