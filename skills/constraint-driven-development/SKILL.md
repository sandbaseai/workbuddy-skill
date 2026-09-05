---
name: "constraint-driven-development"
display_name: "约束驱动开发"
display_name_en: "Constraint-Driven Development"
description: "Use when a project needs a written, measurable quality bar that agents and CI can enforce without quietly weakening tests, security, performance, accessibility, or architecture checks."
description_zh: "用于为项目建立可书面记录、可度量、可执行的质量门槛，防止 Agent 为了变绿而降低测试、安全、性能、可访问性或架构标准。"
description_en: "Interview for the quality dimensions that matter, record commands and thresholds in a durable contract, wire checks to the right lifecycle stage, and detect weakened gates or unfinished work."
category: "development"
version: "0.1.0"
author: "addyosmani/agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with repository source, tests, CI and configuration access; adding tools, changing gates, installing dependencies, and modifying protected workflows require explicit project authorization"
---

# 约束驱动开发

将“什么才算足够好”从对话中的隐含判断变成项目内可持续检查的书面契约。规格说明定义要做什么，测试证明它能工作，本 Skill 定义发布前不能低于什么质量线，并防止 Agent 通过删测试、降阈值或关闭检查换取绿色结果。

## 何时使用

- 新项目或大型功能没有写下质量门槛；
- 团队要定义测试、安全、性能、可访问性或架构标准；
- CI 有检查但没人知道哪些会阻塞合并；
- 自动化 Agent 频繁跳过测试、添加抑制注释或把阈值调低；
- 需要为覆盖率、性能预算或依赖漏洞设定可复现数字。

如果项目已经有 `CONSTRAINTS.md`，先读取并遵守；不要在一次性脚本、短期原型或用户只要求即时代码评审时强行建立整套约束。

## 核心边界

- 先调查仓库现状再提问：语言、测试、lint、覆盖率、CI、Agent 配置和已有文档都是证据。
- 非交互场景（CI、自动循环、无人值守批处理）不得假装完成访谈；使用下方 Floor，并把需要负责人选择的项目列为待决。
- 不擅自安装依赖、提高/降低门槛、改保护分支、跳过失败检查或编辑外部 CI；这些是独立变更，需要项目授权。
- 约束文件只记录质量契约，不放凭据、客户数据、私有提示词或内部机密。公开仓库中只发布可对外的原则和脱敏示例。
- 检查只能证明其定义的范围；不要把单元测试通过写成安全、性能或生产可用性已证明。

## Step 1：先探测，不重复提问

读取以下位置（存在才读）：

| 项目 | 证据位置 |
|---|---|
| 语言与技术栈 | `package.json`、`pyproject.toml`、`go.mod`、`Cargo.toml` |
| 测试运行器 | 依赖、脚本、测试目录、覆盖率产物 |
| 现有 lint | ESLint/Biome/Ruff/静态分析配置 |
| CI | `.github/workflows/`、`.gitlab-ci.yml` |
| Agent 入口 | `AGENTS.md`、`.claude/`、`.codex/`、WorkBuddy 配置 |
| 质量现状 | 最近测试结果、基线指标、例外记录和分支保护 |

用两三句话报告发现，然后只追问没有证据覆盖的内容。记录仓库提交 SHA 和检查运行环境，避免把另一分支的结果当基线。

## Step 2：最多四个质量访谈问题

按一问一答询问，并给出默认值：

1. 除基础底线外，哪些维度需要强制：新代码覆盖率、安全扫描、性能、可访问性、架构边界？默认选择已有测试和安全扫描。
2. 检查失败时阻塞还是告警？默认底线阻塞，其余新门槛先告警再观察。
3. 已有目标数字，还是测量现状并保持不下降？默认测量现状并建立 ratchet。
4. Agent 任务结束前可接受最慢检查多久？默认约 90 秒；更慢的检查放到 CI。

停止在四个问题。回答“不知道”也要成为明确默认或 `TBD`，不能无限扩大 intake。

## Step 3：建立约束契约

在仓库根目录创建或更新 `CONSTRAINTS.md`，记录确认的项目专属标准：

```markdown
# Constraints

Last reviewed: <date> by <owner>

## Floor (always enforced)
- 不新增静默失败或秘密；
- 不新增未实现 stub、空 catch 或无理由跳过/删除测试；
- 不为让检查通过而削弱本文件。

## Enforced with numbers
| Dimension | Rule | Checked by | Runs at | Owner |
|---|---|---|---|---|
| Types | zero errors | <repository command> | edit/task/CI | <owner> |
| Secrets | no findings | <redacted scanner> | task/CI | <owner> |

## Measured, not yet enforced
| Metric | Today | Direction | Source |
|---|---:|---|---|

## Exceptions
| ID | Rule | Path | Reason | Owner | Expires |
|---|---|---|---|---|---|
```

每一行数字必须有产生 verdict 的命令；只有愿望而没有检查器的是目标，不是门禁。例外必须有原因、owner 和过期时间，不得成为永久旁路。若项目维护 Agent 指令文件，补充“写代码前读取约束，不得为通过变更而削弱约束”的公开原则。

## Step 4：选择检查和默认阈值

优先复用仓库已有工具，并为每个维度写清命令、范围和阶段：

| 维度 | 常见机制 | 默认起点 |
|---|---|---|
| 类型/lint | 现有编译器和 lint 配置 | 零错误 |
| 新代码覆盖率 | 现有测试 runner + diff | ≥ 80%（未准备好则先保持当前基线） |
| 代码安全 | Semgrep/同类扫描 | 无 high finding |
| 秘密 | gitleaks 等 | 无 finding，始终 redact |
| 依赖安全 | OSV 等数据库 | 无 high 或更高 |
| Web 性能 | Lighthouse/实测 | LCP ≤ 2500ms，CLS ≤ 0.1 |
| 可访问性 | axe 或等效运行时检查 | 零 critical/serious |
| 架构 | dependency-cruiser 等 | 零已知违规 |

不要机械安装所有工具：Lighthouse 和 axe 需要可访问 URL，CLI/库项目应说明不适用；昂贵扫描应限于变更文件或移到 CI。安全扫描使用脱敏模式，报告规则和位置，不报告秘密值。

## Step 5：接入正确生命周期

不要把所有检查都塞进每次编辑环节：

| 阶段 | 内容 | 目标 |
|---|---|---|
| 快速反馈 | 类型、lint、秘密、Floor | 秒级，尽量 diff-scoped |
| 任务验证 | 相关测试、变更覆盖率、契约检查 | 约 90 秒内 |
| Review/CI | 完整安全、依赖、架构、性能和回归 | 可较慢但必须可复现 |
| 发布 | 方向检查、全量门禁、产物与回滚证据 | 不绕过失败 |

命令应进入项目自己的 script/Make target/CI，而不只存在于 Agent 记忆中。约束文件是带理由的 canonical source，脚本只是执行入口；两者冲突时报告并修复漂移。

## Step 6：检查质量线是否被削弱

在 review 时比较分支起点与当前 diff，重点检查：

1. 阈值、严重级别、检查路径或 CI 阶段被调低/移除；
2. 测试被 `.skip`、删除，或断言被抽掉；
3. 新增 `@ts-ignore`、`eslint-disable`、`# noqa`、`istanbul ignore`、`Stryker disable`、`nosemgrep`、`gitleaks:allow` 等抑制；
4. 用 `throw Not implemented`、空 catch、TODO 占位或静默 fallback 掩盖未完成工作；
5. 新增未讨论、无 owner 或无过期时间的例外。

收紧门槛通常不需要额外审批；放松门槛必须显式记录理由、影响、owner、期限和替代控制。至少保留一项不完全由 Agent 自己定义的外部检查，例如漏洞数据库、浏览器测量或标准化可访问性规则。

## Step 7：Ratchet 与例外治理

如果现状覆盖率是 62%，直接要求 80% 会制造永久红灯。先记录当前值并要求不下降，之后每次改善再提高基线。对每个数字记录来源、采样范围、容忍度、更新时间和 owner；不能用改变分母或删除失败样本制造“提升”。

例外应最小化到路径和规则，写明补救任务和过期时间。到期自动转为失败或重新评审；未授权的临时关闭不算完成。

## 完成交付前检查

- [ ] 现有栈、测试、lint、CI 和质量基线已有证据。
- [ ] 关键选择有 owner；未知项和默认值被明确标记。
- [ ] `CONSTRAINTS.md` 每条数值规则都有可执行命令和阶段。
- [ ] Floor 阻止秘密、静默失败、未实现 stub、无理由删/跳测试和自我削弱。
- [ ] 检查按成本分层，适用性和数据/权限边界已说明。
- [ ] diff 未降低阈值、删测试、添加未经批准的抑制或永久例外。
- [ ] ratchet、例外过期、失败处理和恢复路径可追踪。
- [ ] 结果只声称已被实际证据覆盖的范围。

## Related Skills

- `test-driven-development` - 以 RED/GREEN/REFACTOR 建立行为回归
- `github-actions-hardening` - 审计 CI 触发器、权限和供应链
- `skill-quality-audit` - 审查 Skill 本身的结构、边界和可执行性
