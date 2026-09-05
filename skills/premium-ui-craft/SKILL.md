---
name: "premium-ui-craft"
display_name: "高质量界面设计"
display_name_en: "Premium UI Craft"
description: "Use when designing or refining product interfaces, dashboards, forms, navigation, or component states; make hierarchy, interaction, accessibility, and motion intentional without defaulting to a template."
description_zh: "用于设计或优化产品界面、仪表盘、表单、导航和组件状态，建立清晰层级、可靠交互、无障碍和克制动效，避免模板化设计。"
description_en: "Design and refine product UI with deliberate hierarchy, semantic tokens, complete interaction states, responsive navigation, accessibility, and restrained motion; verify the result with concrete evidence."
category: "design"
version: "0.1.0"
author: "kleosr/kleosrules; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Web or native product interface with an established component/token system or an explicitly documented replacement"
---

# Premium UI Craft

Use this skill when an interface needs to feel deliberate, calm, and product-specific rather than assembled from generic cards and badges. Start from the user's primary job and the existing product language. Do not impose an aesthetic, palette, typography, or navigation pattern without evidence from the brief, repository, platform, and audience.

## Establish the design contract

Before changing markup, styles, or components, record the primary user task, existing type/color/spacing/motion tokens, target viewports and input modes, supported browsers and themes, localization/RTL needs, existing primitives, intentional exceptions, and measurable acceptance criteria.

Prefer one coherent visual language. Color should communicate role—action, status, danger, or selection—not decorate every section. Use semantic tokens such as `surface`, `text-muted`, `focus-ring`, and `action-primary` instead of hard-coded color names. Typography should establish hierarchy through a small, consistent scale and readable measure.

## Design the information hierarchy

Give every screen one primary job. Make the title, context, and primary action understandable before adding chrome. Compose pages from meaningful structure—header, filters, list, detail, or empty state—rather than a pile of identical cards. Use real, human-readable labels and dates where they improve comprehension; expose IDs and technical values only where the task requires them.

Keep visual density intentional:

- reserve the strongest contrast and accent for the current task and its result;
- use spacing and subtle dividers to group content before adding containers or badges;
- make full-row entities and clear labels the hit target when users navigate lists;
- keep secondary actions discoverable without competing with the primary action;
- preserve hierarchy when text becomes longer, translated, zoomed, or empty.

## Specify every interaction state

For each control and content surface, define default, hover, focus-visible, active, disabled, loading, success, empty, error, and permission states that apply. State changes must be understandable without color alone and must not expose stack traces, internal IDs, or ambiguous error copy.

Check keyboard order, pointer and touch behavior, repeat clicks, cancellation, optimistic updates, stale responses, retry behavior, and focus placement after dialogs, navigation, validation, and asynchronous updates. Follow the repository's accessibility constraints and make touch targets comfortably usable.

## Treat navigation and responsive layout as behavior

Choose a persistent rail, top navigation, tab bar, or compact mobile navigation from destination count, task frequency, viewport, and platform convention. Define breakpoint behavior, safe-area padding, overflow policy, focus order, active indication, and back/forward semantics. Test narrow, wide, zoomed, long-content, and localized layouts. Verify that content is not clipped, fixed elements do not cover tasks, tables have an intentional overflow strategy, and dialogs remain usable.

Include dark/high-contrast themes and reduced-motion behavior when supported. Motion should explain continuity, hierarchy, or feedback. Use a small family of durations and easing curves, animate transforms and opacity where practical, and remove non-essential transitions under `prefers-reduced-motion` while preserving state feedback.

## Verify with evidence

Use repository-native component, accessibility, visual, type, lint, and end-to-end checks. When a browser check is available, capture route, viewport/device, browser, input mode, theme, data state, and console/network limitations. Exercise representative default, loading, empty, error, permission, long-text, keyboard, and reduced-motion paths; a single screenshot or automated scan proves only the state it covered.

Before handoff, confirm:

- the primary task and action are obvious without decorative noise;
- tokens, contrast, focus, semantics, labels, and non-color state cues are sound;
- responsive, localization, zoom, theme, keyboard, touch, and reduced-motion behavior are intentional;
- loading, empty, error, disabled, unauthorized, and recovery copy is designed;
- performance, layout shift, long lists, asset loading, and request behavior stay within project budgets;
- changed states have reproducible evidence and known gaps are recorded.

Return the design decision, affected surfaces, states checked, evidence, exceptions, unresolved risks, and exact next review gate. Stop when the primary user task, platform support, or accessibility contract is ambiguous.
