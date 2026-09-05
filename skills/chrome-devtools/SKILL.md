---
name: "chrome-devtools"
display_name: "Chrome 浏览器诊断"
display_name_en: "Chrome DevTools Diagnostics"
description: "Use when inspecting an authorized live Chrome page, debugging console or network failures, capturing visual evidence, emulating conditions, or profiling browser performance with DevTools."
description_zh: "用于在已授权的 Chrome 页面上检查控制台、网络、视觉状态、环境模拟或浏览器性能，并形成可复核诊断证据。"
description_en: "Inspect authorized browser pages with snapshot-first navigation, console and network evidence, bounded script evaluation, screenshots, emulation, and performance traces without unsafe side effects."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized Chrome DevTools connector and explicitly scoped URL/session; form submission, file upload, external navigation, JavaScript evaluation, and data export require separate authorization"
---

# Chrome DevTools Diagnostics

使用 Chrome DevTools 对已授权页面进行浏览器自动化、故障排查、网络检查和性能分析。优先收集可复核证据，不把页面表象、时间相关性或单一控制台错误直接当作根因。

## 安全边界

- 开始前确认 URL、环境、登录会话、允许的域名、数据范围和目标；默认只访问本地、测试或明确授权的站点。
- 默认只读：导航、快照、截图、读取控制台/网络/性能数据。点击提交、删除、购买、发送消息、上传文件、改变设置或跨域导航必须单独授权。
- `evaluate_script` 仅执行最小、无副作用的 DOM/状态读取；不读取 localStorage 中的令牌，不执行任意注入代码，不绕过认证或 CSP。
- 截图、请求、响应、DOM 和控制台输出脱敏；不得分享 Cookie、Authorization、个人数据、客户内容或完整响应体。
- 不把 DevTools MCP 可用性当作生产安全保证；连接器、浏览器版本和目标页面均需记录。

## 会话与页面上下文

先列出页面并确认当前 tab、URL、来源和环境。多个页面之间切换时记录 page ID；导航或显著 DOM 变化后重新获取快照，因为元素 UID 可能失效。为等待设置有界超时，超时后报告页面状态和缺失证据。

## Snapshot-first 交互

定位元素时优先 `take_snapshot`，从可访问性树获取当前 UID，再执行最小的 click、fill、hover 或按键操作。操作前确认目标、输入值和副作用；输入使用合成或脱敏数据。操作后重新快照并核对可见状态、URL、请求和错误，不以“点击成功”代替业务结果验证。

## 故障排查

对页面失败同时检查：

1. 控制台消息：时间、级别、来源文件、重复次数和是否发生在目标操作之后。
2. 网络请求：方法、脱敏 URL、状态码、耗时、失败阶段、请求关联 ID 和必要的响应摘要。
3. 页面状态：快照中的可见错误、关键 DOM 状态和最小无副作用脚本读取。

将 4xx/5xx、CORS、DNS/TLS、超时、资源阻塞和前端异常分类；不要仅凭控制台错误声称后端根因。必要时比较成功与失败请求的差异，并记录缺失请求、缓存和重试影响。

## 性能与环境模拟

性能分析前记录浏览器版本、视口、网络/CPU 模拟、缓存状态和 URL。使用有界 trace，优先分析 LCP、CLS、INP、长任务、资源瀑布和布局变化；将实验条件与真实用户环境分开。模拟网络、CPU、地理位置或 viewport 只作用于当前授权会话，完成后确认已恢复或明确标记会话仍被修改。

## 证据交付

报告包含：目标与授权范围、页面/浏览器上下文、复现步骤、快照/截图/请求/控制台/trace 引用、观察事实、推断、未知项、时间线、影响范围和下一项安全检查。对每个结论标注 `observed`、`derived` 或 `unknown`；关联不等于因果。生产修复、配置变更、数据操作和外部发布另行授权。

## 质量门禁

- [ ] URL、域名、环境、会话和副作用范围已确认。
- [ ] 元素定位采用最新 snapshot，UID 未跨导航复用。
- [ ] 控制台、网络和页面状态已交叉检查，查询和等待有界。
- [ ] 性能结果包含浏览器、视口、模拟条件和缓存上下文。
- [ ] 脚本评估、表单、上传、导航和导出没有越权副作用。
- [ ] 证据脱敏，事实与推断分离，缺口和未知项可见。
