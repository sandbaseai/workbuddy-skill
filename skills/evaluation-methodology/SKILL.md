---
name: "evaluation-methodology"
display_name: "Skill 评估方法"
display_name_en: "Skill Evaluation Methodology"
description: "Use when measuring WorkBuddy Skill quality, interpreting evaluation results, calibrating thresholds, or deciding which triggering, output, robustness, or orchestration gap to improve first."
description_zh: "用于评估 WorkBuddy Skill 的触发准确性、输出质量、鲁棒性和编排适配度，解释分数并决定优先改进项。"
description_en: "Apply layered static, judge, and simulation evaluation with transparent dimensions, normalized scores, confidence limits, anti-pattern checks, and actionable remediation."
category: "testing"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with a deterministic analyzer, representative test prompts, and an authorized isolated evaluation harness"
---

# Skill 评估方法

评估 Skill 不只是数行数或看一条示例。将静态结构、受控评审和真实/模拟任务结果分层，分别回答“能否被正确触发”“是否能产出好结果”“是否稳定且适合编排”。每个分数都要能追溯到检查、样本和已知限制。

## 三层评估

### 1. 静态分析

快速、确定性、无模型调用。检查：

- frontmatter 是否包含清晰触发条件、名称和足够具体的描述；
- 输入/输出、代码示例、故障处理和相关 Skill 是否写清楚；
- 主文件是否精炼，细节是否合理分层；
- MUST/ALWAYS/NEVER 的密度和重复段落是否造成过度约束；
- 交叉引用和本地文件是否真实存在；
- 安全信号、秘密样式、悬空链接和未解释脚本是否被标记。

静态通过只证明结构检查通过，不能推断真实任务质量。静态发现的未知、超大文件或安全标记应进入报告，不得静默当成零风险。

### 2. 受控评审

使用至少一名对任务和评分锚点都不了解实现细节的评审者，分别给出 0–1 分：

| 维度 | 核心问题 |
| --- | --- |
| 触发准确性 | 相关请求会触发，不相关请求不会误触发吗？ |
| 编排适配度 | Skill 是专注工作的 worker，还是越权充当 supervisor？ |
| 输出质量 | 模拟真实任务时，结果完整、可执行、证据边界清楚吗？ |
| 范围校准 | 既不是空泛短文，也没有把所有边缘情况塞进主上下文吗？ |

评审输入应固定到 Skill 版本和同一份提示集；多个评审者时平均分，并记录分歧，而不是只保留最有利分数。

### 3. 任务模拟

在隔离环境运行一组真实但无副作用的代表性提示，记录：

- 触发率：相关样本中正确激活的比例；
- 输出一致性：质量分数的离散程度，不能只看最好的一次；
- 失败率：崩溃、违反格式、越权执行或证据缺失的比例；
- 成本效率：中位 token、IQR 和异常值；
- 是否产生未授权写入、网络调用、凭据暴露或不可逆副作用。

样本数量、提示来源、模型/运行时版本和随机种子要写入报告。模拟不能替代真实用户验证，也不能为了提高分数删除困难样本。

## 复合分数

除非项目已有固定权重，否则使用透明的默认权重，并在报告中披露：

| 维度 | 权重 |
| --- | ---: |
| 触发准确性 | 0.25 |
| 编排适配度 | 0.20 |
| 输出质量 | 0.15 |
| 范围校准 | 0.12 |
| 渐进披露 | 0.10 |
| token 效率 | 0.06 |
| 鲁棒性 | 0.05 |
| 结构完整性 | 0.03 |
| 模板质量 | 0.02 |
| 生态一致性 | 0.02 |

对每个维度，仅合并实际运行的层，并对可用层重新归一化：

```text
blended[d] = sum(weight[d, layer] * score[d, layer])
             / sum(weight[d, layer] for available layers)
composite = sum(dimension_weight[d] * blended[d]) * 100 * penalty
```

如果静态检查发现反模式，可使用 `penalty = max(0.5, 1 - 0.05 * count)`，并列出每个扣分原因。没有运行 judge 或模拟时，不得暗示复合分数代表完整认证。

## 分数解释与改进顺序

| 等级 | 分数 | 含义 |
| --- | ---: | --- |
| A | 0.90–1.00 | 没有明显缺口 |
| B | 0.80–0.89 | 小幅改进即可 |
| C | 0.70–0.79 | 存在明确改进项 |
| D | 0.60–0.69 | 需要定向修复 |
| F | < 0.60 | 重要能力不合格 |

先修复“高权重 × 低分”的维度：触发描述模糊通常比少一个示例更值得优先处理；失败路径和越权风险优先于追求更高平均分。置信区间宽时，优先增加代表性样本或澄清触发边界，不要过度解读小样本排名。

## 反模式检查

- **过度约束**：硬性 MUST/ALWAYS/NEVER 过密；只保留真正的安全和正确性边界。
- **空泛描述**：没有明确“何时使用”和具体场景，路由器无法可靠选择。
- **臃肿主文件**：大段低频细节没有合理分层；将参考材料拆到真实存在的 `references/`。
- **悬空引用**：链接的文件不存在，或相关 Skill/Agent 路径无法解析。
- **伪完整性**：只写“运行测试/检查文档”而没有命令、样本、结果或缺失证据。

每个反模式必须附证据和最窄修复建议；未知不等于失败，但必须显式标记。不要为了过静态分析删除安全说明、缩短真实范围或伪造参考文件。

## 评估流程

1. 固定候选 commit、Skill 文件、依赖、模型/运行时和配置，收集触发正例、负例及真实任务样本。
2. 运行静态分析，先修复死链、缺字段、未脱敏内容和可确定的结构问题。
3. 使用版本化评分表进行受控评审，保留逐维度理由和不确定性。
4. 在隔离环境运行只读/合成任务模拟，捕获输出、错误、成本和副作用证据；不得使用生产数据。
5. 计算归一化分数和置信区间，按优先级提出一个最小改进切片。
6. 修改后用同一提示集回归，比较绝对分数、失败类型和触发误报，不只比较总分。

## 报告模板

```markdown
# Skill Evaluation

Candidate: <commit and path>
Depth: quick | standard | deep
Verdict: PASS | PASS WITH CAVEATS | FAIL

## Evidence
- Static: <command, version, result>
- Judge: <reviewers, prompt set, result>
- Simulation: <N, runtime, seed, result>

## Dimensions
| Dimension | Score | Layer(s) | Confidence/evidence | Priority |
| --- | ---: | --- | --- | --- |
| Triggering accuracy | <0..1> | <...> | <...> | <...> |

## Findings
| Severity | Evidence | Impact | Narrowest fix |
| --- | --- | --- | --- |

## Missing evidence
- <what did not run and why>
```

没有代表性样本、评估运行时不一致、结果含秘密、存在未授权副作用或关键检查失败时，结论必须是 `FAIL`；仅有明确范围内的缺失证据可写 `PASS WITH CAVEATS`。评估分数不是发布、付费、合并或生产执行授权。

## Related Skills

- `agentic-evaluation` - 设计 Agent 行为评估和回归集
- `skill-quality-audit` - 审查 Skill 的结构、触发、引用和安全质量
- `test-runner` - 执行仓库测试并保留可复现结果
