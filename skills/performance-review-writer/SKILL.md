---
name: "performance-review-writer"
display_name: "绩效反馈写作"
display_name_en: "Performance Review Writer"
description: "Use when drafting an evidence-based self-assessment, peer review, 360 feedback, or upward feedback in the user's voice."
description_zh: "用于以用户的语气起草有证据的自评、同事评价、360 反馈或向上反馈。"
description_en: "Draft honest, specific, and constructive performance feedback from authorized evidence using STAR structure, privacy-safe synthesis, explicit gaps, and human submission controls."
category: "writing"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with explicitly authorized review context and source material, synthetic or redacted evidence handling, and a local draft workspace; accessing mail/chat/calendar data, naming people, saving drafts, or submitting reviews requires separate authorization"
---

# 绩效反馈写作

把真实贡献和可观察行为整理成具体、诚实、建设性的绩效反馈。支持自评、同事评价、360 反馈和向上反馈；输出是供人审阅的草稿，不代替事实核验、管理判断或向公司系统提交。

## 隐私与授权边界

- 开始前确认反馈类型、被评价对象/角色、评审周期、字数/表单限制、语气、读者、材料来源和授权范围；没有这些信息时先列最小问题，不猜测身份或周期。
- 只使用用户明确授权的邮件、聊天、会议记录、项目文档、指标或用户提供的要点；默认不要检索整个邮箱、私聊、私人日历或与评审无关的线程。
- 处理同事、客户和下属信息时坚持最小化：只保留与工作行为和结果有关的内容，删除私人细节、健康/家庭信息、敏感身份、无关参与者和完整原文。
- 不编造项目、数字、赞扬、因果、评价或引用；证据不足写 `[NEEDS DETAIL]` 或 `unknown`。推断必须标明为推断，并允许用户删改。
- 不发送邮件、写入 HR 系统、提交评价、通知被评价者或改变任何记录；只在已授权本地目录保存草稿，提交动作永远由用户完成。

## 反馈类型

| 类型 | 关注对象 | 推荐语气与证据 |
|---|---|---|
| Self-assessment | 自己 | 自信、具体、成长导向；贡献与影响 |
| Peer review | 同事 | 平衡、尊重、可观察行为；协作与结果 |
| 360 feedback | 多方关系 | 分离事实与观点；说明观察范围和限制 |
| Upward feedback | 经理/负责人 | 外显行为、影响和可行动请求；不评价人格 |

先确认表单真正需要的类型；同一材料不能未经重写就复制到不同类型。匿名反馈要避免能反推出身份的独特细节，并说明匿名性由系统而非 WorkBuddy 保证。

## 工作流

### 1. 收集上下文

建立范围卡：周期、角色、目标、项目、责任、读者、提交格式、字数和排除项。若授权的企业搜索连接器可用，只检索时间、项目和参与者范围内的相关证据，先输出证据摘要和来源类别，不直接复制原文。若连接器不可用，请用户提供 3–5 个要点、指标或链接；不要为了补全而访问未授权资料。

### 2. 建立证据账本

每条候选贡献记录 Situation、Task、Action、Result（STAR）、来源、日期、作者/角色（能匿名则匿名）、置信度和缺口。区分：

- `observed`：材料直接支持的事实；
- `derived`：由多个事实计算或归纳的结果，写出推导；
- `reported`：他人反馈或用户回忆，标注来源类别；
- `unknown`：无法验证的数字、因果或范围。

只使用与周期相关且可公开给评审读者的证据；不要把一次赞扬推广成稳定特质，不要把相关性写成因果，不要将活动数量当成果质量。

### 3. 起草与校准

每个成就尽量使用：背景/挑战 → 责任 → 具体行动 → 影响/结果 → 学习/下一步。写清项目、行为、受影响用户/团队和可验证结果；没有数字时使用可观察变化，不用伪精确百分比。避免“team player”“above and beyond”“hard worker”等空泛词，改为行为和结果。

自评可包含总结、3–5 项关键成就、协作与影响、成长、发展方向和下一周期目标；同事评价聚焦优势、具体例子、成长建议和合作体验；向上反馈聚焦有效做法、行为影响和一个清晰请求。发展建议针对行为和环境，不针对人格、动机、年龄、外貌或其他受保护特征。

### 4. 审阅与交付

先展示草稿、使用过的证据类别、`[NEEDS DETAIL]`、假设和敏感信息处理，再按用户要求迭代。让用户逐项确认名字、代词、数字、归因、语气、保密范围和表单限制；任何未经确认的字段留空或标记。保存前检查路径和访问权限，文件名不要包含不必要的敏感姓名；不自动提交。

## 质量与公平性检查

检查每个结论是否有足够证据、是否只评价可观察工作行为、是否同时呈现影响和限制、是否给出具体可行动的成长建议。搜索偏差、可见性偏差、远程/异步工作偏差和样本不足要在限制中说明；不要用消息量、加班痕迹、会议存在感或单一评价者作为绩效代理指标。

对负面反馈用“当 [行为/情境] 发生时，我观察到 [影响]；如果 [具体改变]，会更有帮助”的结构。拒绝个人攻击、歧视性内容、报复性负面评价或要求伪造证据，改写为基于事实、影响和支持请求的表达。对匿名、多方或敏感反馈，只保留必要的聚合结论和可安全披露的证据。

## 输出模板

```markdown
# [周期] [反馈类型] — [姓名/匿名]

## Summary
[1–2 句；事实与范围明确]

## Key contribution / Strength
**[项目或行为]**
- Situation/Task: ...
- Action: ...
- Result: ... (observed / derived / reported)
- Evidence scope: ...
- [NEEDS DETAIL] ...

## Growth / What could be better
[针对可观察行为、影响和具体下一步]

## Next goals / Request
[2–3 个可衡量但不虚构基线的目标或一个行动请求]

## Limits
[周期、材料、样本、匿名性和未验证事项]
```

交付时另附内部证据索引（若用户授权且安全），不要把隐私材料或完整原文直接放入提交草稿。所有指标注明来源和时间；缺乏基线就写“待补充基线”。

## 质量门禁

- [ ] 类型、对象/角色、周期、读者、格式、语气、范围和数据授权已确认。
- [ ] 证据按 STAR、来源、时间、置信度和 observed/derived/reported/unknown 分类，未编造事实或数字。
- [ ] 内容只评价可观察行为与工作影响，已处理偏差、敏感信息、匿名性和最小化原则。
- [ ] 自评/同事/向上反馈结构正确，弱证据标记 `[NEEDS DETAIL]`，负面内容可行动且非人格攻击。
- [ ] 姓名、代词、归因、数字、保密范围、字数和表单限制已由用户审阅或明确留空。
- [ ] 草稿已脱敏并保存到授权位置；没有自动发送、提交、通知或修改外部记录。

## Related Skills

- `documentation-writer` - 组织不同目的的结构化文档
- `deep-evidence-research` - 管理带来源、争议和限制的研究证据
- `user-research-synthesis` - 综合用户研究中的主题与证据
