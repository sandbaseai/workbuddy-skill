## What changed

<!-- Describe the user-facing problem and the smallest evidence-backed change. -->

## Scope checklist

- [ ] This changes documentation, the Atlas, validation, governance, or an existing reviewed package.
- [ ] I did not add catalog records or re-enable the crawler; the public snapshot remains frozen.
- [ ] If a reviewed package changed, its source commit, license, compatibility notes, and bundled resources remain traceable.
- [ ] Public docs do not expose secrets, private prompts, customer data, or internal-only build constraints.

## Verification

- [ ] `python3 scripts/validate_skill.py`
- [ ] `python3 scripts/validate_catalog.py --minimum 10000 --require-analysis`
- [ ] `python3 scripts/build_site_data.py`
- [ ] `python3 -m unittest discover -s tests -q`
- [ ] `./scripts/package_skill.sh` (when package or packaging behavior changed)
- [ ] `git diff --check`

## Review notes

<!-- Link relevant source, issue, release, screenshot, or remaining uncertainty. -->

Auto-merge should be enabled only after the checks above and human review are complete.
