---
name: "screen-reader-testing"
display_name: "屏幕阅读器测试"
display_name_en: "Screen Reader Testing"
description: "Use when validating web application compatibility with screen readers, debugging ARIA or form accessibility, or verifying announcements and keyboard navigation for assistive technology users."
description_zh: "用于验证 Web 应用与屏幕阅读器的兼容性，排查 ARIA、表单、动态播报和键盘导航的无障碍问题。"
description_en: "Test page structure, landmarks, headings, focus, forms, errors, dynamic announcements, and custom widgets with a declared screen-reader/browser matrix and evidence-backed fallbacks."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized browser/test environment and, where available, VoiceOver, NVDA, JAWS, TalkBack, or Narrator; form submission, uploads, external navigation, and production testing require separate authorization"
---

# Screen Reader Testing

验证 Web 页面是否能被屏幕阅读器理解、导航和操作。关注可访问性树、语义结构、焦点、表单错误、动态状态和自定义组件；自动化结果是证据的一部分，不能替代真实辅助技术体验。

## 范围和安全边界

- 开始前声明目标 URL、环境、浏览器/屏幕阅读器组合、登录会话、数据范围和验收标准；优先本地、测试和合成数据。
- 默认只读检查页面结构、键盘焦点、可访问性树和视觉/控制台证据。提交表单、上传、支付、发送消息、跨域导航和生产测试需单独授权。
- 不把 ARIA 属性数量、自动化扫描通过或一台组合的结果当成完整合规证明；记录工具、版本、未覆盖项和人工验证状态。
- 截图、DOM、快照、朗读记录和网络数据脱敏，不保存令牌、Cookie、客户内容或个人数据。

## 测试矩阵

为项目选择并记录实际可用的组合，例如：

| 组合 | 重点 |
|---|---|
| VoiceOver + Safari（macOS/iOS） | Rotor、地标、标题、焦点和动态播报 |
| NVDA + Firefox/Chrome（Windows） | Browse/Focus mode、元素列表、表单和错误 |
| JAWS + Chrome（Windows） | 企业场景和复杂组件兼容性 |
| TalkBack + Chrome（Android） | 触摸探索、手势、焦点和移动 viewport |
| Narrator + Edge（Windows） | Windows 原生辅助技术路径 |

若无法运行真实屏幕阅读器，使用浏览器可访问性树、键盘序列和静态规则作“部分证据”，明确标注 `[TODO: real assistive-technology validation]`，不得声称已完成屏幕阅读器验证。

## 页面加载和结构

在页面加载完成后检查并记录：标题是否有意义，是否存在唯一且正确的主地标，跳过链接是否可用，标题层级是否表达内容结构，地标是否有清晰名称，语言/方向是否正确。使用屏幕阅读器的标题、地标和链接列表逐项导航；发现重复、跳级、空名称或隐藏重要内容时保留页面与节点证据。

## 键盘、焦点和组件

仅使用键盘完成 Tab/Shift+Tab、Enter、Space、Esc 和方向键路径。检查顺序、可见焦点、跳转、模态框焦点陷阱/返回、菜单/组合框/树/表格的角色和状态。每次 DOM 或导航变化后重新获取快照，不跨页面复用节点标识。

自定义组件必须验证角色、名称、值、状态和可操作方式；不要用 `div` 点击处理代替原生按钮/链接，除非补齐等效键盘和辅助技术语义。确认禁用、展开、选中、加载和错误状态被正确播报。

## 表单和错误

对每个字段确认可关联 label、用途/格式说明、必填状态、输入类型、错误关联和恢复路径。用合成无效输入提交测试环境表单，验证错误文本被播报、`aria-invalid` 和 `aria-describedby` 关系正确、焦点移动到合理位置且不会丢失用户输入。记录真实提交是否被授权；未授权时只验证本地校验或拦截路径。

## 动态内容和异步状态

触发搜索、加载、通知、验证、对话框和列表更新，检查加载状态、成功/失败结果和变化是否以适当的 live region/状态被播报，且不会重复或打断重要朗读。将“DOM 内容改变”与“用户听到了有用提示”分开记录；确认无障碍名称不会被视觉装饰或隐藏文本污染。

## 证据和交付

报告包含测试矩阵与版本、页面/提交、键盘步骤、可访问性树快照、屏幕阅读器口述观察、缺陷复现、严重性、影响范围、自动化/人工覆盖、未知项和修复后复验。每条结论标记 `observed`、`derived` 或 `unknown`，引用具体节点/步骤；将 WCAG 或团队标准映射作为独立证据，不从单个工具结果推导合规结论。

## 质量门禁

- [ ] URL、环境、矩阵、版本、会话和副作用范围明确。
- [ ] 标题、地标、跳过链接、键盘焦点、组件角色/状态均已检查。
- [ ] 表单 label、必填、错误关联、焦点和数据保留已验证。
- [ ] 动态加载、通知、模态框和 live region 的用户可感知结果已检查。
- [ ] 真实屏幕阅读器与自动化/静态证据明确区分，未覆盖项可见。
- [ ] 测试数据和证据已脱敏，未执行未授权生产或外部副作用。
