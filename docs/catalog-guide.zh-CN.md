# 如何阅读目录条目

Skill Atlas 是发现入口，不是自动批准名单。导入公开 Skill 前，按下面的清单检查。

## 1. 先打开精确来源

打开结果中的 `source` 链接，确认仓库、路径、许可证和提交版本。目录 ID 的格式是：

```text
github:owner/repository:path/to/SKILL.md
```

固定到提交版本的来源链接才是可复现的依据。不要只根据仓库名或显示名称判断，因为名称可能重复，内容也会变化。

## 2. 正确理解审阅字段

- **WorkBuddy 状态**描述的是适配准备度，不代表可信度。`workbuddy-ready` 表示发现了预期元数据；`adaptable` 表示还需要少量改造；`needs-review` 和 `unreviewed` 需要进一步检查。
- **评分**是 0–100 的兼容性提示，不是质量、安全性或性能评分。
- **安全状态**只报告保守的静态信号。`no-static-flags` 仅表示扫描器没有匹配到已知模式，不代表安全；仍要阅读脚本、网络调用、凭据和权限。
- **Copies**表示有多少个目录路径共享同一个 blob SHA，是来源线索，不是热度或可信度评分。想让相同内容只显示一次时使用 `--unique`。
- **Source context**用于区分可能的主来源、镜像、Fork 或休眠路径。在其他条件相近时可以优先看 `primary-looking`，但仍要自己核对仓库。

## 3. 带着审阅目标搜索

本地工具要求所有关键词都匹配，也可以同时使用审阅筛选：

```bash
python3 scripts/query_catalog.py invoice OCR --limit 10
python3 scripts/query_catalog.py research --security no-static-flags \
  --source-context primary-looking --min-score 80 --unique --sort score
```

人类可读输出会直接给出完整的 `catalog id`。把这个值复制给
`review_skill.py` 或 `adapt_skill.py` 即可，不要根据显示名称手工拼接 ID。

```bash
python3 scripts/review_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

也可以把同一个 ID 粘贴回本地搜索工具或 Atlas 搜索框，重新定位精确条目：

```bash
python3 scripts/query_catalog.py 'github:owner/repository:path/to/SKILL.md'
```

搜索只负责缩小候选范围，不会自动安装。选定条目后，先检查来源，再按照[适配教程](adapting-skills.zh-CN.md)制作经过审阅的 WorkBuddy 包。

选择“来源顺序”时，结果会先按仓库、再按路径稳定排序，不依赖目录文件的爬取顺序，便于复查和分享同一个查询。

## 4. 先做只读试运行

确认输入和副作用后再导入。第一次只使用公开、非敏感数据；在允许写入、发送消息、付费 API 调用或访问生产环境前，先要求 Skill 给出执行计划。需要复现结果时，保存来源提交版本和包版本。
