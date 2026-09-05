---
name: "parallel-debugging"
display_name: "并行调试与假设仲裁"
display_name_en: "Parallel Debugging"
description: "Use when a bug has multiple plausible causes or spans components, and independent investigations are needed to compare evidence without confirmation bias."
description_zh: "用于存在多个可能原因或跨组件的复杂缺陷，通过相互独立的调查比较证据，降低确认偏误并仲裁根因。"
description_en: "Run bounded, independent investigations across competing hypotheses, cite direct evidence, preserve contradictions, and arbitrate confirmed, plausible, falsified, or inconclusive results before proposing a fix."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized source, fixtures, logs, traces, metrics, and isolated investigation contexts; parallel work does not grant production access or mutation authority"
---

# 并行调试与假设仲裁

当一个问题有多个合理原因时，把调查拆成相互独立、范围明确的假设分支，再用同一证据标准进行仲裁。并行不是让更多人重复猜测，也不是把多个低质量意见投票成事实；每个分支必须能被证伪，并保留冲突、未知和未完成工作。

## 安全前置门禁

开始前确认问题范围、授权材料、环境、数据处理规则、允许的工具、并行上下文边界和汇总负责人：

- 默认只读、离线或隔离调查；生产观察和任何写入、部署、通知、数据修改或外部请求都需独立授权；
- 每个调查者只能读取其分配范围，不复制凭据、客户数据、完整请求体、私有密钥或未脱敏转储；
- 固定基线、版本、时间窗口和样本 hash；未经汇总负责人批准不得改变公共 fixture、共享配置或结果文件；
- 真实直接证据、相关证据、口述和缺失证据分开记录；禁止把并行报告数量当成证据强度；
- 授权、输入完整性、隔离或证据来源不清时返回 `BLOCKED`，不通过合并意见补齐事实。

## 假设空间

至少从以下类别检查候选原因，必要时说明不适用项：

1. **逻辑**：条件、边界、状态转移、算法或错误处理；
2. **数据**：类型、空值、编码、序列化、截断、溢出或不变量；
3. **状态**：竞态、缓存、初始化、共享可变状态、重试或顺序；
4. **集成**：契约、版本、配置、依赖、超时、权限或外部响应；
5. **资源**：内存、连接、句柄、磁盘、配额、CPU、队列或限流；
6. **环境**：运行时、平台、时区、区域、依赖安装或发布差异。

不要因为某个类别“看起来常见”就提升其优先级；优先级应由影响、可检验预测、现有证据和实验成本决定。

## 并行调查流程

1. **固定问题陈述**：写出期望/实际、影响、复现率、首次出现、范围和停止条件。
2. **建立候选表**：每个假设写支持证据、反证、预测、最小验证、负责人/上下文和截止时间。
3. **隔离调查**：每个分支从同一基线开始，只改变获批的调查变量，不读取其他分支的结论，避免锚定。
4. **收集证据**：引用精确文件/行号、日志时间窗、trace/span、指标、提交、fixture hash 或测试结果；原始数据先脱敏。
5. **尝试反证**：主动寻找能推翻假设的样本、边界、对照环境和替代解释，不只收集支持材料。
6. **提交报告**：使用统一格式，声明未运行的测试、缺失访问、工具限制和冲突；禁止把猜测写成修复建议。
7. **独立仲裁**：由未参与至少一个调查分支的汇总者按证据强度、因果链、反证和置信度比较结果。
8. **形成结论**：允许单一根因、复合原因、没有确认项或保持 `Inconclusive`；每种状态都要给安全下一步。
9. **验证修复**：修复前后运行最小复现、相关边界、回归和副作用检查；修复未验证时状态仍不是 `Confirmed`。

## 证据等级与结果状态

| 证据/状态 | 规则 |
| --- | --- |
| `Direct` | 可定位到代码、输入输出、时间窗、测试或可复核系统记录 |
| `Correlated` | 时间/统计相关但不能独立证明因果 |
| `Testimonial` | 口述或经验，仅作为待验证线索 |
| `Absent` | 在明确范围内未观察到，不等于全局不存在 |
| `Confirmed` | 多个直接证据支持，因果链清晰，无未解释反证 |
| `Plausible` | 证据支持但仍有重要歧义或替代解释 |
| `Falsified` | 可复核证据与预测冲突 |
| `Inconclusive` | 材料不足，不能确认或证伪 |

置信度不是调查者投票结果。高置信度需要多项直接证据和可复现因果链；中/低置信度必须明确缺口、反证和安全补证动作。

## 调查报告模板

```markdown
# Parallel Debugging Report — <issue>

Status: Confirmed | Plausible | Falsified | Inconclusive | Blocked
Baseline: <revision, environment, fixture hash, time window>
Impact: <scope and severity>
Arbitrator: <role>

## Fixed problem statement
- Expected: <...>
- Actual: <...>
- Reproduction: <stable/intermittent/not reproduced>

## Hypotheses
| ID | Category | Prediction | Scope | Status | Confidence |
| --- | --- | --- | --- | --- | --- |

## Evidence ledger
| ID | Hypothesis | Type | Exact citation | Supports/contradicts | Redaction |
| --- | --- | --- | --- | --- | --- |

## Independent reports
### H-<id>
- Observation: <...>
- Test and result: <...>
- Counter-evidence: <...>
- Missing access or limitation: <...>

## Arbitration
- Dominant/compound/inconclusive: <...>
- Why: <evidence, causal chain, alternatives>
- Dissent: <...>

## Fix validation
- Original reproduction: <result>
- Edge/regression tests: <result>
- Side effects and residual risk: <...>

## Safe next step
- <authorized fixture, test, read-only query, or escalation>
```

## 质量与停止条件

- 所有分支从同一基线开始，范围、变量和截止时间可审计；
- 证据含精确引用、时间和脱敏说明，未运行的命令/测试明确标注；
- 至少有一个反证尝试，报告保留矛盾和不同意见；
- 仲裁者独立于关键分支，不能以多数意见代替证据；
- 修复通过原始复现、边界、回归和副作用检查后才可标记 `Confirmed`；
- 生产权限、秘密、敏感样本、关键访问或因果证据缺失时返回 `BLOCKED` 或 `Inconclusive`。

## Related Skills

- `debugging-strategies` - 进行单变量复现、差分和回归调试
- `bug-reproduction-brief` - 将模糊或间歇性问题收敛为最小复现
- `doubt-driven-development` - 对非平凡结论进行对抗式复核
