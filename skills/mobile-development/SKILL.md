---
name: "mobile-development"
display_name: "移动应用开发"
display_name_en: "Mobile Development"
description: "Use when building or reviewing iOS, Android, React Native, Flutter, SwiftUI, or Jetpack Compose applications; choose architecture and platform boundaries while designing for unreliable networks, battery, memory, accessibility, security, testing, and staged release."
description_zh: "用于构建和审查 iOS、Android、React Native、Flutter、SwiftUI 或 Jetpack Compose 应用，在不可靠网络、续航、内存、无障碍、安全、测试和分阶段发布约束下选择架构和平台边界。"
description_en: "Build production mobile apps with explicit platform trade-offs, offline-first behavior, performance budgets, secure storage, accessible UI, real-device testing, and staged delivery."
category: "development"
version: "0.1.0"
author: "majiayu000; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "iOS or Android SDK; React Native, Flutter, SwiftUI, or Jetpack Compose; real-device and CI testing"
---

# Mobile Development

Use this skill for mobile architecture, UX, performance, offline behavior, platform APIs, testing, security, accessibility, and store delivery. Start with users, devices, connectivity, battery, data sensitivity, and release constraints; framework choice follows those facts.

Do not promise identical behavior across platforms without testing it. Do not store secrets in app bundles, trust client-side authorization, or declare an app ready from simulator-only testing. Confirm supported OS versions, device classes, SDK/toolchain versions, store rules, privacy requirements, and crash/rollback strategy.

## Choose the platform boundary

- **React Native:** useful when JavaScript/TypeScript and web sharing matter; isolate native capabilities behind small, tested modules.
- **Flutter:** useful for a controlled cross-platform UI and custom rendering; verify platform semantics and accessibility rather than assuming widget parity.
- **Swift/SwiftUI:** best when deep Apple integration, platform features, or maximum iOS control dominate.
- **Kotlin/Jetpack Compose:** best when Android platform integration, Material behavior, and Android-specific control dominate.

Document the decision, native escape hatches, team expertise, build/release complexity, performance risks, and migration cost. Keep domain logic platform-independent where it improves testability, but let navigation, permissions, lifecycle, typography, gestures, and system UI follow platform conventions.

## Design for real mobile conditions

Treat the network as intermittent, slow, reordered, and metered. Define loading, empty, stale, retry, conflict, cancellation, and offline states for every important flow. Use a local source of truth where appropriate, queue idempotent mutations, attach operation IDs, resolve conflicts explicitly, and show users what has or has not synchronized.

Set budgets before implementation and measure on representative low-end and high-end devices:

- time to interactive and screen transition latency;
- frame pacing and dropped frames during scroll/animation;
- memory high-water mark, image sizes, and crash/OOM rate;
- network bytes, request count, cache hit rate, and retry behavior;
- background work, wakeups, location use, and battery impact;
- binary/download size and startup behavior after upgrade.

Optimize from traces and user-impact evidence. Prefer pagination, bounded caches, compressed/resized media, lazy work, cancellation, and batched requests. Do not trade correctness, accessibility, or battery for an unmeasured micro-optimization.

## Architecture and state

Separate presentation, domain decisions, data access, and platform adapters. Make loading/error/empty/success states explicit and model lifecycle transitions such as backgrounding, process death, rotation, permission change, token expiry, and interrupted uploads. Persist only what is needed and version local storage migrations.

For authentication, use the platform secure store (Keychain/Keystore or an approved abstraction), short-lived tokens, refresh/revocation handling, and server-side authorization. Bind sensitive operations to the current user and tenant; never trust a client-supplied role or object identifier without server checks. Minimize telemetry and redact personal data, tokens, and free-form text.

## UI, accessibility, and localization

Follow the platform’s navigation, back behavior, safe areas, system bars, text scaling, keyboard, haptics, and permission conventions. Design touch targets and focus order for assistive technology. Provide labels, roles, state announcements, contrast, reduced motion, dynamic type, and a non-color-only signal.

Test long text, right-to-left layouts, locale/date/number/currency formats, dark mode, font scaling, small screens, large screens, notches, keyboards, and interrupted permission prompts. Accessibility is a release requirement, not a polish pass.

## Testing strategy

Use a layered test matrix:

- unit tests for domain rules, reducers, parsers, migrations, and sync conflict decisions;
- integration tests for storage, networking, authentication, deep links, push notifications, and permission boundaries;
- UI/E2E tests for critical journeys, offline/reconnect, background/restore, upgrade, and destructive-action confirmation;
- accessibility, localization, performance, battery, security, and real-device checks.

Control time, network, randomness, feature flags, and test data. Test duplicate delivery, stale responses, process death, clock skew, revoked credentials, partial uploads, and schema upgrades. Keep a small smoke suite on every change and a broader device matrix before release; attach logs, screenshots, traces, device/OS, build, and reproduction steps to failures.

## Secure staged delivery

Protect signing keys and provisioning credentials in an approved secret system with rotation and access audit. Generate reproducible builds, verify dependencies, scan manifests and permissions, and review SDK/vendor data collection. Use internal, closed/beta, staged, and production channels with explicit expansion criteria, crash/ANR/error guardrails, owner, rollback or kill-switch plan, and privacy-policy synchronization.

Before submission, verify package identity, signing, entitlements/permissions, deep links, privacy declarations, store metadata, localization, billing rules, support contact, and recovery after an interrupted upgrade. A green build is not evidence that users can recover from offline, revoked, or partially migrated states.

## Handoff

Report framework and SDK versions, supported devices/OS, architecture decision, offline and lifecycle model, permissions and data flows, budgets and measurements, tests and device matrix, known limitations, rollout gates, monitoring, rollback/kill switch, and next authorized action. Stop when a platform assumption, data boundary, signing authority, or release criterion is unclear.
