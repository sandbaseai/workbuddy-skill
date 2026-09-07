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
- **精选包是否可用**是另一套信号。标记为精选包的结果，表示本仓库在 Release 中提供了固定来源的 WorkBuddy ZIP；并不是所有 `workbuddy-ready` 条目都有 ZIP，只有目录记录也不等于自动不安全。
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

同样的审阅筛选也可以使用快捷参数：

```bash
python3 scripts/query_catalog.py research --high-signal --limit 10
```

`--high-signal` 等价于无静态标记、优先疑似主来源、兼容分数至少 80、按唯一
blob 去重并按分数排序。它只是缩小候选范围的辅助条件，不代表可信或安全。

如果想使用与 Atlas 相同的分类词表，可以加上 `--category`（例如
`research`、`development` 或 `security`）；中文用户也可以直接写 `研究`。
它会使用目录名称/路径推导分类，并优先采用精选包元数据中的分类：

```bash
python3 scripts/query_catalog.py --category research --package-status reviewed \
  --sort score --limit 10
```

以下是几组已经验证可以直接开始的查询配方（都使用同一套审阅筛选）：

| 目标 | 命令 |
|---|---|
| 调研和网页资料 | `python3 scripts/query_catalog.py research --high-signal --limit 10` |
| OCR 和文档提取 | `python3 scripts/query_catalog.py ocr --high-signal --limit 10` |
| MCP 和连接器工作流 | `python3 scripts/query_catalog.py mcp --high-signal --limit 10` |
| 测试和 QA | `python3 scripts/query_catalog.py testing --high-signal --limit 10` |
| 文档工作流 | `python3 scripts/query_catalog.py documentation --high-signal --limit 10` |

将关键词替换成你的任务即可；如果需要从本仓库 Release 下载精选包，再加上
`--package-status reviewed`。

如果要评估新的 GitHub 来源或爬取范围，可以给
`scripts/crawl_github_skills.py` 加上 `--dry-run`。它会执行发现并报告候选数量，
但不会写入 JSONL 输出或统计文件；公开冻结目录仍需要另外显式授权。只想审阅某个
仓库而不触发全局 Code Search 时，组合使用
`--repository owner/name --repository-only`。
在仓库定向模式中，`--target` 只是数量上限；小仓库完整扫描后，即使候选少于上限也会成功返回。
如果要重复扫描一组公开来源，可以在 UTF-8 文件中每行写一个 `owner/name`，再使用
`--repository-file`；空行和 `#` 注释会被忽略：

```bash
python3 scripts/crawl_github_skills.py --dry-run \
  --repository-file config/upstream-skill-sources.txt \
  --repository-only --target 12500 \
  --dry-run-output /tmp/upstream-skill-probe.jsonl
```

仓库的定时 `Refresh skill catalog` 工作流也会对一组代表性的上游 Skill 仓库执行只读探测。
它只报告新发现的路径，不会写入冻结目录、生成精选包或改变已发布快照；Actions Artifact
保留 30 天，会保存发现到的 JSONL 行，便于后续处理。需要详细审阅某个候选时，仍请在本地运行上面的命令。
其中第二个文件只保留冻结目录中尚未出现的路径和内容 SHA，便于直接筛选新候选。
第三个文件会为这些新候选增加不会执行源内容的兼容性和静态信号预审；这些信号只是线索，不代表批准。

如果只想查看本仓库已经提供审阅版 Release ZIP 的条目，可以使用精选清单：

```bash
python3 scripts/query_catalog.py research --package-status reviewed
```

精选结果会直接显示 Release ZIP 地址；使用 `--json` 时，包地址、稳定的资产文件名、校验地址和可复制的 GitHub CLI 命令分别位于 `workbuddy_package_url`、`workbuddy_package_asset`、`workbuddy_checksum_url` 和 `workbuddy_download_command`，脚本可以直接下载并校验包，不需要手工拼接 Release 路径。结果的 Atlas 分类位于 `workbuddy_category`，便于后续程序路由或分组。

如果想得到一份可供程序读取的“高信号可安装包”候选清单，可以组合精选包筛选、`--json` 和数量限制，再在复制命令前检查第一条结果：

```bash
python3 scripts/query_catalog.py research \
  --high-signal --package-status reviewed --limit 5 --json \
  > research-packages.json
jq -r '.[].workbuddy_download_command' research-packages.json
```

如果环境没有 `jq`，可以改用 Python 标准库：

```bash
python3 -c 'import json; from pathlib import Path; print("\\n".join(item["workbuddy_download_command"] for item in json.loads(Path("research-packages.json").read_text())))'
```

第二条命令只打印下载命令，不会自动执行。选定条目后，先打开 `source_url`，确认许可证和副作用，再运行选中的 `gh release download` 命令，并按照[快速开始](quickstart.zh-CN.md)校验 `SHA256SUMS`。

人类可读输出会直接给出完整的 `catalog id`。把这个值复制给
`review_skill.py` 或 `adapt_skill.py` 即可，不要根据显示名称手工拼接 ID。

如果本地查询没有匹配结果，命令会打印 Atlas 和 GitHub 当前 `SKILL.md`
搜索入口，帮助继续发现目录之外的内容。这些链接只扩大搜索范围，不代表自动批准或安装外部来源。

```bash
python3 scripts/review_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

也可以把同一个 ID 粘贴回本地搜索工具或 Atlas 搜索框，重新定位精确条目：

```bash
python3 scripts/query_catalog.py 'github:owner/repository:path/to/SKILL.md'
```

搜索只负责缩小候选范围，不会自动安装。选定条目后，先检查来源，再按照[适配教程](adapting-skills.zh-CN.md)制作经过审阅的 WorkBuddy 包。

如果 Atlas 没有匹配结果，可以使用页面中的“在 GitHub 搜索当前 Skill 文件”链接查找当前目录之外的新内容。该链接只用于发现，不代表可信或自动安装；适配前仍需检查仓库、许可证、脚本、权限和提交。

脚本和数据看板可以直接读取[紧凑目录数据](https://sandbaseai.github.io/workbuddy-skill/catalog.json)，字段定义见对应的 [JSON Schema](https://sandbaseai.github.io/workbuddy-skill/catalog-schema.json)。普通用户可浏览[精选包静态页面](https://sandbaseai.github.io/workbuddy-skill/packages.html)；程序则使用独立的[精选包 JSON](https://sandbaseai.github.io/workbuddy-skill/packages.json)及其 [Schema](https://sandbaseai.github.io/workbuddy-skill/packages-schema.json)。每条包记录都提供用于 GitHub CLI 下载的 `asset` 文件名、可直接复制的 `download_command`，以及用于校验 ZIP 的 `checksum_url`。

选择“来源顺序”时，结果会先按仓库、再按路径稳定排序，不依赖目录文件的爬取顺序，便于复查和分享同一个查询。

程序可以根据公开的[目录元数据 Schema](https://sandbaseai.github.io/workbuddy-skill/catalog-meta-schema.json)
验证元数据字段结构。

## 4. 先做只读试运行

确认输入和副作用后再导入。第一次只使用公开、非敏感数据；在允许写入、发送消息、付费 API 调用或访问生产环境前，先要求 Skill 给出执行计划。需要复现结果时，保存来源提交版本和包版本。
