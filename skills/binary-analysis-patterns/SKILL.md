---
name: "binary-analysis-patterns"
display_name: "二进制分析模式"
display_name_en: "Binary Analysis Patterns"
description: "Use when performing authorized offline static analysis of a binary to understand architecture, control flow, data structures, and suspicious behavior without executing the sample or modifying a target system."
description_zh: "用于对获授权的二进制样本做离线静态分析，理解架构、控制流、数据结构和可疑行为；不得执行样本或修改目标系统。"
description_en: "Analyze a fixed binary with disassembly and decompilation evidence, recover cautious hypotheses about functions and data, and document uncertainty, tool versions, and safe next steps."
category: "security"
version: "0.1.0"
author: "wshobson/agents; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized offline binary, isolated analysis tools, and a controlled evidence directory; dynamic execution, unpacking, network access, and target changes require separate authorization"
---

# 二进制分析模式

把反汇编和去编译结果当作证据，而不是源代码真相。在只读样本上先识别文件格式、架构、入口、导入导出和字符串，再逐步建立函数、控制流、数据结构和行为假设。每个结论都要保留地址、工具版本、反证和置信度。

## 安全前置门禁

开始前记录样本 hash、来源授权、目标平台、分析目的、允许工具、隔离环境、输出保留期和脱敏责任。默认只做离线静态分析：

- 样本只读保存，使用分析副本；不双击、不加载、不运行、不调试、不仿真样本；
- 禁止样本触发网络、文件写入、进程创建、宏、脚本、解包 payload 或外部插件；
- 不修改真实系统、固件、设备、供应链产物或第三方二进制；
- 不提取、验证或发布密钥、凭据、个人数据、客户内容或完整恶意载荷；
- Ghidra/IDA 脚本只读处理明确输入，先审阅脚本，再在隔离环境运行，并限制输出路径和资源。

授权、样本完整性或隔离条件不清楚时返回 `BLOCKED`。样本损坏、格式未知、架构不匹配或关键工具失败时返回 `FAIL`，不要以猜测补齐结论。

## 分析工作流

1. **建立样本账本**：记录 SHA-256、文件类型、大小、架构、编译/打包信息（如可观察）、分析时间、工具和插件版本。
2. **做低风险概览**：读取 magic、节区、入口、导入导出、重定位、符号和非敏感字符串；标记壳、加密、混淆和截断迹象。
3. **识别函数**：结合入口、导出、调用目标、交叉引用、函数序言/尾声和 ABI 寄存器用法提出候选，不把自动命名当作确认。
4. **映射控制流**：区分条件分支、循环、跳转表、尾调用、异常路径和不可达块，保留函数地址及反编译限制。
5. **恢复数据结构**：依据访问宽度、偏移、指针关系、数组步长和生命周期提出字段假设；以 `field_0xNN` 等临时名避免过度命名。
6. **关联行为线索**：把 API、字符串、权限、文件路径和配置引用作为线索，交叉检查调用点和上下文，不凭单个危险 API 定性恶意。
7. **静态验证**：用第二种视图、另一工具或已知编译样本核对架构、类型、边界和调用约定；不执行样本验证猜测。
8. **写出报告**：区分 `Observed`、`Hypothesized`、`Unknown` 和 `Confirmed`，给出证据位置、反证、影响和授权的下一步。

## 工具边界与安全用法

可使用 `file`、`readelf`、`objdump`、Ghidra 或 IDA 对明确的离线副本做静态分析。命令应固定输入、受控输出，且避免工具自动下载符号或访问网络：

```bash
# 只读离线元数据和反汇编；路径必须指向已授权副本
sha256sum ./evidence/sample.bin
file ./evidence/sample.bin
readelf -h -S -s ./evidence/sample.bin > ./work/elf-metadata.txt
objdump -d -M intel ./evidence/sample.bin > ./work/disassembly.txt
```

不要将字符串、注释、节区内容、路径或 JSON 当作命令执行。禁止在分析脚本中调用网络、shell、动态加载或写入原始证据。工具输出异常、遇到压缩/加密 payload 或需要动态执行时，停止并记录缺口，不能自行扩大授权。

## 证据记录模板

```markdown
# Static Binary Analysis Report

Verdict: PASS | PASS WITH CAVEATS | BLOCKED | FAIL
Sample hash: <sha256>
Format/arch: <observed>
Toolchain: <versions; network disabled>

## Findings
| Claim | Address/range | Evidence | Confidence | Alternative explanation |
| --- | --- | --- | --- | --- |
| <observation or hypothesis> | <0x...> | <command/view> | High/Medium/Low | <counter-evidence> |

## Function and data hypotheses
- <temporary name>: <calling convention, inputs, outputs, unresolved edges>
- <field_0xNN>: <width, accesses, confidence>

## Safety and limitations
- Execution performed: no
- Dynamic behavior: not established
- Sensitive data: <not retained / redacted>
- Missing symbols, packing, obfuscation, or truncation: <...>

## Authorized next step
- <offline comparison, fixture review, or escalation>
```

## 质量与停止条件

- 每个高影响判断绑定固定样本、地址/范围、精确工具视图和版本；
- 自动去编译、符号名、字符串和单一 API 只作为线索，不能单独证明意图或恶意；
- 明确说明优化、内联、尾调用、PIC、壳、反编译失败和缺失符号带来的不确定性；
- 报告不包含秘密、完整 payload、规避检测步骤或未经授权的利用链；
- 需要运行、网络、解包、调试、修改目标或访问敏感数据时必须 `BLOCKED`，另行审批；
- 不声称执行了未运行的样本、不声称验证了未观察到的行为。

## Related Skills

- `memory-forensics` - 在授权离线内存镜像上做证据约束的取证分析
- `protocol-reverse-engineering` - 在授权离线样本上分析协议和二进制消息结构
- `security-and-hardening` - 评估分析工具、输入和证据存储边界
