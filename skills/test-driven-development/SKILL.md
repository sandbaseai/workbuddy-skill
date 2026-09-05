---
name: "test-driven-development"
display_name: "测试驱动开发"
display_name_en: "Test-Driven Development"
description: "Use when implementing a feature, bug fix, refactor, or behavior change and a regression-safe test-first workflow is appropriate."
description_zh: "用于实现新功能、修复缺陷、重构或改变行为时，以测试先行建立可验证的回归安全工作流。"
description_en: "Write one behavior-focused failing test, verify the expected failure, implement the smallest change, verify all tests, and refactor only while green."
category: "development"
version: "0.1.0"
author: "obra/superpowers; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with an authorized repository and test runner; production changes, external integrations, generated code, and configuration exceptions require explicit scope and separate approval"
---

# Test-Driven Development

以 RED → GREEN → REFACTOR 建立可信回归保护：先写一个只描述真实行为的失败测试，确认它因预期缺失而失败，再写最小实现，最后只在全绿状态下重构。

## 适用范围与边界

- 默认用于新功能、缺陷修复、重构和行为变化；一次性原型、纯生成物或配置变更只有在明确记录例外理由、替代验证和风险后才可跳过。
- 测试只使用授权的本地/测试环境和合成或脱敏 fixture；不为测试改写生产数据、发送真实消息、支付、删除资源或泄露凭据。
- 先确认测试命令、提交、依赖和可接受的副作用。测试输出、快照、trace 和日志脱敏后再写入报告。
- 测试通过不等于实现正确；仍需检查测试是否真的覆盖用户行为、权限、错误和回滚路径。

## RED：写一个行为测试

每次只写一个最小行为，名称描述结果而不是实现细节。优先调用真实生产 seam；只有无法安全或合理集成时才使用 mock，并说明其限制。测试必须包含有意义的断言，而不是只断言函数被调用或程序未崩溃。

```text
test("[observable behavior]", async () => {
  result = await real_boundary(minimal_safe_input)
  assert(result == expected_observable_result)
})
```

先明确“什么生产变化会使它失败”，再写测试。测试不得因为过度 mock 而绕过真正的代码路径。

## VERIFY RED：确认失败有效

运行最窄的测试命令并记录输出。失败必须是预期行为尚不存在或缺陷仍存在，而不是拼写错误、导入错误、fixture 污染、环境缺失或测试自身异常。若测试立即通过，说明它覆盖现有行为或断言无效，修正测试后重新观察失败。

## GREEN：最小实现

只做让当前测试通过的必要改动，不顺手加入未要求的选项、抽象、重构、性能优化或依赖。测试失败时修改实现而不是把期望改弱；每次只改变一个变量，并保留差异范围和证据。

## VERIFY GREEN：验证完整回归

先运行当前测试确认通过，再运行相关单元/集成/端到端门禁和完整测试集。检查错误、警告、环境泄漏、未清理临时文件和权限边界。对于异步、时间、随机数、网络和并发行为，固定可控输入并记录仍存在的不确定性。

## REFACTOR：只在全绿后整理

在行为已经由测试保护后，才移除重复、改善命名、提取稳定辅助函数或整理结构。重构不能改变行为；每个小改动后都重新运行测试。若测试难写，视为接口/依赖边界的设计信号，不通过增加脆弱 mock 掩盖它。

## 重复循环与例外

下一个行为重新从 RED 开始。对原型、生成代码或配置例外，记录为何不适合 TDD、采用的替代检查、人工审批和后续转化为自动测试的风险；例外不能悄悄变成默认模式。

## 完成交付

报告包含测试路径、基线提交、每次 RED/GREEN 命令和关键输出、覆盖的行为、未覆盖的边界、mock/fixture 限制、完整回归结果、清理结果和未解决风险。标注 `observed`、`derived`、`unknown`，不声称看过未实际运行的失败或通过。

## 质量门禁

- [ ] 每个行为测试先写后实现，并实际观察到预期失败。
- [ ] 失败原因是缺失行为/真实缺陷，而非测试或环境错误。
- [ ] 实现是让当前测试通过的最小改动，没有捆绑无关重构。
- [ ] GREEN 后相关门禁和完整测试均已运行并记录结果。
- [ ] 重构只在全绿后进行，测试断言真实行为而非无意义 mock。
- [ ] 例外有替代验证、批准、风险和后续计划。
- [ ] fixture、日志和输出脱敏，未产生未授权外部副作用。
