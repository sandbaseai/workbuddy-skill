---
name: "postgresql-table-design"
display_name: "PostgreSQL 表设计"
display_name_en: "PostgreSQL Table Design"
description: "Use when designing or reviewing PostgreSQL schemas, data types, keys, constraints, indexes, JSONB, partitioning, RLS, or live migrations."
description_zh: "用于设计或审查 PostgreSQL schema、数据类型、键、约束、索引、JSONB、分区、RLS 或在线迁移。"
description_en: "Design PostgreSQL schemas with workload-backed types, constraints, access-path indexes, partitioning, JSONB/RLS boundaries, safe migrations, and rollback evidence."
category: "database"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized schema metadata, representative workload/plan evidence, an isolated database clone, and migration tooling; production DDL, locks, permissions, and data changes require separate authorization"
---

# PostgreSQL Table Design

先从数据语义、访问路径、写入/更新模式和生命周期设计 PostgreSQL 表，再决定类型、约束、索引和分区。schema 质量不仅是 DDL 能执行，还要保证一致性、查询计划、迁移可回滚、权限和数据删除要求。

## 使用边界

- 开始前确认 PostgreSQL/extension 版本、数据量、读写比例、查询/SLO、复制、分区、tenant/PII、owner、备份和目标环境。
- 默认只读审查 DDL、schema/catalog、查询计划、锁/复制指标和迁移脚本；在隔离 clone 用脱敏或合成数据验证。
- 不擅自执行生产 DDL、索引构建、`VACUUM`/`CLUSTER`、权限/RLS、回填、删除或扩容；这些操作需要授权、备份和回滚方案。
- DDL、路径、样本、错误和统计信息不得泄露凭据、个人数据或完整业务行。

## 类型、键与约束

保持 snake_case，避免依赖带引号的大小写标识符。默认使用 `BIGINT GENERATED ALWAYS AS IDENTITY` 或有明确理由的 UUID；事件时间用 `TIMESTAMPTZ`，金额/精确小数用 `NUMERIC`，字符串用 `TEXT` 并在确有业务限制时加 length check。`BOOLEAN` 通常 `NOT NULL`，枚举只适合小且稳定的集合；会演进的业务值使用受约束 text 或 lookup table。

优先 3NF 消除更新异常，只有在真实 plan/基线证明收益后才反规范化。每个 reference/entity 表定义 PK；FK 明确 `ON DELETE/UPDATE` 语义并手动为引用列建索引。`CHECK` 中的 NULL 会通过三值逻辑，需与 `NOT NULL` 配合；确认 UNIQUE 对 NULL 的语义，PG15+ 可按需要使用 `NULLS NOT DISTINCT`。

```sql
CREATE TABLE orders (
  order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'paid', 'canceled')),
  total NUMERIC(12,2) NOT NULL CHECK (total >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX orders_customer_id_idx ON orders (customer_id);
CREATE INDEX orders_active_customer_idx ON orders (customer_id)
  WHERE status IN ('pending', 'paid');
```

用 exclusion constraint 防止时间/range 重叠等数据库可表达的不变量；对循环关系或批量导入谨慎使用 `DEFERRABLE`，并验证提交时行为。不要只在应用层实现唯一性、金额范围、状态转移或租户边界。

## 索引与 workload

索引必须对应实际 access path：B-tree 适合等值/范围/排序，复合索引服从 leftmost-prefix，partial index 适合热子集，expression index 必须与查询表达式一致，INCLUDE 只在 plan 证实 index-only scan 时使用。GIN 适合 JSONB/数组/全文，GiST 适合 range/空间/排他约束，BRIN 适合磁盘顺序与时间相关的大表。

建立索引前保存查询基线和 `EXPLAIN (ANALYZE, BUFFERS)` 证据，检查写放大、大小、缓存、锁、复制延迟和维护成本。禁止用索引数量替代查询分析；删除或改索引也要验证所有消费者和回滚窗口。

JSONB 只存可变/半结构化属性，关键过滤字段提取成类型明确的列或 generated column；按查询选择 GIN default/jsonb_path_ops 或 B-tree，避免把整个文档当作无界 schema。敏感 JSONB 字段仍需 ACL、脱敏和 retention。

## 分区、存储与生命周期

只有当表规模、查询过滤、维护/删除模式和分区裁剪证据支持时才分区。RANGE 适合时间、LIST 适合离散租户/类别、HASH 适合均匀分布；声明式分区优先，检查 PK/UNIQUE 是否包含分区键及跨分区 FK 限制。为未来分区、默认分区、边界、归档、压缩和 retention 设计运维流程，不用 inheritance 伪装分区。

评估 TOAST、fillfactor、HOT 更新、dead tuples、autovacuum、临时/UNLOGGED 表、备份和复制；不要以 `CLUSTER` 或一次性 vacuum 取代长期 workload 设计。大表迁移和批量删除按有界批次执行，监控锁、WAL、复制和恢复时间。

## RLS 与在线迁移

RLS/权限策略默认 fail closed，按 tenant/角色测试 SELECT/INSERT/UPDATE/DELETE、owner、后台任务、superuser 绕过和连接池上下文；不要把租户 ID 仅作为客户端可修改的字段。敏感数据的列级暴露、备份、日志和缓存一起审查。

在线迁移拆成 expand → dual-read/write 或兼容代码 → backfill → validate → contract，逐步加约束和索引。评估 `NOT VALID`/validate、`CREATE INDEX CONCURRENTLY`、默认值、长事务、锁超时、触发器、副作用和旧客户端；每步有观测、停止条件、回滚或前向修复。schema version、迁移 hash、执行范围和结果必须留证。

## 质量门禁

- [ ] 类型、PK/FK/UNIQUE/CHECK/exclusion、NULL、时间、金额和状态语义符合数据与业务契约。
- [ ] 索引来自真实 access path/plan，并评估写放大、空间、锁、缓存、WAL 和复制成本。
- [ ] JSONB、extension、分区、TOAST、vacuum、retention、备份和恢复策略有版本依据。
- [ ] RLS/权限/tenant/PII 边界在所有角色和后台路径通过正向与负向测试。
- [ ] 在线迁移有 expand/compat/backfill/validate/contract、锁/复制监控、停止和回滚证据。
- [ ] 生产 DDL、索引、权限、回填、删除和数据写入均有授权、备份与恢复方案。
