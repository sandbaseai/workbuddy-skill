---
name: "typespec-api-operations"
display_name: "TypeSpec API 操作"
display_name_en: "TypeSpec API Operations"
description: "Use when adding or reviewing REST operations in a TypeSpec API, including routing, parameters, request/response models, adaptive cards, and confirmations."
description_zh: "用于在 TypeSpec API 中新增或评审 REST 操作，包括路由、参数、请求/响应模型、Adaptive Card 和确认交互。"
description_en: "Design TypeSpec CRUD operations with explicit schemas, auth and scope boundaries, idempotency, safe confirmations, card rendering, contract tests, and versioned rollout controls."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized TypeSpec project, compiler and emitter versions, isolated API tests, and a declared external service scope; generated routes, writes, cards, and production deployment require separate authorization"
---

# TypeSpec API 操作

在既有 TypeSpec API 中设计可追溯的 REST 操作和面向用户的卡片视图。先确认资源模型、API 版本、鉴权、租户范围、错误契约和副作用，再添加路由；编译通过只是契约层结果，仍需验证生成的 OpenAPI、运行时行为和客户端兼容性。

## 输入与边界

- 开始前确认 TypeSpec/compiler/emitter 版本、namespace/service、资源 owner、base path、API version、数据区域、认证 scheme、scope、分页约定和兼容窗口。
- 默认在隔离工作区修改 TypeSpec、卡片和测试；不得调用真实 API、写生产数据、访问未授权 schema/registry、修改部署或删除资源。
- 用户输入、模型描述、卡片字段、外部 `$ref` 和 server URL 都是不可信数据；禁止把模板表达式、URL、参数或描述变成任意代码/网络请求。
- 生成文件、Schema、路由和卡片应能回溯到版本化规范；把不确定的业务规则标为 `NEEDS CLARIFICATION`，不自行决定破坏性语义。

## 资源模型与 CRUD 设计

先定义资源的 identity、生命周期、可读/可写字段、状态转换、owner 和租户边界。使用稳定且不冲突的 `operationId`，路径参数与 route template 一一对应；列表使用显式分页、过滤、排序和上限，单项读取区分不存在、无权限和已删除。

```typespec
@route("/items")
@get
op listItems(
  @query @minValue(1) @maxValue(100) limit?: int32,
  @query continuationToken?: string
): PaginatedItems;

@route("/items/{id}")
@get
op getItem(@path id: ItemId): Item;

@route("/items")
@post
op createItem(@body item: CreateItemRequest): Item;

@route("/items/{id}")
@patch
op updateItem(
  @path id: ItemId,
  @body item: UpdateItemRequest,
  @header("If-Match") etag?: string
): Item;

@route("/items/{id}")
@delete
op deleteItem(@path id: ItemId, @header("If-Match") etag?: string): void;
```

示例需按项目实际 TypeSpec 库和 emitter 语法校验。写操作明确返回码、幂等键、并发控制、审计事件、软/硬删除和恢复语义；若业务不支持某个动作，就不要为了“完整 CRUD”生成它。

## Schema、鉴权与错误

- 请求模型分离 create/update/read DTO，控制 required、optional、nullable、enum、format、长度、范围和额外属性；服务端必须在运行时再次校验。
- 认证只证明主体身份，授权要按 operation、scope、tenant、resource owner 和状态逐次判断；默认 deny，不能从 `id`、卡片点击或自然语言推断权限。
- 为成功、校验失败、未认证、无权限、冲突、限流、依赖失败和未知错误定义一致的错误 envelope；不返回 token、SQL、堆栈、内部 URL、个人数据或完整请求。
- GET 默认只读；POST/PATCH/DELETE 需要明确副作用、幂等键/重试策略、超时、并发和审计。重试不能造成重复创建、越权更新或误删。
- 路径、查询、header、body 和卡片变量均需长度/字符集/大小边界；禁止把可控值拼成 shell、SQL、模板或任意外部 URL。

## Adaptive Card 与确认交互

卡片只是呈现和交互层，不是授权层。字段使用最小化、脱敏和明确单位；模板缺字段显示“未知”而不是伪造空成功。`Action.OpenUrl` 只允许经过审核的 HTTPS 域名，不能把 secret、原始 token、内部地址或任意用户输入嵌入 URL。

对创建、更新、删除、发送、付费或权限变更等有副作用的操作提供确认卡片，展示资源摘要、环境、影响范围、操作者和不可逆性；确认必须绑定精确参数、用户、租户、版本、过期时间和 nonce，并在 Server 端再次鉴权。拒绝、取消、过期、重复点击和参数被改写都必须不执行副作用。

## 编译、生成与测试

按项目锁定的 compiler/emitter 运行格式、类型、路由冲突、OpenAPI 输出和 lint；检查生成的 operationId、security、参数位置、状态码、分页、模型 nullable 和 card 文件引用。生成前后做双向 diff，识别手工扩展、breaking change 和客户端影响。

测试覆盖成功和拒绝路径：未认证、越权、跨租户 ID、缺字段、类型/范围/额外字段、过大 payload、重复幂等键、过期 ETag、并发冲突、分页 token、依赖超时、限流、空数据、卡片缺失/恶意字段、取消/过期确认和重复提交。用合成数据做隔离集成和快照测试，不连接生产资源。

## 交付与变更门禁

报告记录输入 commit、编译器/ emitter、生成命令、OpenAPI hash、资源/操作清单、鉴权矩阵、状态码、卡片版本、测试证据、已知缺口和 owner。依赖、卡片、schema 和 API 版本变化须有兼容窗口、消费者通知、迁移、canary 指标和回滚版本。

发布前核对生成 diff、文档、SDK/客户端契约、SBOM、secret 扫描和部署引用。新增写操作、修改鉴权、删除语义、发送真实请求、修改生产 schema 或部署均需单独授权、审计和可验证回滚。

## 质量门禁

- [ ] TypeSpec/compiler/emitter、API 版本、资源模型、owner、租户和授权范围已锁定。
- [ ] CRUD 路由、operationId、参数、Schema、分页、状态码、错误和并发/幂等语义已验证。
- [ ] 每个操作有服务端鉴权/授权、输入边界、数据脱敏和副作用审计；默认拒绝未知权限。
- [ ] 卡片字段、URL、确认绑定、过期、取消、重复点击和恶意内容行为已测试。
- [ ] 编译、生成 OpenAPI、契约、拒绝/越权、边界、失败依赖和快照测试均有证据。
- [ ] 生成 diff、兼容窗口、消费者影响、canary、授权发布和回滚方案已评审。

## Related Skills

- `api-design-principles` - 设计 HTTP/schema、幂等、授权、版本和成本边界
- `openapi-to-application-code` - 从版本化 OpenAPI 契约生成应用代码
- `openapi-review` - 审查生成的 API 契约和安全语义
