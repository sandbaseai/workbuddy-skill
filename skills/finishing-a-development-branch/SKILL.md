---
name: "finishing-a-development-branch"
display_name: "完成开发分支"
display_name_en: "Finishing a Development Branch"
description: "Use when implementation is complete and you need to verify the merged result, integrate the branch safely, publish it, and remove only disposable development state."
description_zh: "用于开发工作完成后验证合并结果、执行安全集成与发布，并仅清理明确属于本次工作的临时分支或工作树。"
description_en: "Follow a test-first finish sequence: identify repository state, verify the target branch, integrate without force, rerun checks, publish, and clean up only proven disposable state."
category: "workflow"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with Git and repository-native tests; direct main publication is authorized only when the active task explicitly grants it"
---

# 完成开发分支

把“代码写完”与“安全集成并交付”分开。核心顺序是：确认状态 → 运行完整检查 → 核对目标分支 → 集成 → 在集成结果上复验 → 发布 → 只清理有明确归属的临时状态。

## 1. 集成前门禁

先固定当前 commit、分支、工作树路径、远端和目标分支，保存状态快照：

```bash
git status --short --branch
git branch --show-current
git worktree list
git log -1 --oneline
git fetch --prune origin
```

运行仓库完整测试和与任务相关的 lint、构建、打包、生成器及安全检查。之前某次运行通过，只能证明当时的树；任何修改、rebase、merge 或生成文件变化后都要在即将集成的结果上重跑。

测试失败时停止集成，保留现场，记录失败命令和输出；不要以“可能是 flaky”为理由继续，也不要通过降低阈值、跳过测试或删除断言来制造绿色结果。

## 2. 确认集成对象

明确：

- 当前工作是否处于正常仓库、命名分支、独立 worktree 或 detached HEAD；
- 目标分支及其当前远端 commit，不能凭习惯猜测；
- 工作分支相对目标分支的提交范围、未提交文件、未跟踪文件和可能被覆盖的修改；
- 发布、合并、标签、外部通知和生产变更分别需要哪些授权。

当目标分支不明确、远端已经移动、存在未提交用户文件或合并会覆盖不属于本次工作的改动时，暂停并报告风险；不要 force push、硬重置、强制删除或覆盖用户工作。

## 3. 安全集成与复验

在已获授权且目标明确时：

1. 先获取目标分支最新状态，确认没有未预期的远端差异；
2. 使用普通 merge/rebase 或仓库规定的集成方式，保留冲突上下文和来源；
3. 解决冲突时逐项判断，不用“选一边”掩盖行为变化；
4. 在最终集成树上重新运行完整测试、构建、目录/文档生成和安全门禁；
5. 对照 diff、版本号、发布工件、来源指纹和文档，确认没有临时文件、秘密或内部约束泄露；
6. 只在复验通过后推送、打标签、发布或通知。

本仓库若已明确授予直接 main 路径，可在验证后直接推送 main 并按仓库发布流程打标签；没有该授权时只准备集成结果，不擅自创建外部合并请求或发布。发布成功不等于可以删除来源分支。

## 4. 清理边界

只清理本次工作创建且已证明不再需要的开发状态：

- 合并成功、远端发布成功并且没有未提交内容后，才考虑删除对应临时分支；
- 只有明确属于本次工作的 `.worktrees/` 或 `worktrees/` 工作树才可移除；宿主环境管理的工作树保留；
- 移除前检查 `git status --porcelain -uall`、未跟踪文件、未提交计划和是否存在唯一副本；
- 工作树含有只存在于其中的文件时，不使用 `--force`，先保留并记录；
- 不删除 fork、远端分支、标签、发布资产或用户文件，除非目标和删除授权明确且可恢复范围已记录。

如果推送被拒绝，先 fetch 并审查远端变化；不要用 force push 绕过保护。若集成结果失败，停止发布和清理，保留分支与工作树供修复。

## 交付检查表

```markdown
# Branch Finish Handoff

Source: <branch/worktree and commit>
Target: <branch and remote commit>
Integration: <merge/rebase/direct-main path>
Verdict: PASS | PASS WITH CAVEATS | FAIL

## Checks
- Pre-integration tests: <commands/results>
- Integrated-tree tests: <commands/results>
- Build/package/docs/security: <commands/results>
- Remote/tag/release: <evidence>

## Cleanup
- Removed: <exact disposable paths, or none>
- Preserved: <uncommitted/user-owned state>

## Risks and missing evidence
- <conflict, remote drift, skipped check, or residual risk>
```

只有集成树完整通过且远端证据匹配时才写 `PASS`；缺失检查、未验证发布、冲突未解释、状态不清或存在潜在用户数据损失时必须写 `FAIL` 或明确的 `PASS WITH CAVEATS`。本 Skill 的报告不替代生产变更、外部通知和删除动作的授权。

## Related Skills

- `release-traceability` - 记录版本、工件、环境和发布证据
- `merge-conflict-resolution` - 处理冲突并验证行为未被静默改变
- `constraint-driven-development` - 定义集成前后的质量门禁
