---
name: "api-design-principles"
display_name: "API 设计原则"
display_name_en: "API Design Principles"
description: "Use when designing, reviewing, documenting, versioning, or migrating REST or GraphQL APIs and their client, security, performance, and compatibility contracts."
description_zh: "用于设计、评审、记录、版本化或迁移 REST/GraphQL API，并明确客户端、安全、性能与兼容性契约。"
description_en: "Design resource-oriented REST and schema-first GraphQL APIs with explicit HTTP semantics, error contracts, pagination, idempotency, authorization, versioning, and bounded query cost."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository/specification access and an approved API test environment; production writes, migrations, client notifications, and traffic-policy changes require separate authorization"
---

# API Design Principles

设计可理解、可演进、可验证的 REST 或 GraphQL API。先建立资源、契约和兼容性边界，再讨论实现；不要把数据库结构、单个客户端便利或未经授权的线上行为直接变成公共 API。

## 范围和安全边界

- 明确 API 所有者、消费者、环境、身份/租户模型、数据分类、SLO、兼容窗口和变更授权。
- 设计与评审默认只读规格、schema、现有调用、契约测试、指标摘要和脱敏样例；不向生产发送写请求、不迁移数据、不改限流/WAF/权限策略。
- 请求/响应示例使用合成数据，隐藏令牌、Cookie、个人数据、内部主机名和完整错误堆栈。
- 将设计决策、观察事实、推导和未知分开；没有消费者或业务意图证据时标记 `[ASK USER]`/`[TODO]`，不要猜测。

## 资源与 HTTP 语义

REST 路径使用稳定的资源名词和层级，动作由 HTTP 方法表达：`GET` 安全且幂等，`POST` 创建或非幂等动作，`PUT` 全量替换且幂等，`PATCH` 局部更新，`DELETE` 删除且应可重复处理。若业务动作不适合资源模型，显式记录命名和幂等性理由，不用含糊的动词路径掩盖副作用。

为每个操作定义认证、授权、租户隔离、输入校验、状态码、响应 schema、错误码、超时、重试和审计字段。区分 2xx、4xx、5xx、业务拒绝、超时、部分成功和异步受理；不要把所有失败映射为 200，也不要泄露内部异常。

## 契约优先与 GraphQL

REST 使用 OpenAPI 或等价的版本化契约，GraphQL 先设计类型/schema，再实现 resolver。每个字段说明可空性、格式、敏感级别、所有权、演进策略和默认值。GraphQL mutation 返回结构化业务错误，查询和 resolver 做输入授权；使用 DataLoader 或等价批处理避免 N+1，并限制深度、复杂度、分页大小和执行时间，防止资源耗尽。

## 分页、过滤与一致性

大集合必须有明确上限、排序稳定性、游标/偏移策略、下一页语义、重复/遗漏风险和快照一致性。过滤、排序和字段选择列入契约并做索引/成本评估；不能把任意查询表达式直接暴露给服务端。报告空页、删除/并发更新、时区和最终一致性对客户端的影响。

## 幂等、重试与并发

对创建、支付、消息发送、导入等可能重试的操作定义幂等键、作用域、保存时长、冲突响应和去重证据。声明哪些操作可安全重试，设置客户端/服务端退避、超时和重试预算；不要对非幂等 POST 自动重放。并发更新需选择版本号、ETag/If-Match、条件写或明确的 last-write-wins，并说明冲突处理。

## 版本化与演进

选择 URL、媒体类型/请求头或 schema 演进策略，并记录选择理由。破坏性变更包括删除/重命名字段、收窄枚举、改变含义、改变错误/排序/默认值、权限扩大和副作用变化；每项都要有消费者影响、迁移步骤、兼容窗口、弃用通知、契约测试、回滚/双读双写计划和删除日期。优先向后兼容新增字段，但仍要考虑未知字段、客户端严格解析和字段敏感性。

## 限流、可观测性和文档

按身份、租户、操作和资源设置有依据的限流、配额和成本预算，响应中说明重试时间而不泄露内部策略。记录脱敏 correlation ID、延迟、状态、容量、查询复杂度和拒绝原因；不要记录完整请求体或凭据。文档至少包含认证、权限、示例、错误、分页、幂等、版本、弃用、SLO 和安全联系人，并由契约/集成测试验证。

## 交付与质量门禁

交付报告包含消费者/资源地图、契约链接、操作矩阵、认证授权、数据分类、HTTP/schema 语义、错误/分页/幂等/版本策略、性能与限流假设、兼容性风险、测试证据和待决问题。任何线上写入、迁移、策略变更或通知作为后续需授权动作列出。

- [ ] 资源、操作、消费者、身份/租户和数据范围明确。
- [ ] HTTP/schema、状态码、错误、输入校验、分页、幂等和并发语义可验证。
- [ ] REST/OpenAPI 或 GraphQL schema 有版本、所有权、敏感级别和演进策略。
- [ ] 限流、查询复杂度、超时、重试、可观测性和成本边界明确。
- [ ] 破坏性变更有消费者影响、迁移、弃用、回滚和删除日期。
- [ ] 契约/集成测试覆盖成功、失败、权限、兼容和资源耗尽场景。
- [ ] 示例和证据已脱敏，没有未授权线上写操作或策略变更。
