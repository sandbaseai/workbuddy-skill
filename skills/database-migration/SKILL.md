---
name: "database-migration"
display_name: "数据库迁移"
display_name_en: "Database Migration"
description: "Use when planning or reviewing database schema/data migrations, ORM changes, zero-downtime deployment, backfills, compatibility, or rollback."
description_zh: "用于规划或审查数据库 schema/数据迁移、ORM 变更、零停机部署、回填、兼容性或回滚。"
description_en: "Design observable database migrations with expand-contract compatibility, bounded backfills, lock/replication analysis, data validation, staged rollout, and recoverable rollback."
category: "database"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized schema/data metadata, an isolated database clone, migration tooling, backup/recovery evidence, and deployment coordination; production DDL, backfills, permissions, and destructive actions require separate authorization"
---

# Database Migration

以可兼容、可观测、可暂停的阶段演进 schema 和数据。迁移的成功条件不仅是脚本退出 0，还包括旧/新应用兼容、数据完整性、锁与复制影响、回填进度、权限、恢复时间和明确的停止/回滚路径。

## 使用边界

- 开始前确认数据库/ORM 版本、表规模、读写模式、复制拓扑、备份、SLO、租户/PII、owner、发布窗口和目标环境。
- 默认只读审查 schema、迁移脚本、查询计划、锁/WAL/复制指标和应用兼容性；在隔离 clone 使用脱敏/合成数据演练。
- 不擅自执行生产 DDL、回填、重命名/删除、权限/RLS、索引、replica 操作或 restore；这些动作需要授权、备份和恢复演练。
- 日志、备份、迁移报告和样本不得泄露 secret、完整业务行或个人数据。

## 迁移契约与 expand-contract

每个迁移记录不可变版本、前置条件、目标 schema、数据不变量、owner、预计锁/资源、监控、停止条件、验证、兼容窗口和回滚/前向修复。优先采用：

1. **Expand**：新增可选列/表/索引或兼容字段，不破坏旧客户端。
2. **Migrate**：应用同时兼容旧/新，按有界批次回填或双读/双写，记录 watermark 和失败项。
3. **Validate**：校验计数、hash、NULL/重复、约束、读写、延迟、复制和下游消费者。
4. **Contract**：所有消费者切换并观察稳定窗口后，才收紧约束、停止双写或移除旧结构。

破坏性变更不能伪装成一次 rename/drop。字段/类型/语义变化要有兼容版本、消费者影响和迁移文档；数据库回滚不等于应用版本回滚。

## Schema 与 ORM

迁移文件是审计记录，不依赖当前模型自动推导覆盖历史。检查 Sequelize/TypeORM/Prisma 或其他 ORM 生成 SQL、默认值、NULL 语义、索引、FK、事务和 provider 方言；在目标数据库版本上审查实际 SQL。大表避免长事务和全表锁，必要时拆分 `NOT VALID`/validate、并发索引、分批更新和低优先级窗口。

```text
add nullable column ──> deploy dual-compatible code
        │                         │
        └── bounded backfill ─────┘
                 ↓
      validate counts/invariants/consumers
                 ↓
      enforce constraint ──> stop dual-write ──> retire old field
```

## 数据转换与回填

转换先定义旧值到新值的可逆/不可逆映射、空值/异常/重复规则、精度/时区、幂等键和审计摘要。回填按主键/时间分片有界执行，支持暂停/重启，限制 batch、锁、CPU、WAL、复制延迟和下游负载；失败行进入隔离清单，不静默跳过。

写入新结构前后比较抽样与聚合校验（计数、金额/范围、关系、不变量、hash），避免把 PII 放入证据。双写要处理顺序、重复、部分成功和未知结果；优先 outbox/事务或可证明的一致性协议。缓存、搜索索引、CDC、备份和下游 ETL 也要纳入迁移图。

## 锁、复制与发布

预估 DDL 锁模式、等待队列、长事务、deadlock、WAL/IO、vacuum、replication lag、连接池和恢复时间；设置 lock/statement timeout 和停止条件。部署前验证旧代码、新代码、迁移中间态和混合版本可以同时运行，按 canary/分批逐步推进。

监控迁移进度、剩余量、速率、失败项、数据质量、错误率、延迟、锁、复制和下游 freshness。监控缺失或指标不可信时暂停晋级，不把“未测量”当成“无影响”。

## 回滚、恢复与安全

优先设计向前修复和兼容开关；对数据转换准备备份/快照、版本化新表、补偿脚本和恢复时间证据。不要假设 `down` 可安全逆转已产生的业务副作用，也不要用 `DROP`/restore 覆盖生产数据作为默认回滚。任何恢复都要验证权限、计数、约束、索引、应用读写和复制一致性。

迁移凭据最小权限、短期有效且不写入脚本/日志；生产执行前确认目标账号、区域、数据库、tenant 和 schema，防止将 staging 脚本跑到生产或反之。

## 测试与交付

隔离测试覆盖 up/down 或前向修复、空/大/脏数据、重复运行、并发 writer、旧/新应用混合、锁超时、复制延迟、部分回填、失败重启、权限、备份恢复和验证器故障。报告包含版本/hash、前置条件、SQL/ORM 证据、阶段状态、数据质量、锁/复制/成本、消费者、授权、停止/回滚与未覆盖范围，并区分 observed、derived、unknown。

## 质量门禁

- [ ] schema/data 契约、版本、owner、消费者、数据不变量、PII 和目标环境已确认。
- [ ] expand/兼容/回填/验证/contract 阶段、混合版本和停止条件已设计。
- [ ] SQL/ORM 实际语义、锁、长事务、WAL、复制、连接池和成本有隔离证据。
- [ ] 回填幂等、有界、可暂停，失败项、重复、部分成功和下游索引/CDC 已处理。
- [ ] 计数/hash/约束/业务不变量、备份恢复、权限和旧新应用均通过验证。
- [ ] 生产 DDL、数据、权限、回填、删除、restore 和回滚均有授权与恢复方案。
