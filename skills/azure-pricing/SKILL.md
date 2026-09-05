---
name: "azure-pricing"
display_name: "Azure 实时定价与估算"
display_name_en: "Azure Pricing and Estimation"
description: "Use when fetching current Azure retail prices, comparing regions or SKUs, or estimating authorized workload costs."
description_zh: "用于查询当前 Azure Retail Prices、比较区域/SKU、评估 Azure 工作负载和 Copilot Studio 用量成本。"
description_en: "Query current Azure retail pricing with bounded filters, explain currency and discount assumptions, and produce reproducible cost estimates without hard-coded stale rates."
category: "cloud"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with internet access to approved Azure pricing and Microsoft Learn sources, isolated estimation reports, and no need for Azure credentials; purchases, billing changes, deployments, and production changes require separate authorization"
---

# Azure 实时定价与估算

查询 Azure Retail Prices API 和 Microsoft Learn 的当前计费资料，比较服务、SKU、区域、消费/预留/节省计划，生成可复现的月度/年度估算。价格会变化，任何估算都必须标注来源时间、币种、单位、税费、折扣、承诺期限和不确定性。

## 激活与边界

在用户要求 Azure 价格、SKU/区域比较、预算估算、预留实例/节省计划、Azure AI 或 Copilot Studio 用量估算时激活。默认只读，不修改订阅、账单、资源或部署。

- 先收集服务名、service family、region、SKU、计量单位、用量、时间窗、币种、环境、折扣/协议、税费和是否需要预留/Spot；缺少关键条件时标为 `unknown`，不擅自假设。
- 只访问批准的公开价格/官方文档来源；固定 URL、API version、查询参数、获取时间、响应 hash 和分页状态。第三方报价、搜索摘要和缓存价格只能作为未验证参考。
- URL 过滤器必须编码并限制结果量；不把用户输入直接拼成任意网络请求，服务名/区域/SKU 使用 allowlist 或先发现后确认。
- 估算输入、资源名、订阅/租户信息和报告脱敏；不需要 Azure 身份验证就不要索取凭据，也不输出 token、连接串或完整内部配置。

## Retail Prices API 流程

使用官方 endpoint：`https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview`。按 `serviceName`、`serviceFamily`、`armRegionName`、`armSkuName`、`priceType` 和 `meterName` 逐步收窄 `$filter`；区域使用 API 所需的小写无空格标识。读取 `Items`，按 `isPrimaryMeterRegion` 过滤（除非用户明确需要其它 meter），跟随 `NextPageLink`，记录 Count 和空结果。

结果表至少包含 service、product、SKU、region、meter、unitOfMeasure、priceType、retailPrice、unitPrice、currencyCode、有效时间和 savingsPlan 条件。不得把 USD 当作用户本地币种，不得把每小时、每请求、每 GiB 等单位直接当月度价格。

## 成本估算

明确公式和用量假设，例如：

```text
period_cost = unit_price × measured_units × active_periods
monthly_estimate = sum(period_cost) + fixed_charges + data_transfer + support
```

将按需、预留、节省计划和 Spot 分开；包含承诺期限、利用率、提前退出/容量风险、区域差异、免费层、最小计费粒度、税费、汇率和折扣未知项。输出低/基准/高三档或节省区间，并展示输入、公式、结果和来源，而不是只给一个数字。

对于 Copilot Studio 或 AI 用量：先从当前 Microsoft Learn 计费/许可页面获取最新费率和资格条件，再根据用户给出的用户数、会话、答案/工具/flow 比例计算 credits 与货币成本；不要依赖仓库里的旧费率快照，不要把不同租户/许可证的免费项混用。

## 校验与交付

检查 serviceName 大小写、区域映射、SKU 版本、货币/单位、API 分页、primary meter、有效日期、价格异常、免费层和重复 meter。若没有结果，按顺序放宽 region/priceType/SKU 并记录变化；不能把空结果解释为服务不存在。

交付脱敏 Markdown/表格，包含查询请求摘要、来源/时间/hash、筛选条件、输入假设、价格明细、公式、月/年区间、折扣与税费说明、风险和未知项。结果过期、页面不可访问、API schema 改变或汇率缺失时标记 `unknown` 并停止承诺。

## 变更闸门

价格分析本身不授权购买 Reserved Instances/Savings Plans、修改预算/账单、创建资源、变更 SKU/区域、部署、修改 IaC 或创建 GitHub Issue/EPIC。上述动作需绑定订阅/账户、资源范围、承诺期限、成本上限、审批人、canary/退出方案和回滚条件的独立授权。

## 质量门禁

- [ ] 服务、SKU、区域、单位、用量、时间窗、币种、税费和折扣假设已明确。
- [ ] API version、过滤器、分页、primary meter、来源时间和响应状态可追溯。
- [ ] 估算有公式、单位换算、固定/变量费用、低/基准/高区间和不确定性。
- [ ] Copilot/AI 计费事实来自当前官方页面，没有使用未经验证的旧费率。
- [ ] 报告已脱敏，不含 Azure 凭据、订阅内部信息或不可复用的秘密。
- [ ] 购买、账单、资源、IaC、部署和 GitHub 写入均通过独立授权。

## Related Skills

- `aws-cost-optimize` - 分析 AWS 资源、利用率和账单成本
- `azure-well-architected-review` - 评审 Azure 成本优化与架构支柱
- `azure-resource-health-diagnose` - 诊断 Azure 资源健康与指标
