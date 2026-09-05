---
name: "github-release"
display_name: "GitHub 发布编排"
display_name_en: "GitHub Release"
description: "Use when planning or executing a GitHub release: inspect changes since the last tag, determine SemVer, update a Keep a Changelog entry, run gates, publish tags/assets, and verify rollback and provenance."
description_zh: "用于规划或执行 GitHub 发布：审计上个标签以来的变更、确定 SemVer、更新 Keep a Changelog、运行门禁、发布标签/资产并核验回滚与来源。"
description_en: "Reconcile immutable diffs and intent, choose a justified version, prepare user-facing release notes, validate artifacts, and complete an authorized PR or direct-release path without claiming unverified success."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with git, GitHub CLI, repository release workflows, and an authorized publication path; protected branches, approvals, credentials, and external notifications remain subject to repository policy"
---

# GitHub Release

## Purpose and boundary

Coordinate a reproducible GitHub release from change evidence to published assets. The workflow
supports SemVer, Keep a Changelog, tags, release notes, package/asset verification, and rollback
evidence. It does not make a release merely because a commit message says “release,” and it must
not rewrite history, bypass branch protection, expose credentials, or publish artifacts from an
unclean or unverified tree.

Use one of two explicit modes:

- **PR mode:** create a release branch and PR when repository policy requires review;
- **direct mode:** commit/tag/publish on the protected release path only when the caller has already
  authorized direct automation and branch policy permits it.

Do not infer authorization from a request to “prepare” a release. If authority, target branch,
version, or publication destination is unknown, produce a plan/report and state the gap.

## Step 1: preflight the repository

Verify:

```bash
gh auth status
gh repo view --json nameWithOwner,defaultBranchRef
git status --short --branch
git fetch --tags --prune
```

Require a clean worktree, the intended repository, and a known default branch before writing.
Record repository, revision, actor, current branch, workflow files, package/build metadata,
protected checks, artifact naming, and release workflow behavior. Do not change branches or pull
over uncommitted user work without a safe, authorized boundary.

## Step 2: establish the previous release

Read tags directly because a GitHub Release may be absent even when a tag exists:

```bash
git tag --sort=-version:refname
git ls-remote --tags origin
```

Choose the newest valid SemVer tag that exists on the remote. If there is no tag, use the first
release convention documented by the repository and label the baseline accordingly. Verify that
the tag resolves to a commit and record `previous_tag` and `previous_sha`; never compare against
an unpushed local-only tag without reporting it.

## Step 3: classify the change from evidence

Inspect the complete diff and non-merge commit log between `previous_sha` and `HEAD`. Focus on
public interfaces, exported symbols, CLI flags, schemas, configuration, migrations, workflows,
asset names, and user-visible behavior. Use commit messages as context, not as proof.

| Evidence | SemVer signal |
|---|---|
| removed/renamed public API, incompatible schema/behavior, breaking CLI change | MAJOR |
| new public API, feature, compatible capability, user-visible addition | MINOR |
| backward-compatible bug/security/performance fix, docs or internal change | PATCH |

When code diff and commit message conflict, prefer the diff and record the conflict. Check changes
outside the primary source directory that still affect consumers, packaging, CI, migrations,
configuration, or release behavior. Do not classify unverified speculation as a breaking change.

## Step 4: choose and explain the version

Start from the previous `MAJOR.MINOR.PATCH`, apply the highest supported change level, and preserve
the repository's `v` prefix convention. Confirm the tag does not already exist locally or remotely.
Record:

```text
Previous tag/SHA: <...>
Next version: <vX.Y.Z>
Highest signal: major | minor | patch
Evidence: <files, symbols, behavior, commits>
Conflicts/uncertainty: <...>
```

If the caller has authorized unattended release, continue with the selected version and retain
the rationale in the release record. Otherwise stop at a proposed version and request the owner’s
decision; never silently choose a materially different version.

## Step 5: prepare release notes

Read the existing `CHANGELOG.md` and follow its conventions. For Keep a Changelog repositories,
add a dated version section with only relevant headings: Added, Changed, Deprecated, Removed,
Fixed, and Security. Write from the user's perspective, tie entries to the verified diff, and
avoid exposing internal credentials, private issue text, or unsupported claims. Include a compare
link to the previous tag when the repository uses one.

The release notes must state notable limitations, migrations, compatibility changes, security
implications, and required operator actions. Keep an Unreleased section coherent; do not delete
unreleased entries that are not part of this release.

## Step 6: run release gates

Run repository-native validation before committing release metadata. At minimum inspect:

- format/lint/type/test/build and migration/schema checks;
- package or archive contents, version consistency, checksums/signatures where required;
- documentation links, changelog format, generated files, and artifact names;
- workflow status/check conclusions and required branch protections;
- clean diff containing only intended release changes.

For a catalog or multi-asset project, verify the count and identity of every expected asset, not
just that a release page exists. Preserve command, revision, environment, duration, exit status,
and safe output. If a gate is unavailable, classify the release as partial/blocked for that gate.

## Step 7: publish through the authorized path

In PR mode, create a release branch, commit only the release metadata, open the PR with a body
file, and wait for required checks. Merge only when repository policy and the caller’s authority
allow it. In direct mode, commit the prepared release metadata to the authorized branch, wait for
the branch workflows, then create and push the immutable tag. Never force-push or delete a tag to
repair a mistake; use a corrective release or a documented recovery path.

After tag publication, wait for release workflows to finish. Do not call a release complete while
validation or packaging is still running. If a workflow fails, preserve the failed run ID and
diagnosis; do not rerun indefinitely or publish around a required failure.

## Step 8: verify the published release

Check:

```bash
gh release view <tag> --json tagName,isDraft,isPrerelease,assets
git ls-remote --tags origin <tag>
git status --short --branch
gh pr list --state open
```

Reconcile tag SHA, release state, asset count/names/checksums, source commit, changelog, and
download links. Verify expected packages can be found and that no unrelated asset or branch was
created. Record deployment/site publication status separately from GitHub Release status.

## Rollback and handoff

Define rollback before publication: stop/disable a failed workflow, revert a release metadata
commit with a new commit, mark a release deprecated if needed, and issue a corrective version.
Do not erase public history. For every migration or incompatible change, link the operator action,
compatibility window, recovery evidence, and owner.

Return:

```text
Release: <repository/tag/SHA/date>
Mode/authority: PR | direct | report-only; <authorization evidence>
Baseline/diff: <previous tag, files, SemVer rationale>
Notes: <changelog path and compare link>
Gates: <commands/results/unavailable checks>
Publication: <branch/PR/tag/release/workflows>
Assets: <expected versus observed names/counts/checksums>
Rollback: <recovery path and owner>
Residual risk: <unknowns, failed/partial evidence, next review>
```

A release is complete only when the tag, source commit, release page, assets, checks, notes, and
handoff agree. A successful API call alone is not release proof.

