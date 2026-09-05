---
name: "airflow-dag-patterns"
display_name: "Airflow DAG 模式"
display_name_en: "Airflow DAG Patterns"
description: "Use when designing or reviewing Apache Airflow DAGs, task dependencies, sensors, retries, backfills, or pipeline tests."
description_zh: "用于设计或审查 Apache Airflow DAG、任务依赖、传感器、重试、回填和数据流水线测试。"
description_en: "Design observable, idempotent Airflow DAGs with safe scheduling, dependency sensors, retries, backfills, testing, and deployment boundaries."
category: "data"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized Airflow metadata and an isolated development environment; production scheduling, backfills, retries, connections, and data writes require separate authorization"
---

# Airflow DAG Patterns

设计可观察、可重试、可回放的数据编排。重点是 DAG 的时间语义、幂等任务、依赖等待、失败处理、测试和部署边界，而不是替用户直接触发生产任务。

## 使用边界

- 开始前确认 Airflow 版本、provider、时区、DAG 提交、数据范围、owner、SLA、连接引用和目标环境。
- 默认只读检查 DAG、配置、任务日志、依赖和测试；验证使用本地/CI/隔离环境及合成或脱敏数据。
- 不擅自触发生产 DAG、重试、清理、`backfill`、`clear`、`pause/unpause`、连接/变量修改或数据写入；这些操作需要明确授权。
- 日志、XCom、样本和报告不得保存 secret、token、完整客户行或可还原的个人标识。

## DAG 设计

每个 DAG 说明业务目的、输入分区、输出、粒度、调度时区、数据就绪条件、最大并发、超时、SLA、重跑和所有者。任务应满足：

- 幂等：同一逻辑日期重复执行不会重复写入或产生不同结果；用分区键/幂等键和事务边界约束写入。
- 原子：失败不会留下“成功”标记或半成品；临时结果在校验后再发布。
- 可增量：按逻辑日期和 watermark 处理，明确迟到数据、删除和更新语义。
- 可观察：结构化日志、耗时/行数/新鲜度指标、失败上下文和告警都能追溯到 DAG run 与 task instance。

使用 TaskFlow API 或清晰的 Operator 封装任务逻辑。DAG 文件保持轻量，避免导入时联网、查询数据库、读取不稳定的全局状态或执行重计算。

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task

@dag(
    dag_id="daily_orders",
    schedule="0 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(hours=2),
    tags=["etl"],
)
def daily_orders():
    @task(retries=3, retry_exponential_backoff=True,
          execution_timeout=timedelta(minutes=30))
    def extract(logical_date=None):
        # Use the logical date/partition, not wall-clock "now".
        return {"partition": logical_date.strftime("%Y-%m-%d")}

    @task
    def validate(input_ref):
        # Validate completeness and schema before publishing output.
        return input_ref

    validate(extract())

daily_orders()
```

## 依赖、传感器与分支

用 `upstream >> downstream` 表达依赖；fan-out/fan-in 的汇聚任务要显式设置合适的 `trigger_rule`。跨 DAG、文件、对象存储或 API 的等待应设置超时、合理的 `poke_interval`，长等待优先使用 `mode="reschedule"` 或 deferrable operator，避免占满 worker。

依赖检查应回答“数据是否完整且属于本次逻辑日期”，不能只回答“文件存在”。分支后的 join 要区分 skipped、failed 和 success；数据质量降级路径必须显式记录并阻止不合格数据悄悄发布。

## 重试、失败与回填

重试只适合暂时性错误；对权限、契约、代码和数据质量错误应快速失败并告警。为外部 API 使用退避、超时、限流和幂等请求；不要通过无限重试掩盖根因。清理任务可用 `ALL_DONE`，但不得把清理成功当成业务成功。

回填前先评估目标分区、下游影响、重复写入、资源成本和并发；在隔离环境演练，使用有界日期范围、dry-run 和校验摘要。生产 `backfill`、`clear`、`full rerun`、删除或覆盖数据必须单独授权，并保留回滚/恢复方案。

## 测试与质量门禁

CI 至少覆盖 DAG 加载无导入错误、无环、任务 ID/依赖、调度时区、默认重试/超时、分支 join、模板渲染和关键任务逻辑。对传感器测试超时与 reschedule 行为；对任务测试空输入、重复运行、迟到分区和部分失败。

```python
from airflow.models import DagBag

def test_dags_load_without_import_errors():
    bag = DagBag(dag_folder="dags", include_examples=False)
    assert not bag.import_errors

def test_daily_orders_is_bounded():
    bag = DagBag(dag_folder="dags", include_examples=False)
    dag = bag.get_dag("daily_orders")
    assert dag and dag.max_active_runs == 1
    assert all(task.execution_timeout for task in dag.tasks if task.task_id == "extract")
```

报告把事实、推导和未知项分开，记录 DAG/提交/target、输入输出分区、依赖证据、测试结果、失败分类、成本、敏感数据处理和未覆盖范围。静态加载通过不等于任务在生产成功运行。

## 交付检查清单

- [ ] 调度、时区、逻辑日期、catchup、并发、超时和 owner 已确认。
- [ ] 任务具备幂等、原子、增量和可观察性证据。
- [ ] 外部依赖有完整性检查、超时、reschedule/deferrable 策略和失败分类。
- [ ] 重试、分支、join、迟到数据、重跑和回填边界已测试。
- [ ] CI 覆盖加载、无环、模板、关键依赖和安全数据处理。
- [ ] 所有生产副作用均有明确授权、隔离演练和恢复方案。
