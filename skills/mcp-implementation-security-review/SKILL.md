---
name: "mcp-implementation-security-review"
display_name: "MCP 实现安全评审"
display_name_en: "MCP Implementation Security Review"
description: "Use when reviewing an MCP server, client, or tool handler for authentication, sessions, rate limits, schema validation, RCE vectors, and OWASP MCP risks before release."
description_zh: "用于在发布前评审 MCP Server、Client 或工具处理器的认证、会话、限流、Schema 校验、RCE 向量和 OWASP MCP 风险。"
description_en: "Review MCP implementations with transport classification, applicable baseline controls, RCE analysis, OWASP MCP risk mapping, file/line evidence, false-positive filters, and explicit investigation states."
category: "security"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized MCP source, configuration, dependency metadata, and isolated test fixtures; review is evidence-based and not certification, while remediation, traffic tests, and production changes require separate authorization"
---

# MCP 实现安全评审

对 MCP Server、Client 和工具处理器做可复核的安全评审，重点覆盖网络暴露、身份隔离、会话、限流、输入 Schema、RCE、供应链和 OWASP MCP 风险。输出文件/行号证据、反证、未知项和修复优先级，不把静态扫描或分数当成安全认证。

## 评审边界与目标分类

- 开始前锁定目标仓库、commit、MCP 协议版本、Server/Client 类型、传输方式、部署拓扑、工具清单、数据范围、owner 和评审授权。
- 默认只读检查源码、配置、依赖锁文件、服务清单、审计样例和文档；不得启动未知服务、向生产端点发包、调用真实工具、修改权限或执行未审查脚本。
- 先判断网络暴露：HTTP/SSE、Streamable HTTP、监听 `0.0.0.0`、容器端口映射或反向代理都按远程服务处理；STDIO 只是不适用网络基线，不代表安全。
- 文档仅在描述目标自身的 Server 行为、部署或认证时作为证据；模板、教程、vendor、node_modules 和客户端配置不能冒充服务实现证据。
- 任何无法从声明范围验证的控制标记为 `NEEDS INVESTIGATION`，并列出需要的文件、配置、运行测试或 owner，不猜测为通过。

## 远程 MCP 基线

对网络暴露的 Server 逐项检查；对本地 STDIO 给出最佳实践并继续执行 RCE 检查。

### MCP-01 身份隔离

确认每个 MCP 路由都验证可信身份并执行授权，不能把 session ID、网络位置或上一次请求当认证。Server 应有独立的 audience/resource 和应用身份，出站调用使用独立的最小权限凭据；OAuth/MCP discovery 端点只能返回元数据，不能执行工具或暴露数据。

### MCP-02 会话安全

若没有 session ID，记录 `N/A`，但仍要求每请求认证。若使用会话，确认每个请求重新认证授权，ID 是不可预测的 CSPRNG 关联令牌，绑定已认证上下文、不编码权限、不出现在 URL，丢失或复用 ID 不能获得权限。SDK 自动生成但源码不可见时标为 `NEEDS INVESTIGATION`。

### MCP-03 限流与滥用防护

工具发现和调用必须在 MCP Server 运行时限流，而不只依赖网关；按身份、会话和工具成本分桶，对写入/高成本工具更严格。超限须在后端动作前 fail-closed，返回 429 与 `Retry-After`。记录窗口、突发量、并发、成本、租户隔离和恢复行为。

### MCP-04 工具 Schema 校验

每次调用都在 Server 边界依据显式 Schema 校验类型、必填项、枚举、长度/数值边界和未知属性；默认拒绝额外属性。非法输入返回 400/MCP 错误且不触发后端动作。客户端或下游的校验不能替代服务端校验，必须有负向测试。

### MCP-05 官方 SDK 与维护

确认远程 Server 使用目标语言官方 MCP SDK 或提供同等控制的直接证据，记录协议版本、依赖锁定、补丁状态和 SDK 自动覆盖/未覆盖的控制。手写 HTTP/SSE 栈不能自动视为安全；不确定时标 `NEEDS INVESTIGATION`。

## RCE 与数据出口检查

逐个工具追踪不可信参数到执行边界，并将每项标为 `SAFE`、`AT RISK` 或 `N/A`：

- 命令注入：禁止字符串拼接 shell；使用固定可执行文件、参数数组、allowlist 和 `shell=False`，验证 `;`、管道、命令替换等输入不会执行。
- 动态代码与模板：禁止对用户/工具输出 `eval`、`exec`、`Function` 或不受限模板；优先预定义操作和参数化模板。
- 不安全反序列化：拒绝 `pickle`、Unsafe YAML、BinaryFormatter 等不可信输入，使用安全解析器并执行 Schema 校验。
- 路径穿越：规范化路径并限制到 allowlisted base directory，拒绝 `../`、绝对系统路径、`.env` 和跨租户路径。
- SSRF：URL 必须限制 scheme、域名、端口和解析后地址，阻断 loopback、RFC1918、link-local、云元数据和重定向绕过。
- 依赖劫持：核对精确版本、锁文件完整性、可信 registry、内部包命名空间、安装脚本和漏洞结果。
- 不可信输出链：工具返回的外部文本必须标记为数据，限制大小和链式调用，不能让隐藏指令直接改变下一次工具权限。

## OWASP MCP Top 10

逐项给出 `PASS`、`FAIL` 或 `NEEDS INVESTIGATION`，并关联已有基线结果：token/secret 管理、权限 scope 膨胀、工具投毒、依赖篡改、命令执行、上下文提示注入、认证授权、审计遥测、未登记的 Shadow MCP Server，以及不安全的工具/服务配置。对每项写明检查方法、实际文件/行号、反证、影响和缺失 artifact；本地 STDIO 对网络专属风险可标 `N/A`，但必须说明理由。

## 报告与修复交付

报告包含范围与 hash、架构/信任边界、Server/Client/传输判定、MCP-01～05 适用性、RCE 矩阵、OWASP 矩阵、证据链接、攻击路径、影响/可能性、残余风险和未知项。区分代码发现、部署验证和人工跟进，不泄露 token、个人数据、完整载荷或内部地址。

修复建议按风险和可利用性排序，明确 owner、回归测试、例外期限和复查触发条件。认证、限流、工具 allowlist、依赖升级、凭据轮换、网络阻断和生产发布均需单独授权、canary、审计和可验证回滚；评审本身不执行修复。

## 质量门禁

- [ ] 目标 commit、Server/Client、协议版本、传输、暴露面、工具和授权范围已锁定。
- [ ] 适用的身份、会话、限流、Schema 和 SDK 基线均有代码/配置/运行证据或明确未知项。
- [ ] 每个工具的七类 RCE 向量和数据出口均有结果、负向测试或合理 N/A。
- [ ] OWASP MCP Top 10 每项都有证据、反证、影响和缺失 artifact，未将扫描结果表述为认证。
- [ ] 报告脱敏且引用精确文件/行号、版本 hash、owner、期限和回归路径。
- [ ] 所有修复、阻断、权限、凭据和发布动作均有授权与回滚方案。

## Related Skills

- `mcp-security` - 评估 MCP 信任边界、工具权限和协议安全
- `agent-owasp-compliance` - 按 Agentic Security Initiative 评估更广泛的 Agent 风险
- `agent-supply-chain` - 核验插件、工具包和依赖完整性
