---
name: "frontend-review"
display_name: "前端变更审查"
display_name_en: "Frontend Review"
description: "Use when reviewing frontend changes for interaction correctness, responsive behavior, accessibility, performance, state handling, and browser-facing regressions."
description_zh: "用于审查前端变更中的交互正确性、响应式行为、无障碍、性能、状态处理和浏览器回归。"
description_en: "Perform a diff-first frontend review with implementation and runtime evidence; inspect states, responsive boundaries, accessibility, performance, errors, and browser compatibility; and report prioritized findings with reproducible checks."
category: "development"
version: "0.1.0"
author: "aydabd/github-bootstrap; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authorized frontend repository, change diff, component and route context, supported browsers/devices, repository-native checks, and approved fixtures or test accounts"
---

# Frontend Review

Review user-facing frontend changes for correctness and durable usability. Start with the diff and affected component or route, then verify important states with repository-native tests or a bounded browser check when available. Do not treat visual preference as a defect, claim browser coverage that was not tested, or submit real data without authorization.

## Establish the surface

Identify changed components, routes, forms, navigation, data loaders, state stores, styles, assets, browser support, input modes, localization, and API contracts. Enumerate initial, loading, empty, success, error, offline, unauthorized, disabled, long-content, slow-network, and repeated-action states relevant to the change. Inspect existing tests, design tokens, accessibility requirements, performance budgets, and feature-flag behavior. Record unavailable browsers, devices, APIs, and fixtures as limitations.

## Review behavior and resilience

Check:

- interaction states, event handlers, keyboard and pointer paths, focus placement, cancellation, repeat clicks, optimistic updates, retries, and stale responses;
- loading, empty, partial, error, timeout, offline, permission, and recovery states with useful user feedback and no leaked internals;
- form labels, validation, error association, semantics, headings, landmarks, ARIA, focus visibility, screen-reader announcements, contrast, zoom, reflow, reduced motion, and non-color cues;
- responsive breakpoints, overflow, text expansion, localization, right-to-left or locale-sensitive formats, touch targets, orientation, and supported browsers;
- API/data contracts, null and unexpected values, caching, hydration, race conditions, serialization, authentication expiry, and safe fallback behavior;
- bundle and rendering cost, image/font loading, layout shift, long lists, unnecessary requests, memory cleanup, and performance budget impact;
- security boundaries including output encoding, unsafe HTML/URLs, sensitive data in markup or storage, clickjacking-sensitive flows, and permission-dependent UI that is not the server's authorization control.

Prefer exact evidence from changed code, component tests, accessibility trees, keyboard checks, visual or responsive snapshots, network traces, performance profiles, and browser console output. Use synthetic or redacted data. Record command/tool version, viewport/device, browser, network conditions, test identity, route, state, and limitations. A passing snapshot or automated accessibility scan covers only the exercised state.

## Classify findings

Separate confirmed regression, likely risk, observation, and unknown. For each material finding record severity and rationale, route/component/state, input mode or viewport, expected and observed behavior, concrete evidence, affected users or contract, safe fix, and regression-test idea. Prioritize task blockers, data loss or duplicate submission, inaccessible controls or missing information, security exposure, broken responsive layouts, and severe performance regressions. Avoid style-only comments unless they cause a concrete usability, correctness, accessibility, security, or maintenance problem.

Use the repository's required finding format when one exists; otherwise use concise Markdown or JSONL. Do not include credentials, personal data, or unnecessary exploit details. Report environment or provider failures separately from product findings and do not hide them with retries.

## Handoff and retest

Recommend the smallest durable fix and define acceptance criteria across affected states, input modes, viewports, browsers, and assistive technology. Re-test the changed path and adjacent states, then run the required lint, typecheck, unit, component, visual, and end-to-end checks. The final handoff includes scope, evidence matrix, findings, tested environments, skipped checks, performance/accessibility limitations, owner, rollout or flag considerations, and the exact next review gate.
