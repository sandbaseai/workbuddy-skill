---
name: "writing-plans"
display_name: "实现计划编写"
display_name_en: "Writing Implementation Plans"
description: "Use when a specification or requirements describe a multi-step implementation and a file-specific, testable plan is needed before editing code."
description_zh: "用于需求或规格涉及多步实现时，在修改代码前生成按文件拆分、可测试、可执行的实现计划。"
description_en: "Turn a specification into a scoped implementation plan with file responsibilities, interfaces, bite-sized testable tasks, constraints, rollback, and self-review evidence."
category: "productivity"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository read access and a scoped plan output location; code changes, commits, deployments, and external coordination require separate authorization"
---

# Writing Implementation Plans

在修改代码前，把规格和需求转换成能由陌生工程师执行的实现计划。计划必须说明改哪些文件、接口如何衔接、每一步如何验证，以及哪些动作需要额外授权；计划本身不代表代码已经实现。

## 范围和授权

- 先确认目标、非目标、验收标准、约束、依赖、截止时间和计划保存位置；多子系统需求拆成可独立验证的子计划。
- 默认只读分析规格、仓库结构、现有约定、测试入口和 Git 状态；不修改代码、不创建分支、不安装依赖、不提交或部署。
- 不把 README、愿望或未批准的设计当成实施事实。冲突写为 `unknown` 或 `[ASK USER]`，不要擅自选择高影响方案。
- 计划中可展示命令，但标注副作用、环境和预期结果；敏感配置只写名称和脱敏摘要。

## 计划头部

计划开头必须包含：

```markdown
# [Feature Name] Implementation Plan

**Goal:** [one sentence]
**Architecture:** [approach and boundaries]
**Tech Stack:** [verified technologies]
**Spec:** [exact specification path or source]

## Global Constraints
- [exact version/platform/security/authorization constraints]
```

同时记录调查提交、仓库范围、未覆盖目录、依赖前提和回滚/停止条件。

## 先画文件和接口地图

在拆任务前列出每个将创建、修改、删除和测试的精确路径，并说明单一责任。对每个跨任务接口写明：输入、输出、错误、所有权、兼容性和调用方。遵循仓库现有结构，不因为计划方便而无授权重构。

## 任务颗粒度

每个任务必须能独立审查和测试，优先按以下顺序拆成小步骤：

1. 写一个针对具体行为的失败测试或可观察验收信号。
2. 运行它确认失败，并记录命令、输出和环境。
3. 写最小实现或配置变更，明确不包含的范围。
4. 运行单测、集成测和必要的静态门禁确认通过。
5. 检查差异、回滚路径和副作用；提交动作仅作为需授权的最后一步。

每个步骤包含 `Files`、`Interfaces`、`Consumes`、`Produces`、确切命令、预期结果、失败处理和完成证据。代码步骤给出足够的伪代码/签名/数据形状，不能写“适当处理边界情况”“之后补测试”或“实现类似功能”这种占位语句。

## 约束、依赖和风险

把全局约束逐字带到每个任务的隐含前提中：版本下限、平台、性能、许可证、安全和数据边界。区分生产依赖与开发工具，记录新增依赖的来源、锁定策略和许可证。对数据库迁移、接口兼容、权限扩张、外部 API、生成文件和回滚制品建立明确门禁。

## 自审与验收

计划完成后执行自审：

- 逐段对照规格，列出每项需求对应的任务和证据；
- 搜索 `TBD`、`TODO`、`later`、`appropriate`、`similar` 等占位或模糊表述并消除，真实未知改写为 `[TODO]`；
- 核对任务间的函数名、字段、类型、路径和版本一致；
- 确认测试覆盖成功、失败、权限、兼容和回滚路径；
- 标出规格意图与当前仓库现实的差异、需要用户决定的 `[ASK USER]` 项和不可安全执行的动作。

交付时给出计划路径、任务清单、验证命令、风险/回滚、所有问题和明确的“计划完成但实现未执行”状态。若需求允许直接实施，由后续执行流程读取计划并在每个检查点重新验证，而不是把计划当作批准。

## 质量门禁

- [ ] 目标、非目标、验收标准、约束、规格来源和调查提交明确。
- [ ] 文件、责任、接口、依赖和任务顺序具体到路径/签名/数据形状。
- [ ] 每个任务有失败信号、最小实现、验证命令、预期结果和回滚边界。
- [ ] 没有模糊占位语句；未知和需要意图的决定分别标记。
- [ ] 成功、失败、权限、兼容性和回滚路径有覆盖。
- [ ] 没有执行未授权代码或外部副作用，计划与实现状态明确区分。
