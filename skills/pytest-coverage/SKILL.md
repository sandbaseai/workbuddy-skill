---
name: "pytest-coverage"
display_name: "pytest 覆盖率分析"
display_name_en: "pytest Coverage Analysis"
description: "Use when measuring pytest coverage, locating untested lines, and prioritizing behavior-focused tests without treating 100% line coverage as proof of correctness."
description_zh: "用于运行 pytest 覆盖率分析、定位未覆盖代码并按风险补测试；不把 100% 行覆盖率误认为正确性证明。"
description_en: "Measure pytest coverage, locate untested lines, and prioritize behavior-focused tests without equating line coverage with correctness."
category: "testing"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized Python test workspace and pytest-cov; test execution may have external side effects and must use an isolated environment"
---

# pytest 覆盖率分析

用 pytest-cov 生成覆盖率报告，定位未覆盖行、分支和关键行为，再按风险补充测试。覆盖率是取样信号，不是质量终点；优先保护公开契约、错误路径、权限边界、并发和数据转换。

## 工作流程

1. 先确认 Python 版本、测试命令、包范围、隔离环境、外部依赖和覆盖率基线。
2. 运行 `pytest --cov --cov-report=term-missing`；需要逐文件定位时生成 `--cov-report=annotate:cov_annotate`。
3. 将缺口按业务影响、变化风险和可观察行为排序，不为无意义的 getter 或生成代码盲目追求数字。
4. 为每个重要缺口补充行为、错误、边界、权限或回归测试；测试应可重复且不依赖真实生产服务。
5. 重新运行测试并比较基线、覆盖率、失败分类和新增测试价值，记录无法覆盖的理由。

## 约束与安全边界

- 默认在临时环境运行；不使用生产凭据、客户数据或不可逆的外部调用。
- 覆盖率报告可能包含源码路径、分支和敏感常量；发布前审查并脱敏。
- 不修改测试来掩盖失败，不把 `# pragma: no cover` 当成默认逃生口；例外要有范围、理由和复核日期。
- 结论必须同时说明测试通过、覆盖率变化、未覆盖风险和未验证外部依赖。
