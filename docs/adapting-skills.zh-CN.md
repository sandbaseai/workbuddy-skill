# 将公开 Skill 适配为 WorkBuddy Skill

这篇教程适合需要把目录中的公开 Skill 做成可导入 WorkBuddy 的用户。只想使用已有精选 Skill？请先看[快速开始](quickstart.zh-CN.md)。

## 先区分两套兼容要求

开放的 [Agent Skills 规范](https://agentskills.io/specification) 与 WorkBuddy Open
Platform 都使用带 YAML frontmatter 的 `SKILL.md`，但元数据要求并不完全相同。开放规范要求
小写、连字符连接的 `name`（最长 64 个字符），并将 `scripts/`、`references/` 和 `assets/`
列为可选目录；WorkBuddy 的[官方 Skill 指南](https://open.workbuddy.cn/zh/docs/skill)
还为 Marketplace 包说明了中英文描述、`version` 和 `author`。本仓库适配器会生成 WorkBuddy
所需字段，同时保持标准 `name` 形态，使结果更容易导入 WorkBuddy，也更容易被其他支持
Agent Skills 的宿主理解。

不要假设所有宿主都支持 `allowed-tools`、`user-invocable` 或
`disable-model-invocation` 等可选字段；使用前先检查目标宿主。连接器包还拥有独立的
`connector-meta.json` 与 `mcp.json`/`cli.json` 契约；这些文件应按[官方连接器指南](https://open.workbuddy.cn/docs/connector)
编写，不要把连接器配置塞进 `SKILL.md`。

## 适配前：先确认能不能发布

目录是发现入口，不是自动安装源。先打开精确的来源链接，确认：

- 源仓库许可证允许再发布或改编；
- Skill 的目标、输入、输出和依赖与你的使用场景匹配；
- `scripts/`、`references/`、`assets/` 和 `templates/` 中的文件是否被引用；
- 是否会访问网络、读取凭据、写入数据、发送消息或产生费用。

## 第一步：搜索并审核

从 [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) 或本地目录找到条目。使用记录的完整 `id`，不要只凭名称猜路径：

```bash
python3 scripts/query_catalog.py invoice OCR --json
```

先生成不会执行源内容的审核报告：

```bash
python3 scripts/review_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

报告会列出来源、引用资源、指令和脚本信号，以及缺失的 WorkBuddy 字段。它不能替代人工完成的许可证、安全、网络和权限审查。

## 第二步：生成 WorkBuddy 包

完成审核并确认来源许可证允许适配后，运行：

```bash
python3 scripts/adapt_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md' \
  --display-name-zh '中文名称' \
  --display-name-en 'English name' \
  --description-zh '说明这个技能做什么，以及何时使用。' \
  --description-en 'Explain what the skill does and when to use it.' \
  --author '原作者；WorkBuddy 适配者' \
  --source-license 'MIT'
```

生成的 ZIP 可以直接导入 WorkBuddy，`SKILL.md` 位于 ZIP 根目录，并附带 `SOURCE.json`。后者记录不可变来源 URL、blob SHA、声明的许可证、适配说明和已打包资源，方便追溯。

### 导入前快速检查

确认 ZIP 至少符合下面的结构：

```text
my-skill.zip
├── SKILL.md              # 必须位于 ZIP 根目录
├── SOURCE.json           # 本仓库适配器生成的来源信息
└── references/           # 只有 SKILL.md 引用了资源时才需要
```

打开 `SKILL.md` 的前 35 行，确认 frontmatter 包含官方指南要求的
`description`、`description_zh`、`description_en`、`version` 和 `author`。
适配器还会写入 `license`、`category` 和中英文展示名称，让包离开本仓库后仍然
可理解。若正文引用了不存在的资源文件，应补齐文件或删除引用，不能把它当作
普通提示忽略。

不解压也可以先做一次快速检查：

```bash
unzip -l dist/adapted/*.zip
unzip -p dist/adapted/*.zip SKILL.md | sed -n '1,35p'
```

如果 Marketplace 的解析规则或必填字段发生变化，以[官方 Skill 指南](https://open.workbuddy.cn/zh/docs/skill)
为准。

## 第三步：验证后再分享

导入前检查 ZIP 结构和 `SOURCE.json`；导入后用只读提示词做一次小范围测试。确认来源、权限、费用和副作用都清楚，再分享给其他用户或用于真实数据。

默认情况下，适配遇到静态风险、缺失引用资源或同名输出时会停止：

- 只有确认风险可接受后，才使用 `--allow-flagged`；
- 只有确认 Skill 不依赖缺失文件时，才使用 `--allow-missing-resources`；
- 只有确实要替换已有输出时，才使用 `--force`。

生成的元数据不能代替原始许可证或安全审查。来源许可证不允许时，不要发布适配包。
