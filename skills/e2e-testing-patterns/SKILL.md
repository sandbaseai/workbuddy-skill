---
name: "e2e-testing-patterns"
display_name: "端到端测试模式"
display_name_en: "E2E Testing Patterns"
description: "Use when creating or repairing browser end-to-end tests for critical user journeys, cross-browser behavior, accessibility, or release confidence; keep tests deterministic, independent, user-facing, and safe for CI."
description_zh: "用于为关键用户旅程、跨浏览器行为、可访问性或发布信心创建/修复浏览器端到端测试；保持测试确定、独立、面向用户且适合安全运行于 CI。"
description_en: "Design a small, high-value E2E suite with stable semantic selectors, isolated data, explicit synchronization, safe authentication, meaningful assertions, artifact redaction, and evidence-based flake triage; do not replace unit or contract tests with browser tests."
category: "testing"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized test environment, browser runner, disposable data, seeded accounts, CI artifacts, and documented side-effect limits; tests do not authorize production access or data mutation"
---

# 端到端测试模式

端到端测试验证用户通过真实浏览器可观察到的关键行为和系统集成。它们数量应少而有价值：用单元测试覆盖逻辑，用契约/集成测试覆盖 API 和依赖，用 E2E 覆盖跨页面、认证、关键业务流程和真实交互。

## 环境与安全门禁

开始前记录应用 revision、环境 URL、浏览器/运行器版本、测试账号来源、数据清理方式、允许的外部依赖、并发限制和报告读者。

- 默认只使用专用测试环境、合成数据和最小权限账号；禁止将生产 cookie、令牌、客户数据或秘密写入测试代码、日志、trace、截图或视频。
- 对会产生邮件、付款、删除、消息或第三方写操作的流程使用 sandbox、拦截器或明确的 dry-run；不得通过 E2E 直接验证生产副作用。
- 测试超出授权环境、关键账号不可用、数据清理失败或副作用边界不明时返回 `BLOCKED`。
- 浏览器测试失败只说明当前环境/路径的证据，不自动批准发布、修改代码或重试高风险操作。

## 测试范围

### 适合 E2E

- 登录、注册、结账、关键表单、权限边界和多步骤用户旅程；
- 浏览器渲染、导航、键盘交互、可见错误恢复和跨页面状态；
- 真实 API 集成、关键浏览器兼容性和发布 smoke path；
- 影响用户的可访问性要求，如语义角色、键盘路径、焦点和错误提示。

### 不适合 E2E

- 每个分支、算法边界、纯函数和异常组合：使用单元测试；
- 所有 API schema 和错误组合：使用契约/集成测试；
- 内部状态、私有函数、CSS 层级或实现细节；
- 可由更快、更精确的低层测试覆盖的重复案例。

每条 E2E 都要写出用户风险、成功标准和为什么不能由低层测试替代。

## 设计原则

1. **以用户行为断言**：通过角色、标签、可见文本、URL 和可访问状态判断结果，不读取私有状态。
2. **稳定定位**：优先 `getByRole`、`getByLabel`、`getByText` 等语义定位器；必要时使用有意设计的 `data-testid`/`data-cy`。避免 CSS 类、XPath、`nth-child` 和深层 DOM 结构。
3. **显式同步**：等待具体条件、网络响应或 UI 状态，不使用任意固定 sleep；为外部依赖设置有意义的超时。
4. **测试独立**：每个测试准备自己的数据和会话，可任意顺序、并行或单独运行；不要依赖前一个测试留下的购物车、登录态或数据库行。
5. **最小路径**：一个测试覆盖一个清晰旅程；公共准备逻辑抽成 fixture/页面对象，但不要把所有断言藏在黑盒 helper 中。
6. **可重复与可诊断**：固定必要的时区、locale、随机种子和时钟；失败时保留安全的 trace、截图、控制台和网络摘要。

## 分阶段流程

### 1. 建立测试契约

```markdown
Journey: <用户目标>
Risk: <失败会影响什么>
Preconditions: <测试账号、种子数据、feature flag>
Steps: <用户可见步骤>
Assertions: <用户可观察结果和关键后置状态>
Isolation: <创建/清理/命名空间>
Environment: <浏览器、URL、依赖和副作用>
Evidence: <报告、trace、截图、日志的安全保留方式>
```

先确认需求和验收标准，再确定最短可验证路径。缺少稳定的用户结果或数据清理方式时不要开始堆叠步骤。

### 2. 准备数据与会话

- 使用 API/fixture 快速创建合成数据，UI 只覆盖真正需要的初始化路径；
- 为每个 worker/测试分配命名空间或唯一 ID，避免并发碰撞；
- 认证状态由专用 fixture 创建并短期保存，权限按测试显式声明；
- 清理在测试失败时也执行，并验证没有残留敏感或高成本数据；
- 不把 token 放在命令行、断言、截图、URL query、浏览器 localStorage 导出或 artifact 名称中。

### 3. 实现与断言

每一步都要有用户语义；断言优先检查可见反馈、可访问名称、导航结果、错误恢复和经过授权的持久化结果。不要只断言“按钮存在”或内部变量变成某个值。

```typescript
test('用户可以提交联系表单', async ({ page }) => {
  await page.goto('/contact');
  await page.getByLabel('邮箱').fill('e2e-user@example.test');
  await page.getByLabel('消息').fill('需要帮助');
  await page.getByRole('button', { name: '发送' }).click();

  await expect(page.getByRole('status')).toHaveText('消息已发送');
  await expect(page).toHaveURL(/\/contact\/success/);
});
```

页面对象应封装定位器和可复用动作；业务断言留在测试或领域 fixture 中，避免 helper 让失败位置不可见。

### 4. CI 运行

- PR smoke suite 只包含高价值、短时、确定的路径；完整浏览器矩阵按风险和发布阶段运行；
- 浏览器、依赖、seed、locale 和环境配置固定或明确记录；
- 并行运行前确认数据隔离、端口、限流和第三方 sandbox 能力；
- 失败时保存脱敏的 trace/screenshot/video/console/network evidence，设置保留期；
- 测试 runner 错误、环境不可用和产品断言失败要分开报告；未知状态不能被当作通过。

## Flaky 测试诊断

Flaky 不是随机重跑后就可以忽略的噪声。记录测试、commit、浏览器、环境、时间、重现率和失败阶段，先分类：

| 类别 | 证据方向 | 修复方向 |
| --- | --- | --- |
| 同步竞态 | 元素可见但状态未完成、网络仍在 pending | 等待具体状态/响应，修复产品或测试竞态 |
| 数据碰撞 | 并行时同一 ID、顺序依赖、残留行 | 唯一命名空间、独立 seed、可靠清理 |
| 环境/依赖 | DNS、第三方、资源耗尽、浏览器崩溃 | 隔离依赖、健康检查、容量和失败分类 |
| 定位脆弱 | 文案/DOM 改动后选择器失效 | 语义 locator 或稳定测试契约 |
| 时钟/动画 | 超时与动画、时区、轮询边界相关 | 控制时钟/动画或等待业务条件 |
| 真回归 | 同一 revision 在可重复条件下断言失败 | 最小复现、提交缺陷并补回归测试 |

禁止用增加全局 timeout、加入固定 sleep、无限重试或跳过断言掩盖问题。重试只能作为诊断信号，并必须区分首次失败和重试通过。

## 可访问性与跨浏览器

- 关键流程用键盘完成：焦点可见、顺序合理、弹窗可关闭、错误能被感知；
- 通过角色/名称定位同时验证语义，而不是仅依赖视觉截图；
- 针对支持矩阵选择 Chromium/Firefox/WebKit 或移动视口；失败报告包含浏览器和视口；
- 视觉快照只用于稳定的布局/品牌风险，避免把字体、动画和时间戳差异误报为产品缺陷；
- E2E 可发现明显可访问性回归，但不能替代屏幕阅读器、静态规则和人工审查。

## 失败报告模板

```markdown
# E2E Failure

Test/Journal: <name>
Revision: <commit>
Environment: <non-secret URL label, browser, viewport>
First failure: <step and timestamp>
User-visible symptom: <what a user would observe>
Expected/actual: <bounded comparison>
Classification: Product regression | Test defect | Environment | Unknown
Evidence: <redacted trace/screenshot/log IDs>
Reproduction: <safe command or rate, no secrets>
Next action: <owner and smallest verification>
Security note: <what was redacted and retention>
```

## 质量门槛

- 每个 E2E 对应高价值用户风险和明确可见断言；
- 定位器稳定、同步基于条件、测试数据和会话隔离；
- 失败 artifact 不含秘密或客户数据，且保留期和访问范围明确；
- flaky 结论有分类和证据，不用 sleep、无限重试或跳过断言掩盖；
- CI 中产品失败、测试缺陷、环境故障和未运行状态可区分；
- 未授权环境、数据清理失败、关键证据缺失或高风险副作用不明时返回 `BLOCKED`。

## Related Skills

- `playwright-webapp-qa` - 对授权浏览器页面执行更广泛的可见行为与控制台/网络诊断
- `screen-reader-testing` - 深入验证屏幕阅读器、键盘和动态内容
- `test-driven-development` - 先用行为测试固定需求，再以最小实现收敛
- `regression-risk-review` - 评估变更影响范围和回归证据
