---
name: "workflow-orchestration-patterns"
display_name: "工作流编排模式"
display_name_en: "Workflow Orchestration Patterns"
description: "Use when designing durable multi-step workflows across services, distributed transactions, long-running processes, human approvals, retries, compensation, or resumable failure recovery."
description_zh: "用于设计跨服务的持久工作流、分布式事务、长流程、人工审批、重试、补偿或可恢复失败流程。"
description_en: "Separate deterministic orchestration from side-effecting activities, design idempotent retries and Saga compensation, bound timeouts and payloads, and verify durable recovery without unsafe mutations."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized workflow/runtime metadata and an isolated test or time-skipping environment; external calls, approvals, provisioning, data changes, and production replay require separate authorization"
---

# Workflow Orchestration Patterns

为跨服务、长时间运行或需要恢复的流程设计持久编排。将确定性的状态机与执行外部副作用的 Activity 分离，明确重试、超时、补偿、人工介入和恢复证据；不要把普通 CRUD 或无状态请求包装成复杂工作流。

## 适用范围和边界

- 适合跨机器/服务/数据库的多步流程、需要断点恢复的长任务、分布式事务、基础设施流程和人工审批；简单 CRUD、纯批处理、实时流和普通 request/response 优先使用更简单的模式。
- 开始前确认工作流 ID、版本、状态/数据所有者、任务队列、环境、租户、超时预算、失败策略和副作用授权。
- 默认只读审查 workflow/activity 代码、契约、队列、指标、历史和测试；不启动生产执行、不调用外部 API、不写业务数据、不创建资源或批准人工动作。
- payload、日志、事件和搜索属性脱敏并设置大小/保留边界；不得放入 secret、令牌、完整客户内容或不必要的 PII。

## Workflow 与 Activity 分离

Workflow 负责确定性编排、状态转移、条件、计时器、信号、查询和子工作流；Activity 负责数据库、网络、文件、队列、邮件和其他外部副作用。Workflow 不直接调用外部 API、读取当前时间/随机数、启动线程或依赖不可重复的全局状态；使用运行时提供的确定性时钟、随机性和版本兼容机制。

每个 Activity 定义输入/输出 schema、所有者、幂等键、超时、心跳、重试策略、可重入范围、错误分类和补偿。短 Activity 应在秒到分钟级完成；长任务报告进度、支持取消并有总时限，不能无限等待。

## 状态、版本与确定性

将状态转移写成可审计的状态机，区分 `pending`、`running`、`waiting`、`succeeded`、`failed`、`compensating`、`cancelled` 和 `timed_out`。记录版本/变更 ID、事件顺序、信号来源和幂等去重结果。新增/修改 workflow 逻辑要考虑正在运行的旧实例，使用兼容版本、分支或迁移策略；不能仅依赖当前代码重放历史。

验证所有 workflow 路径可重放且结果一致，避免 wall clock、外部响应、未排序集合、线程竞态、语言运行时副作用和超过 payload 限制的数据。大对象放受控存储，工作流只传引用、摘要和不可逆关联 ID。

## 重试、超时和容量

为启动、执行、心跳、等待、总流程和人工审批分别设置有界超时。仅对瞬态且幂等的错误重试，配置最大次数、指数退避/抖动、总预算和不可重试分类；避免客户端、Activity 和下游同时重试造成放大。认证/授权、校验、版本冲突和不可逆副作用失败默认不自动重放。

监控工作流时长、Activity 失败率、重试次数、排队/待处理数、心跳丢失、补偿失败、取消和资源消耗。任务队列按租户/优先级/容量隔离，批量和子工作流只在能证明降低负载且不破坏顺序时使用。

## Saga、补偿与人工介入

对非原子分布式事务列出正向步骤、提交点、可补偿副作用、补偿顺序、不可补偿状态和人工升级条件。补偿必须幂等、可重试、有审计事件和最大次数；补偿失败不能伪装成原流程成功。明确最终一致性、用户可见中间状态、超时后的资源占用和取消语义。

人工审批使用不可伪造的 workflow/任务关联、审批人/角色、过期时间、最小权限和拒绝/撤回路径。审批、部署、付款、删除、权限变更和跨租户操作始终作为需单独授权的 Activity，WorkBuddy 不因“工作流已到下一步”自动执行。

## 测试和恢复验证

在隔离或 time-skipping 环境测试正常路径、重放、Activity 超时/重试、队列积压、worker 重启、重复信号、取消、版本兼容、部分完成、Saga 补偿和人工超时。使用合成输入和模拟外部服务，验证状态、事件、幂等结果和恢复点；不要用生产 replay 或真实副作用替代测试。

## 交付报告

报告包含用例选择、状态机、workflow/activity 边界、schema/payload、版本策略、队列/容量、超时/重试、幂等、Saga 补偿、人工审批、安全/租户隔离、观测指标、测试证据、未覆盖路径和恢复/回滚授权。区分 `observed`、`derived`、`unknown`，未验证的确定性或恢复能力不得声称已证明。

## 质量门禁

- [ ] 用例适合持久编排，状态、版本、租户、所有者和授权边界明确。
- [ ] Workflow 确定性，Activity 副作用、输入输出、幂等、错误和超时可追踪。
- [ ] 重试、心跳、总时限、payload、队列容量和取消语义有界。
- [ ] Saga 补偿、不可补偿状态、人工升级和最终一致性明确且可审计。
- [ ] 测试覆盖重放、重启、重复信号、失败恢复、版本兼容和补偿。
- [ ] 日志/事件脱敏，不执行未授权外部调用、审批、写入或生产 replay。
