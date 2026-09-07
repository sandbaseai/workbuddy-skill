# Reading a catalog result

The Atlas is a discovery index, not an approval list. Use this short checklist
before importing any public Skill.

## 1. Start with the exact source

Open the result's `source` link and confirm the repository, path, license, and
commit. A catalog ID has the form:

```text
github:owner/repository:path/to/SKILL.md
```

The commit-pinned source link is the reproducible reference. A repository name
or display title alone is not enough, because names can be ambiguous and
content can change.

## 2. Read the review fields correctly

- **WorkBuddy status** describes packaging readiness, not trust. `workbuddy-ready`
  means the expected metadata was found; `adaptable` means the package needs
  small changes; `needs-review` and `unreviewed` need more inspection.
- **Reviewed package availability** is a separate signal. A result marked as a
  reviewed package has a repository-maintained, source-pinned WorkBuddy ZIP in
  Releases; it does not mean every catalog record with `workbuddy-ready` has a
  ZIP, and a catalog-only result is not automatically unsafe.
- **Score** is a compatibility hint from 0–100. It is not a quality, security,
  or performance rating.
- **Security status** reports conservative static signals. `no-static-flags`
  only means the scanner found none of its known patterns; it is not a safety
  guarantee. Read scripts, network calls, credentials, and permissions yourself.
- **Copies** tells you how many indexed paths share the same blob SHA. It is a
  provenance clue, not a popularity or trust score. Use `--unique` when you
  want one representative per identical blob.
- **Source context** helps separate a likely primary source from a mirror,
  fork, or dormant path. Prefer `primary-looking` when the source is otherwise
  comparable, then verify the repository yourself.
- **Source order** is deterministic: it sorts by repository and then path, so
  the same query can be compared or shared without depending on crawl order.

## 3. Search with a review goal

The local helper requires every search term to match and can apply review
filters:

```bash
python3 scripts/query_catalog.py invoice OCR --limit 10
python3 scripts/query_catalog.py research --security no-static-flags \
  --source-context primary-looking --min-score 80 --unique --sort score
```

The same review-oriented filter is available as a shortcut:

```bash
python3 scripts/query_catalog.py research --high-signal --limit 10
```

`--high-signal` means no static flags, a primary-looking source, a score of at
least 80, one result per unique blob, and score ordering. It is a triage aid,
not a trust or safety guarantee.

To use the same category vocabulary as Atlas, add `--category` (for example,
`research`, `development`, or `security`). Chinese labels such as `研究` are
accepted too. The filter uses name/path inference and honors curated package
category metadata:

```bash
python3 scripts/query_catalog.py --category research --package-status reviewed \
  --sort score --limit 10
```

Useful starting queries (all use the same review-oriented filter):

| Goal | Command |
|---|---|
| Research and web sources | `python3 scripts/query_catalog.py research --high-signal --limit 10` |
| OCR and document extraction | `python3 scripts/query_catalog.py ocr --high-signal --limit 10` |
| MCP and connector workflows | `python3 scripts/query_catalog.py mcp --high-signal --limit 10` |
| Testing and QA | `python3 scripts/query_catalog.py testing --high-signal --limit 10` |
| Documentation workflows | `python3 scripts/query_catalog.py documentation --high-signal --limit 10` |

Replace the term with your task, then add `--package-status reviewed` when you
need a package that can be downloaded from this repository's Releases.

If you are evaluating a new GitHub source or crawler range, pass
`--dry-run` to `scripts/crawl_github_skills.py`. It will perform discovery and
report the candidate count without writing the output JSONL or its stats file;
the published frozen catalog still requires a separate, explicit opt-in.
Normal scans keep a checkpoint beside the output (or at the path supplied with
`--checkpoint`). If a run is interrupted by a rate limit, network failure, or
process stop, repeat the same command to resume the pending repository or size
shard; the checkpoint is removed after a successful completion. `--dry-run`
does not create a checkpoint.
For a repository-specific preview that does not require global Code Search,
combine it with `--repository owner/name --repository-only`.
In repository-only mode, `--target` is only a cap: a smaller repository still
returns success after its complete tree scan.

The scheduled `Refresh skill catalog` workflow also runs a read-only probe over
representative upstream Skill repositories. It reports newly discoverable
paths without writing the frozen catalog, creating packages, or changing any
published snapshot. Its short-lived Actions artifact contains the discovered
JSONL rows plus a second file containing only paths and content SHAs not already
represented by the frozen catalog. Use the local command above when you need to
inspect a candidate in detail.

To restrict local results to packages that have a reviewed Release ZIP, use the
curated manifest maintained by this repository:

```bash
python3 scripts/query_catalog.py research --package-status reviewed
```

Reviewed results include the direct Release ZIP URL. With `--json`, the package
URL, stable asset filename, checksum URL, and a copy-ready GitHub CLI command are available as
`workbuddy_package_url`, `workbuddy_package_asset`, `workbuddy_checksum_url`, and
`workbuddy_download_command`; the inferred or curated Atlas category is available as
`workbuddy_category`, so a small script can download, route, and verify the selected
package without reconstructing release paths.

For a machine-readable shortlist of installable, high-signal results, combine
the reviewed-package filter with `--json` and inspect the first result before
copying its command:

```bash
python3 scripts/query_catalog.py research \
  --high-signal --package-status reviewed --limit 5 --json \
  > research-packages.json
jq -r '.[].workbuddy_download_command' research-packages.json
```

If `jq` is not available, use the Python standard library instead:

```bash
python3 -c 'import json; from pathlib import Path; print("\\n".join(item["workbuddy_download_command"] for item in json.loads(Path("research-packages.json").read_text())))'
```

The second command only prints commands; it does not run them. Open the
selected `source_url`, confirm its license and side effects, then run the
chosen `gh release download` command and verify `SHA256SUMS` as described in
the [quickstart](quickstart.md).

The human-readable output includes a complete `catalog id`. Copy that value
directly into `review_skill.py` or `adapt_skill.py`; do not reconstruct an ID
from the display name.

If a local query returns no matches, the command prints the Atlas and GitHub's
current `SKILL.md` search as next discovery steps. Those links only widen
discovery; they do not approve or install an external source.

```bash
python3 scripts/review_skill.py \
  --catalog-id 'github:owner/repository:path/to/SKILL.md'
```

You can also paste the same ID back into the local search or the Atlas search
box to find the exact record again:

```bash
python3 scripts/query_catalog.py 'github:owner/repository:path/to/SKILL.md'
```

Search narrows candidates; it does not install anything. For a selected result,
inspect the source and then follow the [adaptation guide](adapting-skills.md)
to create a reviewed WorkBuddy package.

If the Atlas returns no match, use its **Search current GitHub Skill files** link
to look beyond the current catalog. That link is only a discovery shortcut:
inspect the repository, license, scripts, permissions, and commit before adapting anything.

For scripts and dashboards, the compact browser dataset is available at
[`catalog.json`](https://sandbaseai.github.io/workbuddy-skill/catalog.json),
with field definitions in its [JSON Schema](https://sandbaseai.github.io/workbuddy-skill/catalog-schema.json).
If you only need reviewed packages that have a Release ZIP, use the separate
[human-readable package index](https://sandbaseai.github.io/workbuddy-skill/packages.html), its
[machine-readable package index](https://sandbaseai.github.io/workbuddy-skill/packages.json), and
its [Schema](https://sandbaseai.github.io/workbuddy-skill/packages-schema.json). Each package record includes an `asset` filename, a ready-to-copy `download_command` for GitHub CLI, and a `checksum_url` for verifying the ZIP.

Machine consumers can validate the metadata shape against the published
[catalog metadata Schema](https://sandbaseai.github.io/workbuddy-skill/catalog-meta-schema.json).

## 4. Run a read-only first test

Import the package only after checking its inputs and side effects. Start with
public, non-sensitive data and ask for a plan before allowing writes, messages,
paid API calls, or production access. Keep the source commit and package
version with any result that needs to be reproduced.
