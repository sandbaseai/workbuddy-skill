---
name: "bug-reproduction-brief"
display_name: "缺陷复现简报"
display_name_en: "Bug Reproduction Brief"
description: "Use when a bug report is vague, intermittent, environment-specific, or mixed with an assumed cause, and a minimal evidence-backed reproduction is needed before diagnosis or repair."
description_zh: "用于缺陷描述模糊、间歇性、环境相关或夹杂假设原因的场景，在诊断或修复前建立最小且有证据支撑的复现。"
description_en: "Turn an incomplete report into a minimal, repeatable, redacted reproduction with explicit expected and actual behavior, environment facts, evidence, unknowns, and a safe next hypothesis."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository and test-environment access; production data changes, implementation edits, external issue publication, and remediation require separate authorization"
---

# Bug Reproduction Brief

把模糊、间歇性或环境相关的缺陷报告收敛成最小、可重复、可复核的失败证据。交付物是复现简报，不是根因结论，也不是修复补丁。

## 边界与授权

- 默认先进行只读检查：读取代码版本、测试配置、日志和锁文件，并在本地或已授权的测试环境复现。
- 不修改实现代码、生产数据、共享环境配置、依赖锁文件或缺陷状态；不为了复现执行破坏性操作。
- 目标仓库、提交、环境、数据范围和允许的命令必须明确。无法确认时记录 `unknown`，不猜测生产配置或凭据。
- 日志、请求和 fixture 脱敏；不得复制令牌、Cookie、授权头、客户记录或不必要的个人数据。

## 记录已观察失败

先记录原始观察，不把假设原因写进事实：

```text
Observed at: [timestamp and timezone]
Target: [route, command, test, component]
Input: [smallest known input, redacted]
Expected: [observable result]
Actual:   [observable result, status, error, or trace]
```

将二手描述、推测和无法复核的截图标为 `unverified`。保留提交 SHA、命令、退出码和相关证据引用。

## 固定环境事实

只记录可检查的事实：仓库和提交、操作系统/容器、运行时、包管理器、锁文件摘要、相关 feature flag，以及 local/test/staging/production 环境。比较环境时逐项列出差异；不要把“看起来相同”当成证明。

## 收敛最小复现

从原始路径开始，逐次移除无关数据、服务、步骤、并发和配置。每次只改变一个变量：

1. 先在隔离环境用最小输入、最小 fixture 或独立测试运行。
2. 若仍失败，记录命令、版本、输出和被移除条件。
3. 若失败消失，恢复最后移除的条件，确认它是否是必要条件。
4. 优先使用本地测试、合成数据和最小安全请求；不要直接改写生产数据来“制造”复现。

记录已排除的变量和仍未排除的变量，防止把一次巧合当成最小条件。

## 验证重复性

在安全且授权的范围内至少运行两次最小复现，保存每次的输入摘要、开始/结束时间、输出、退出码和环境。间歇性问题报告观察频率、持续时间、样本量和失败窗口；不要把偶发成功称为修复，也不要把一次失败称为确定性。

如果无法复现，交付“未复现”状态及缺少的观测、环境或数据，不要编造根因。时间关联只能作为下一假设，必须与独立证据区分。

## 停止条件与交付

达到以下任一条件就停止复现工作：已得到两次一致的最小失败、已确认间歇性失败的可量化模式，或在安全范围内仍无法复现。不得在建立简报期间修改实现，以免破坏证据并混合诊断与修复。

简报至少包含：

- 目标、提交和授权环境；
- Expected / Actual；
- 最小步骤、fixture 和命令证据；
- 重复性结果与样本信息；
- 已排除条件、未知项和限制；
- 一个可证伪且安全的下一假设；
- 明确列出的后续诊断/修复授权需求。

## 质量门禁

- [ ] 事实、假设、未知和二手描述已分开。
- [ ] 期望行为与实际行为均可观察、可复核。
- [ ] 环境、提交、锁文件和 feature flag 有证据。
- [ ] 复现逐变量缩减，最小 fixture 未包含敏感数据。
- [ ] 重复性、样本量或“未复现”状态诚实记录。
- [ ] 未修改实现、生产数据或共享配置。
- [ ] 报告脱敏，并在复现交付处停止。
