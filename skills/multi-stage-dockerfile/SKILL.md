---
name: "multi-stage-dockerfile"
display_name: "多阶段 Dockerfile"
display_name_en: "Multi-Stage Dockerfile"
description: "Use when creating or reviewing reproducible, minimal, and secure multi-stage Dockerfiles for an application or service."
description_zh: "用于创建或评审可复现、精简且安全的应用或服务多阶段 Dockerfile。"
description_en: "Design multi-stage container builds with pinned bases, cache-aware layers, minimal runtime contents, non-root execution, secret-safe builds, health checks, scanning, and rollback evidence."
category: "devops"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with authorized repository, Docker/BuildKit builder, image registry, and isolated build/test environment; publishing images, changing deployment manifests, or running privileged containers requires separate authorization"
---

# 多阶段 Dockerfile

设计可复现、体积受控、最小权限的容器镜像。先明确运行时、架构、端口、数据目录、健康语义、来源和发布环境，再把依赖、构建、测试与运行时分开；Dockerfile 是构建输入，不应携带凭据或隐含生产变更。

## 使用边界

- 开始前确认应用入口、语言/框架版本、CPU/OS 架构、构建器、基础镜像来源、registry、镜像 owner、扫描策略、运行 UID/GID、网络和数据持久化。
- 默认在隔离环境执行 lint、构建、测试和镜像检查；不得拉取不可信镜像、挂载宿主敏感目录、使用 privileged、访问生产 registry 或部署新镜像。
- 不把 secret 放入 `ARG`、`ENV`、Dockerfile、镜像层、构建日志或标签；需要凭据时使用 BuildKit secret/SSH mount，并确认最终层、history 和 provenance 不含秘密。
- 镜像构建成功不等于应用安全；记录 observed、derived、unknown，并把 registry 推送、部署、回滚和运行时权限变更交给明确授权流程。

## 阶段结构

按依赖 → 构建 → 测试 → 运行时组织阶段，并使用有意义的 `AS` 名称。构建阶段可包含编译器、包管理器和测试工具；runtime 只复制必要产物、证书、配置模板和非敏感资源，不能整段复制源码、缓存、`.git`、测试数据或构建工具。

```dockerfile
FROM python:3.12.4-slim-bookworm AS builder
WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=secret,id=private_index \
    python -m pip install --no-cache-dir --prefix=/opt/app -r requirements.txt
COPY src ./src
RUN python -m compileall -q src

FROM gcr.io/distroless/python3-debian12:nonroot AS runtime
WORKDIR /app
COPY --from=builder /opt/app /opt/app
COPY --from=builder /build/src /app/src
USER nonroot:nonroot
ENV PYTHONPATH=/app:/opt/app
ENTRYPOINT ["python", "-m", "src.main"]
```

示例中的版本、依赖文件、入口和镜像必须替换为项目实际契约；不要因为示例使用 distroless/Alpine 就忽略兼容性、C 库、证书、时区或调试需求。

## 基础镜像与可复现性

- 优先选择官方、维护中的最小镜像，并固定 digest；至少固定完整版本 tag，记录来源、架构、发布时间和漏洞基线。
- 明确 glibc/musl、CA certificates、时区、字体、动态库、用户数据库和 DNS 行为；运行时缺失依赖要在隔离 smoke test 中暴露。
- 锁定直接和传递依赖、包源、校验和及构建工具版本；避免浮动 tag、未认证第三方 registry 和构建时在线解析未锁定版本。
- 多架构构建必须分别验证产物、启动、健康、性能和扫描结果；不要把一个架构的 digest 或测试结果套用到全部架构。

## 层、缓存与上下文

先复制依赖清单并安装，再复制频繁变动的源码，使缓存边界可解释。提供严格的 `.dockerignore`，排除 `.git`、凭据、密钥、虚拟环境、缓存、构建产物和本地数据；使用 BuildKit cache mount 时确认缓存不进入最终层。合并相关 RUN 可以减少层，但不要牺牲可审计性或把不相关下载与清理混在一起。

检查最终镜像的大小、层树、文件列表、用户、暴露端口和启动命令；用 `docker history`、镜像解包和 secret 扫描确认敏感输入没有残留。构建日志、缓存导出和 provenance 也应按同样的保密级别处理。

## 权限与运行时安全

- 运行时使用固定的非 root UID/GID，明确可写目录和文件 owner；尽量使用 read-only root filesystem、丢弃 Linux capabilities、禁止 privilege escalation，并在部署层设置 seccomp/AppArmor 等约束。
- 只声明实际端口；`EXPOSE` 不是访问控制。网络、服务账号、云身份、挂载、临时目录和出站域名需在部署配置中单独审查。
- 不在镜像中放 SSH key、云凭据、`.env`、token、内部证书或生产配置。构建参数不是秘密存储，镜像标签和环境变量也可能被读取。
- HEALTHCHECK 应检查真实可用性且无副作用，设置合理 timeout、interval、retries 和 start period；区分进程存活、依赖可用和业务就绪。

## 验证、扫描与交付

隔离验证 Dockerfile 语法、依赖安装、构建、单元/集成测试、启动、健康、信号处理、优雅停机、非 root 文件权限、网络失败和无数据目录场景。扫描最终镜像和 SBOM，检查 OS/语言依赖漏洞、恶意包、secret、许可、digest、provenance、镜像签名和 registry policy；记录工具版本、扫描时间、例外 owner 和过期日。

发布前核对镜像 digest、架构、标签、SBOM、签名、部署引用、配置兼容性、canary 指标和回滚镜像。禁止仅用 `latest` 回滚；保留上一个已验证 digest，并对 registry 不可用、拉取失败、启动失败和健康恶化演练恢复。生产 push、部署、删除旧 tag 和修改 runtime 安全策略均需授权。

## 质量门禁

- [ ] 构建/测试/运行时阶段边界清晰，最终镜像仅含必要产物。
- [ ] 基础镜像、依赖、包源、架构和构建工具可追溯并已固定或说明例外。
- [ ] `.dockerignore`、BuildKit cache/secret、history、层和日志检查确认无凭据泄露。
- [ ] runtime 使用非 root 和最小权限，端口、可写目录、能力、网络和身份边界已验证。
- [ ] 启动、健康、信号、失败依赖、SBOM、漏洞/secret/许可扫描和例外治理有证据。
- [ ] 镜像 digest、签名、provenance、canary、发布授权和可验证回滚已准备。

## Related Skills

- `container-security` - 评估镜像、运行时、registry 和容器隔离风险
- `github-release` - 编排带校验和资产核对的可追溯发布
- `secrets-management` - 设计凭据注入、轮换、扫描和审计边界
