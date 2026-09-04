---
name: "browser-automation"
display_name: "浏览器自动化"
display_name_en: "Browser Automation"
description: "Use when a task requires navigating websites, filling forms, extracting structured page data, capturing screenshots or PDFs, or validating an end-to-end browser flow; use explicit selectors, bounded waits, and user-approved destinations."
description_zh: "用于网站导航、表单填写、结构化页面采集、截图/PDF 和端到端浏览器流程验证；使用明确选择器、有界等待和用户批准的目标。"
description_en: "Automate browser navigation, forms, extraction, screenshots, PDFs, and end-to-end flows with explicit selectors, bounded waits, and safe data handling."
category: "automation"
version: "1.0.0"
author: "Claude Office Skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Requires a browser automation client such as Playwright or Puppeteer; network access may be required for remote pages."
---

# Browser Automation

Use a real browser client to complete a concrete, authorized task. Before acting, identify the target origin, intended outcome, authentication state, data sensitivity, and whether the action is read-only or changes external state. Never infer permission to access private sites, bypass controls, or submit irreversible changes.

## Plan the flow

1. Confirm the exact URL or application origin and the user-visible goal.
2. Check the available browser client and its version; prefer the repository's existing tool and conventions.
3. Open the page and capture a fresh DOM snapshot or accessibility tree.
4. Use stable semantic selectors, labels, roles, or test IDs. Avoid coordinates and brittle generated classes.
5. After navigation, modal changes, tab switches, or significant DOM updates, capture a new snapshot before using element references.
6. Bound navigation, selector, download, and retry waits; stop and report the failing stage when a bound expires.

## Interact safely

Prefer `goto`, snapshot, inspect, interact, and snapshot again. For forms, verify field labels, destination, and visible validation before submitting. Treat file uploads, purchases, account changes, deletion, publication, messages, and permission changes as external side effects: preview the exact payload and obtain explicit user authorization immediately before the irreversible action.

Never expose passwords, session cookies, API keys, authorization codes, or personal data in logs, screenshots, traces, URLs, or generated artifacts. Use synthetic accounts and redacted fixtures for testing. Do not disable TLS, origin checks, certificate validation, or anti-CSRF controls to make a flow pass.

## Extract data

Define the output schema before scraping. Extract only the requested fields, preserve source URLs and timestamps, normalize types deterministically, and record missing values rather than guessing. Respect robots, terms, access controls, rate limits, pagination bounds, and reasonable request pacing. Stop when the maximum page/item/time budget is reached.

For tables or repeated cards, validate a sample against the page before collecting all rows. Deduplicate by a stable source identifier when available. Do not collect unrelated navigation, hidden fields, or data belonging to other users.

## Capture and test

Capture screenshots, PDFs, or traces only when useful for the task. Store artifacts in the repository's designated output directory and redact sensitive content before sharing. For an end-to-end test, state the preconditions, perform one deterministic flow, assert the expected URL/role/text/state, and test a representative denied or invalid path without weakening production safeguards.

When a selector fails, snapshot again and diagnose whether the page navigated, the element is inside a frame, a consent dialog changed the DOM, or the application returned an error. Do not repeatedly retry a side effect without proving whether the first attempt succeeded.

## Report

Return the target origin, flow stages, actions taken, extracted schema and counts, artifacts, assertions, warnings, and any blocked or unverified step. Distinguish observed page content from inferred meaning, and state clearly when authentication, permissions, rate limits, or missing selectors prevented completion.
