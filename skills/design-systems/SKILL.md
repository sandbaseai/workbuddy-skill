---
name: "design-systems"
display_name: "设计系统"
display_name_en: "Design Systems"
description: "Use when creating or evolving a component library, design tokens, patterns, or UI guidelines; establish a coherent, accessible, documented system with stable APIs, governance, adoption evidence, and controlled change."
description_zh: "用于创建和演进组件库、设计令牌、交互模式或 UI 指南，建立一致、可访问、有文档、API 稳定且可治理和验证采用度的设计系统。"
description_en: "Build and operate accessible design systems with token foundations, composable components, documented APIs, visual and interaction contracts, governance, versioning, and measurable adoption."
category: "design"
version: "0.1.0"
author: "majiayu000; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Design tokens and component tooling; web or native UI platform; documentation and visual regression workflow"
---

# Design Systems

Use this skill to create a shared language between design and engineering. A design system is more than a component folder: it combines principles, tokens, components, patterns, documentation, contribution rules, and evidence that products can adopt it without losing accessibility or product intent.

Do not standardize a component merely to reduce visual variation. Confirm the user problem, supported platforms, existing patterns, ownership, accessibility requirements, localization, theming, browser/device support, and migration cost before changing a public contract.

## Establish the system contract

Record the system’s principles, target products, supported frameworks, design/code sources of truth, owners, contribution path, release policy, deprecation window, and adoption goals. Inventory existing components and patterns before adding a new one. Prefer extending a stable primitive when semantics and states match; document intentional exceptions.

Define quality gates for every public component:

- semantic HTML or platform-native behavior and keyboard/focus support;
- accessible name, role, state, description, contrast, reduced motion, and screen-reader behavior;
- responsive layout, text scaling, localization, RTL, high-contrast, dark mode, and error/empty/loading states;
- stable API, controlled/uncontrolled behavior, event semantics, composition points, and migration path;
- unit, interaction, accessibility, visual, and integration evidence on supported environments.

## Build a token foundation

Use layers so product intent is not coupled directly to raw values:

```text
primitive values -> semantic tokens -> component tokens -> product theme
```

Primitive tokens describe scales such as color, type, spacing, size, radius, elevation, motion, and breakpoints. Semantic tokens describe roles such as `surface-default`, `text-muted`, `focus-ring`, `action-primary`, and `status-danger`. Component tokens map roles to component states. Keep names role-based rather than color-based so themes can change safely.

For each token define type, unit, allowed values, owner, intended use, contrast implications, platform mapping, and deprecation status. Validate references, cycles, naming, unused tokens, contrast pairs, and generated outputs in CI. Do not expose arbitrary escape hatches that undermine the system without documenting their risk.

## Design composable components

Use a hierarchy appropriate to the product—primitives, composed controls, complex organisms, templates, and pages—but prioritize semantic responsibility and API clarity over labels. A component contract should include:

- purpose, non-goals, when to use, and when not to use;
- anatomy, variants, sizes, states, slots, content limits, and responsive behavior;
- properties, events, controlled state, focus order, keyboard gestures, and test selectors;
- examples for common and edge cases, do/don’t guidance, and migration notes;
- accessibility behavior, localization constraints, and visual/interaction acceptance criteria.

Avoid boolean-prop explosions and mutually contradictory variants. Prefer composable slots or explicit variants when they make state combinations legible. Keep styling decisions behind tokens; do not let consumer overrides silently break focus, contrast, hit targets, or motion preferences.

## Documentation and contribution

Make documentation executable where possible: story galleries, interactive examples, generated API tables, usage snippets, accessibility notes, and visual regression fixtures should use the same components consumers receive. Include realistic long text, empty/error/loading states, keyboard flows, RTL, dark mode, and reduced-motion examples.

Define contribution stages: problem statement, existing-pattern audit, design proposal, token/API review, implementation, accessibility review, visual review, documentation, release note, and adoption follow-up. Assign decisions to named owners and record rationale. A contribution is incomplete until a consumer can discover, use, test, and upgrade the component.

## Version and migrate safely

Treat tokens, component props, CSS variables, events, and visual behavior as public contracts. Prefer additive changes. For a breaking change, publish the replacement, codemod or migration guide, compatibility period, owner, and removal criteria. Keep old and new themes/components interoperable during migration and compare screenshots and interaction behavior across representative products.

Do not accept visual drift as harmless when it changes hierarchy, status, target size, focus visibility, or meaning. Label intentional changes and verify them with product owners and accessibility users.

## Measure health and adoption

Track more than component count:

- adoption by product, route, component, and version;
- token override and escape-hatch rates;
- duplicate-pattern reduction and migration completion;
- accessibility and visual regression failures;
- API breakage, issue resolution time, build size/performance, and documentation usage;
- consumer satisfaction and time from request to safe delivery.

Use these signals to prioritize enablement and remove friction. Do not force adoption where the system cannot meet a product or platform need; document the gap and feed it into the roadmap.

## Review checklist and handoff

- User problem, scope, owner, supported platforms, and existing alternatives are explicit.
- Tokens are semantic, typed, validated, themed, and mapped without hidden overrides.
- Component API, states, semantics, accessibility, localization, and edge cases are documented.
- Story/examples, interaction tests, visual checks, and supported-environment evidence pass.
- Versioning, deprecation, migration, release notes, and rollback/compatibility plan exist.
- Adoption, exceptions, regressions, and unresolved risks have owners and review dates.

Report the decision, artifacts, checks, consumers, migration state, exceptions, evidence, and next authorized action. Stop when ownership, accessibility behavior, or a public contract is ambiguous.
