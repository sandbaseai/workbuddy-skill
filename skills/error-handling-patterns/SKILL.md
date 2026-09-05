---
name: "error-handling-patterns"
display_name: "错误处理模式"
display_name_en: "Error Handling Patterns"
description: "Use when implementing or reviewing error handling for applications, APIs, asynchronous workflows, retries, circuit breakers, graceful degradation, or distributed-system failures."
description_zh: "用于实现或审查应用/API 的错误处理、异步失败、重试、熔断、优雅降级和分布式系统故障边界。"
description_en: "Classify failures, choose exceptions or Result types deliberately, preserve safe context, clean up resources, handle async boundaries, and design bounded retry, circuit-breaker, and degradation behavior."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository and test-environment access; production fault injection, policy changes, data recovery, and external service actions require separate authorization"
---

# Error Handling Patterns

建立可预测、可诊断且不会泄露数据的失败处理。先分类错误和责任边界，再选择异常、Result、错误码或 Option；错误处理应恢复可恢复故障、快速暴露程序错误，并为调用方提供稳定契约。

## 范围和安全边界

- 默认只读审查代码、API 契约、日志策略、依赖、测试和运行指标；不触发生产故障、不重放真实请求、不改重试/熔断/告警策略。
- 错误、stack trace、请求 ID、输入摘要和上下文脱敏；不得记录 token、Cookie、密码、客户内容、完整请求体、支付信息或内部秘密。
- 只在能有意义处理时捕获错误；不要用全局 catch、空 catch、吞错或把所有异常映射为成功。
- 目标环境、错误预算、降级可接受范围、数据一致性和恢复授权必须明确；未知项标记 `unknown`。

## 分类与边界

先区分：

- 预期业务/校验失败：调用方可修正，使用稳定类型/Result 和字段级错误；
- 可恢复基础设施失败：超时、限流、临时网络/依赖不可用，使用有界重试、退避、熔断或降级；
- 不可恢复资源失败：内存耗尽、栈溢出、损坏状态，安全停止并报警；
- 程序缺陷：断言、空引用、违反不变量，保留根因证据，不伪装成正常业务失败。

为每个跨层边界定义所有者：谁发现、谁补充上下文、谁转换协议、谁决定重试/降级、谁向用户返回错误。一次错误应在合适层记录或转换，避免每层重复日志和重复计费。

## 异常、Result 与错误契约

异常适用于当前层无法正常继续的意外故障；Result/typed error 适用于调用方需要显式处理的预期失败；Option/Maybe 只表达“没有值”，不要隐藏错误。选择必须与语言惯例、调用图、性能和公共 API 兼容性一致。

内部错误类型至少包含稳定 code、可安全展示的 message、cause 分类、correlation ID、重试建议、HTTP/RPC 映射和敏感级别。对外消息不包含 stack trace、SQL、主机、路径或 secret；内部证据保存在受控系统并关联不可逆的请求标识。

## 上下文、清理与异步

在错误边界补充操作、组件、版本、相关资源和脱敏 correlation ID，保留原始 cause 和链路，不重复包装同一故障。使用 `finally`、context manager、defer 或等价机制释放连接、锁、临时文件、取消令牌和 tracing span；清理失败要有独立可见状态。

异步任务必须显式等待/收集、取消和传播错误，处理超时、取消、部分完成和重入。禁止未处理 promise rejection、后台任务静默失败、竞态覆盖错误或在取消后继续写入共享状态。

## 重试、超时、熔断和降级

仅对幂等或具备幂等键的瞬态错误重试；设置单次超时、总时限、最大次数、指数退避/抖动和预算，禁止嵌套重试造成放大。区分客户端取消、服务端超时、限流、认证失败和永久业务错误。

熔断定义 closed/open/half-open 条件、窗口、探测上限、恢复和告警；降级定义数据新鲜度、正确性、一致性和用户可接受边界。缓存、陈旧读、空结果和备用服务不能悄悄伪装成成功；对可能造成数据丢失、重复提交或安全绕过的降级默认 fail closed。

## 可观测性与验证

记录错误率、类别、延迟、重试次数、熔断状态、降级比例、取消/超时和恢复时间，但控制 cardinality 和敏感信息。测试正常、预期失败、依赖超时/限流、重试耗尽、熔断恢复、取消、部分失败、资源清理和错误契约兼容；使用合成故障或隔离环境，不用生产数据做故障注入。

## 交付报告

报告包含错误分类/状态机、层级责任、对外契约、上下文和日志字段、超时/重试/熔断/降级参数、幂等与一致性风险、测试证据、未覆盖场景和回滚/恢复要求。区分 `observed`、`derived`、`unknown`；任何生产注入、策略变更、数据恢复和外部操作列为需单独授权的后续动作。

## 质量门禁

- [ ] 预期、瞬态、永久、资源和程序错误已分类，责任边界清晰。
- [ ] 异常/Result/错误码选择有理由，公共错误契约稳定且对外脱敏。
- [ ] cause、correlation、资源清理和异步取消/传播可验证。
- [ ] 重试只作用于安全错误，超时/总预算/抖动/熔断/降级边界有依据。
- [ ] 降级不掩盖数据丢失、重复操作、安全绕过或陈旧性风险。
- [ ] 日志和指标可观测但不泄露敏感数据，测试覆盖失败与恢复状态。
- [ ] 未执行未授权生产故障注入、策略变更或数据操作。
