---
name: "architecture-patterns"
display_name: "后端架构模式"
display_name_en: "Backend Architecture Patterns"
description: "Use when designing or refactoring a backend module or service with Clean, Hexagonal, Onion, or Domain-Driven Design patterns; make boundaries, dependencies, ports, adapters, and test seams explicit before changing code."
description_zh: "用于使用整洁架构、六边形架构、洋葱架构或领域驱动设计设计/重构后端模块或服务；在改代码前明确边界、依赖、端口、适配器和测试接缝。"
description_en: "Choose architecture patterns from actual coupling and change forces, define inward dependency rules, bounded contexts, domain invariants, ports and adapters, migration seams, and evidence-based trade-offs without imposing ceremony or authorizing production changes."
category: "development"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized repository, runtime constraints, dependency graph, domain requirements, and test environment; architecture guidance does not authorize code or infrastructure changes"
---

# 后端架构模式

架构模式是边界和依赖规则，不是固定目录名。先识别业务不变量、变化方向、外部依赖和团队约束，再选择能降低耦合并改善验证的最小结构。任何模式都必须用可检查的依赖、契约和测试证据证明价值。

## 适用范围与安全门禁

开始前记录仓库 revision、模块/服务范围、业务目标、非功能约束、运行时和部署边界、现有测试、数据迁移限制以及决策人。

- 只读取获授权的代码、配置、架构图和运行证据；报告不复制秘密、客户数据或内部地址。
- 架构建议不等于实现、数据库迁移、依赖升级、流量切换或生产变更授权。
- 如果目标边界、关键调用链、数据所有权或回滚路径不可确认，标记 `BLOCKED`，不要用模式名称掩盖未知信息。
- 先记录现状和证据，再提出目标结构；不以“大规模重写”作为默认方案。

## 模式选择

| 模式 | 适合解决 | 关键规则 | 常见误用 |
| --- | --- | --- | --- |
| Clean/Onion | 业务规则需要脱离框架、数据库和交付层验证 | 依赖指向领域/应用内层，外层实现内层定义的接口 | 只改目录，不改变依赖方向 |
| Hexagonal | 外部系统多、替换成本高、需要测试替身 | 核心通过 driving/driven ports 与 adapters 交互 | 为每个类机械创建接口 |
| DDD bounded context | 术语、规则和数据所有权在子域间不同 | 每个上下文维护自己的模型，通过明确映射协作 | 跨上下文共享实体和数据库表 |
| Modular monolith | 需要先治理边界，暂不承担分布式成本 | 模块接口和数据所有权清晰，进程内调用也受契约约束 | 把包名当作边界，任意跨模块读写 |

选择时写出未选模式及原因。若真正问题是查询慢、发布流程或单个缺陷，先解决问题，不要为了“架构完整”引入额外层次。

## 依赖方向

推荐的最小分层如下：

```text
外部系统 / HTTP / CLI / 消息 / 数据库
             ↓ adapters
       ports + application use cases
             ↓
       domain entities / value objects / policies
```

- **Domain**：实体、值对象、领域服务和不变量；不导入 HTTP、ORM、消息客户端或框架装饰器。
- **Application**：编排用例、事务边界和权限上下文；依赖领域和抽象端口，不依赖具体数据库/网络实现。
- **Ports**：由需要能力的一侧定义最小接口；命名契约、错误、幂等和超时，不隐藏重要副作用。
- **Adapters**：将 HTTP、SQL、队列、第三方 API 和序列化映射到端口；负责技术细节、重试和观测。

依赖必须向内。若内层直接导入外层，记录具体 import/call 证据、产生的耦合和最小隔离方案；不要把“禁止循环依赖”简化为全局静态规则而忽略合法的编译期类型引用。

## 领域边界与模型

### Bounded Context

为每个上下文写明：核心能力、拥有的数据、术语、外部协作者、公开契约和不变量。上下文之间通过 ID、DTO、事件或 anti-corruption layer 交换，不共享可变领域实体。

### 领域对象

- **Entity**：有稳定身份，生命周期内状态可变；身份和不变量由领域负责。
- **Value Object**：由属性定义，优先不可变；在构造时校验 Email、Money、Address 等约束。
- **Aggregate**：一致性边界；外部只通过 aggregate root 修改内部对象，避免跨聚合隐式事务。
- **Repository**：保存/恢复领域对象的端口，不把 ORM 查询细节泄露到用例或领域。
- **Domain Event**：描述已发生的业务事实；说明顺序、重复、失败、重放和敏感字段处理。

不要为了“DDD”给简单 CRUD 增加空洞实体、仓储和事件。只有当不变量、所有权或替换边界需要它们时才引入。

## 设计流程

1. **建立现状图**：列出入口、核心规则、数据库/队列/第三方依赖、调用者、数据流和已有故障证据。
2. **识别变化力**：哪些规则频繁变，哪些技术依赖需替换，哪些边界必须独立部署或独立授权。
3. **定义不变量**：为每个用例写前置条件、状态变化、错误、幂等语义、事务/一致性要求和后置条件。
4. **划分边界**：确定上下文、模块、聚合和数据所有权；记录跨边界调用的契约与映射。
5. **定义最小端口**：由用例或领域定义需要的能力，明确超时、重试、错误、分页、并发和副作用。
6. **选择适配器**：将框架、ORM、消息和第三方 API 留在外层，映射输入/输出并保留可观测性。
7. **设计迁移切片**：优先选一个可回滚的用例或边界，使用 seam、facade、adapter 或 strangler 路径，避免一次性重写。
8. **验证并记录取舍**：运行依赖检查、领域单测、适配器契约测试和必要的集成测试；用 ADR 记录替代方案、代价和复查条件。

## 测试边界

每个用例应能在不启动真实数据库、网络或 Docker 的情况下验证核心行为。使用内存端口或 fake 时，确保它实现的契约足以暴露错误，不要把 fake 当成真实系统的性能/事务证明。

建议的证据层次：

- 领域单元测试：值对象、聚合不变量、策略和边界错误；
- 应用测试：用例编排、权限上下文、幂等和端口错误；
- 契约测试：适配器与数据库/HTTP/消息协议的 schema、状态码、重试和错误映射；
- 集成测试：真实依赖中的事务、索引、序列化、并发和迁移行为；
- 架构检查：依赖方向、禁止导入、模块所有权和公共 API 的可重复检查。

未运行的测试必须标记 `Unknown`；内存测试通过不代表真实数据库、网络或部署已验证。

## 常见诊断

### 用例测试需要真实数据库

如果业务规则直接调用 ORM 或数据库客户端，先把能力收敛成由应用层定义的 repository/query port，再提供隔离测试替身。保留需要真实数据库验证的查询、事务和约束到契约/集成测试。

### 层之间循环依赖

找出环中的具体 import 和运行时调用。通常由用例导入具体适配器、共享模型同时承担领域和持久化职责或跨上下文直接复用实体导致。反转依赖、移动映射或引入 anti-corruption layer，并用架构检查防回归。

### 框架装饰器进入领域

将 ORM/Pydantic/HTTP 模型与领域对象分开，在 adapter mapper 中双向转换。若性能或序列化约束要求共享类型，记录这是有意取舍，并测试框架升级的影响。

### 控制器承载所有业务逻辑

控制器只解析输入、建立授权上下文、调用用例并映射响应。把跨请求可复用的规则移到领域/应用层，同时保留错误和观测语义。

### 上下文模型泄漏

例如订单模块直接导入身份模块的 `User` 实体。改为本地 `CustomerId`/快照或显式端口，并定义数据新鲜度、失败和权限边界；不要靠共享数据库表“解决”模型冲突。

## 架构决策记录模板

```markdown
# ADR: <decision>

Status: Proposed | Accepted | Deprecated | Superseded
Scope: <module/service and revision>
Context: <business and technical forces with evidence>
Decision: <boundaries, dependency direction, ports, adapters>
Alternatives: <rejected options and reasons>
Consequences: <benefits, costs, operational and migration risks>
Migration: <smallest reversible slices and rollback>
Evidence: <tests, dependency graph, benchmarks, incidents>
Review trigger: <what change reopens this decision>
```

## 质量门槛

- 模式选择与实际耦合、变化力和约束相连，而不是只引用术语；
- 领域/应用不依赖具体框架，跨边界契约、数据所有权和错误语义明确；
- 关键不变量有测试，适配器有契约或集成证据，未验证项显式标注；
- 迁移有小切片、兼容窗口、观测和回滚边界；
- 不把建议描述成已实施，不在没有独立授权时修改代码、数据或基础设施；
- 依赖方向、上下文边界或回滚证据无法确认时返回 `BLOCKED`。

## Related Skills

- `api-design-principles` - 设计公共 API 的资源、契约、错误和兼容性
- `workflow-orchestration-patterns` - 设计跨步骤、重试和补偿的工作流边界
- `architecture-decision-records` - 沉淀有证据的架构取舍与生命周期
- `database-migration` - 规划可回滚、可验证的数据结构迁移
