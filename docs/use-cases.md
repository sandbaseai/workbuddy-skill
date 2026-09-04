# Copy-ready use cases / 可复制使用场景

Each prompt is designed to make the expected stopping condition explicit and reduce accidental cost.

## Research / 调研

```text
用 SandBase 找到适合实时网页搜索的 API，比较最多 3 个候选的输入、输出和价格。选择最合适的一个，搜索“AI Agent 交付平台”的最新资料，并给出来源链接。
```

## Structured extraction / 结构化提取

```text
先用 SandBase 搜索网页结构化提取能力并检查 schema。确认价格后，从我提供的公开网页提取公司名、产品、定价和更新时间，输出 JSON 表格；缺失字段保留 null，不要猜测。
```

## Model comparison / 模型比较

```text
在 SandBase 中寻找适合中文长文总结的模型。只比较候选的上下文能力、输入要求和当前价格，不要执行。最后推荐一个低成本方案和一个质量优先方案。
```

## Image or video / 图像或视频

```text
用 SandBase 找一个支持 16:9 的文生视频能力。检查参数和价格后告诉我预计成本；我同意执行后只创建一次任务，并用同一个 run_id 等待最终结果。
```

## Embeddings / 向量化

```text
用 SandBase 找支持中文的 embedding 模型，比较维度、输入限制和价格。选择满足需求的最低成本方案，把这些公开文档片段转成向量并返回可复现的模型名称与参数。
```

## Safe account diagnosis / 安全诊断

```text
检查为什么 SandBase 调用失败。区分工具未配置、鉴权、余额、限流和参数错误；不要让我在聊天里粘贴 API key，也不要原样重试无效参数。
```

