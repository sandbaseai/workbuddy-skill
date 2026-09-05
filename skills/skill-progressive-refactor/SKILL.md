---
name: "skill-progressive-refactor"
display_name: "Skill 渐进式重构"
display_name_en: "Skill Progressive Refactor"
description: "Use when a SKILL.md is too long or costly to load and needs a safe progressive-disclosure refactor into focused references without changing its contract."
description_zh: "用于 SKILL.md 过长或上下文成本过高时，将细节安全拆分到聚焦 references 中，同时保持原有契约不变。"
description_en: "Refactor an oversized Skill into a concise workflow core and on-demand references, preserving frontmatter, behavior, provenance, rollback, and a complete quality re-audit."
category: "development"
version: "0.1.0"
author: "dEitY719/authoring-skills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "A version-controlled Skill directory with writable files, references, and repository-native validation"
---

# Skill Progressive Refactor

Use this Skill after a quality audit identifies excessive length, duplicated
detail, or poor progressive disclosure. It changes files only within the
authorized Skill directory, preserves the original revision for rollback, and
must not silently alter the Skill's trigger, safety policy, output contract, or
frontmatter identity.

## Freeze the contract

Read the target `SKILL.md` completely and inventory its content hash, line and
character count, frontmatter, triggers, tools, commands, outputs, stopping
conditions, links, and existing `references/`. Read repository instructions
and native validators. Record the baseline and make a bounded refactor plan;
for this authorized maintenance workflow, proceed without an extra approval
round unless a scope, ownership, or destructive-action ambiguity exists.

Separate content into:

- **core control flow:** triggers, phases, decisions, safety boundaries,
  prerequisites, and output handoff; keep these in `SKILL.md`;
- **on-demand detail:** help, templates, examples, reference tables, domain
  knowledge, long checklists, and explanations; move these to single-purpose
  files under `references/`.

Do not split a sentence so that its guard, exception, or stopping condition is
left behind. Preserve exact names, stable anchors, commands, and cross-links;
never rename a colon-form name or external identifier merely to satisfy a style
preference.

## Perform the smallest safe extraction

Create or update one focused reference file per coherent topic. Each file gets
a clear heading, purpose, prerequisites, and an explicit trigger sentence in
the core. Replace extracted blocks with concise pointers such as “Read
the relevant reference file when …”. Keep references bounded and avoid creating a
second hidden router or duplicating the same rule in multiple locations.

The compact core should make the full workflow understandable quickly. A
target of 100 lines is a useful warning threshold, not permission to delete
necessary safety or contract material. Preserve tables/examples when their
structure carries meaning; compress prose only after checking that the result
still entails the original behavior.

## Validate behavior and disclosure

Run repository-native frontmatter, link, path, markdown, package, and relevant
tests. Confirm that the core is within the agreed budget, every reference is
reachable from a documented trigger, all expected outputs remain reachable,
and no old links or commands point at removed content. Inspect the diff for
lost negations, weakened authorization, changed paths, secret exposure,
accidental network/command expansion, or references loaded unconditionally.

Re-run the complete Skill quality audit, including security, license,
capability, description-length, and model/dependency checks. Compare before
and after behavior on representative trigger prompts or deterministic fixtures;
record tests not run and environment limits. If a check fails, fix the bounded
refactor or restore the affected file from the recorded revision rather than
publishing a partial split.

## Report and rollback

Return the original and final hashes, line/character counts, files created or
changed, extraction map, contract checks, test commands and exit codes,
quality-audit result, unresolved limitations, and rollback revision. Preserve
the original content in version control; do not delete history or unrelated
references. End only after the next audit command and the maintainer's next
review trigger are explicit.
