# WorkBuddy Skill Hub

![WorkBuddy Skill Atlas](site/social-preview.png)

一个面向 WorkBuddy 的开放 Skill 目录与精选工作流集合。你可以发现公开
Skills，查看来源与许可证，选择适合的能力，并下载经过整理的 WorkBuddy
版本。

[![Latest release](https://img.shields.io/github/v/release/sandbaseai/workbuddy-skill)](https://github.com/sandbaseai/workbuddy-skill/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/sandbaseai/workbuddy-skill?style=flat)](https://github.com/sandbaseai/workbuddy-skill/stargazers)

[中文](#中文) · [English](#english) · [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/)

## 中文

### 三步开始

1. 在 [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) 或[中文目录](https://sandbaseai.github.io/workbuddy-skill/zh-CN.html)中搜索需求。
2. 打开条目的来源链接，阅读说明、许可证、权限和外部依赖。
3. 从 [Releases](https://github.com/sandbaseai/workbuddy-skill/releases/latest) 下载所需 ZIP，在 WorkBuddy 的 **专家 · Skills · Connectors → Skills → 添加 Skill** 中上传。

精选成品也可以按精确路径安装：

```bash
gh skill install sandbaseai/workbuddy-skill skills/oss-review --dir .workbuddy/skills
```

### 可以解决什么问题

- 找到适合研究、开发、测试、设计、数据、文档和运营的 Agent 能力
- 在执行前了解来源、许可证、权限、输入输出和潜在风险
- 用经过 WorkBuddy 适配的工作流完成代码评审、故障排查、发布、研究和内容处理
- 对不支持的工具、缺失权限或不确定结果明确说明，不把猜测当成执行结果

### 示例

```text
找一个适合中文发票 OCR 的 API，只比较候选、参数和价格，不要执行付费调用。
```

```text
审查这次代码变更的回归风险，并给出每个结论对应的证据。
```

```text
设计一次只在测试环境执行的韧性实验，先写假设、基线、影响范围和回滚方案。
```

### 精选 WorkBuddy Skills

| Skill | 适合场景 |
|---|---|
| [SandBase](skills/sandbase/) | 发现、比较并调用实时 API 和模型 |
| [Code Reviewer](skills/code-reviewer/) | 评审正确性、回归、维护性、安全和发布风险 |
| [Bug Reproduction Brief](skills/bug-reproduction-brief/) | 将模糊或间歇性缺陷收敛为最小、可重复、有证据的复现简报 |
| [Systematic Debugging](skills/systematic-debugging/) | 以红色反馈回路、数据流追踪和可证伪假设定位根因并验证回归 |
| [Test-Driven Development](skills/test-driven-development/) | 以 RED、GREEN、REFACTOR 建立行为测试、最小实现和回归保护 |
| [Screen Reader Testing](skills/screen-reader-testing/) | 验证屏幕阅读器、键盘、ARIA、表单和动态内容的可感知行为 |
| [Documentation](skills/documentation/) | 编写有证据、可执行、易维护的项目文档 |
| [Network Troubleshooting](skills/network-troubleshooting/) | 分层定位 DNS、路由、TLS、HTTP 和资源问题 |
| [Chaos Engineer](skills/chaos-engineer/) | 设计有授权、可回滚、影响范围受控的韧性实验 |
| [Cloud Cost Optimization](skills/cloud-cost-optimization/) | 按实际成本驱动因素排序，验证取舍，建模节省并治理授权变更 |
| [Cloud Architect](skills/cloud-architect/) | 设计跨云架构、迁移波次、灾备、成本与安全取舍 |
| [Database Query Optimizer](skills/database-query-optimizer/) | 从执行计划和性能基线定位慢 SQL，并验证单变量优化 |
| [Data Quality Frameworks](skills/data-quality-frameworks/) | 以数据契约、质量维度、基线和有界证据治理数据管道质量 |
| [dbt Transformation Patterns](skills/dbt-transformation-patterns/) | 以分层模型、契约、测试、lineage 和增量边界构建可追溯转换 |
| [Airflow DAG Patterns](skills/airflow-dag-patterns/) | 设计具备幂等、可观察、可测试和安全回填边界的数据编排 DAG |
| [RAG Implementation](skills/rag-implementation/) | 构建具备权限过滤、混合召回、重排、引用校验和拒答能力的知识增强生成 |
| [Spark Optimization](skills/spark-optimization/) | 依据运行基线优化分区、shuffle、AQE、倾斜、缓存、内存和分布式作业成本 |
| [Distributed Tracing](skills/distributed-tracing/) | 用隐私安全的 OpenTelemetry 追踪上下文、依赖、延迟、故障和日志关联 |
| [LLM Evaluation](skills/llm-evaluation/) | 用可复现数据集、分层指标、人工校准和回归门禁验证模型与 RAG 质量 |
| [Hybrid Search Implementation](skills/hybrid-search-implementation/) | 组合向量与关键词召回，以融合、重排、权限过滤和评测提升检索质量 |
| [Vector Index Tuning](skills/vector-index-tuning/) | 依据召回、延迟、内存、构建和删除证据调优向量索引与生命周期 |
| [Python Observability](skills/python-observability/) | 以隐私安全的日志、黄金信号、关联 ID、指标和追踪诊断 Python 服务 |
| [Python Resilience Patterns](skills/python-resilience/) | 以超时、退避、熔断、背压、幂等重试和安全降级应对依赖故障 |
| [Python Background Jobs](skills/python-background-jobs/) | 以持久状态、幂等投递、DLQ、背压、取消和优雅停机运行后台任务 |
| [Async Python Patterns](skills/async-python-patterns/) | 用有界并发、非阻塞 I/O、取消传播、deadline、背压和资源清理构建异步服务 |
| [Python Packaging](skills/python-packaging/) | 用现代元数据、锁定依赖、可复现构建、provenance 和发布门禁分发 Python 包 |
| [PostgreSQL Table Design](skills/postgresql-table-design/) | 依据 workload 设计类型、约束、索引、分区、RLS 和可回滚在线迁移 |
| [Database Migration](skills/database-migration/) | 用 expand-contract、幂等回填、兼容窗口、锁/复制证据和回滚设计数据库演进 |
| [SLO Implementation](skills/slo-implementation/) | 用用户旅程 SLI、错误预算、多窗口 burn 告警和治理策略管理可靠性 |
| [Prometheus Configuration](skills/prometheus-configuration/) | 用指标契约、受控抓取、规则、告警、HA、保留和高基数治理构建监控 |
| [Grafana Dashboards](skills/grafana-dashboards/) | 用 RED/USE、SLO、变量、阈值、告警和 Dashboard as Code 构建可行动的观测视图 |
| [Agent OWASP ASI Compliance](skills/agent-owasp-compliance/) | 按 Agentic Security Initiative 十项风险，以证据评估工具、身份、策略、供应链和运行时行为 |
| [MCP Implementation Security Review](skills/mcp-implementation-security-review/) | 评审 MCP 传输、认证、会话、限流、Schema、RCE、供应链和 OWASP MCP 风险 |
| [Multi-Stage Dockerfile](skills/multi-stage-dockerfile/) | 用可复现基础镜像、缓存、最小运行时、非 root、扫描、签名和回滚构建容器 |
| [OpenAPI to Application Code](skills/openapi-to-application-code/) | 将版本化 OpenAPI 契约转换为带校验、鉴权、测试、溯源和发布门禁的应用代码 |
| [TypeSpec API Operations](skills/typespec-api-operations/) | 在 TypeSpec 中构建带路由、Schema、鉴权、幂等、卡片确认和契约测试的 API 操作 |
| [Web Application Testing](skills/webapp-testing/) | 用 Playwright 验证浏览器流程、响应式行为、控制台/网络证据和安全的失败工件 |
| [Diátaxis Documentation Writer](skills/documentation-writer/) | 按教程、How-to、参考和解释四类，以证据、版本和维护门禁编写技术文档 |
| [MCP Security Audit](skills/mcp-security-audit/) | 审计 MCP 配置中的凭据、命令注入、依赖版本、Server 清单、网络和权限边界 |
| [Performance Review Writer](skills/performance-review-writer/) | 基于授权证据和 STAR 结构起草自评、同事评价、360 或向上反馈 |
| [Project Architecture Blueprint](skills/architecture-blueprint-generator/) | 从代码、配置、依赖、测试和部署证据生成真实可追溯的架构蓝图 |
| [Web Design Reviewer](skills/web-design-reviewer/) | 跨视口评审布局、响应式、可访问性和视觉一致性，并以证据安全回归验证 |
| [Agentic Workflows Router](skills/agentic-workflows/) | 路由 GitHub Agentic Workflow 的设计、创建、调试、升级、报告和安全输出流程 |
| [Azure Well-Architected Review](skills/azure-well-architected-review/) | 按 Azure 五大支柱对 IaC 和线上资源做只读评审、漂移分析和风险分级 |
| [STRIDE-A Threat Model Analyst](skills/threat-model-analyst/) | 对代码库建立信任边界、数据流和 STRIDE-A 威胁模型，并支持增量安全态势对比 |
| [Secret Scanning](skills/secret-scanning/) | 配置 Secret Scanning、Push Protection、自定义模式和安全的凭据泄露处置流程 |
| [CodeQL Code Scanning](skills/codeql/) | 配置最小权限的 CodeQL Actions/CLI 扫描、语言矩阵、SARIF 和 monorepo 分析 |
| [Repository Standardizer](skills/repo-standardizer/) | 清理公开 README 与文档，分离内部建设约束，并审计模板、CI、CODEOWNERS 和治理配置 |
| [Azure Resource Health Diagnosis](skills/azure-resource-health-diagnose/) | 基于只读健康状态、日志、遥测和依赖证据诊断 Azure 资源并生成分阶段修复计划 |
| [AWS Cost Optimization](skills/aws-cost-optimize/) | 基于 AWS IaC、使用指标、账单和价格证据生成可验证的成本优化建议 |
| [Azure Pricing and Estimation](skills/azure-pricing/) | 查询 Azure 实时零售价格、比较 SKU/区域并生成带假设和区间的成本估算 |
| [API Design Principles](skills/api-design-principles/) | 设计具备 HTTP/schema、幂等、分页、授权、版本和成本边界的 API 契约 |
| [Microservices Architect](skills/microservices-architect/) | 设计服务边界、通信、数据所有权、故障隔离和迁移验证 |
| [Cloud Design Patterns](skills/cloud-design-patterns/) | 按约束选择韧性、性能、消息、安全、部署和迁移模式 |
| [Technical Spike](skills/technical-spike/) | 用时间盒和最小实验解决实现前的关键技术未知数 |
| [Writing Implementation Plans](skills/writing-plans/) | 将规格拆成按文件、接口、测试、约束和回滚定义的可执行计划 |
| [Cloud Resource Health](skills/cloud-resource-health/) | 从资源状态、指标、日志、依赖和变更记录诊断云资源健康问题 |
| [Code Tour](skills/code-tour/) | 为上手、评审、排障和架构理解生成经过真实锚点校验的代码导览 |
| [Subagent-Driven Development](skills/subagent-driven-development/) | 以隔离实施、任务级评审和整分支复核执行多步开发计划 |
| [Acquire Codebase Knowledge](skills/acquire-codebase-knowledge/) | 从源码、配置和历史证据生成技术栈、架构、集成、测试与风险地图 |
| [Agentic Evaluation](skills/agentic-evaluation/) | 用明确量规、证据和有界迭代评测并改进 Agent 输出 |
| [GitHub Actions Hardening](skills/github-actions-hardening/) | 审查工作流触发器、注入、权限、供应链、Secrets 和 Runner 风险 |
| [GitHub Actions Efficiency](skills/github-actions-efficiency/) | 用运行数据优化 CI 时间、成本、缓存、并发、路径和矩阵，同时保留必要门禁 |
| [AWS Resource Query](skills/aws-resource-query/) | 将自然语言转换为带账号、区域、分页和脱敏边界的 AWS 只读查询 |
| [AWS CloudWatch Investigation](skills/aws-cloudwatch-investigation/) | 用日志、指标、告警、CloudTrail 和 Health 证据关联变更并重建事件时间线 |
| [Azure Deployment Preflight](skills/azure-deployment-preflight/) | 在 Azure 部署前校验 Bicep、参数、权限和 what-if 变更风险 |
| [AWS Well-Architected Review](skills/aws-well-architected-review/) | 按 AWS 六大支柱结合 IaC 与线上证据审查架构和风险 |
| [Incident Post-Mortem](skills/incident-postmortem/) | 以证据重建时间线、量化影响、无责分析根因并跟进行动项 |
| [Dependabot Management](skills/dependabot/) | 治理多生态依赖更新、安全更新、分组策略、调度和告警分流 |
| [Agent Governance](skills/agent-governance/) | 以策略、审批、限额、信任和审计约束 Agent 工具与委派行为 |
| [Agent Supply Chain Integrity](skills/agent-supply-chain/) | 核验 Agent 插件和工具包完整性、依赖锁定、来源证明与晋级门禁 |
| [Secrets Management](skills/secrets-management/) | 以最小权限、短期身份、轮换、扫描和审计保护 CI/CD 凭据 |
| [Error Handling Patterns](skills/error-handling-patterns/) | 以分类、上下文、清理、重试、熔断和降级构建可靠错误边界 |
| [Workflow Orchestration Patterns](skills/workflow-orchestration-patterns/) | 以确定性编排、幂等 Activity、Saga 补偿和恢复验证治理长流程 |
| [Architectural Decision Record](skills/architectural-decision-record/) | 记录架构决策、证据、替代方案、取舍、状态和复查路径 |
| [GitHub Release](skills/github-release/) | 用变更证据、SemVer、校验和资产核对编排可追溯发布 |
| [Incident Response and Triage](skills/incident-triage/) | 处理事件、稳定服务、验证恢复并沉淀经验 |
| [Security Audit](skills/security-audit/) | 审查信任边界、控制措施、漏洞和残余风险 |
| [RAG Evaluation](skills/rag-evaluation/) | 评估检索、引用、事实依据、拒答、成本和回归 |
| [Playwright Web App QA](skills/playwright-webapp-qa/) | 验证浏览器流程、可见状态和网络/控制台问题 |
| [Chrome DevTools Diagnostics](skills/chrome-devtools/) | 用快照、控制台、网络请求和性能 trace 诊断授权浏览器页面 |
| [Deep Evidence Research](skills/deep-research/) | 产出带来源、争议和限制说明的研究结果 |

浏览 [完整精选目录](skills/) 或直接打开 [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/)。每个精选条目都提供来源说明；外部来源的许可证和适配信息见对应的 `SOURCE.json`。

### 目录与来源

目录收录公开 GitHub `SKILL.md` 条目，并提供来源路径、内容指纹、许可证/来源信息和兼容性提示。目录条目不是安装批准：安装前请自行阅读原始内容，尤其注意脚本、网络访问、凭据和副作用。

<!-- CATALOG-METRICS:START -->
| Metric | Current snapshot |
|---|---:|
| Indexed GitHub paths | 12,716 |
| Unique content SHAs | 8,089 |
| Source repositories | 6,432 |
<!-- CATALOG-METRICS:END -->

静态检查只能帮助筛选，不能替代人工安全审查。目录的字段说明和来源约定见[目录文档](catalog/README.md)；适配指南见[中文文档](docs/adapting-skills.zh-CN.md)和[English guide](docs/adapting-skills.md)。

<!-- CATALOG-ANALYSIS:START -->
The catalog is reviewed for structural compatibility and conservative security signals; inspect each source before installation.
<!-- CATALOG-ANALYSIS:END -->

需要更多 WorkBuddy 文档、MCP、工作流、评测与 Skills，可浏览 [Awesome WorkBuddy](https://github.com/sandbaseai/awesome-workbuddy)。

## English

WorkBuddy Skill Hub is an open catalog of public Agent Skills plus a curated set of reviewed, bilingual WorkBuddy workflows.

1. Search the [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/).
2. Read the immutable source, license, permissions, dependencies, and side effects.
3. Download a ZIP from [Releases](https://github.com/sandbaseai/workbuddy-skill/releases/latest) and add it in WorkBuddy under **Experts · Skills · Connectors → Skills → Add Skill**.

The catalog is for discovery, not automatic approval. Review every external Skill before use, and pin a release or commit when reproducibility matters. See the [English adaptation guide](docs/adapting-skills.md) for preparing a reviewed workflow.

## Compatibility

| Environment | Support |
|---|---|
| WorkBuddy | Primary package format |
| Other Agent Skills-compatible hosts | Instructions are generally portable; metadata or tools may need adaptation |
| Chat-only assistants | Guidance only; they cannot execute WorkBuddy connectors |

## Contributing

Issues and pull requests are welcome. To nominate a public Skill, include its exact source, license, permissions, and the user problem it solves. Please never commit API keys, access tokens, private prompts, or customer data.

For help, see [SUPPORT.md](SUPPORT.md); for vulnerability reports, see [SECURITY.md](SECURITY.md). Release history is in the [changelog](CHANGELOG.md).

## License

[MIT](LICENSE)
