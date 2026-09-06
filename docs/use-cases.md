# Copy-ready use cases / 可复制使用场景

Each prompt is designed to make the expected stopping condition explicit and reduce accidental cost.

## How to use / 使用方法

1. 先确认 WorkBuddy 中已有可用连接器，再复制最接近目标的一段提示词。
2. 把示例中的主题、格式或限制替换成你的实际需求；保留“先检查、再执行”的顺序。
3. 涉及创建任务、付费或写入外部系统时，先让 WorkBuddy 只返回方案和预计成本，确认后再执行。

如果找不到合适的连接器，先让 WorkBuddy 返回“未配置/不可用”的原因和替代方案，不要把密钥直接粘贴到对话中。

## Research / 调研

```text
在 WorkBuddy 中使用已配置的搜索连接器，找到适合实时网页搜索的 API，比较最多 3 个候选的输入、输出和价格。选择最合适的一个，搜索“AI Agent 交付平台”的最新资料，并给出来源链接。
```

## Structured extraction / 结构化提取

```text
先用 WorkBuddy 中已配置的搜索连接器寻找网页结构化提取能力并检查 schema。确认价格后，从我提供的公开网页提取公司名、产品、定价和更新时间，输出 JSON 表格；缺失字段保留 null，不要猜测。
```

## Model comparison / 模型比较

```text
在 WorkBuddy 中寻找适合中文长文总结的模型。只比较候选的上下文能力、输入要求和当前价格，不要执行。最后推荐一个低成本方案和一个质量优先方案。
```

## Image or video / 图像或视频

```text
在 WorkBuddy 中找一个支持 16:9 的文生视频能力。检查参数和价格后告诉我预计成本；我同意执行后只创建一次任务，并用同一个 run_id 等待最终结果。
```

## Embeddings / 向量化

```text
在 WorkBuddy 中找支持中文的 embedding 模型，比较维度、输入限制和价格。选择满足需求的最低成本方案，把这些公开文档片段转成向量并返回可复现的模型名称与参数。
```

## Safe account diagnosis / 安全诊断

```text
检查为什么连接器调用失败。区分工具未配置、鉴权、余额、限流和参数错误；不要让我在聊天里粘贴 API key，也不要原样重试无效参数。
```
