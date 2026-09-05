---
name: "webapp-testing"
display_name: "Web 应用浏览器测试"
display_name_en: "Web Application Testing"
description: "Use when testing or debugging an authorized local web application with Playwright, including user flows, responsive behavior, screenshots, console logs, and network evidence."
description_zh: "用于使用 Playwright 测试或调试已授权的本地 Web 应用，包括用户流程、响应式行为、截图、控制台日志和网络证据。"
description_en: "Test browser behavior with scoped environments, accessible selectors, deterministic waits, safe synthetic data, failure artifacts, console/network diagnostics, and explicit side-effect controls."
category: "testing"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized local/staging web app, Node.js/Playwright or Playwright MCP, synthetic test accounts, and isolated browser artifacts; production browsing, real submissions, payments, destructive actions, and external URLs require separate authorization"
---

# Web 应用浏览器测试

使用真实浏览器验证已授权 Web 应用的可见行为、交互流程和失败证据。先确认测试环境、构建版本、浏览器矩阵、账号权限、数据隔离和副作用，再执行 Playwright；测试结果只代表声明的环境与时间窗口，不自动证明无障碍、性能或生产安全。

## 范围与安全边界

- 开始前记录目标 URL、应用 commit/build、浏览器/OS、视口、语言/时区、测试账号、允许的域名、数据清理方式和授权人；优先使用本地或隔离 staging。
- 默认只访问 allowlist URL，禁止把用户提供的 URL 直接交给浏览器；阻断不必要的外链、下载、WebSocket、内网/云元数据地址和跨租户跳转，避免 SSRF。
- 使用合成账号、非敏感数据和测试支付/邮件通道；不得填入真实密码、token、银行卡、个人数据，不得提交真实订单、消息、权限变更或删除操作。
- 截图、trace、HAR、DOM、控制台和网络日志要脱敏并限制保存时间；禁止把 Authorization、Cookie、localStorage、完整请求体或个人数据写进 artifact。
- 测试完成后关闭 browser/context/page，清理临时数据和监听器；失败时保留最小必要证据，不能以清理失败掩盖原始失败。

## 测试前检查

确认应用可访问、健康接口与版本匹配，浏览器/Playwright 版本锁定，依赖安装可复现，测试服务器不会连接生产资源。先收集页面标题、版本标识、初始 console/page errors 和关键网络失败，再执行交互；若应用未运行、认证未授权或环境不确定，标记 `BLOCKED/NEEDS INVESTIGATION`，不猜测通过。

```javascript
import { test, expect } from "@playwright/test";

test("authorized smoke flow", async ({ page }) => {
  await page.goto("http://127.0.0.1:3000", { waitUntil: "domcontentloaded" });
  await expect(page).toHaveTitle(/expected app/i);
  await expect(page.getByRole("main")).toBeVisible();
});
```

示例地址、标题和账号必须替换为隔离环境的实际契约；不要把示例密码或未经审核的 URL 带入测试。

## 交互与断言

- 优先使用 `getByRole`、可访问名称、`getByLabel`、`data-testid` 等稳定选择器；不要依赖脆弱 CSS、DOM 深度、动画时序或本地化文本的偶然片段。
- 每个流程定义前置状态、动作、可观察结果、清理和副作用；断言用户可见文本、状态、URL、表单错误、下载/导航和后端 mock，而不只断言“没有抛异常”。
- 先做小而清晰的导航/渲染 smoke，再逐步验证表单、筛选、分页、上传、弹窗、键盘、错误恢复和跨视口流程；每个断言对应需求或缺陷编号。
- 使用 locator 自动等待和明确的 `expect`；只有在等待外部系统且理由可记录时才使用 bounded polling，禁止无边界 sleep 或无限重试掩盖 race condition。
- 对异步加载、动画、网络空闲和 debounce 设置合理 timeout；区分应用超时、测试选择器错误、环境故障和真实产品失败。

## 表单、认证与副作用

表单测试覆盖必填、格式、长度、边界、重复提交、服务端错误、取消、刷新和返回后状态。认证流程使用预置的合成 session 或隔离 identity provider，验证未登录、过期、越权和登出行为；不要通过读取或打印 cookie/token 来证明登录成功。

对创建、更新、删除、付款、发送、上传、权限和外部集成默认使用 dry-run、mock 或拦截请求；若确需写入，必须有精确授权、唯一测试数据、幂等键、影响上限和回滚/清理步骤。对话框和确认操作要验证取消、Esc、重复点击、过期和参数未被篡改；浏览器测试不能替代服务端授权测试。

## 控制台、网络与失败证据

在测试前注册 console、pageerror、requestfailed 和响应状态监听器，按页面/步骤关联事件；过滤 favicon、已知第三方噪声，并记录规则版本。对失败保存脱敏 screenshot、trace 或 DOM 摘要、当前 URL、视口、步骤、选择器、应用 build 和关键网络状态；不要自动保存全部 HAR 或页面 storage。

```javascript
const errors = [];
page.on("pageerror", error => errors.push({ type: "pageerror", message: error.message }));
page.on("requestfailed", request => errors.push({
  type: "requestfailed", url: new URL(request.url()).pathname,
  failure: request.failure()?.errorText
}));

try {
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByRole("status")).toHaveText(/saved/i);
} catch (error) {
  await page.screenshot({ path: "artifacts/failure.png", fullPage: true });
  throw error;
}
```

artifact 路径、文本和 URL 必须经过项目脱敏策略；错误重抛后由测试框架标记失败，不要捕获后继续报告成功。

## 响应式、可访问性与覆盖

选择代表性桌面、平板和移动视口，验证关键布局、导航、溢出、触控目标和横竖屏状态；不要把少数像素快照当作全部视觉质量。浏览器流程至少使用键盘和可访问 role/name 验证主要路径，并将自动化结果与屏幕阅读器/人工检查分开报告。

建立覆盖矩阵：角色 × 浏览器 × 视口 × 状态（首次、空数据、加载、错误、离线、权限拒绝）× 流程。记录已覆盖、未覆盖、环境限制、flaky 次数和证据链接；修复 flaky 应收敛状态/等待条件，不应盲目增加重试次数。

## 交付与质量门禁

报告包含应用 commit/build、环境 URL、浏览器/视口、测试账号类别、流程/需求、步骤、断言、结果、耗时、console/network 摘要、失败 artifact、已知限制和数据清理结果。把 observed、derived、unknown 分开，明确是否使用 mock、是否产生副作用、是否只验证前端。

- [ ] 目标环境、版本、浏览器、视口、账号、域名 allowlist 和授权已记录。
- [ ] 测试只使用合成数据/隔离资源，凭据、storage、请求和截图均已脱敏。
- [ ] 关键流程有稳定选择器、确定性等待、可见断言、错误路径和清理步骤。
- [ ] 未登录、越权、过期、重复提交、边界输入、网络失败和副作用确认路径已覆盖或明确未知。
- [ ] 失败有最小充分的截图/trace/console/network 证据，且真实失败不会被吞掉。
- [ ] 响应式、键盘/可访问性自动检查、浏览器矩阵、flaky 处理、报告和回滚/清理方案已评审。

## Related Skills

- `playwright-webapp-qa` - 做浏览器流程、网络和控制台诊断
- `screen-reader-testing` - 执行屏幕阅读器和键盘可感知性验证
- `chrome-devtools` - 用浏览器快照、网络和性能证据诊断问题
