---
name: "playwright-webapp-qa"
display_name: "Playwright Web 应用验收"
display_name_en: "Playwright Web App QA"
description: "Run browser-based QA for web apps with critical user-flow validation, console and network checks, screenshots, and responsive evidence."
description_zh: "使用真实浏览器验证 Web 应用关键用户流程，并检查控制台、网络请求、截图和响应式证据。"
description_en: "Run browser-based QA for web apps with critical user-flow validation, console and network checks, screenshots, and responsive evidence."
category: "development"
version: "0.1.0"
author: "aims1425-lab; adapted for WorkBuddy by SandBase AI"
license: "MIT"
---

# Playwright Web App QA

Use this skill when a web application needs evidence that real user paths work
through the browser. It complements component-level tests by checking routing,
rendered state, browser errors, failed requests, responsive behavior, and the
handoff between UI and backend. It must use test accounts and authorized
environments only; it must not imply that a browser session was run when no
runtime or tool execution was available.

## Define the test contract

List the application URL, build or commit, browser and viewport matrix, locale,
feature flags, test data ownership, authentication method, and cleanup plan.
Prioritize user journeys by risk and impact: landing and navigation,
authentication, dashboard, core forms, uploads, settings, permissions, and
logout. For each journey specify preconditions, observable success state,
negative cases, evidence artifact, and the condition that makes the test stop.

Never use real customer accounts, production secrets, or unbounded data. Mask
tokens and personal data in traces, videos, screenshots, console output, and
reports. If the target or credentials are ambiguous, report the missing
precondition rather than probing an unintended system.

## Execute browser checks

1. Start a fresh isolated browser context with deterministic locale, timezone,
   viewport, and test data.
2. Navigate using stable, user-facing locators and wait for an observable state;
   do not make arbitrary sleeps the proof of readiness.
3. Capture uncaught console errors, failed or unexpected network requests,
   navigation failures, page exceptions, and relevant response status codes.
4. Exercise the happy path and the highest-value validation, permission,
   timeout, empty, loading, and recovery states.
5. Assert visible UI state and URL or accessibility state where appropriate;
   successful API status alone is not proof that the user saw the result.
6. Repeat critical paths at mobile and desktop viewports, including keyboard
   navigation when interaction or accessibility risk is material.
7. Save screenshots, traces, or videos only for the bounded evidence needed to
   reproduce a failure, and attach the exact test-data identity without secrets.

Keep selectors resilient: prefer roles, labels, visible text with a clear
contract, and dedicated test IDs over CSS implementation details. Distinguish
an application defect from a harness, environment, third-party, or test-data
failure. A flaky retry may help diagnose a race, but it must not turn an
intermittent failure into a pass without recording the original result.

## Verify and diagnose

For every failed path, record the first observable failure, preceding console
and network evidence, browser and viewport, reproduction rate, expected versus
actual state, and the smallest next diagnostic. Check whether an API response
was transformed, rendered, persisted, and visible to the correct user. For
uploads, verify ownership and display of the test artifact; for authentication,
verify redirect, session boundaries, logout, and unauthorized access behavior.

Do not modify production data, bypass authorization, disable security checks,
or accept a screenshot that hides a broken interaction. If a test requires an
authorized configuration change, stop at the boundary and report it explicitly.

## Report format

```text
Target / build / browser / viewport / timestamp:
Test data and authorization boundary:
Journey and preconditions:
Steps and observable assertions:
Console / network / page-error evidence:
Pass, fail, blocked, or flaky result:
Artifacts and redaction status:
Likely owner and smallest next action:
Regression coverage and retest condition:
```

The final report must separate executed evidence from assumptions and
recommendations. A green API call, a successful navigation, or one passing
retry is insufficient unless the user-visible contract and relevant negative
states were also verified.
