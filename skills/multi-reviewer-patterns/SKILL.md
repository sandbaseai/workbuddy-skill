---
name: "multi-reviewer-patterns"
display_name: "多评审者协同模式"
display_name_en: "Multi-Reviewer Patterns"
description: "Use when coordinating independent code reviews across security, performance, architecture, testing, accessibility, or reliability dimensions and consolidating findings without losing evidence or dissent."
description_zh: "用于协调安全、性能、架构、测试、可访问性或可靠性等独立代码评审维度，在汇总发现时保留证据、冲突和异议。"
description_en: "Allocate review dimensions, isolate reviewers, deduplicate co-located findings, calibrate severity to impact and likelihood, preserve conflicting recommendations, and produce an evidence-linked report without modifying code automatically."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized repository revision or diff, reviewer contexts, test evidence, and a controlled report destination; findings do not authorize code changes or merges"
---

# 多评审者协同模式

多评审者评审的价值在于独立视角和可比较证据，不在于把更多意见相加。先按变更风险分配维度，再让每个评审者从同一 base/head 范围独立工作，最后去重、校准严重度、保留分歧并形成可行动报告。

## 范围与安全门禁

开始前记录仓库、精确 base/head、文件范围、授权读者、是否允许访问依赖/测试环境、报告保留期和合并权限：

- 评审只读取授权代码、配置、测试和证据；不把私有代码、秘密、客户数据或内部 URL复制到评审上下文或报告；
- 评审者之间默认隔离，不共享未整理的结论，避免早期意见造成锚定；
- 发现必须绑定精确文件/行号或可复核范围、触发条件、影响和证据；没有证据的内容标记 `Hypothesis` 或不纳入结论；
- 多数票、作者身份、代码风格偏好或同一行出现多次不能单独证明严重度；
- 评审结果不自动修改代码、关闭线程、批准合并或发布；这些动作需要独立授权和门禁。

目标范围变化、base/head 不稳定、关键文件缺失或敏感材料无法脱敏时返回 `BLOCKED`。

## 维度分配

| 维度 | 关注点 | 典型触发 |
| --- | --- | --- |
| Security | 信任边界、认证、授权、输入、秘密、供应链 | 用户输入、权限、外部集成 |
| Correctness/Architecture | 不变量、边界、耦合、接口、迁移 | 新模块、跨层改动、架构变化 |
| Performance/Reliability | 查询、资源、并发、超时、降级 | 热路径、依赖、容量或并发变化 |
| Testing | 行为覆盖、负面路径、隔离、回归 | 新功能、修复、风险较高的重构 |
| Accessibility/UX | 键盘、语义、ARIA、反馈和错误恢复 | UI、表单、动态内容 |

只选择与变更风险相关的维度，并说明未选择维度的理由。一个评审者可以承担多个低冲突维度，但高风险安全结论最好由独立上下文复核。

## 独立评审流程

1. **固定范围**：记录精确 base/head、生成 diff、文件列表、构建/测试状态和已知限制。
2. **创建任务卡**：为每个维度写关注问题、排除范围、截止时间、证据格式和停止条件。
3. **独立阅读**：先读需求/不变量和调用边界，再读变更；不读取其他评审者的 finding 草稿。
4. **验证发现**：检查调用者、错误路径、测试、配置和依赖上下文；能运行时只在授权隔离环境执行最小验证。
5. **标准化 finding**：每项包含标题、位置、维度、事实、触发条件、影响、证据、严重度、建议和不确定性。
6. **去重与关联**：按“同一问题”而非仅按同一行合并；保留不同维度的独立风险和所有支持证据。
7. **校准严重度**：结合影响、可利用性/发生概率、暴露范围、可检测性、可逆性和现有控制；记录为何高于或低于初始评级。
8. **处理冲突**：对矛盾事实、严重度或建议保留双方依据，指定复核动作，不用投票静默覆盖。
9. **汇总与门禁**：按严重度和证据排序，给出整体结论、未决项、合并前阻断项和安全下一步；报告完成不代表代码已合并。

## Finding 模板

```markdown
### [<ID>] <concise title>

Dimension: Security | Correctness | Architecture | Performance | Reliability | Testing | Accessibility
Status: Confirmed | Likely | Hypothesis | Disputed | Resolved | Rejected
Severity: Critical | High | Medium | Low | Informational
Location: `<file>:<line or range>`

## Fact and trigger
<what the code does and the input/state required>

## Impact
<user, data, security, reliability, cost, or maintenance impact; scope and likelihood>

## Evidence
- `<evidence ID>`: <test, code path, config, trace, or exact observation>
- Counter-evidence/limitation: <...>

## Recommendation
<bounded remediation or safe investigation; do not claim it was implemented>

## Disposition
Owner: <role>
Decision: Fix before merge | Track | Needs evidence | Accept risk
Follow-up evidence: <test or review needed>
```

## 去重规则

- 同一位置、同一根本问题：合并，保留更完整事实和所有维度归属；
- 同一位置、不同问题：分开，标为 co-located；
- 同一问题、不同位置：分开定位并交叉引用，避免修一处漏一处；
- 冲突严重度：回到影响、概率和控制证据重新校准，不能机械取最高或最低；
- 冲突建议：并列呈现取舍、前置条件和决策人，不静默选择。

## 汇总报告模板

```markdown
# Consolidated Code Review

Target: <repository, base/head, scope>
Review dimensions: <...>
Evidence freshness: <timestamp>
Overall: Approve | Approve with follow-up | Changes requested | Blocked

## Findings by severity
| ID | Dimension | Location | Severity | Status | Evidence |
| --- | --- | --- | --- | --- | --- |

## Cross-review notes
- Agreement: <...>
- Disagreement and resolution path: <...>
- Unreviewed scope or missing access: <...>

## Merge gates
- Critical/High unresolved: <count and IDs>
- Required tests/evidence: <...>
- Independent approval required: <...>
- Decision authority: <role>
```

## 质量门槛

- 每个 finding 有精确范围、触发条件、影响和可复核证据；
- 评审范围、base/head、工具版本和未覆盖部分明确；
- 评审者保持独立，去重不丢失维度、证据或异议；
- 严重度说明影响、概率、控制和不确定性，不受票数或作者身份影响；
- 未解决的高影响发现、关键测试缺失、冲突事实或越权访问时返回 `BLOCKED`；
- 报告不声称已修复、已批准或已合并未执行的动作。

## Related Skills

- `parallel-debugging` - 对多个根因假设进行独立调查和证据仲裁
- `requesting-code-review` - 准备精确范围、需求和测试证据的评审请求
- `verify-agent-action` - 在高影响提交、合并或发布前核验动作授权
