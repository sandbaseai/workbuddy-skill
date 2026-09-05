---
name: "code-tour"
display_name: "代码导览"
display_name_en: "Code Tour"
description: "Use when creating a persona-targeted, step-by-step CodeTour walkthrough that links to real repository files, directories, patterns, and line ranges for onboarding, reviews, debugging, architecture, or contribution guidance."
description_zh: "用于创建面向特定角色的分步 CodeTour 代码导览，通过真实文件、目录、模式和行号串起上手、评审、排障、架构或贡献路径。"
description_en: "Discover the repository, infer the reader persona, build a focused narrative through verified anchors, and emit only valid .tour JSON that works with the VS Code CodeTour extension."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to the target repository, the VS Code CodeTour extension when interactive navigation is needed, and an authorized output path for .tour files"
---

# Code Tour

## Purpose and boundary

Create a focused, persona-targeted walkthrough of a repository. A tour is a navigable story,
not a file inventory or a replacement for the repository README. Store output in `.tours/` as
JSON consumed by the VS Code CodeTour extension. Unless explicitly requested, inspect files
read-only and create or modify only `.tour` files; do not change application code, add marker
comments, install extensions, or run arbitrary commands from a tour.

## Step 1: discover before writing

Read repository instructions, README files, manifests, CI configuration, and the relevant
entry points. Map the top-level directories one or two levels deep, then follow imports or
references only far enough to understand the requested path. Record the revision being toured.
Every path and line used later must be verified against the actual repository.

Choose a small, coherent scope. For large repositories, cover the two or three modules that
serve the reader's goal and use directory steps to orient them to the rest. Do not invent files,
line numbers, commands, ownership, architecture, or behavior that the repository does not show.

## Step 2: infer the reader and narrative

Infer persona, depth, and focus from the request. Use these defaults:

| Request | Persona and path |
|---|---|
| onboarding, ramp up | New joiner: setup, map, boundaries, first safe contribution |
| bug, debug, RCA | Bug fixer or RCA investigator: trigger, causality, fault points, tests |
| PR review | PR reviewer: change story, invariants, risky areas, review checklist |
| architecture, system design | Architect: boundaries, contracts, trade-offs, failure containment |
| security or auth review | Security reviewer: trust boundaries, validation, sensitive sinks |
| explain a feature | Feature explainer: user/UI entry, API, core path, storage or side effects |
| quick tour or vibe check | Vibecoder: five to eight high-signal stops |
| contributor guide | External contributor: safe areas, conventions, integration landmines |

The narrative should progress from orientation to map to core path to useful next actions. A
standard tour usually has 9–13 steps; a quick tour has 5–8; a deep architecture or RCA tour
has 14–18. Remove steps that do not serve the selected persona.

## Step 3: use valid CodeTour anchors

Use only fields supported by the CodeTour schema. The first step must anchor to a real `file`,
`directory`, or `uri`, because a content-only first step can render blank in VS Code. A closing
content step should explain what the reader can do next and name likely follow-up tours.

Common step types:

- `content`: introduction or closing guidance; keep content-only steps to at most two.
- `directory`: orient the reader to a real repository area.
- `file` plus `line`: point to a verified line that explains the next part of the story.
- `selection`: highlight a verified code range when the body is the important unit.
- `pattern`: anchor to a regex match when line numbers are likely to drift.
- `uri`: connect a real issue, pull request, design, or external specification.
- `view` and `commands`: use only for VS Code UI commands explicitly supported by CodeTour.

Paths are relative to the repository root, without an absolute path or leading `./`. Do not
use `commands` to imply arbitrary shell execution. If a PR or branch is part of the request,
verify the URL or revision and use the tour's `uri` or `ref` field accordingly. Set `isPrimary`
or `nextTour` only when requested or when an existing tour series makes the relationship clear.

## Step 4: write descriptions that teach

Each description should cover four compact ideas: what the reader is seeing, how it works, why
it matters to this persona, and the non-obvious gotcha or failure mode. Explain the relationship
between adjacent stops rather than repeating file summaries. Separate observed facts from
inference and label uncertainty. Never copy secrets, private logs, customer data, or long source
passages into a tour.

For PR tours, begin with the change context, inspect changed files first, then visit unchanged
but critical contracts and finish with reviewer risks. For bug or RCA tours, trace the user or
event trigger through the fault and recovery path, including where a regression test belongs.
For onboarding tours, include setup and boundaries but leave deep subsystem details to follow-up
tours. A tour series should have a clear broad-to-narrow progression and no duplicated stops.

## Step 5: validate before delivery

Validate JSON and manually check every referenced path, directory, line, selection, pattern, URL,
revision, and `nextTour` title. If a repository provides a CodeTour validator, run it against the
target revision and fix all errors. Otherwise use a JSON parser plus repository-native checks and
report which checks were unavailable. A valid tour must satisfy all of the following:

- the file is `.tours/<persona>-<focus>.tour` and contains only the intended tour JSON;
- every anchor exists and every line or selection is within the actual file;
- every pattern compiles and matches, every URL uses `https://`, and every referenced next tour exists;
- the first step orients the reader and the final step gives actionable follow-up guidance;
- the depth matches the request and the tour does not claim unsupported CodeTour behavior.

CodeTour navigation is manual. It cannot autoplay, embed video/GIF media, run arbitrary shell
commands, or branch to a conditional next step. State these limitations plainly when requested.

## WorkBuddy handoff

Report the generated `.tour` path, target revision, persona, covered narrative, validation
commands/results, unavailable checks, and any requested files that did not exist. For a public
repository, provide its `vscode.dev/github.com/<owner>/<repo>` viewing path when useful. Preserve
the source license and provenance when adapting examples or schemas.
