---
name: "review-accessibility"
display_name: "无障碍审查"
display_name_en: "Accessibility Review"
description: "Review interfaces for keyboard, screen-reader, low-vision, motor, cognitive, and motion barriers."
description_zh: "审查网页和应用中的键盘、屏幕阅读器、低视力、认知与动态效果障碍，并以可复现证据报告问题。"
description_en: "Review web and app interfaces for keyboard, screen-reader, low-vision, cognitive, and motion barriers with reproducible evidence."
category: "design"
version: "0.1.0"
author: "skills contributors; adapted for WorkBuddy by SandBase AI"
---

# Review Accessibility

Find barriers that affect real user journeys, explain their impact, and propose
the smallest robust correction. Apply this Skill to source code, rendered pages,
designs, screenshots, specifications, or a combination of them.

## Establish scope

Before testing, record what is actually available:

- critical journeys and content types
- supported browsers, platforms, input modes, and viewport sizes
- the requested standard and level, such as WCAG 2.2 AA
- whether the evidence comes from code inspection, a live interface, assistive
  technology, automated checks, or static visuals

If the user does not specify a standard, use WCAG 2.2 AA as an organizing
reference, but do not imply a formal conformance audit.

## WorkBuddy review workflow

1. Map the essential journeys, including success, validation-error, empty,
   loading, timeout, and permission-denied states.
2. Inspect document language, page title, landmarks, headings, reading order,
   lists, tables, labels, instructions, errors, and status announcements.
3. Verify each control's accessible name, role, value, state, relationship, and
   programmatic description. Prefer native HTML semantics over custom ARIA.
4. Complete the journeys with keyboard alone. Check focus order and visibility,
   traps, skip paths, shortcuts, composite widgets, overlays, and focus
   restoration after dialogs or route changes.
5. Check text alternatives, captions or transcripts where applicable, color
   independence, contrast, zoom, reflow, text spacing, target size, orientation,
   reduced motion, flashing content, and time limits.
6. Use automated tooling for broad signals, then manually confirm every reported
   issue. Automated checks do not prove accessibility.
7. When a supported browser and screen reader are available, test representative
   paths with them and name the exact combination. Otherwise mark screen-reader
   behavior as unverified.

Do not trigger destructive actions, purchases, messages, or account changes
while testing. Use test data and reversible states where possible. Respect the
user's existing authenticated session and permission boundaries.

## Evidence and findings

Report only reproducible findings. For each one include:

- severity: blocker, high, medium, or low
- affected users and practical impact
- exact page, state, element, and reproduction steps
- observed behavior and expected accessible behavior
- relevant success criterion when known
- evidence source and test environment
- a focused remediation and a way to verify it

Prioritize blockers in essential journeys over raw finding count. Separate
confirmed defects from likely risks and untested areas. Do not treat a missing
automated warning as evidence that an interface passes.

## Completion boundary

End with coverage, unresolved items, and limitations. Never claim WCAG
conformance, legal compliance, or universal accessibility from a partial review.
Formal conformance claims require representative pages and states, documented
methodology, qualified human judgment, and all required success criteria.
