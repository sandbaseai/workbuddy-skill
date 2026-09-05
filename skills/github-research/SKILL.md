---
name: "github-research"
display_name: "GitHub 资料研究"
display_name_en: "GitHub Research"
description: "Use when research requires GitHub repositories, source files, specifications, examples, issues, releases, or configuration patterns; choose the right search surface and preserve reproducible source evidence."
description_zh: "当研究需要查找 GitHub 仓库、源文件、规范、示例、Issue、Release 或配置模式时使用，选择合适的搜索面并保留可复现的来源证据。"
description_en: "Research GitHub intelligently across repository, code, issue, commit, and API surfaces; rank candidates by maintenance, license, relevance, and evidence quality while respecting limits and privacy."
category: "research"
version: "0.1.0"
author: "ever-just/agentskills; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Authenticated GitHub access when available, bounded research scope, and permission to read public or authorized repositories"
---

# GitHub Research

Use this skill when GitHub is the research surface rather than merely a place to download a known file. Start with the question and evidence needed, then choose repository search, code search, issue/PR search, commit history, REST contents, GraphQL, or direct file reads. Do not treat a search result, README claim, star count, or generated index as proof until the relevant source is opened and its date, branch, license, and context are checked.

## Define the research contract

Record the topic, inclusion/exclusion criteria, target date, public/authorized scope, desired artifact, and stopping condition. Partition broad searches by stars, date, language, owner, topic, or exact path so result caps do not silently bias the sample. Prefer canonical or maintained sources, but do not equate popularity with correctness.

For Skill discovery, require a real `SKILL.md` or equivalent artifact, an immutable commit URL, repository URL, content hash, declared or repository license, and a brief adaptation decision. Reject forks, duplicates, abandoned or unclear-license sources, unsafe content, and platform-specific material unless the scope explicitly calls for them. Never copy secrets, private data, or untrusted command output into a durable report.

## Choose the right GitHub surface

- **Repository search:** find projects by name, description, topics, language, stars, forks, license, creation date, push date, owner, or archived state.
- **Code search:** locate exact paths, symbols, phrases, imports, configuration, or usage patterns in indexed default branches; authenticate and narrow queries when possible.
- **Issue/PR search:** find reported behavior, accepted fixes, discussions, labels, ownership, and project precedent; distinguish closed from merged/accepted.
- **Commit/release history:** establish when behavior or a file changed, the latest maintained version, and whether a source is pinned or moving.
- **Contents/tree API:** inspect the repository tree, read a specific file, discover references/assets, and fetch a fixed revision without cloning unrelated data.
- **GraphQL or batched API:** use for precise nested metadata or bounded batches when the query cost and timeout are known.

Do not use code search to prove runtime behavior, use stars as a quality guarantee, or use a default-branch URL as immutable provenance. If a search surface is unavailable, continue with an independent surface and state the coverage gap.

## Rank and verify candidates

Rank candidates by relevance to the question, source authority, license clarity, recent maintenance, reproducibility, test/evidence quality, security signals, and compatibility with the target host. Inspect the repository README, license endpoint/file, tree, target artifact, recent commits, issues/releases, and any referenced resources needed to interpret it.

For each selected source, capture:

```text
repository + owner
artifact path
fixed commit SHA and content/blob SHA
source and raw URLs pinned to that commit
license evidence and compatibility
security/static-scan result
what was used, omitted, or adapted
limitations and verification status
```

Read referenced files when their rules affect meaning. Do not package missing resources, private local paths, provider-specific tools, executable scripts, or copied assets without separately checking their authorization, license, and security boundary. Prefer a clean adaptation with explicit omissions over a broken bundle.

## Handle limits and uncertain results

Track request count, remaining rate budget, pagination, query result caps, incomplete results, timestamps, and retry/backoff. Narrow or partition a query after a timeout, secondary limit, or incomplete response; do not retry the identical broad query indefinitely. Cache immutable content hashes and avoid re-fetching identical blobs. Search results are a sample, so state the query, page limit, excluded candidates, and possible blind spots.

Treat redirects, generated pages, deleted files, changed default branches, and stale indexes as evidence hazards. Re-resolve a candidate's fixed commit before publication. If the repository's license is absent or contradictory, do not infer permission from public visibility; mark it unverified and exclude it from curated packaging unless a clear compatible license is found.

## Report reproducibly

Return the research question, queries/surfaces, date, scope, candidate table, ranking rationale, exact source links, hashes, license/security checks, extracted findings, rejected candidates and reasons, limitations, and next action. Separate observed source facts from inference and recommendation. For a Skill adaptation, ensure the catalog record, source manifest, installed Skill metadata, README entry, and download URL all refer to the same source identity.

Stop when the requested evidence is sufficient, the search boundary is exhausted, or authority/license/source integrity is ambiguous. Never claim “all GitHub” from a bounded search, never fabricate unavailable results, and never mutate external repositories merely because research found a possible improvement.
