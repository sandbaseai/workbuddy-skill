---
name: sandbase
display_name: SandBase 能力调用
display_name_en: SandBase Capability Runner
description: 通过 SandBase 发现、检查并调用模型与 API；当用户需要搜索、抓取、数据、SaaS、多模态、嵌入或第三方模型能力时使用。
description_zh: 按需求发现 SandBase 能力，确认参数与价格后执行，并可靠获取异步结果。
description_en: Discover, inspect, and run SandBase models and APIs, including reliable polling for asynchronous results.
category: productivity
version: 0.1.0
author: SandBase
license: MIT
---

# SandBase

使用工作区中已配置的 SandBase MCP 工具，把用户的业务需求转成可交付结果。

## 何时使用

当任务需要 WorkBuddy 当前工具之外的模型、搜索、网页/文件提取、数据源、SaaS、图像、音频、视频或 embedding 能力时使用。普通问答、纯本地编辑，或现有专用工具已经能直接完成时不要触发。

## 工作流

1. 将请求归纳为能力、输入、输出格式、时效性和成本约束。不要要求用户提供 SandBase 内部工具名。
2. 调用 `sandbase_discover` 搜索能力。优先使用一个精确关键词；结果过多时再按 `type` 或 `vendor` 收窄，结果为空时换用更短的同义词重试。
3. 对候选调用 `sandbase_inspect`。执行前必须读取输入 schema、价格和同步/异步行为；绝不猜测参数。
4. 选择满足任务的最小能力。若多个候选效果接近，优先更低成本、更少数据暴露、输出更直接的选项。费用明显或用户要求比较时，先呈现候选与费用。
5. 调用 `sandbase_run`，仅传 schema 要求和任务必需的参数。不要把密钥、令牌或无关私人数据放入请求。
6. 同步调用直接整理结果；若返回 `run_id`，按 @references/execution.md 查询到 `completed` 或 `failed`。
7. 返回实际产物、关键限制与来源。工具失败时说明错误和已尝试的安全重试，不得编造结果。

## 约束

- 顺序始终是 discover → inspect → run；已知名称也必须 inspect 后再运行。
- 用户只是比较能力或询价时，不要执行付费调用。
- 会发布、发送、购买、交易或更改外部数据的能力，必须沿用宿主环境的授权边界；发现工具不等于获得操作许可。
- 同一失败参数不要无限重试。修正一次明显的格式问题后仍失败，返回可行动的错误信息。
- SandBase 工具不可用时，按 @references/troubleshooting.md 处理。

## 参考

- 异步轮询、结果整理和成本处理：@references/execution.md
- 无结果、鉴权、限流及服务异常：@references/troubleshooting.md
