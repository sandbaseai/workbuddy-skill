---
name: playwright-component-testing
display_name: Playwright Component Testing
display_name_zh: Playwright 组件测试
description: Design, implement, migrate, and diagnose isolated React or Vue component tests with Playwright and an application-owned story gallery.
description_en: Design, implement, migrate, and diagnose isolated React or Vue component tests with Playwright and an application-owned story gallery.
description_zh: 使用 Playwright 与应用自有 Story Gallery 设计、实现、迁移和诊断隔离的 React 或 Vue 组件测试。
category: development
version: 0.1.0
author: Microsoft Corporation; adapted for WorkBuddy by SandBase AI
license: Apache-2.0
compatibility: WorkBuddy; React or Vue projects using Playwright Test
---

# Playwright Component Testing

Use this skill for isolated React or Vue component tests with ordinary Playwright tests and an application-owned story gallery. Preserve the project's framework, bundler, package manager, test conventions, and existing Playwright configuration.

## Decide whether component testing fits

Use component tests for focused UI states, event behavior, accessibility semantics, visual variants, and boundary props. Keep full navigation, authentication, multi-service journeys, and browser-policy integration in end-to-end tests. Do not duplicate the same behavior at every layer.

Before changing files, inspect the framework and version, bundler, package scripts, Playwright version and config, existing test layout, global CSS, providers, aliases, and CI commands. Confirm that the installed Playwright version exposes the required mount fixture; do not assume an API solely from the source skill.

## Build an application-owned gallery

A story is a small component wrapper for one stable scenario. A gallery page resolves a story ID, renders the story into a dedicated root, and exposes mount, update, and unmount behavior to Playwright.

- With Vite, prefer a gallery HTML entry inside the project so existing plugins, aliases, transforms, and CSS apply.
- With another bundler, use the application's supported development entry or a deliberately small standalone server. Avoid introducing a second build system unless necessary.
- Keep framework-specific mounting code in the gallery rather than the tests.
- Import production providers and global styles explicitly. Mock only the boundary the case intends to control.
- Make unknown story IDs fail loudly with actionable context.

Each named story should express one reviewable state. Derive stable IDs from paths and export names, and namespace them in monorepos. Prefer a new named story over a large parameter matrix; use serializable props only for genuine boundary sweeps.

## Configure without replacing existing behavior

Merge a component project into the current Playwright configuration. Give it a dedicated test directory and base URL. Reuse the existing web server when it can serve the gallery; otherwise add a bounded gallery server with a readiness URL and deterministic port.

Block service workers when they could bypass Playwright route mocks. Reuse browser contexts only when state is reset between tests and the performance gain is measured. Preserve existing reporters, retries, timeouts, output paths, projects, and CI settings unless evidence requires a change.

## Write observable tests

Mount one story and scope locators to the returned component root. Prefer role, label, text, and test-ID locators over CSS structure. Use Playwright's retrying assertions instead of sleeps or manual polling.

Keep callbacks and mutable state inside the story. Expose observable results in the DOM so a test can prove what happened without callback marshalling or private implementation access. Assert URLs and network effects through public browser behavior.

Register network routes before mounting because mounting may navigate. Keep fixtures deterministic, validate request method and payload where relevant, and fail unexpected requests. Screenshot the component root rather than the whole page; fix fonts, animations, time, locale, color scheme, and viewport when they materially affect pixels.

For prop transitions, update the mounted story without remounting only when the test specifically covers state preservation. Otherwise use a fresh mount so cases remain isolated.

## Preserve isolation

Every test must be runnable alone, in random order, and in parallel unless explicitly marked otherwise. Reset storage, fake servers, timers, singleton stores, and module-level state. Do not share mutable page state across tests. If context reuse is enabled, add evidence that isolation still holds.

Exercise key stories across relevant browser engines, themes, locales, and responsive sizes without multiplying low-value combinations. Separate deterministic release gates from broad exploratory matrices.

## Migrate incrementally

When replacing an experimental component-test runtime:

1. inventory fixtures, hooks, stories, providers, route mocks, screenshots, and CI commands;
2. establish the gallery and one representative test;
3. prove local and CI execution before migrating the next slice;
4. compare coverage and artifacts, not just test counts;
5. remove old dependencies and configuration only after no callers remain.

Keep commits reversible. Do not mass-rewrite snapshots until the rendering environment is pinned and reviewed.

## Diagnose failures from evidence

Classify the earliest broken boundary:

1. gallery server or readiness;
2. story discovery or module transform;
3. provider, CSS, alias, or asset loading;
4. mount/update/unmount lifecycle;
5. locator ambiguity or accessibility regression;
6. application behavior or network contract;
7. visual environment instability;
8. worker isolation, order dependence, or CI resources.

Retain the Playwright trace, screenshot, video, console output, network evidence, and exact command when useful. Reproduce with the failing project and case first, then rerun the affected suite and parallel CI-shaped command. Never fix a race with an arbitrary timeout.

## Deliverable

Report the tested component contract, story and gallery design, configuration changes, cases added or migrated, exact commands, browser matrix, artifacts, isolation evidence, known gaps, and any old runtime files that are now safe to remove.
