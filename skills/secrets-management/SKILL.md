---
name: "secrets-management"
display_name: "Secrets 管理"
display_name_en: "Secrets Management"
description: "Use when designing or reviewing secure secret storage, CI/CD credential injection, rotation, least-privilege access, secret scanning, or audit controls."
description_zh: "用于设计或审查安全的凭据存储、CI/CD 注入、轮换、最小权限、Secrets 扫描和审计控制。"
description_en: "Design provider-agnostic secret flows with scoped identities, short-lived credentials, environment separation, rotation, redaction, scanning, auditability, and fail-closed delivery without exposing secret values."
category: "security"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository/CI/IAM metadata and a secret manager policy view; reading secret values, changing access, rotating credentials, or deploying configuration requires separate authorization"
---

# Secrets Management

设计从创建、存储、注入、使用、轮换到撤销的凭据生命周期。只讨论 secret 的名称、类型、作用域、版本和控制证据，不读取、复制或回显 secret 值；安全交付优先于方便调试。

## 安全边界

- 默认只读审查仓库、CI 配置、IAM/RBAC、secret manager 元数据、扫描结果和审计策略；不读取 secret value，不执行登录、部署或轮换。
- 目标环境、账户/组织、工作流触发信任、身份、租户和 secret 作用域必须明确；开发、测试、预发布和生产使用不同凭据和策略。
- 禁止把凭据写进 Git、镜像层、构建产物、命令行参数、日志、错误、截图、缓存、工件或聊天。示例只能使用明显的占位符，如 `<SECRET_REF>`，不可使用看似真实的 token/password。
- 任何创建、写入、授权、轮换、撤销、迁移、告警或部署变更都需要单独授权；评审结论不代表已执行。

## 选择存储和访问模式

根据风险和运行时选择 Vault、AWS Secrets Manager、Azure Key Vault、Google Secret Manager、Kubernetes External Secrets 或平台等价物。记录加密、备份、版本、区域、可用性、恢复、审计和管理员分离。应用通过运行时身份按引用读取，不把值传给不需要它的 Agent、构建步骤或子进程。

访问策略按 workload/service、环境、租户、secret 路径和操作分层：读取单个必要 secret 不应获得列举、写入、删除或其他环境权限。优先 OIDC/workload identity 和短期凭据，避免长期静态云密钥；CI 触发器、fork、pull request、日志和 artifact 边界必须阻止不受信任代码接触生产 secrets。

## CI/CD 注入

在作业开始前确认触发来源、分支保护、审批环境、runner 信任、权限和可见范围。只将需要的引用映射到需要的步骤，尽量通过临时文件描述符或进程环境短暂使用，并防止 shell tracing、调试输出和错误回显。注入后验证“已设置”只输出布尔状态，不输出长度、前缀或值；步骤结束后清理临时文件和环境。

Pull request、fork、来自外部贡献者的 workflow 和未固定的第三方 action 默认不接触受保护 secrets。动作依赖应固定到可信版本/摘要并审查其权限、网络和输出，避免 secret 通过 stdout、缓存、artifact、依赖安装脚本或子 Agent 委派外泄。

## 轮换、撤销和故障处理

为每类凭据定义生命周期、拥有者、最大年龄、轮换触发器、双 key/重叠窗口、消费者更新顺序、验证、旧值撤销、回滚和到期告警。优先自动轮换短期凭据，但轮换任务本身不得把新值写入日志或未授权系统。泄露怀疑时先隔离和撤销暴露身份，再保留脱敏证据、评估范围、检查审计日志和验证消费者恢复；不要为了“确认泄露”继续使用该凭据。

## 扫描和审计

在 pre-commit、CI、仓库历史、镜像/工件和运行日志中进行 secret scanning，并配置高置信规则、误报安全豁免、历史重写/撤销流程和告警路由。扫描通过不是无泄露证明；报告工具、扫描范围、提交、规则版本、漏报限制和未扫描二进制/外部系统。

审计记录身份、时间、环境、secret 引用、读写动作、策略决策、轮换/撤销事件和结果，但对值、哈希可逆信息和客户数据脱敏。定期检查未使用、过宽、跨环境、未过期和孤立 secret；删除前确认消费者和可恢复策略，避免把清理变成事故。

## 交付报告

报告包含 secret 类型和数据流、存储/注入架构、身份与权限矩阵、环境/fork/CI 信任边界、轮换与撤销计划、扫描/审计证据、备份恢复、失败模式、未知项和需要授权的动作。使用 `observed`、`derived`、`unknown` 区分事实和推断，绝不把 secret 值作为证据。

## 质量门禁

- [ ] secret 仅通过受控引用和运行时身份使用，值从未进入源码、日志、工件或聊天。
- [ ] 环境、触发器、fork/PR、runner、IAM/RBAC 和最小权限边界明确。
- [ ] CI 注入范围、第三方 action、shell tracing、缓存/artifact 和子 Agent 泄露路径已检查。
- [ ] 轮换、重叠、验证、旧值撤销、到期告警和泄露响应可执行且有负责人。
- [ ] 扫描覆盖代码、历史、依赖、镜像、工件和日志，限制与豁免可追踪。
- [ ] 审计记录动作和引用但不记录值；写入、授权、轮换、撤销和部署动作未越权执行。
