---
name: "shipping-and-launch"
display_name: "上线与发布准备"
display_name_en: "Shipping and Launch"
description: "Use when preparing a production launch, significant user release, data/infrastructure migration, beta rollout, monitoring plan, or rollback strategy."
description_zh: "用于准备生产上线、重要用户版本、数据/基础设施迁移、Beta 发布、监控方案或回滚策略。"
description_en: "Prepare an observable, incremental, reversible launch with code, security, performance, accessibility, infrastructure, documentation, rollout thresholds, and rollback evidence."
category: "operations"
version: "0.1.0"
author: "addyosmani/agent-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository, CI, staging/production evidence, monitoring, feature-flag, and rollback capabilities; deployment, traffic changes, notifications, and data mutations require separate authorization"
---

# 上线与发布准备

上线不只是执行部署命令，而是让变更可观察、可分阶段、可逆，并且知道什么结果才算成功。每次上线前都要把代码质量、安全、性能、可访问性、基础设施、文档、监控、放量门槛和回滚证据串起来；缺少关键证据时停在准备/报告阶段，不用乐观假设补齐。

## 边界与证据

- 先锁定目标环境、版本/commit、变更范围、受影响用户/租户、负责人、时间窗、批准人和回滚 owner。
- 默认使用 staging、合成数据、只读检查和 dry-run；生产部署、数据写入、流量切换、feature flag、通知和删除均需独立授权。
- 以仓库实际测试、构建、配置、监控、历史基线和发布策略为证据；无法运行的检查标为 `Missing evidence`，不能写成通过。
- 日志、截图、指标、错误和通知脱敏，不输出凭据、客户数据、完整用户标识、私有 URL 或内部提示词。
- 公开 README/变更记录只写用户需要知道的兼容、配置和操作，项目内部建设约束放在受控位置。

## 上线前清单

### 代码与质量

- 单元、集成、端到端和回归测试按风险覆盖并通过；
- 构建无未解释 warning，类型/lint/契约检查通过；
- 代码评审、依赖锁定、变更说明和迁移顺序可追溯；
- 预期失败路径有处理，未完成 TODO、调试输出和临时旁路已清理或有到期 owner；
- 与上个已发布版本的 diff、schema、API、配置、权限和资产已核对。

### 安全

- 代码、lockfile、日志、artifact 和配置没有秘密；
- 依赖审计没有未处置的 high/critical，且已判断可达性；
- 用户输入、认证、对象级授权、租户边界、CORS、CSRF、Header、限流和错误暴露符合威胁模型；
- 新数据类别、外部集成、上传、回调、权限或合规影响已有 owner 和批准记录；
- 供应链、构建 action、镜像、签名/SBOM（若适用）和产物来源已核验。

### 性能与可访问性

- 关键路径有基线和目标：错误率、P95/P99、吞吐、资源、查询、bundle 和 Core Web Vitals；
- 没有未解释的 N+1、锁、容量、缓存或资源泄漏风险；
- 交互元素可键盘操作，焦点/动态状态/错误消息可感知，颜色对比和屏幕阅读器路径符合项目目标；
- 性能/axe/Lighthouse 等检查只在适用的真实 preview/runtime 环境执行，不能用静态猜测代替运行时证据。

### 基础设施与文档

- 生产环境变量、身份、网络、DNS/SSL、CDN、健康检查、日志和错误报告已通过配置/运行证据确认；
- 数据库迁移、兼容窗口、备份/恢复、队列/缓存和容量计划明确；
- README、API 文档、ADR、changelog、操作手册和用户通知反映真实变更；
- 明确上线后观察人、渠道、时间窗和升级方式。

## Feature flag 策略

用 flag 将“部署代码”和“启用功能”分离，适用时遵循：

```text
DEPLOY OFF → TEAM/BETA → CANARY 5% → 25% → 50% → 100% → CLEAN UP
```

每个 flag 都有 owner、默认值、目标人群、过期/清理日期、审计记录和双状态测试。避免嵌套 flag 的组合爆炸；全量稳定后尽快删除 flag 和旧路径，不把临时开关变成永久架构。

## 分阶段放量与决策阈值

建议顺序：staging 全量验证 → 生产部署但关闭 flag → 内部/受控用户 → 金丝雀 → 逐级扩大 → 全量观察 → 清理 flag。每一阶段都记录版本、样本、时间窗口、基线、当前值、决定人和下一步。

| 指标 | 继续放量 | 暂停调查 | 回滚 |
|---|---|---|---|
| 错误率 | 在基线约 ±10% 内 | 高于基线 10%–100% | 超过基线 2 倍 |
| P95 延迟 | 在基线约 ±20% 内 | 高于 20%–50% | 高于 50% |
| 客户端新错误 | 无新类型 | session 影响低于 0.1% | session 影响高于 0.1% |
| 业务指标 | 持平或改善 | 下降低于 5%，需确认噪声 | 下降超过 5% |

这些是起点，不是跨项目真理；使用仓库自己的基线和批准阈值。数据完整性问题、安全漏洞、用户问题激增或无法解释的新错误应立即暂停/回滚，不等待完整放量。

## 监控与上线后核验

上线后至少观察应用错误率/延迟/流量/业务指标，基础设施 CPU、内存、连接池、磁盘、网络/队列，以及 Web 应用的 LCP/INP/CLS、JS 和客户端 API 错误。第一小时完成：

1. 健康检查和关键用户流程；
2. 错误监控是否出现新类型；
3. 延迟、容量、数据一致性和业务基线比较；
4. 日志是否流入且没有秘密/敏感字段；
5. rollback/flag kill switch 的 dry-run 或实际可用性证据；
6. 记录观察结果、owner、升级和下次检查时间。

## 回滚计划

上线前写清：

```markdown
## Rollback Plan: <feature/release>

Trigger: <threshold, integrity/security signal, or owner decision>
First action: <disable flag | stop rollout | deploy prior artifact>
Steps: <exact authorized operations>
Database: <compatible down path, data handling, or forward-fix decision>
Verify: <health, errors, latency, critical flow, data checks>
Notify: <approved channel and owner>
Target time: <flag / app / database recovery estimate>
```

优先关闭 flag 或停止放量；若需恢复版本，引用不可变 artifact/commit，不强推历史。数据库回滚要单独评估已写入数据，代码回滚不代表数据自动可逆。回滚完成后复核健康、错误、延迟、关键流程、数据和日志，并记录残余风险。

## 完成交付前检查

- [ ] 目标环境、版本、范围、用户、负责人、时间窗和批准边界已锁定。
- [ ] 质量、安全、依赖、性能、可访问性、基础设施和文档证据已核对。
- [ ] 变更、迁移、配置、权限、兼容窗口和产物来源可追溯。
- [ ] 适用时 feature flag 有 owner、过期、双状态测试和清理计划。
- [ ] 分阶段比例、基线、阈值、暂停/回滚条件和观察人已明确。
- [ ] 监控、健康检查、关键用户流程、日志脱敏和错误升级可验证。
- [ ] 回滚步骤、数据库影响、验证、通知和目标恢复时间已实际演练或标明缺失证据。
- [ ] 生产部署、流量/flag、数据写入、通知和政策例外均有独立授权。
- [ ] 未将 staging 通过、静态检查或部署 API 成功误写成生产成功。

## Related Skills

- `devops-rollout-plan` - 设计 preflight、go/no-go、沟通和回滚计划
- `github-release` - 核对版本、tag、资产和发布来源
- `verify-agent-action` - 在高影响上线动作前核验精确目标与审批绑定
- `constraint-driven-development` - 固化上线质量门槛和不下降基线
