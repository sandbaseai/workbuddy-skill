---
name: "code-review-excellence"
display_name: "卓越代码评审"
display_name_en: "Code Review Excellence"
description: "Use when reviewing a change set, establishing review standards, mentoring contributors, or deciding whether findings block integration; produce constructive, evidence-linked feedback focused on behavior and risk."
description_zh: "用于评审变更、建立评审规范、辅导贡献者或判断发现是否阻断集成；以行为和风险为中心，产出建设性且有证据链接的反馈。"
description_en: "Review behavior, correctness, security, performance, tests, and maintainability with a bounded process; separate blocking defects from preferences, make feedback actionable, and record uncertainty without approving unverified work."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized repository revision, diff, requirements, test evidence, and review destination; comments do not authorize code changes or merges"
---

# 卓越代码评审

把代码评审变成发现风险、共享知识和改善设计的协作过程。评审结论必须针对代码和可观察行为，而不是作者；格式化、导入排序和简单拼写优先交给自动化工具。

## 评审边界

开始前记录：仓库、精确 `base`/`head`、需求或关联任务、文件范围、评审截止时间、可访问的测试/依赖环境、报告读者和合并决策人。

- 只读取被授权的代码、配置、测试和证据；不要把秘密、客户数据、私有 URL 或完整凭据复制到评论或报告。
- 先确认 CI、构建和已知限制，再开始逐行阅读；若 diff 过大或需求不清，先提出拆分或补充上下文。
- 评审意见不自动修改文件、批准、关闭线程、合并或发布；这些动作需要独立授权。
- 无法访问关键文件、测试或需求时标记 `BLOCKED`，不要用猜测代替结论。

## 评审目标与优先级

评审应该回答：变更是否满足需求，是否保持已有不变量，失败时是否安全，是否有足够的回归证据，以及维护成本是否可接受。

按以下顺序处理：

1. **正确性与边界**：正常路径、空值、边界、并发、重试、时序、状态迁移和错误传播。
2. **安全与权限**：信任边界、认证授权、输入校验、注入、敏感数据、秘密、上传和外部依赖。
3. **可靠性与性能**：超时、取消、幂等、资源释放、N+1、阻塞 I/O、缓存、容量和降级。
4. **测试与可观测性**：行为测试、负面路径、回归覆盖、测试隔离、日志/指标/追踪和告警。
5. **设计与维护性**：接口契约、模块边界、命名、重复逻辑、迁移、兼容性和文档。

将 lint、格式化、导入顺序和可机械修复的拼写交给 CI，除非它们会造成实际行为或发布风险。

## 分阶段流程

### 1. 了解上下文

- 阅读需求、验收标准、设计决策和变更说明。
- 固定并记录 `base`/`head`，确认 diff 没有被重新生成或混入无关文件。
- 查看 CI、测试、构建产物、迁移说明和已知风险；记录未运行的检查及原因。
- 若变更超过团队可有效审查的规模，建议按接口/抽象、实现、集成和测试拆分。

### 2. 高层检查

先不逐行纠结实现，确认：

- 方案是否直接解决需求，是否引入不必要的复杂度或重复机制；
- 新文件、依赖、配置、数据库迁移和公共 API 是否放在正确边界；
- 失败路径、回滚/兼容路径和运行时开关是否明确；
- 测试策略是否覆盖最重要的行为和风险，而不是只覆盖内部实现细节。

### 3. 逐文件验证

对每个关键文件追踪调用者、数据流和错误路径。每个潜在问题都要验证触发条件、实际影响和现有控制：

- 逻辑：空集合、极值、重复请求、重入、竞态、时区、编码和部分失败；
- 安全：输入是否跨越信任边界，权限是否在每个敏感动作前检查，错误是否泄露信息；
- 性能：查询数量、复杂度、内存、连接、并行度、超时和热路径；
- 测试：测试的是用户可见行为，是否包含负面路径、独立性、确定性和回归断言；
- 维护：职责是否清晰，抽象是否有使用者，契约/迁移/文档是否与实现一致。

能在授权隔离环境验证时，执行最小且可回收的检查，并引用实际输出；不能运行时明确标注未验证。

### 4. 反馈与决定

每条评论都说明事实、触发条件、影响、证据和可行的下一步。优先提出最少但能解决根因的建议，必要时提供示例或测试方向。总结中分别列出优点、阻断项、非阻断建议、疑问和未覆盖范围，再给出：

- `Approve`：没有未解决的高影响问题，关键证据充分；
- `Approve with follow-up`：风险已接受且责任人/期限/证据明确；
- `Changes requested`：存在合并前必须处理的问题；
- `Blocked`：缺少授权、范围、关键证据或存在未解决的高影响不确定性。

决定不等于执行：除非得到独立授权，不要代作者修改、批准、合并或发布。

## 可执行反馈

使用描述问题而非评价作者的语言。把命令式偏好改成可验证的问题：

```markdown
<!-- 不可执行或带人身色彩 -->
这段代码很差，必须重写。

<!-- 可执行 -->
当两个请求同时更新同一记录时，`save()` 先读后写且没有版本检查；第二次写入会覆盖第一次更新。
在并发测试中复现后，请考虑乐观锁或明确的冲突返回，并补充回归断言。
```

评论应尽量包含：

```markdown
### [R-12] 并发更新会丢失写入

Severity: High
Status: Confirmed
Location: `src/store.ts:84-97`

事实与触发条件：两个请求读取同一版本并在没有条件更新的情况下写回。
影响：后提交者静默覆盖前一更新，导致订单状态与审计记录不一致。
证据：`test/concurrency.spec.ts` 的双请求实验；数据库更新语句缺少版本条件。
建议：使用版本条件更新并对冲突返回可重试错误；添加并发回归测试。
```

## 严重度与标签

严重度应由影响、发生概率/可利用性、暴露范围、可检测性、可逆性和现有控制共同决定，而不是由评论数量、作者身份或个人偏好决定：

- `Critical`：可造成重大数据/安全/服务影响，且需要立即阻断；
- `High`：高概率或高影响的正确性、安全、数据完整性或可靠性问题；
- `Medium`：应在近期修复，否则会造成可见缺陷、回归或运维负担；
- `Low`：影响有限且有明确控制或替代路径；
- `Informational`：知识、记录或可选改进，不要求动作。

评论标签建议使用 `[blocking]`、`[important]`、`[nit]`、`[question]`、`[suggestion]`、`[praise]`。`nit` 和 `suggestion` 不得伪装成阻断项；`question` 在事实确认前不是缺陷结论。

## 安全、测试与语言检查表

### 安全

- [ ] 输入在信任边界处校验，查询使用参数化，输出按上下文编码；
- [ ] 认证、授权和租户边界在每个敏感动作前生效；
- [ ] 没有硬编码秘密、过宽错误、危险动态执行或未限制的上传；
- [ ] 密码、令牌、个人数据的存储、日志和传输符合项目策略；
- [ ] 公共端点具备必要的限流、幂等、CSRF 或重放控制。

### 测试

- [ ] 测试描述行为而非私有实现；
- [ ] 覆盖成功、边界、错误、权限和并发/重试路径；
- [ ] 测试相互独立、确定、可按任意顺序运行；
- [ ] 变更后的公共契约、迁移和可观测性有回归证据；
- [ ] 未运行或不可信的测试被明确列出，不被默认为通过。

### Python / JavaScript / TypeScript 提示

- Python：检查可变默认参数、过宽 `except`、共享类属性、资源未关闭和阻塞调用；
- JavaScript/TypeScript：检查 `any` 扩散、未处理的异步失败、输入类型缩窄、可变共享状态和响应状态码；
- 两者都要结合实际项目约定，不因语言习惯单独制造阻断项。

## 争议与收敛

作者不同意时，先确认事实和约束，再用最小实验、基准或测试代替权威争论。记录：

1. 双方主张和各自证据；
2. 哪些部分已经确认、哪些仍是 `Unknown`；
3. 需要谁执行什么验证，以及通过条件；
4. 决策人、风险接受期限和后续追踪位置。

如果问题不是高风险且实现满足契约，接受合理取舍，不把风格偏好升级为阻断。没有证据时保留 `Hypothesis` 或 `Disputed`，不要静默改写结论。

## 评审报告模板

```markdown
# Code Review Report

Target: <repository, base/head, scope>
Requirement: <link or summary>
Checks: <passed, failed, skipped, unavailable>
Overall: Approve | Approve with follow-up | Changes requested | Blocked

## Strengths
- <specific positive observation>

## Findings
| ID | Location | Severity | Status | Evidence | Decision |
| --- | --- | --- | --- | --- | --- |
| R-1 | `file:line` | High | Confirmed | `test/log/trace` | Fix before merge |

## Questions and follow-ups
- <bounded question, owner, due evidence>

## Unreviewed or uncertain scope
- <missing access, skipped test, stale artifact, or dispute>

## Merge gates
- Critical/High unresolved: <count and IDs>
- Required evidence: <tests or review>
- Decision authority: <role>
```

## 质量门槛

- 每个阻断发现有精确位置、触发条件、影响和可复核证据；
- 评审范围、版本、工具/测试状态和未覆盖内容明确；
- 反馈针对行为，严重度与建议一致，非阻断偏好不会阻塞合并；
- 关键事实冲突、证据缺失、越权访问或高影响问题未解决时返回 `BLOCKED`；
- 报告不声称已修复、已批准、已合并或已发布未执行的动作。

## Related Skills

- `multi-reviewer-patterns` - 分配独立评审维度、去重发现并保留异议
- `requesting-code-review` - 准备带精确范围、需求和测试证据的评审请求
- `verify-agent-action` - 在高影响提交、合并或发布前核验授权动作
