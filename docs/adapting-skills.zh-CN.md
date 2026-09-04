# 将索引技能适配为 WorkBuddy Skill

目录是发现入口，不是自动安装源。创建 WorkBuddy 包前，请检查精确的
GitHub 来源、仓库许可证、随附资源、网络行为和请求的权限。

## 创建包

从 `catalog/skills.jsonl` 或 `scripts/query_catalog.py --json` 获取记录的完整
`id`，先生成不会执行源内容的审核报告：

```bash
python3 scripts/review_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

报告会获取引用资源，分别列出指令与脚本信号、缺失的 WorkBuddy 字段，并将许可证、
指令、网络行为和权限检查明确保留为待人工完成。添加 `--json` 可获得机器可读输出。

完成审核后创建包：

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

生成的 ZIP 会把 `SKILL.md` 放在根目录，并附带 `SOURCE.json`，其中记录不可变
的源 URL、blob SHA、声明的许可证、适配说明和已打包资源。`scripts/`、
`references/`、`assets/`、`templates/` 下被引用的文件会从同一个不可变提交获取，
并保留相对路径；适配器不会执行源代码。

源文件和资源单个不能超过 512 KiB，全部资源不能超过 4 MiB；被引用的脚本也会
接受同样的保守静态扫描。资源路径不能逃逸出技能目录。

## 默认拒绝条件

默认情况下，检测到静态风险、无法获取引用资源，或输出已存在时，适配会停止。
请先检查源代码，再谨慎使用 `--allow-flagged`；只有确认技能不依赖缺失文件时才
使用 `--allow-missing-resources`；仅在有意替换时使用 `--force`。

生成的元数据不能代替原始许可证或安全审查。只有在源许可证允许的情况下，才应
发布适配后的包。
