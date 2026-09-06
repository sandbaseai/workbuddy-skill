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

## 4. Run a read-only first test

Import the package only after checking its inputs and side effects. Start with
public, non-sensitive data and ask for a plan before allowing writes, messages,
paid API calls, or production access. Keep the source commit and package
version with any result that needs to be reproduced.
