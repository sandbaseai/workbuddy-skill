---
name: "sql-code-review"
display_name: "SQL 代码评审"
display_name_en: "SQL Code Review"
description: "Use when reviewing SQL across MySQL, PostgreSQL, SQL Server, or Oracle for injection risk, access control, correctness, performance, maintainability, and migration safety."
description_zh: "用于评审 MySQL、PostgreSQL、SQL Server 或 Oracle SQL，检查注入、权限、正确性、性能、可维护性和迁移安全。"
description_en: "Review SQL across major relational databases for injection risk, access control, correctness, performance, maintainability, and migration safety."
category: "database"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized read access to SQL, schema, migration, and query-plan evidence; production writes require separate authorization"
---

# SQL 代码评审

对 SQL 和数据访问代码做跨数据库评审，优先发现会导致数据泄露、错误写入、锁争用或不可逆迁移的风险。结论必须绑定语句、调用位置、数据库类型和可复现证据。

## 检查清单

- **注入与参数**：确认用户输入、排序字段、表名和动态条件使用白名单或参数化；禁止字符串拼接 SQL。
- **权限**：检查最小权限、角色继承、RLS/视图边界、函数执行者权限和敏感列暴露。
- **正确性**：检查 NULL、重复行、JOIN 基数、事务边界、隔离级别、时区、分页和幂等性。
- **性能**：检查谓词可索引性、隐式类型转换、全表扫描、N+1、排序/聚合内存、统计信息和执行计划。
- **可维护性**：检查命名、重复逻辑、硬编码状态、方言依赖、错误处理和测试覆盖。
- **迁移**：检查兼容窗口、锁持有、回填批次、约束验证、复制延迟、回滚和旧客户端行为。

## 工作流程

1. 锁定数据库方言/版本、调用方、数据敏感级别、读写比例和评审范围。
2. 先做静态审查，再结合脱敏 schema、参数样例、基数和 `EXPLAIN`/等效计划验证高风险项。
3. 对每项发现输出严重度、精确位置、触发条件、证据、影响、修复建议和回归验证。
4. 用临时环境和单变量实验验证性能或迁移建议，不直接修改生产数据库。

## WorkBuddy 安全边界

- 默认只读；不得执行未授权 DDL/DML、权限变更、锁表、删除或生产诊断。
- 示例使用占位符和脱敏数据，不输出连接串、令牌、客户记录或完整生产快照。
- 缺少方言、版本、计划或数据量时标为未知，不把通用建议包装成确定结论。
