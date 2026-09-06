---
name: "postgresql-code-review"
display_name: "PostgreSQL 代码评审"
display_name_en: "PostgreSQL Code Review"
description: "Use when reviewing PostgreSQL SQL, schemas, migrations, and data-access code for correctness, performance, maintainability, and database-specific security."
description_zh: "用于评审 PostgreSQL SQL、schema、迁移和数据访问代码，重点检查正确性、性能、可维护性以及 PostgreSQL 特有的安全边界。"
description_en: "Review PostgreSQL SQL, schemas, migrations, and data-access code for correctness, performance, maintainability, and database-specific security."
category: "database"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized read access to the relevant PostgreSQL code, schema, query plans, and migration context; production writes require separate authorization"
---

# PostgreSQL 代码评审

对 PostgreSQL 代码做证据驱动的专项评审，覆盖 SQL 行为、schema 设计、索引、JSONB/数组、事务、迁移、查询计划和 Row Level Security。结论应绑定代码位置、数据规模或可复现的计划/测试证据。

## 评审范围

- **查询行为**：NULL、重复行、排序稳定性、时区、分页、隔离级别、锁和并发竞态。
- **JSONB 与数组**：访问路径是否有约束和合适索引，是否把结构化字段隐藏在无界 JSON 中，是否存在不必要的逐行拼接。
- **schema 与索引**：类型、约束、唯一性、外键、部分/表达式/覆盖索引、选择性和写入成本是否与 workload 一致。
- **迁移**：expand/contract、幂等回填、锁持有时间、复制延迟、兼容窗口、回滚和旧客户端行为。
- **安全**：参数化查询、RLS policy、角色/owner、`search_path`、函数权限、敏感字段暴露和审计边界。
- **性能证据**：优先使用 `EXPLAIN (ANALYZE, BUFFERS)`、实际基数、等待事件和基线；不把静态直觉当作慢查询证明。

## 工作流程

1. 锁定数据库版本、schema 版本、调用方、数据量级、读写比例和评审目标。
2. 先列出可复现的行为风险，再检查计划、索引、约束、事务和迁移影响。
3. 对每项发现说明严重度、触发条件、证据、影响范围、建议和验证命令；区分阻断项、建议项和未知项。
4. 对建议使用最小单变量实验或临时环境验证；比较计划、延迟、锁和写放大，不直接改生产数据库。
5. 评审完成后给出回归测试、监控指标、发布门槛和回滚条件。

## 输出与安全边界

- 不执行未授权的 DDL、DML、权限变更、`VACUUM FULL`、锁表或生产诊断；默认只读。
- SQL 示例使用占位符和脱敏数据，不输出连接串、令牌、客户记录或完整生产快照。
- 不建议为单个查询盲目添加索引；说明写入、存储、缓存和迁移成本。
- 若缺少统计信息、真实计划或版本上下文，明确标为未知，并列出最小安全取证动作。
