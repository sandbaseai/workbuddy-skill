---
name: "systematic-debugging"
display_name: "系统化调试"
display_name_en: "Systematic Debugging"
description: "Use when encountering a bug, test failure, performance regression, build failure, integration issue, or unexpected behavior before proposing or applying a fix."
description_zh: "用于处理缺陷、测试失败、性能回归、构建失败、集成问题或其他异常行为，在提出或实施修复前完成系统化根因调查。"
description_en: "Build a red-capable feedback loop, trace evidence to the originating boundary, compare working and broken paths, test one falsifiable hypothesis at a time, and fix only after root cause is supported."
category: "development"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository, test, and diagnostic access; production instrumentation, implementation edits, deploys, and architectural changes require separate authorization"
---

# Systematic Debugging

用可重复的反馈回路和证据追踪定位根因。核心规则是：在根因调查完成前，不提出“顺手修一下”的补丁；症状修复不能替代根因证据。

## 总原则与安全边界

- 先收集错误、复现、数据流和边界证据，再形成假设；不要用直觉或时间相关性代替调查。
- 默认只读检查代码、配置、日志、提交历史和测试入口；生产数据、共享环境、部署配置和外部服务不因调试而被修改。
- 目标仓库、提交、环境、命令和授权范围必须明确。输出中的命令、日志、请求和抓取工件先脱敏。
- 调试日志、临时 fixture、回放数据和 instrumentation 必须有唯一标记、范围和清理计划，不能包含密钥或客户数据。
- 每次只改变一个变量。若连续三次修复尝试都暴露新问题，停止继续堆补丁，转而评估架构、共享状态和耦合，并单独请求架构决策授权。

## 阶段一：建立红色反馈回路

先建立一个已经运行过、能捕获用户准确症状的命令或测试：优先是失败测试，其次是带断言的 HTTP/CLI、浏览器脚本、受控 trace 回放、最小 harness 或属性测试。它必须：

- 能沿真实代码路径触发该症状，而不是只证明程序没崩；
- 有确定或可量化的失败 verdict，运行时间有界，可无人值守；
- 记录命令、提交、环境、输入摘要、输出、退出码和脱敏证据。

间歇性问题提高复现率并记录样本量、失败频率和时间窗口；无法建立回路时明确写出已尝试项和缺失的日志、HAR、trace、环境或授权，不凭空继续猜测。

## 阶段二：根因调查与数据流追踪

完整读取错误消息、警告和 stack trace，检查相关提交、依赖、配置和环境差异。多组件系统要在每个边界记录输入、输出、配置传播和状态，先确定断点在哪一层，再深入该层。

对于深层错误逆向追踪：坏值从哪里产生？谁把它传入当前函数？上游的哪个转换、默认值、竞态或外部输入首次引入它？持续追踪到第一个可验证的来源，而不是在最后一个报错点加保护分支。

## 阶段三：模式比较

找到同一代码库中可工作的相似路径，与失败路径逐项比较：调用者、输入、配置、依赖版本、状态生命周期、并发、超时和权限。若依赖参考实现，先完整阅读并记录版本与差异；不要因“看起来不相关”而跳过小差异。

## 阶段四：假设和最小测试

形成一个具体、可证伪的假设，例如：“若配置传播是根因，则在边界 B 检查值 X 会观察到缺失；补齐 X 后回路应变绿。”每次只测试一个预测，记录结果和置信度。假设被否定后回到证据阶段，不在原补丁上继续叠加。

测试前可生成 3–5 个候选根因供排序，但不得把候选列表写成已确认结论。每个探针必须对应一个预测；性能问题先建立时间/资源基线，再分析瓶颈。

## 阶段五：修复与回归

根因有证据支持后，在正确的测试 seam 写失败回归测试，先观察它失败，再实施单一根因修复。重新运行最小回路、原始未缩减场景和相关测试，核对没有引入其他回归。没有合适测试 seam 本身就是架构发现，应记录而不是制造虚假覆盖。

修复阶段仍需独立核验：清理 `[DEBUG-...]` 日志和临时 harness，检查差异范围，确认生产或共享环境没有未授权变更，并把已确认根因、证据和未解决风险写入交付说明。

## 交付报告

报告区分 `observed`、`derived`、`hypothesis` 和 `unknown`，包含症状、红色回路、环境/提交、根因追踪、工作/失败路径差异、假设测试、修复与回归证据、清理结果、限制和下一步。若问题确实是外部或环境因素，说明调查覆盖和支持证据，不把“没有找到”写成“没有根因”。

## 质量门禁

- [ ] 已运行过能捕获准确症状的有界、可重复或可量化反馈回路。
- [ ] 错误、环境、最近变更、组件边界和数据来源有证据。
- [ ] 工作路径与失败路径逐项比较，假设可证伪且一次只测一个变量。
- [ ] 根因追踪到第一个可验证来源，而非只处理最后一个症状。
- [ ] 回归测试先失败后通过，原始场景和相关测试均已复核。
- [ ] 三次失败后没有继续堆补丁，架构问题单独升级。
- [ ] 日志、fixture、工件已清理，报告脱敏且未产生越权副作用。
