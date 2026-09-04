# SandBase for WorkBuddy：5 分钟快速开始

## 1. 下载

从[最新 Release](https://github.com/sandbaseai/workbuddy-skill/releases/latest)下载 `sandbase-workbuddy-skill.zip`。安装包已经把 `SKILL.md` 放在 ZIP 根目录，无需重新压缩。

## 2. 导入 WorkBuddy

打开 **专家 · Skills · Connectors → Skills → 添加 Skill**，上传 ZIP 并完成导入。确认当前工作区已启用 SandBase MCP 服务。

## 3. 零费用验证发现流程

发送：

```text
使用 SandBase 搜索一个网页提取 API。只比较候选、必填参数和价格，不要执行付费调用。
```

正确行为是先发现能力，再检查候选的实时 schema，并在执行前停止。它不应猜测服务商名称或请求参数。

## 4. 执行一个小任务

查看候选与价格后，让 WorkBuddy 用少量公开数据执行选定能力。首次验证不要使用公司机密或个人敏感数据。

图像、音频、视频等异步任务应保存返回的 `run_id`，持续查询同一任务直到成功或失败；等待期间不应重复创建付费任务。

## 故障排查

- **看不到 SandBase 工具：** 在当前工作区启用 SandBase MCP 服务，然后重新加载 WorkBuddy。
- **没有候选：** 改用更短的能力词，如 `ocr`、`web search` 或 `video`。
- **参数校验失败：** 重新检查能力，只使用当前 schema 字段重试一次。
- **鉴权或余额错误：** 检查账号状态，不要在聊天中粘贴密钥。

