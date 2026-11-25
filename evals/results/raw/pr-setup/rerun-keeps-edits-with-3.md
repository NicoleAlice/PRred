## pr-setup re-run report

**Sources read:** CONTRIBUTING.md, .gitlab/merge_request_templates/default.md, .gitlab-ci.yml, .claude/references/profile-template.md, .claude/references/rule-precedence.md, the existing .pr-ready/profile.md and .pr-ready/.profile.generated.md. There are no agent rules. The default Python alias was a Windows Store stub, so I ran the scripts with <python>.
Detect summary: host gitlab, base main, no CLIs installed (gh, glab, az and bb are all false). Remote steps would follow references/platforms/none.md. No stack tools. The commit samples are "Add pr-ready profile" and "Add cart total". No ticket keys.

### Draft (as it will be saved to profile.md)

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

### Sections
- Platform: unchanged
- Project rules: unchanged
- Base branch: unchanged
- Commands: unchanged
- Generated files: unchanged
- Budget: unchanged
- Risk paths: unchanged
- Known traps: kept (dev edited). The profile.md row "Flaky test_cache on CI | shared tmp dir | rerun once" differs from .pr-ready/.profile.generated.md, which has the `none yet` row. The new generated section equals the old one, so there is no conflict.

### Notes
- `ai_disclosure` is unclear. The policy says nothing about disclosing AI use. A sentence saying whether AI use must be declared (description, trailer, or none needed) would settle it.
- `commit format` is unclear because the two commit samples show no convention.
- Commands in `.gitlab-ci.yml` are `pip install -r requirements.txt` and `pytest -q`. I skipped the pip install as an environment step. `pytest -q` also appears in CONTRIBUTING.md. There is no build step and no generated-files check.
- CI-related risk paths (.gitlab-ci.yml and similar) are already covered by the built-in defaults.
- No generated files were found. There is no .gitattributes and no tracked file with a "DO NOT EDIT" or "@generated" header.
- The GitLab CLI (glab) is not installed.

### Gate
Question I asked the dev: "Save this to `.pr-ready/profile.md`? Approve, or tell me what to change."
Dev answer (pre-supplied): approve.

### Save
- profile.md: the approved draft is byte-identical to the existing file, so the content is unchanged and the hand-written Known traps row is kept.
- .profile.generated.md: the new unmerged generated draft is identical to the old one, with the `none yet` traps row. It never contains the dev's edits.
- Parse check: found true, policy ai_description forbidden, ai_disclosure unclear, prior_approval not-required, budget 500, warnings empty. This matches the draft.
- Evidence log: added the note "pr-setup saved .pr-ready/profile.md; kept: Known traps; updated: none" at .pr-ready/evidence/main-a80311.md (exit 0).
- Nothing was staged or committed. profile.md and .profile.generated.md can be committed together to share the profile with the team; that choice is the dev's.

**Left for the dev:** `ai_disclosure: unclear` and `commit format: unclear`.
