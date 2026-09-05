---
name: "python-packaging"
display_name: "Python 打包与发布"
display_name_en: "Python Packaging"
description: "Use when creating or reviewing distributable Python libraries/CLIs, pyproject metadata, wheels, source distributions, dependencies, or package releases."
description_zh: "用于创建或审查可分发 Python 库/CLI、pyproject 元数据、wheel、源码包、依赖或包发布。"
description_en: "Build reproducible Python distributions with modern pyproject metadata, source layout, locked dependencies, artifact checks, provenance, and authorized publication gates."
category: "developer-tools"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an isolated build environment, authorized package registry, repository signing/provenance policy, and release credentials; publication, yanking, and dependency changes require separate authorization"
---

# Python Packaging

把 Python 源码构建成可验证、可复现、可安全安装的 wheel 和 source distribution。打包不仅是写一个 `setup.py`：元数据、依赖、构建后端、命名空间、入口点、许可证、源码内容和发布证据必须一致。

## 使用边界

- 开始前确认 Python 支持版本、包名归属、版本策略、构建后端、依赖来源、许可证、registry、owner 和发布授权。
- 默认只读审查 `pyproject.toml`、源码布局、lockfile、构建日志和历史 artifact；在隔离环境构建，不执行安装包中的未知代码。
- 不擅自发布到 PyPI/私有 registry、覆盖/撤回版本、上传凭据、改变依赖范围或执行 release workflow；这些操作需要明确授权。
- 构建日志、metadata 和源码包不得包含 token、内部路径、环境变量、私有 URL 或敏感测试数据。

## 现代项目结构与元数据

优先 `src/<package_name>/` layout，避免从仓库根目录误导入未安装代码。使用 `pyproject.toml` 声明 PEP 517/518 build system 和 PEP 621 project metadata；保留 README、LICENSE、变更记录、类型标记和支持 Python 版本。包名、导入名、发行版本和 CLI entry point 分开校验。

```toml
[build-system]
requires = ["hatchling==1.27.0"]
build-backend = "hatchling.build"

[project]
name = "example-tool"
version = "0.1.0"
description = "A bounded example CLI"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.11"
dependencies = ["httpx>=0.27,<1"]

[project.scripts]
example-tool = "example_tool.cli:main"
```

版本由单一可信来源生成，不能让 tag、metadata、代码常量和发布说明漂移。对 dynamic version、extras、环境标记、optional dependency、namespace package 和 `py.typed` 做构建后检查；避免依赖范围过宽导致不可复现安装。

## 依赖与供应链

锁定直接/间接依赖、Python/平台 markers、build dependencies 和哈希；定期审查许可证、维护状态、已知漏洞、脚本钩子和构建后端。区分 runtime、build、test 和 docs 依赖，避免把测试工具带入生产安装。

构建在干净、无凭据的隔离环境中完成，禁止 setup/build 阶段联网下载未锁定内容或读取 secret。记录源码 commit、lockfile hash、构建器/解释器版本、输入文件清单和 artifact hash，形成可验证 provenance；签名密钥只通过受控 CI 注入。

## 构建与 artifact 检查

分别构建 wheel 和 sdist，检查文件列表、顶层目录、许可证、版本、依赖、入口点、类型文件、shebang、路径泄露、意外二进制和测试/密钥文件。用 clean virtual environment 安装 wheel 与 sdist，验证导入、CLI、依赖解析和最小运行行为；不能只检查“命令退出 0”。

```bash
python -m build --wheel --sdist
python -m twine check dist/*
python -m venv /tmp/example-package-check
/tmp/example-package-check/bin/pip install --no-index --find-links dist example-tool
/tmp/example-package-check/bin/example-tool --help
```

上述命令只应在隔离临时环境执行；发布前验证 `dist` 的 hash、metadata、内容清单和版本未被后续步骤修改。测试 PyPI/私有 staging registry 优先于正式 registry，并使用最小权限 token。

## 发布、回滚与兼容性

发布清单包含版本、commit、artifact hash、许可证、支持 Python 版本、破坏性变化、依赖变化、SBOM/provenance、签名和验证结果。对 public API、CLI 参数、配置、序列化格式和 entry point 做兼容性检查；需要 major/breaking 变化时写迁移与撤回策略。

发布后从干净环境按 hash 安装并运行 smoke test，确认 registry 展示的 metadata 与本地构建一致。错误版本优先停止晋级、发布修复版本或按 registry 政策 yanking；不要删除用户可能依赖的版本或重用同一版本号覆盖 artifact。

## 质量门禁

- [ ] 包名/导入名/版本、许可证、支持 Python、README、入口点和 API 兼容策略一致。
- [ ] `pyproject.toml` 使用明确 build backend，src layout、依赖、extras、markers 和 lockfile 可复现。
- [ ] clean 隔离环境分别构建 wheel/sdist，并检查内容、metadata、hash、路径、secret 和意外文件。
- [ ] wheel/sdist 在无网络环境安装并通过 import、CLI、smoke test 和依赖解析验证。
- [ ] provenance/SBOM/签名/许可证/漏洞审查和 staging registry 验证已留证。
- [ ] 正式发布、yank、依赖/版本变更和凭据使用均有授权、最小权限与回滚方案。
