# Contributing

Thanks for improving the public WorkBuddy Skill catalog and its user experience.

## What to contribute

The public catalog is a frozen snapshot. Contributions should improve documentation,
tutorials, the site, validation, or an existing reviewed WorkBuddy package. Do not add
new catalog records or re-enable the crawler.

For changes to an existing package, preserve the original source, license, security
signals, and compatibility notes. Keep `SKILL.md` concise and move conditional detail
into declared `references/`, `scripts/`, `assets/`, or `templates/` resources. Never
copy proprietary prompts or private customer data.

## Verify locally

Run the same checks used by automation:

```bash
python3 scripts/validate_skill.py
python3 scripts/validate_catalog.py --minimum 10000 --require-analysis
python3 scripts/build_site_data.py
python3 -m unittest discover -s tests -q
./scripts/package_skill.sh
git diff --check
```

Describe the real user request or failure that motivated an instruction change. Do not claim a check passed when it was skipped, flaky, or not run. Existing package adaptations still require a reviewable commit and package verification.

GitHub auto-merge is enabled for this repository, and merged branches are deleted
automatically. Use auto-merge only after the required checks and human review for
the change have completed; this setting does not bypass validation or source review.

Bug reports should include the WorkBuddy version, the requested capability, the failure message with secrets removed, and the expected behavior.
