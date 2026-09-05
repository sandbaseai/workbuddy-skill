---
name: "agent-owasp-compliance"
display_name: "Agent OWASP ASI 合规检查"
display_name_en: "Agent OWASP ASI Compliance Check"
description: "Use when assessing an AI agent codebase against the OWASP Agentic Security Initiative risks before deployment, audit, or security review."
description_zh: "用于在部署、审计或安全评审前，按 OWASP Agentic Security Initiative 风险检查 AI Agent 代码库。"
description_en: "Assess agentic security across prompt injection, tool governance, agency boundaries, escalation, trust, audit, identity, policy integrity, supply chain, and behavioral monitoring with evidence-backed findings."
category: "security"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized source code, configuration, dependency metadata, and isolated static analysis; findings are assessment evidence rather than certification, and remediation or production changes require separate authorization"
---

# Agent OWASP ASI 合规检查

对会调用工具、访问系统或代表用户采取行动的 Agent 做证据驱动的安全评估。把每个风险映射到代码、配置、身份、运行日志和组织控制；输出覆盖状态、证据、反证、未知项、风险和建议，不把静态搜索结果当作安全认证。

## 评估边界

- 开始前确认 Agent、版本/commit、工具清单、部署环境、身份边界、数据范围、租户范围、评估授权人和报告受众。
- 默认只读分析源码、配置、依赖锁文件、策略、审计样例和已有运行证据；不得执行未审查脚本、调用生产工具、发送真实请求、修改权限或尝试绕过控制。
- 评估结果只对声明的 commit、配置和时间窗口有效；把未观察到、未配置和无法访问明确区分为 `unknown`，不要推断为 `pass`。
- 报告中脱敏 token、密钥、个人数据、完整请求、内部地址和业务载荷；保留可复核的文件/行号、配置键、测试编号或 hash。

## 十项风险检查

### ASI-01 Prompt Injection Protection

确认不可信用户输入、检索内容、网页、文件和工具返回值在进入工具调用前经过独立的输入/意图/内容策略检查。检查是否存在提示注入检测、来源标记、上下文隔离和对抗测试；仅过滤模型输出不算充分。记录绕过路径、误报/漏报和 fail-closed 行为。

### ASI-02 Insecure Tool Use

核对工具是否采用显式 allowlist、schema/类型/范围校验、资源与网络边界、超时和结果大小限制。重点检查 Agent 生成的 shell、SQL、路径、URL、代码和模板是否被沙箱或参数化处理；`eval`、`exec`、不受限 shell 和任意 URL 必须有隔离、审计和拒绝测试。

### ASI-03 Excessive Agency

绘制 Agent 能力、资源、数据和副作用范围，确认默认权限最小化、执行环/作用域、租户隔离、预算、速率、步数和时间上限。子 Agent 或委托任务的 scope 不得超过父任务；证明不需要的工具不会自动暴露。

### ASI-04 Unauthorized Escalation

检查敏感操作前是否有独立权限判断、二人/人工审批或外部见证，且 Agent 不能修改自己的角色、策略、信任分或审批记录。验证拒绝、过期批准、重放、审批绑定到精确参数和紧急 kill switch 的行为。

### ASI-05 Trust Boundary Enforcement

对多 Agent、插件、MCP 服务和外部内容验证身份、签名、来源和传递范围；不接受仅凭名称或自然语言声明的信任。检查跨边界消息的完整性、时间戳/nonce、delegation narrowing、数据出口和 confused-deputy 防护。

### ASI-06 Logging & Audit

确认每次用户请求、策略决定、工具调用、参数摘要、结果状态、身份、时间、版本和错误都写入结构化、脱敏、访问受控且不可任意篡改的审计记录。验证日志完整性、时钟、保留、告警和从日志重建行动链的能力；`print` 或只记录成功不够。

### ASI-07 Identity Management

核对用户、Agent、服务账号和工具是否有可验证且可轮换的身份，权限是否绑定到具体主体、环境和能力。检查短期凭据、密钥轮换、吊销、重放防护、跨 Agent 认证和共享凭据；字符串名称不是身份控制。

### ASI-08 Policy Integrity

策略判断应由独立、确定性、可版本化的 enforcement 层执行，而不是让模型自行解释“我是否被允许”。检查策略不可被上下文覆盖、工具参数二次校验、策略错误 fail-closed、版本/审批绑定和回归测试；策略检查失败时不得默认放行。

### ASI-09 Supply Chain Verification

盘点模型、插件、MCP、工具、依赖、镜像和 Skill 的来源、版本、锁定、签名、哈希、维护者和漏洞状态。验证安装包与运行内容一致、传递依赖可追溯、更新需评审、恶意/被攻陷组件可撤销；不要把公共仓库、下载链接或无漏洞报告当作可信证明。

### ASI-10 Behavioral Monitoring

确认有基线和运行时监测识别异常工具序列、数据出口、权限探测、速率/成本漂移、重复失败和策略绕过。检查预算、熔断、隔离、kill switch、人工升级和恢复演练，并把监测盲区、采样率和响应时限写入报告。

## 证据与评分

为每项风险建立 `pass`、`partial`、`fail` 或 `unknown` 状态，附最小充分证据和反证。区分“代码存在控制”“部署启用控制”“运行时有证据”三层，不用单个匹配字符串替代端到端测试。评分必须披露覆盖范围、权重、版本、残余风险和不确定性；“10/10 covered”不等于 OWASP 或任何机构认证。

报告建议包含：范围与 commit、架构/信任边界图、十项风险矩阵、证据链接、攻击路径、影响/可能性、现有控制、缺口、优先级、owner、截止日期、回归测试、例外有效期和复查触发条件。修复建议按风险排序，生产修复、权限变更、凭据轮换和阻断策略必须另行授权并保留回滚证据。

## 质量门禁

- [ ] 评估范围、版本、工具、数据、环境和授权已记录。
- [ ] 十项风险均有证据、反证或明确 `unknown`，覆盖代码、配置和运行时层次。
- [ ] 工具 allowlist、参数校验、能力边界、审批、身份、策略和供应链均验证了拒绝路径。
- [ ] 日志脱敏、完整性、保留、告警、行为基线和 kill switch 有实际证据。
- [ ] 报告不泄露凭据或载荷，不把静态扫描或分数表述为认证结论。
- [ ] 修复项有 owner、优先级、回归测试、例外期限和经授权的发布/回滚方案。

## Related Skills

- `agent-governance` - 设计工具、委托、审批和审计治理
- `agent-supply-chain` - 核验插件、工具包和依赖完整性
- `security-audit` - 评估通用信任边界、控制和残余风险
