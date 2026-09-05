---
name: "subagent-driven-development"
display_name: "子 Agent 驱动开发"
display_name_en: "Subagent-Driven Development"
description: "Use when executing a multi-step implementation plan with independent tasks and each task needs isolated implementation, review, and final branch verification."
description_zh: "用于执行包含独立任务的多步实现计划，并需要每项任务隔离实施、评审以及最终分支级验证。"
description_en: "Execute independent plan tasks with fresh scoped workers, task-level specification and quality reviews, bounded fix loops, and a final whole-branch review while preserving authority and evidence boundaries."
category: "development"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized agent delegation, isolated worktrees or equivalent workspace boundaries, and a plan/ledger store; shared-branch pushes, merges, releases, and external side effects require separate authorization"
---

# Subagent-Driven Development

将实现计划拆成独立任务，由新鲜且范围受限的子 Agent 实施，再逐项进行规格符合性和代码质量评审，最后进行整分支评审。核心是隔离上下文、保留证据和在合并前发现问题，不是无条件增加并发。

## 前置条件和授权

- 只有在计划存在、任务边界独立、输入输出明确且每项都有验收信号时才使用；强耦合任务改用顺序执行。
- 每个计划拥有独立 worktree 或等价隔离目录。确认基线提交、当前分支、忽略规则、依赖和未提交改动，不覆盖其他人的工作。
- 默认子 Agent 只修改其任务范围并运行安全测试；不会自行创建子 Agent、审查其他任务、推送共享分支、合并、发布或触碰生产环境。
- 任务涉及密钥、生产数据、外部消息、部署、删除或共享分支写入时暂停该动作并升级授权；仅因流程“应该继续”不能越过安全门禁。

## 计划与进度账本

开始时记录计划路径、基线 SHA、任务列表、依赖关系、每项的执行 Agent、提交、测试、评审结果和 ruling。账本是恢复点，不依赖对话记忆。任务状态只能是 `pending`、`in_progress`、`review`、`complete` 或 `blocked`，且完成项不得重复派发。

派发提示只包含当前任务的完整需求文件、已确定的接口、范围决策、全局约束和报告路径；不要把历史对话或其他任务的结果复制进去。要求实施 Agent 返回状态、提交、测试摘要、风险，并把详细报告写入指定文件。

## 单任务循环

对每个任务按顺序执行：

1. 记录 `BASE`，读取任务 brief 和全局约束，确认任务不越界。
2. 派发一个新鲜、明确模型和权限的实施 Agent；同一时间不并行修改可能冲突的任务。
3. 实施 Agent 先建立失败信号或验收测试，再做最小改动、自测和自审，提交到隔离分支。
4. 生成从 `BASE` 到当前 HEAD 的审查包，派发独立任务评审 Agent，分别检查规格覆盖、接口、测试、安全、可维护性和范围漂移。
5. 若有发现，逐条记录严重性、证据和 ruling；最多进行有界修复轮次，每轮只解决明确发现并重新评审。无法证明修复正确时保持 `blocked`/`unknown`，不强行通过。
6. 评审通过后在账本写入提交、测试、覆盖范围和未解决低风险观察，再进入下一项。

评审意见与计划冲突时，以绑定规格为准并记录为何选择该 ruling 及错误成本。评审者不得因为测试全绿就忽略未覆盖的安全或权限边界。

## 最终整分支评审

所有任务完成后，从共同基线检查完整差异、跨任务接口、迁移顺序、回滚、依赖、文档、测试和安全边界。至少验证：任务证据齐全、临时调试工件已清理、没有越权文件或未登记改动、集成测试通过、计划与实现状态一致。整分支评审未完成前，不得声称实现完成。

## 失败、冲突和停止

- 子 Agent 请求上下文时补充最小事实，不粘贴整个会话；若任务本身有缺陷，修订计划并记录原因。
- 测试失败先回到任务范围和证据，不把多个猜测性修复打包；冲突使用隔离 worktree 和明确的整合步骤解决。
- 发现不可逆操作、安全敏感行为、超出授权的外部副作用或所有前进路径都依赖猜测时停止该动作并报告，而不是伪造完成。
- 任务完成不等于可以合并；共享分支 push、merge、tag、release 和删除分支是独立授权动作。

## 交付报告

报告计划和账本路径、基线/最终提交、每个任务的实施和评审证据、测试命令/结果、修复轮次、ruling、剩余风险、未覆盖范围、回滚方案和下一步授权。区分 `observed`、`derived`、`unknown`，不把子 Agent 的陈述当作未核验事实。

## 质量门禁

- [ ] 计划、任务边界、依赖、基线和隔离工作区已确认。
- [ ] 每项任务均有独立实施 Agent、测试证据和任务级规格/质量评审。
- [ ] 修复轮次有界，发现、ruling 和未解决风险可追踪。
- [ ] 最终整分支评审覆盖跨任务接口、安全、回滚、清理和集成测试。
- [ ] 没有子 Agent 越权派发、共享分支写入或外部副作用。
- [ ] 实现、合并、发布和删除动作的授权状态明确。
