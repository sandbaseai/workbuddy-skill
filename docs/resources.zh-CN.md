# WorkBuddy 资源地图

先按目的选择资料来源，再搜索目录中的 Skill。

## 按任务选择入口

| 你的目标 | 建议先看 |
|---|---|
| 把精选包安装到 WorkBuddy | [快速开始](quickstart.zh-CN.md) |
| 编写或排查 Skill ZIP | [Open Platform Skill 指南](https://open.workbuddy.cn/zh/docs/skill) |
| 接入 API、MCP Server 或 CLI | [Open Platform 连接器指南](https://open.workbuddy.cn/docs/connector) |
| 开发 OAuth 应用或调用 Open API | [第三方应用指南](https://open.workbuddy.cn/docs/third-party-app) 和 [Open API 接口文档](https://open.workbuddy.cn/docs/openapi) |
| 组装市场专家或专家团 | [专家指南](https://open.workbuddy.cn/docs/expert) 与 [专家团指南](https://open.workbuddy.cn/docs/expert-team) |
| 把公开目录结果制作成自己的包 | [适配教程](adapting-skills.zh-CN.md) |

## 官方产品文档

- [快速开始](https://www.workbuddy.ai/docs/zh/workbuddy/Quickstart)——安装和第一次使用。
- [创建 Skills](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)——编写 Skill。
- [MCP 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide)——MCP 概念和配置。
- [Open Platform 连接器指南](https://open.workbuddy.cn/docs/connector)——官方建议网络 API 优先使用 MCP + Skill，仅在 CLI 成熟且跨平台时使用 CLI + Skill，并说明运行时、凭证、OAuth 和权限。
- [Open API 接口文档](https://open.workbuddy.cn/docs/openapi)——WorkBuddy 集成的官方 API 与 OAuth 参考。
- [第三方应用指南](https://open.workbuddy.cn/docs/third-party-app)——OAuth 2.1 授权、应用注册、回调地址配置，以及用户授权与 Open API 调用之间的权限边界。
- [GitHub CLI `gh skill` 手册](https://cli.github.com/manual/gh_skill)——用于搜索、预览、安装和更新 Agent Skill 的 preview 命令。
- [Agent Skills 开放规范](https://agentskills.io/specification)——说明通用 `SKILL.md` 格式、命名规则、可选目录和跨宿主兼容边界。
- [Automation 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide)——自动化工作流。
- [Skill Marketplace](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) 和 [Explore](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Explore)——内置能力。
- [Open Platform Skill 指南](https://open.workbuddy.cn/zh/docs/skill)——官方说明 Marketplace 入口、ZIP 解析排查、frontmatter 字段和子资源目录结构。
- [Open Platform 总览](https://open.workbuddy.cn/docs/what-is-open-platform)——从入驻、开发、测试、审核到发布和维护的完整流程。
- [Open Platform 入驻指南](https://open.workbuddy.cn/docs/onboarding)——发布生态能力前准备开发者或企业认证。
- [Buddy 应用指南](https://open.workbuddy.cn/docs/buddy-app)——将行业工作流封装成可直接使用的 WorkBuddy 工作台，并配置 Skill、连接器和预览测试。
- [专家指南](https://open.workbuddy.cn/docs/expert)与[专家团指南](https://open.workbuddy.cn/docs/expert-team)——配置市场专家、专家团、Agent、Skill、提示词和连接器依赖。

## 学习与评测

- [WorkBuddy 实战蓝皮书](https://github.com/AlephAITech/WorkBuddyGuide)——按真实任务学习，也可以直接阅读[在线版](https://workbuddy.homes)。
- [WorkBuddy Starter](https://github.com/sunyet-01/WorkBuddy-Starter)——MIT 许可、面向新手的 WorkBuddy 入门资料库，按入门、Skills、场景和案例组织内容。
- [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills)——MIT 许可的本地 Agent Skill 目录与控制平面，可用于研究发现、选择和验证 Skill；仅作资料参考，不要当作自动安装源。
- [semlinker/awesome-workbuddy](https://github.com/semlinker/awesome-workbuddy)——CC0 许可的 WorkBuddy 教程、提示词、Skills、MCP 和场景实践导航；使用其中链接时仍需核对各项目的最新条款。
- [AI Coding / Agent 中文教程](https://github.com/KimYx0207/AI-Coding-Guide-Zh)——覆盖 WorkBuddy 及相关 Agent 工作流。
- [Learn WorkBuddy](https://github.com/adongwanai/learn-workbuddy)——MIT clean-room 定位的 Agent Harness 架构课程。
- [yinqd3/workbuddy-skills](https://github.com/yinqd3/workbuddy-skills)——MIT 许可的社区技能集合，包含学术研究、前端幻灯片和工具调用工作流；仅作为可审阅来源，不代表自动可信。
- [oh-my-workbuddy](https://github.com/mrzhangguoguo/oh-my-workbuddy)——MIT 许可的双语 WorkBuddy 端口，可参考其目录化工作流约定。
- [WorkBuddy Harness 机制蓝皮书](https://github.com/zjp1997720/zhijian-ai-bluebook-workbuddy-harness)——从本地文件、提示词拼装、扩展机制和安全边界理解 WorkBuddy，也提供[在线版](https://zjp1997720.github.io/zhijian-ai-bluebook-workbuddy-harness/)；仓库未声明许可证，仅作研究参考。
- [Tencent WorkBuddy Bench](https://github.com/Tencent/workbuddy-bench)——覆盖 Code、Web、Office 和 Security 工作负载的可复现 Agent 任务评测，支持 Docker 运行和结果报告。
- [GitSkills](https://arxiv.org/abs/2608.10906)——对数百万公开 `SKILL.md` 文件进行整理和分析的研究数据集；用于理解生态规模，不是安装源。
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401)——以需求驱动的基准，评估公开 Skill 是否能改善真实软件工程任务。
- [SkillsBench](https://arxiv.org/abs/2602.12670)——使用确定性验证器，对有 Skill 与无 Skill 的 Agent 任务进行配对评测。
- [Agent Skill Evaluation and Evolution](https://arxiv.org/abs/2606.11435)——梳理评测、反馈、压缩和进化框架，可用于设计质量门禁。
- [Awesome WorkBuddy](https://github.com/sandbaseai/awesome-workbuddy)——精选生态参考。
- [Community Awesome WorkBuddy](https://github.com/staruhub/awesome-workbuddy)——另一份双语官方资源、工作流、教程和对比索引；仅用于导航，不替代信任或许可证判断。
- [WorkBuddy Skill Groups](https://github.com/darker2016/workbuddy-skill-groups)——覆盖工程、研究、营销、设计、法律、财税和数据的多 Agent 专家团工作流集合；复用前仍需逐目录检查归属和许可证。
- [WorkBuddy Skills 归档](https://github.com/infometa/workbuddyskills)——用于离线学习的公开市场归档；该仓库明确说明内容版权归原作者，不代表允许再分发。
- [Community WorkBuddy skills collection](https://github.com/bitcjm/workbuddy-skills)——按场景分类的社区技能集合，并说明用户级/项目级安装方式；复用前仍需检查脚本、依赖和许可证。
- [WorkBuddy × ChatCut MCP](https://github.com/chonpszhou/workbuddy-chatcut-mcp)——MIT 许可的 OAuth/PKCE 与 Streamable HTTP MCP 接入案例，附带本地凭证和密钥扫描说明；使用前仍需确认第三方账号和媒体数据边界。

## 本仓库

- [快速开始](quickstart.zh-CN.md)——下载、校验并导入精选包。
- [目录条目解读](catalog-guide.zh-CN.md)——理解来源和审阅信号。
- [适配教程](adapting-skills.zh-CN.md)——将允许适配的公开来源制作成包。
- [可复制使用场景](use-cases.md)——连接器调用提示词和停止条件示例。
- [Starter Packs 入门包](starter-packs.zh-CN.md)——按任务选择已有的精选包。
- [Skill Atlas](https://sandbaseai.github.io/workbuddy-skill/zh-CN.html)——搜索固定公开快照。

官方文档是产品行为的准确信息源。社区教程和评测只是参考，不构成信任背书。
使用任何外部 Skill 前，仍需检查许可证、权限、引用资源和副作用。
