# Contributing

Thanks for improving the public WorkBuddy Skill catalog.

## Add or adapt a Skill

1. Keep `SKILL.md` concise, self-contained, and useful across WorkBuddy projects; move conditional detail into declared `references/`, `scripts/`, `assets/`, or `templates/` resources.
2. Record the original repository, immutable source commit and blob SHA, source URL, declared license, adaptation changes, and any omitted resources in `SOURCE.json`.
3. Preserve the author's intent while removing host-specific bindings, unsafe implicit execution, credentials, and unverifiable claims. Never copy proprietary prompts or private customer data.
4. Use a valid lowercase Skill name, complete bilingual WorkBuddy frontmatter, an appropriate catalog category, and an accompanying license when the source permits redistribution.
5. Add the Skill to `catalog/curated.json`, the curated README table, and `CHANGELOG.md` only after the source, license, security signals, and compatibility have been reviewed.

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

Describe the real user request or failure that motivated an instruction change. Do not claim a check passed when it was skipped, flaky, or not run. The scheduled catalog crawler publishes provenance-only updates every six hours after validation; curated adaptations still require a reviewable commit and package verification.

Bug reports should include the WorkBuddy version, the requested capability, the failure message with secrets removed, and the expected behavior.
