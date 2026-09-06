# Copy-ready use cases / 可复制使用场景

Each prompt is designed to make the expected stopping condition explicit and reduce accidental cost.

## How to use / 使用方法

1. 先确认 WorkBuddy 中已有可用连接器，再复制最接近目标的一段提示词。
2. 把示例中的主题、格式或限制替换成你的实际需求；保留“先检查、再执行”的顺序。
3. 涉及创建任务、付费或写入外部系统时，先让 WorkBuddy 只返回方案和预计成本，确认后再执行。

如果找不到合适的连接器，先让 WorkBuddy 返回“未配置/不可用”的原因和替代方案，不要把密钥直接粘贴到对话中。

## 先用现成包 / Start with a reviewed package

如果你还没有合适的 Skill，可以先从对应的精选包开始，再把下面的提示词替换成自己的主题：

| 任务 | 推荐起点 |
|---|---|
| 有来源的网页调研 | [deep-research Starter Pack](starter-packs.md) |
| 代码评审和风险排序 | [code-review-excellence Starter Pack](starter-packs.md) |
| 测试失败排查 | [debugging-strategies Starter Pack](starter-packs.md) |
| MCP、凭据和权限检查 | [mcp-security-audit Starter Pack](starter-packs.md) |

先下载并校验精选包，再复制下面最接近的提示词。想查看每个包的固定来源、资产文件名和校验命令，请打开[精选包清单](https://sandbaseai.github.io/workbuddy-skill/packages.html)。

If you do not have a suitable Skill yet, start with the matching [Starter Pack](starter-packs.md), then replace the topic in the prompt below. Download and verify the package before using it.

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

## Pre-publication content review / 发布前内容预审

适合短视频、封面、字幕、口播、商品链接和发布文案的发布前检查。可参考
[self-media-compliance-review](https://github.com/JuneYaooo/self-media-compliance-review)，
但它是外部项目，不代表平台或法律背书；先检查其许可证、规则文件和本地工具。

```text
使用自媒体发布前合规审核流程，检查我提供的视频、封面、标题、字幕、口播、商品链接和发布文案。
目标平台：抖音和小红书。
先只做本地、只读的证据整理：列出视频元数据、时间点、可见文字、音频/字幕是否已核验、商品价格/赠品/功效声明和缺失材料。
输出 Pass、Low、Medium、High 或 Blocker，并为每个风险附上原始证据和待确认事项。
不要发布、发送消息、调用实时平台接口、上传素材或修改文件；不要把“未检出”写成“合规通过”。
如果需要实时规则或案例，先说明将使用的工具、凭据、网络访问和预计费用，等待我明确确认。
```

完成预审后，人工复核原始视频和平台最新规则；这个流程不能替代法务、平台审核或版权/资质确认。
