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

To restrict local results to packages that have a reviewed Release ZIP, use the
curated manifest maintained by this repository:

```bash
python3 scripts/query_catalog.py research --package-status reviewed
```

Reviewed results include the direct Release ZIP URL. With `--json`, the package
URL, stable asset filename, checksum URL, and a copy-ready GitHub CLI command are available as
`workbuddy_package_url`, `workbuddy_package_asset`, and
`workbuddy_checksum_url`, and `workbuddy_download_command`, so a small script can download and verify the selected
package without reconstructing release paths.

The human-readable output includes a complete `catalog id`. Copy that value
directly into `review_skill.py` or `adapt_skill.py`; do not reconstruct an ID
from the display name.

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
to look beyond the frozen snapshot. That link is only a discovery shortcut:
inspect the repository, license, scripts, permissions, and commit before adapting anything.

For scripts and dashboards, the compact browser dataset is available at
[`catalog.json`](https://sandbaseai.github.io/workbuddy-skill/catalog.json),
with field definitions in its [JSON Schema](https://sandbaseai.github.io/workbuddy-skill/catalog-schema.json).
If you only need reviewed packages that have a Release ZIP, use the separate
[human-readable package index](https://sandbaseai.github.io/workbuddy-skill/packages.html), its
[machine-readable package index](https://sandbaseai.github.io/workbuddy-skill/packages.json), and
its [Schema](https://sandbaseai.github.io/workbuddy-skill/packages-schema.json). Each package record includes an `asset` filename, a ready-to-copy `download_command` for GitHub CLI, and a `checksum_url` for verifying the ZIP.

To verify that a local checkout still contains the exact frozen snapshot used by
the Atlas, run:

```bash
python3 scripts/build_site_data.py
python3 scripts/verify_catalog_snapshot.py
```

The command compares the SHA-256 of `catalog/skills.jsonl` with the
`catalog_sha256` value in `site/catalog-meta.json`; it does not fetch or modify
third-party content.

Machine consumers can validate the metadata shape against the published
[catalog metadata Schema](https://sandbaseai.github.io/workbuddy-skill/catalog-meta-schema.json).

## 4. Run a read-only first test

Import the package only after checking its inputs and side effects. Start with
public, non-sensitive data and ask for a plan before allowing writes, messages,
paid API calls, or production access. Keep the source commit and package
version with any result that needs to be reproduced.
