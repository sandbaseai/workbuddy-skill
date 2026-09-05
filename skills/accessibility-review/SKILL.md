---
name: "accessibility-review"
display_name: "无障碍审查"
display_name_en: "Accessibility Review"
description: "Use when reviewing a web interface or interaction for semantic, keyboard, focus, screen-reader, ARIA, and contrast accessibility risks."
description_zh: "用于审查网页界面和交互中的语义、键盘、焦点、屏幕阅读器、ARIA 与对比度无障碍风险。"
description_en: "Perform an evidence-first accessibility review of changed or in-scope UI, prioritizing user-blocking barriers, verifying behavior with repository-native tools, and reporting actionable findings without treating style preferences as defects."
category: "development"
version: "0.1.0"
author: "aydabd/cacad; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized repository, changed UI or explicitly scoped pages, browser/device checks when available, and repository-native test tooling"
---

# Accessibility Review

Review an interface for barriers that prevent or degrade use by people with disabilities. Work from observable evidence and the declared scope. Do not claim WCAG conformance from a checklist alone, and do not treat visual taste or unverified assumptions as accessibility defects.

## Establish scope and safety

Identify the changed components, routes, states, supported browsers and input modes, and any applicable product or regulatory requirements. Prefer local fixtures, test accounts, and redacted data. Do not submit forms, alter user data, or exercise privileged flows without authorization. Record unavailable environments and untested states as limitations.

## Inspect the implementation

Start with the diff and the component's surrounding markup, styles, state transitions, and tests. Check:

- semantic elements, heading order, landmarks, labels, names, descriptions, and form errors;
- keyboard reachability, logical order, visible focus, escape behavior, and absence of keyboard traps;
- focus placement after dialogs, navigation, validation, loading, and conditional content changes;
- correct ARIA roles, states, properties, relationships, and native-control preference;
- screen-reader announcements for status, errors, live updates, and dynamic content;
- text and non-text contrast, resizing, reflow, reduced motion, touch targets, and zoom;
- alternative text, captions, transcripts, meaningful link text, and non-color cues;
- timing, autoplay, drag-only interaction, pointer cancellation, and error recovery.

Use repository-native linters, unit tests, browser automation, accessibility trees, and manual keyboard checks when available. For every command or tool, record its target, version, result, and limitations. A passing automated scan is evidence about the tested surface, not proof that all user journeys are accessible.

## Validate and classify findings

Reproduce each material finding with the smallest safe check and capture the affected route, component, state, input mode, expected behavior, observed behavior, and evidence location. Separate confirmed barriers from possible issues and unknowns. Prioritize blockers that prevent task completion, then severe loss of information or control, then broader usability risks. Avoid style-only comments unless they create a concrete accessibility or maintenance risk.

For each finding, provide a stable identifier, severity and rationale, affected users or task, exact evidence, a standards reference when confidently applicable, a suggested fix, and a regression test idea. Do not include personal data, credentials, or unnecessary exploit-like details. Use the repository's required finding format when one exists; otherwise use concise Markdown or JSONL with one finding per record.

## Remediate and hand off

Prefer native semantics and the smallest durable fix. Define acceptance criteria for keyboard, focus, announcements, zoom/reflow, contrast, and assistive-technology behavior as relevant. Re-test the repaired state and its adjacent states, document remaining limitations, and assign an owner and follow-up trigger. The final report includes scope, methods, tested paths and modes, findings, evidence, fixes or exceptions, retest status, and the next safe action.
