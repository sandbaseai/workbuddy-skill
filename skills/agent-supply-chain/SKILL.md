---
name: "agent-supply-chain"
display_name: "Agent 供应链完整性"
display_name_en: "Agent Supply Chain Integrity"
description: "Use when generating or verifying integrity manifests, auditing dependency pinning, detecting tampered agent plugins or tools, or establishing provenance gates for agent-component promotion."
description_zh: "用于生成或核验完整性清单、审查 Agent 组件依赖锁定、发现被篡改或未登记文件，或为 Agent 组件晋级建立来源证明门禁。"
description_en: "Hash and verify agent plugins and tool packages, audit version pinning, preserve provenance, and gate promotion with reproducible, fail-closed evidence."
category: "security"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with local filesystem access to the component under review and an approved manifest/signing or provenance policy; promotion and registry changes require separate authorization"
---

# Agent Supply Chain Integrity

审查 Agent 插件、工具包、MCP 组件和其依赖的完整性与来源。通过确定性文件清单、精确版本审计、来源链和晋级门禁，发现篡改、漂移、未登记文件和不可复现的构建输入。

## 安全边界

- 默认只读：扫描目标、读取配置、计算哈希、比较已批准清单并生成报告。
- 不执行被审查的脚本、安装依赖、访问网络、签署制品、修改注册表或晋级环境。
- 目标目录、基线清单、提交/制品标识和信任策略必须明确；缺失时标记为 `unknown`，不得猜测。
- 完整性证明不等于代码安全。仍需审查权限、网络、凭据、动态执行和依赖行为。
- 清单与报告不得包含密钥、令牌、私有路径中的敏感名称或用户数据。

## 完整性清单

为组件生成确定性清单时：

1. 固定根目录和允许的文件类型；排除 `.git`、缓存、虚拟环境、依赖下载目录及清单自身，并记录排除规则。
2. 按规范化的相对 POSIX 路径排序，使用 SHA-256 分块读取文件；不跟随根目录外的符号链接。
3. 保存 `component_name`、`source_revision`、`algorithm`、`file_count`、`files`、`generated_at` 和清单链哈希。
4. 将来源仓库、提交 SHA、构建器、锁文件、构建时间和制品摘要作为 provenance 字段；未知字段明确标注。

清单链哈希应由排序后的路径及其文件哈希稳定计算。时间戳不得参与内容链哈希，否则同一内容无法复现。

## 核验与漂移分类

核验时先验证清单格式、算法和来源，再计算当前文件集合。分别报告：

- `MISSING`：基线登记但当前缺失；
- `MODIFIED`：路径存在但哈希不一致；
- `UNTRACKED`：当前存在但未登记；
- `OUT_OF_SCOPE`：链接或文件越过批准根目录；
- `BASELINE_UNKNOWN`：没有可信、固定版本的比较基线。

任何缺失、修改、未登记或越界项都使核验失败；不要用“文件数量相同”替代逐文件比较。生成报告时同时给出基线来源、扫描范围、排除项、错误列表和可复核命令。

## 依赖与版本审计

检查 `package.json`、锁文件、`requirements.txt`、`pyproject.toml`、容器清单和 Agent 配置：

- 标记 `latest`、`*`、浮动 `^`/`~`、无上界范围和未锁定 Git 引用；
- 优先以 lockfile、发布制品摘要或提交 SHA 作为可复现依据；
- 将直接依赖、传递依赖、构建工具和运行时插件分开统计；
- 记录弃用、来源切换、维护者变化、权限扩张和新增安装脚本等升级风险；
- 不因为版本已锁定就断言无漏洞，漏洞与许可证判断需独立证据。

## 来源链与晋级门禁

在 `dev → staging → production` 或发布前，至少核对：

1. 源代码提交、构建输入、锁文件和制品摘要相互一致。
2. 构建结果与已审查清单逐文件匹配，且清单由批准的 CI 身份生成。
3. 签名、证明或不可用状态被明确记录；不能验证签名时 fail closed，不得改写状态为 verified。
4. 晋级范围、批准人/策略、时间、环境和回滚制品可追溯。
5. 任何重建、依赖变化、权限变化或基线更新都触发重新审查。

## 交付报告

报告应区分 `observed`、`derived`、`inferred` 和 `unknown`，并包含：目标与范围、来源和基线、文件统计、漂移明细、依赖锁定发现、签名/证明状态、风险等级、证据引用、限制与下一步只读检查。修复、安装、删除、签署和晋级作为需单独授权的动作列出，不在本 Skill 中执行。

## 质量门禁

- [ ] 目标根目录、来源版本、算法、排除规则和时间基准明确。
- [ ] 文件按规范化路径逐项哈希，清单链哈希可复现。
- [ ] 缺失、修改、未登记和越界项分别分类并使失败状态可见。
- [ ] 依赖版本、锁文件、构建输入和制品摘要已交叉核对。
- [ ] 未验证的签名/证明保持 `unknown`，没有安全性过度断言。
- [ ] 报告脱敏，且不执行被审查代码或产生外部副作用。
