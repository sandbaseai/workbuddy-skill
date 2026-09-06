# WorkBuddy 快速开始

先按你的目标选择入口：

- **只想直接使用精选 Skill：** 下载 Release 中的 ZIP，然后导入 WorkBuddy。
- **想寻找更多公开 Skill：** 在 [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) 搜索，先阅读来源和风险，再安装。
- **想把公开 Skill 做成自己的 WorkBuddy 包：** 阅读[适配教程](adapting-skills.zh-CN.md)。
- **精选包遇到问题：** 使用[精选包反馈表](https://github.com/sandbaseai/workbuddy-skill/issues/new?template=package-feedback.yml)，并注明失败阶段。

不确定如何判断搜索结果？先阅读[目录条目解读](catalog-guide.zh-CN.md)，再选择候选 Skill。

如果想按类别查找官方文档、学习资料和评测参考，请看[WorkBuddy 资源地图](resources.zh-CN.md)。

如果想按任务直接选择一个起点，可以先看 [Starter Packs 入门包](starter-packs.zh-CN.md)。

如果你想找经过人工整理的 WorkBuddy 文档、MCP 集成、工作流和评测，也可以浏览
[Awesome WorkBuddy 生态索引](https://github.com/sandbaseai/awesome-workbuddy)。它补充的是本仓库的
广泛元数据目录，但不能替代对具体来源和许可证的检查。

想按真实任务学习，可以看 [WorkBuddy 实战蓝皮书](https://github.com/AlephAITech/WorkBuddyGuide)；
想了解可复现的 Agent 任务评测，可以看 [Tencent WorkBuddy Bench](https://github.com/Tencent/workbuddy-bench)。
这些资料可以作为参考，但仍请结合你选择的 Skill 的具体来源和许可证进行判断。

当前目录提供 **21,818 条公开 Skill 快照**，适合先缩小搜索范围，再通过每条结果的来源链接确认上游最新版本。

## 先安装 WorkBuddy

导入 Skill 前，先按你的电脑选择官方安装说明：

| 平台 | 官方安装说明 |
|---|---|
| macOS 12 及以上 | [Mac 安装指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Installation-Mac-Guide) |
| Windows 10 1809 及以上或 Windows 11 | [Windows 安装指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide) |

WorkBuddy 启动并登录后，再继续下面的 Skill 安装路径。系统要求、安装包、首次启动安全提示和权限说明，以官方指南为准。

第一次执行真实任务前，建议保持[默认权限模式](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes)，并使用独立、可恢复的工作目录。只有在任务可信、隔离且确认影响范围后，才短暂切换到完全访问权限。

## 最短使用路径

| 如果你想…… | 先做什么 |
|---|---|
| 直接从 WorkBuddy 安装 Skill | 打开内置的 [Skill Marketplace](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)，检查作者和版本，安装后再确认权限。 |
| 现在就安装精选包 | 打开[精选包清单](https://sandbaseai.github.io/workbuddy-skill/packages.html)，下载 ZIP，校验 `SHA256SUMS`，再把原始 ZIP 上传到 WorkBuddy。 |
| 找一个特定能力 | 在 [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/) 搜索；需要可安装结果时打开“有精选包可用”，然后检查来源和许可证。 |
| 在本地搜索目录 | 执行 `python3 scripts/query_catalog.py <关键词> --package-status reviewed --sort score --limit 10`。 |
| 把公开来源制作成 WorkBuddy 包 | 阅读[适配教程](adapting-skills.zh-CN.md)，确认固定来源和许可证后再制作。 |

平台功能请优先参考[官方快速开始](https://www.workbuddy.ai/docs/zh/workbuddy/Quickstart)、[官方 Skills 教程](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)、[MCP 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide)和[Automation 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide)。如果导入的 Skill 需要连接器，请先阅读[官方连接器指南](https://open.workbuddy.cn/docs/connector)，确认选择 MCP + Skill 还是 CLI + Skill，并检查认证和权限。也可以浏览官方的 [Skill Marketplace](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) 和 [Explore](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Explore)，查看现成能力和案例。如果需要确认 Open Platform 的 ZIP 结构、必填 frontmatter 和解析失败排查，请查看[官方 Open Platform Skill 指南](https://open.workbuddy.cn/zh/docs/skill)。如果计划发布 Skill、连接器或其他生态能力，可以继续阅读[Open Platform 总览](https://open.workbuddy.cn/docs/what-is-open-platform)和[入驻指南](https://open.workbuddy.cn/docs/onboarding)，了解认证、测试、审核和发布前置条件。本仓库负责目录发现与打包说明；产品界面和平台行为以官方文档为准。

开始任务前，可先阅读[官方新建任务栏说明](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar)，选择工作目录、模型、已安装的 Skill、连接器和权限模式。
如果面对单体仓库或大型代码库，再参考官方的[大型代码库指南](https://www.workbuddy.ai/docs/cli/large-codebases)，通过目录级说明、聚焦 worktree 和按包配置缩小工作范围。
如果需要选择模型、使用自动模式、配置供应商预设、自定义接口或本地 Ollama，请阅读[官方模型配置说明](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Model)。

## 直接使用内置 Skill Marketplace

如果不需要下载本仓库的 ZIP，可以直接从 WorkBuddy 左侧打开 **Skill Marketplace**。按能力或分类搜索，打开条目查看说明、作者和版本，再点击 **安装**。安装后，先检查已启用的 Skill 及其权限，再用于真实数据。已安装的 Skill 可以在 Skills 区域停用、更新或卸载。具体界面和内置安全扫描行为请以[官方 Skill Marketplace 说明](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)为准。

## 先选择安装路径

| 路径 | 适合谁 | 作用范围 | 说明 |
|---|---|---|---|
| WorkBuddy 界面 | 大多数用户 | 当前工作区 | 在 **专家 · Skills · Connectors → Skills** 上传 Release 原始 ZIP，不需要本地 CLI。 |
| `gh skill install` | 支持 Agent Skills 约定的宿主 | `--dir` 指定的目录 | 项目专属能力可安装到 `.workbuddy/skills` 并纳入版本管理；该命令仍处于 preview。 |
| 本地 `~/.workbuddy/skills/` | 本地开发和反复试用 | 当前用户 | 审阅来源后再复制；如果宿主没有自动发现目录，请重新加载 Skill。 |

不要在同一次安装中混用这些路径。先确定作用范围，记录来源提交或
Release 版本，后续更新和删除时继续使用同一路径。

## 5 分钟安装一个精选 Skill

### 1. 下载

从[最新 Release](https://github.com/sandbaseai/workbuddy-skill/releases/latest)下载需要的 ZIP。精选包索引中的每条记录都提供可直接复制的 `download_command`；想用命令行下载 `oss-review` 时，等价命令如下：

```bash
mkdir -p workbuddy-download
gh release download \
  --repo sandbaseai/workbuddy-skill \
  --pattern 'oss-review-workbuddy-skill.zip' \
  --pattern SHA256SUMS \
  --dir workbuddy-download \
  --clobber
```

`--clobber` 会覆盖同名旧文件，方便你重复执行命令来刷新已有下载目录。

不要解压后重新打包；安装包已经把 `SKILL.md` 放在 ZIP 根目录。

需要可复现地校验下载内容时，同时下载同一 Release 中的 `SHA256SUMS`，并在 ZIP 所在目录执行：

```bash
cd workbuddy-download
sha256sum --check SHA256SUMS --ignore-missing
```

如果环境没有 `sha256sum`，也可以使用仓库提供的跨平台 Python 校验器；它还会拒绝不在 `SHA256SUMS` 中的额外 WorkBuddy ZIP：

```bash
python3 scripts/verify_release.py workbuddy-download
```

如果本地已经有仓库，建议优先使用 Python 校验器完成整套包检查；只想校验选中的 ZIP 时，再使用 `sha256sum`。

### 2. 导入

在 WorkBuddy 打开 **专家 · Skills · Connectors → Skills → 添加 Skill**，上传 ZIP 并完成导入。需要连接器的 Skill，还要在当前工作区启用对应服务。

如果使用连接器，第一次执行真实任务前先做以下检查：

1. 确认连接器需要的服务、账号、权限范围，以及它采用 MCP + Skill 还是 CLI + Skill。
2. 网络 API 优先选择 MCP + Skill；只有在 CLI 成熟且跨平台时才选择 CLI + Skill；同一个连接器不能混用两种方式。
3. 通过 WorkBuddy 的连接器流程完成认证，不要把 Token 或 API Key 粘贴到对话中。
4. 先执行状态检查或只读操作，并确认目标工作区和数据边界。
5. 让 Skill 在批准前列出所有写入、发消息、付费调用和外部副作用。

对于 CLI 连接器，应使用连接器声明的安装和状态步骤，不要假设系统已经安装 Node.js 或 Python。连接器声明运行时后，WorkBuddy 可以提供受管理的运行环境；字段和认证流程请以[官方连接器指南](https://open.workbuddy.cn/docs/connector)为准。

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
命令细节以 [GitHub CLI 官方 `gh skill` 手册](https://cli.github.com/manual/gh_skill) 为准；该命令族目前仍处于 preview 阶段。

```bash
gh skill search incident --limit 10
gh skill preview owner/repository skills/path/to/skill
gh skill install owner/repository skills/path/to/skill --pin v1.2.0 --dir .workbuddy/skills
```

如果希望由命令行按宿主管理安装位置，请显式指定宿主和作用域；需要可复现时同时固定版本，避免无意中安装默认分支的最新内容：

```bash
gh skill preview sandbaseai/workbuddy-skill skills/oss-review
gh skill install sandbaseai/workbuddy-skill skills/oss-review \
  --agent codex --scope project --pin v4.66.0
```

使用 `--scope user` 可安装到用户级目录；需要自定义目录时继续使用 `--dir`。由于该命令仍处于 preview，支持的宿主和作用域可能变化，复制命令到自动化流程前请查看[当前安装参考](https://cli.github.com/manual/gh_skill_install)。

如果你的宿主没有提供 `gh skill`，请使用 Atlas 中的来源链接，并按照[适配教程](adapting-skills.zh-CN.md)制作包。安装始终应在审阅来源和权限后显式执行。

## 更新、停用或移除 Skill

更新和删除时，继续使用安装时选择的同一作用范围：

- **WorkBuddy Marketplace：** 打开已安装的 Skills 页面，可以单独更新或批量更新；敏感任务前可以先停用，不再需要时再卸载。详见[官方 Skills Marketplace 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。
- **Release ZIP：** 从同一发布渠道下载新版 ZIP，重新校验校验和，再通过同一 WorkBuddy 流程导入。如果需要可回滚，先保留旧版本，完成一次小型只读检查后再移除旧版本。
- **项目级 `gh skill`：** 先审阅新的来源和固定版本，再把替换版本安装到同一个项目目录；提交目录变更，确保团队成员使用同一版本。
- **自定义 `--dir` 或用户级目录：** 确认精确路径后，只移除对应的 Skill 目录；不要删除父目录或其他 Skill。重新加载宿主，并确认列表中已不再出现该 Skill。

需要可复现时，在项目中记录来源 URL、提交或标签、包版本和校验和。如果更新改变了权限、连接器或外部副作用，使用真实数据前要重新完成一次安全试运行。

## 一个可复制的任务模板

```text
使用「Skill 名称」完成「目标」。
先给出计划、需要的权限、输入数据、费用和副作用。
第一步只做只读验证；不要猜测参数，不要执行未确认的付费或写入操作。
每个结论附上依据；如果失败，说明失败点、已尝试内容和下一步选项。
```

图像、音频、视频等异步任务，要保存返回的 `run_id`，持续查询同一个任务直到成功或失败；等待期间不要重复创建付费任务。

## 常见问题

按第一条匹配的情况处理，并在“下一步”完成前不要重复付费或写入操作，避免把未知故障扩大。

| 现象 | 先检查 | 下一步 |
|---|---|---|
| 导入失败 | Release 原始 ZIP 的根目录是否有 `SKILL.md` | 不要重复压缩；重新下载并校验包 |
| 看不到工具或连接器 | 当前工作区是否启用了对应服务 | 重新加载 WorkBuddy，再做一次只读状态检查 |
| 没有 `gh skill` 命令 | 当前宿主是否提供 preview 命令 | 打开 Atlas 固定来源链接，按适配教程制作包 |
| 找不到合适的 Skill | 搜索词是否是简短的能力词 | 搜索相近目录条目；目录用于发现，不代表自动信任 |
| 参数校验失败 | 当前能力的 schema 和必填字段 | 只用当前字段重试一次，不要猜参数 |
| 鉴权、余额或权限错误 | 账号、工作区和权限模式 | 检查设置，不要粘贴密钥；询问缺少的具体授权 |
| 结果不确定 | 返回结果中的证据、来源和限制 | 不要把推测当执行结果，要求可验证的结果 |

需要进一步帮助时，请查看 [支持说明](../SUPPORT.md)；发现安全问题请阅读 [安全政策](../SECURITY.md)。
