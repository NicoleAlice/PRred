# pr-setup re-run report (rerun-keeps-edits-with-1)

## Sources read
SKILL.md, references/profile-template.md, references/rule-precedence.md, CONTRIBUTING.md, .gitlab-ci.yml, .gitlab/merge_request_templates/default.md, .pr-ready/profile.md, .pr-ready/.profile.generated.md.
Detect summary: host gitlab, base main, remote git@gitlab.example.com:team/shop.git, no CLIs (gh/glab/az/bb all false), no stack tools, no agent rules, no ticket keys, commit samples "Add pr-ready profile" / "Add cart total".
Note: `python3`/`python` were Windows Store stubs, so I ran the scripts with <python>.

## Draft (complete, exactly as saved in profile.md)

```markdown
# pr-ready profile

## Platform

- host: gitlab
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: CONTRIBUTING.md
- pr template: .gitlab/merge_request_templates/default.md
- commit format: unclear
- agent rules: none
- ai_description: forbidden
  > "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
- ai_disclosure: unclear
- prior_approval: not-required
  > "Small fixes may be sent without an issue" (CONTRIBUTING.md, section Process)

## Base branch

- base: main

## Commands

- reproduce CI: `pytest -q`
- tests: `pytest -q`
- build: none found
- generated check: none found

## Generated files

- none

## Budget

- max_lines: 500

## Risk paths

- none

## Known traps

| Symptom | Cause | What to do |
|---|---|---|
| Flaky test_cache on CI | shared tmp dir | rerun once |
```

## Sections
- Platform: unchanged
- Project rules: unchanged
- Base branch: unchanged
- Commands: unchanged (CI still only runs `pytest -q` after `pip install -r requirements.txt`; the install step is not a test/build step so reproduce CI stays as before)
- Generated files: unchanged
- Budget: unchanged
- Risk paths: unchanged (defaults already cover `.gitlab-ci.yml`; no extras found)
- Known traps: kept (dev edited), because profile.md differs from .pr-ready/.profile.generated.md (your hand-written row "Flaky test_cache on CI"). The new generated section is still the "none yet" row, so there is no conflict.

## Notes
- `ai_disclosure: unclear`: no sentence in CONTRIBUTING.md or the MR template addresses declaring AI use. A sentence saying whether to disclose AI use (or forbidding a trailer) would settle it.
- `commit format: unclear`: the two sample commits do not follow a common format.
- `pytest -q` also appears in CONTRIBUTING.md but it is already the CI command, so nothing extra was suggested.
- No glab CLI: remote steps will follow references/platforms/none.md.

## Gate question (asked to the dev)
"Save this to `.pr-ready/profile.md`? Approve, or tell me what to change."

dev answers: approve (pre-supplied; applied after the draft was shown above).

## Save
- Because the merged draft equals the current profile.md and the new generated draft equals the old .profile.generated.md, both files are byte-identical to what was approved, so nothing was rewritten and the hand-written Known traps row is preserved. No other files were modified.
- Parse check (read_profile): policy ai_description=forbidden, ai_disclosure=unclear, prior_approval=not-required, budget 500, generated [], risk_paths [], warnings [] (empty).
- Evidence log: `evidence.py add --kind note --text "pr-setup saved .pr-ready/profile.md; kept: Known traps (dev edited); updated: none"` exited 0 (added to .pr-ready/evidence/main-df6da5.md).
- Nothing staged or committed. profile.md and .profile.generated.md can be committed together to share the profile with the team; that choice is yours.

## Final report
Draft shown, approval received, files written: none changed (evidence note only), sections kept: Known traps (your hand-written row), unclear fields left: ai_disclosure, commit format.
