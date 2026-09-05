---
name: "deprecation-and-migration"
display_name: "退役与迁移"
display_name_en: "Deprecation and Migration"
description: "Use when replacing or sunsetting an old system, API, library, feature, or schema; plan consumer migration, compatibility windows, usage proof, and safe removal."
description_zh: "用于替换或下线旧系统、API、库、功能或数据库结构，并规划消费者迁移、兼容窗口、使用证据和安全移除。"
description_en: "Manage deprecation from decision through incremental migration and verified removal, with expand-contract patterns for production schemas and explicit rollback evidence."
category: "development"
version: "0.1.0"
author: "addyosmani/agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized code, dependency, usage, metrics, logs, schema, deployment, and consumer evidence; production migrations, announcements, deletion, and rollout require separate authorization"
---

# 退役与迁移

代码、API、依赖和功能不仅有开发成本，还有测试、补丁、文档、兼容和认知成本。退役是移除不再值得维护的表面，迁移是把用户和消费者安全地带到替代方案。本 Skill 防止“发一个弃用通知就算完成”，要求先证明替代方案、量化使用者、分阶段迁移、验证零活跃引用，再单独移除旧系统。

## 核心边界

- 先读取真实消费者、依赖图、指标、日志、配置、文档和历史；不要仅凭搜索结果或“没人提过”宣布零使用。
- 生产数据、schema、流量、权限、开关和删除操作默认只读；实施、通知、切流、删除和发布要有独立授权、回滚点和负责人。
- 公开迁移文档只包含经过脱敏的契约、步骤和版本信息，不包含客户数据、凭据、私有地址或内部讨论。
- 数据库 schema 不能依赖一次回滚恢复：添加、回填、切读、停写、删除必须拆成兼容阶段。
- 默认 advisory 弃用；只有安全风险、阻塞关键进展或维护成本明确证明必须强制迁移时，才使用硬截止日期，并同时提供工具、文档和支持。

## 何时使用

- 替换旧系统、API、库或重复实现；
- 下线功能、删除死代码或治理无人维护的“僵尸代码”；
- 迁移生产数据库 schema，尤其是列/表重命名、拆分、合并和删除；
- 在新系统设计阶段规划未来可退役性；
- 需要决定继续维护旧系统还是投入迁移。

## Step 1：做退役决策

在写公告或删代码前回答并记录来源：

1. 旧系统是否仍提供独特价值？如果是，先维护或缩小范围；
2. 有多少用户、服务、脚本、报表、插件和外部消费者依赖它？如何测量；
3. 是否存在覆盖关键用例的替代方案？没有替代方案时不得直接退役；
4. 每个消费者的迁移成本、手工步骤、兼容风险和 owner 是什么；
5. 不迁移的持续成本是什么：安全漏洞、工程时间、依赖风险和机会成本；
6. advisory 还是 compulsory？选择的风险证据、截止日期和升级路径是什么？

形成 decision record，分离 `Observed`、`Estimated` 和 `Unknown`。低活跃度不能直接证明没有隐性消费者，因为未记录的行为也可能已经成为契约。

## Step 2：先构建并证明替代方案

替代方案必须：

- 覆盖旧系统的关键用例和权限模型；
- 有版本化 API/配置、迁移指南、示例、支持渠道和所有者；
- 在目标环境中经过代表性集成/生产证据验证，而不只是“理论上更好”；
- 明确性能、成本、数据一致性、错误语义和可观测性差异；
- 有 feature flag、adapter 或兼容层时，定义启用、退出和清理日期。

若替代方案尚未具备，不宣布最终删除；可以建立并行试用或仅发布设计计划。

## Step 3：公告与迁移契约

公开通知至少包含：

```markdown
## Deprecation Notice: <OldSurface>

Status: Advisory | Compulsory
Effective: <date/version>
Replacement: <new surface and link>
Removal: <date or explicitly no hard deadline>
Reason: <user-facing reason without private data>
Impact: <affected behavior, compatibility, cost, and risk>

### Migration
1. <concrete source/config change>
2. <data or permission preparation>
3. <verification command or expected result>
4. <support/escalation path>
```

迁移指南必须说明旧/新行为差异、数据转换、权限、错误处理、回滚、兼容窗口、版本范围和完成判据。基础设施 owner 对自己拥有的消费者负责迁移或提供无需消费者改动的兼容更新，不能把成本无记录地转嫁给用户。

## Step 4：增量迁移消费者

逐个或按可回滚批次迁移：

1. 盘点代码、配置、部署、数据流和文档中的所有触点；
2. 更新到替代方案，保留必要 adapter 或 dual-read/dual-write；
3. 用单元、契约、集成、回放或合成流量验证行为等价；
4. 观察错误率、延迟、容量、成本、数据一致性和权限拒绝；
5. 删除该消费者对旧系统的引用，记录 commit、环境、时间和证据；
6. 失败时停止批次、恢复开关或回滚到仍兼容的版本。

常用模式：

- **Strangler**：旧系统 100% 流量起步，替代方案按 10%/50%/100% 金丝雀切流，确认旧流量为 0 后再删除；
- **Adapter**：保留旧接口，把调用转换到新实现，按消费者逐步切换；
- **Feature flag**：按租户/用户/消费者迁移，记录开关 owner、默认值、过期和清理条件。

不要同时改所有消费者和删除旧系统；并行窗口内旧、新代码都必须可用。

## Step 5：生产 schema 的 expand-contract

数据库变更采用以下顺序，不能原地 rename/drop：

```text
EXPAND → MIGRATE → CUT OVER → CONTRACT
添加兼容结构   批量回填/双写   切换读取并观察   停止旧写入后单独删除
```

例如将 `name` 改为 `full_name`：

1. 添加可为空的 `full_name`，先部署；
2. 应用同时写 `name` 与 `full_name`；
3. 低速、分批、可暂停地回填旧行；
4. 切换读取到 `full_name`，继续双写并观察；
5. 停止写 `name`，确认零读取/写入后，在后续独立部署删除旧列。

每阶段都要有前后兼容性、数据校验、锁/WAL/复制影响、限流、监控和恢复证据。大表回填不可在热路径执行；大型索引使用不阻塞写入的方式（例如 PostgreSQL 的 concurrent 构建，若该数据库支持）。每个 migration 都要编写并实际验证 down/recovery 路径；“能回滚代码”不等于能回滚数据。

## Step 6：移除前的零使用证明

只有在以下证据满足后才提出 contract/removal：

- 所有已知消费者已切换，使用指标/日志/依赖分析覆盖目标窗口；
- 旧 API、配置、权限、队列、报表、测试和文档没有活跃引用；
- 替代方案的关键用例、错误和权限行为已通过验证；
- 删除范围、顺序、备份/恢复、监控和 owner 已记录；
- 旧代码、测试、文档和配置可一起清理，且不会删掉仍代表新契约的测试；
- 通知、支持和观察窗口已结束，未决异常有明确处理。

删除后再次搜索引用并运行回归；发现活跃消费者时停止删除，不用“强制开关”掩盖证据缺口。

## 僵尸代码

僵尸代码没有清晰 owner，却有活跃消费者或安全/兼容负担。典型信号包括长期无提交、无人维护、无人修复的失败测试、已知高风险依赖和指向不存在系统的文档。对它只能做两种决定：指定 owner 并投入维护，或建立替代方案和迁移计划；不要无限期放在中间状态。

## 完成交付前检查

- [ ] 已量化活跃消费者、触点和迁移范围，Observed/Estimated/Unknown 分离。
- [ ] 替代方案覆盖关键用例，有版本化文档、支持、owner、验证和回滚路径。
- [ ] advisory/compulsory 选择有风险依据；强制迁移有工具、期限和支持。
- [ ] 公告、迁移指南、权限/数据影响和兼容窗口已脱敏且可执行。
- [ ] 消费者按批次迁移，测试、指标、开关、停止条件和恢复证据可追踪。
- [ ] 数据库变更按 expand→migrate→cut over→contract 分阶段，未原地删除或重命名。
- [ ] 回填有批量、限流、校验和暂停机制；down/recovery 已实际测试。
- [ ] 删除前有目标窗口内零使用证据，删除后完成引用搜索和回归。
- [ ] 所有生产写入、通知、切流、删除和发布均有独立授权。

## Related Skills

- `database-migration` - 设计兼容、回填、锁和复制边界
- `feature-flags` - 管理分阶段切换和开关清理
- `devops-rollout-plan` - 编排验证、go/no-go、沟通和回滚
- `constraint-driven-development` - 为迁移门禁和不下降基线建立质量契约
