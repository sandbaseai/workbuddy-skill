# WorkBuddy 快速开始

先按你的目标选择入口：

- **只想直接使用精选 Skill：** 下载 Release 中的 ZIP，然后导入 WorkBuddy。
- **想寻找更多公开 Skill：** 在 [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) 搜索，先阅读来源和风险，再安装。
- **想把公开 Skill 做成自己的 WorkBuddy 包：** 阅读[适配教程](adapting-skills.zh-CN.md)。

不确定如何判断搜索结果？先阅读[目录条目解读](catalog-guide.zh-CN.md)，再选择候选 Skill。

如果想按类别查找官方文档、学习资料和评测参考，请看[WorkBuddy 资源地图](resources.zh-CN.md)。

如果想按任务直接选择一个起点，可以先看 [Starter Packs 入门包](starter-packs.zh-CN.md)。

如果你想找经过人工整理的 WorkBuddy 文档、MCP 集成、工作流和评测，也可以浏览
[Awesome WorkBuddy 生态索引](https://github.com/sandbaseai/awesome-workbuddy)。它补充的是本仓库的
广泛元数据目录，但不能替代对具体来源和许可证的检查。

想按真实任务学习，可以看 [WorkBuddy 实战蓝皮书](https://github.com/AlephAITech/WorkBuddyGuide)；
想了解可复现的 Agent 任务评测，可以看 [Tencent WorkBuddy Bench](https://github.com/Tencent/workbuddy-bench)。
这些是参考资料，不是本目录新增条目，也不构成信任背书。

当前目录是 **21,818 条 Skill 的固定快照**。你可以用它寻找和审阅已有条目；不会自动发布新的 Skill。

平台功能请优先参考[官方快速开始](https://www.workbuddy.ai/docs/zh/workbuddy/Quickstart)、[官方 Skills 教程](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)、[MCP 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide)和[Automation 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide)。如果导入的 Skill 需要连接器，请先阅读[官方连接器指南](https://open.workbuddy.cn/docs/connector)，确认选择 MCP + Skill 还是 CLI + Skill，并检查认证和权限。也可以浏览官方的 [Skill Marketplace](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) 和 [Explore](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Explore)，查看现成能力和案例。如果需要确认 Open Platform 的 ZIP 结构、必填 frontmatter 和解析失败排查，请查看[官方 Open Platform Skill 指南](https://open.workbuddy.cn/zh/docs/skill)。本仓库负责目录发现与打包说明；产品界面和平台行为以官方文档为准。

## 5 分钟安装一个精选 Skill

### 1. 下载

从[最新 Release](https://github.com/sandbaseai/workbuddy-skill/releases/latest)下载需要的 ZIP。想用命令行精确下载时，把 `oss-review` 替换为 Atlas 中显示的包名，然后执行：

```bash
mkdir -p workbuddy-download
gh release download \
  --repo sandbaseai/workbuddy-skill \
  --pattern 'oss-review-workbuddy-skill.zip' \
  --pattern SHA256SUMS \
  --dir workbuddy-download
```

不要解压后重新打包；安装包已经把 `SKILL.md` 放在 ZIP 根目录。

需要可复现地校验下载内容时，同时下载同一 Release 中的 `SHA256SUMS`，并在 ZIP 所在目录执行：

```bash
cd workbuddy-download
sha256sum --check SHA256SUMS --ignore-missing
```

如果环境没有 `sha256sum`，也可以使用仓库提供的跨平台 Python 校验器：

```bash
python3 scripts/verify_release.py workbuddy-download
```

### 2. 导入

在 WorkBuddy 打开 **专家 · Skills · Connectors → Skills → 添加 Skill**，上传 ZIP 并完成导入。需要连接器的 Skill，还要在当前工作区启用对应服务。

如果使用连接器，第一次执行真实任务前先做以下检查：

1. 确认连接器需要的服务、账号、权限范围，以及它采用 MCP + Skill 还是 CLI + Skill。
2. 通过 WorkBuddy 的连接器流程完成认证，不要把 Token 或 API Key 粘贴到对话中。
3. 先执行状态检查或只读操作，并确认目标工作区和数据边界。
4. 让 Skill 在批准前列出所有写入、发消息、付费调用和外部副作用。

### 3. 先做一次安全的试运行

第一次使用时，先让 Skill 解释计划，不要立刻执行有费用、写入数据或发送消息的操作。可以直接复制：

```text
先说明你准备使用的能力、输入、权限、外部副作用和预计费用。
只做只读检查，不要调用付费接口、修改数据或发送消息。
如果信息不足，请列出需要我确认的事项。
```

确认来源、权限和计划后，再用少量公开数据执行。首次验证不要使用公司机密、个人敏感数据或生产环境。

## 从目录寻找 Skill

1. 在 [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) 或[中文目录](https://sandbaseai.github.io/workbuddy-skill/zh-CN.html)搜索任务或能力，例如 `ocr`、`web search`、`incident`。如果想直接找可安装的精选包，先把 **WorkBuddy 包状态 → 有精选包可用** 打开。
2. 打开条目的来源链接，确认许可证、输入输出、网络访问、凭据要求和潜在副作用。
3. 优先选择有明确说明、固定版本和可验证来源的 Skill；需要复现时固定到标签或提交 SHA。
4. 导入后按照上面的“安全试运行”提示词先检查，再执行真实任务。

支持开放 Agent Skills 约定的宿主，也可以从 GitHub 预览并安装：

```bash
gh skill search incident --limit 10
gh skill preview owner/repository skills/path/to/skill
gh skill install owner/repository skills/path/to/skill --pin v1.2.0 --dir .workbuddy/skills
```

如果你的宿主没有提供 `gh skill`，请使用 Atlas 中的固定来源链接，并按照[适配教程](adapting-skills.zh-CN.md)制作包。目录不会静默安装第三方 Skill。

## 一个可复制的任务模板

```text
使用「Skill 名称」完成「目标」。
先给出计划、需要的权限、输入数据、费用和副作用。
第一步只做只读验证；不要猜测参数，不要执行未确认的付费或写入操作。
每个结论附上依据；如果失败，说明失败点、已尝试内容和下一步选项。
```

图像、音频、视频等异步任务，要保存返回的 `run_id`，持续查询同一个任务直到成功或失败；等待期间不要重复创建付费任务。

## 常见问题

- **导入失败：** 确认上传的是 Release 原始 ZIP，且 `SKILL.md` 位于 ZIP 根目录；不要重复压缩。
- **看不到工具或连接器：** 在当前工作区启用对应服务，然后重新加载 WorkBuddy。
- **没有 `gh skill` 命令：** 打开 Atlas 结果中的固定来源链接，并按照适配教程制作包。
- **找不到合适的 Skill：** 用更短的能力词搜索，或先阅读目录中的相近条目；目录是发现入口，不代表自动信任。
- **参数校验失败：** 重新读取当前能力的 schema，只使用现有字段重试一次，不要凭经验猜参数。
- **鉴权、余额或权限错误：** 检查账号和工作区设置，不要在聊天中粘贴密钥。
- **结果不确定：** 要求 Skill 给出证据、来源和限制；不要把推测当作执行结果。

需要进一步帮助时，请查看 [支持说明](../SUPPORT.md)；发现安全问题请阅读 [安全政策](../SECURITY.md)。
