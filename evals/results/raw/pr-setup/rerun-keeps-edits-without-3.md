# Report: rerun-keeps-edits-without-3

## What I did
Worked only in the eval repo (rerun-keeps-edits-without-3). Re-read .gitlab-ci.yml, CONTRIBUTING.md, the MR template, README.md, requirements.txt, the existing .pr-ready/profile.md, and the stored snapshot .pr-ready/.profile.generated.md (what the tool generated last time).

## Findings
- Fresh read of CI and contribution files gives the same values as the snapshot: host gitlab, tracker none, base main, `pytest -q` for CI/tests, ai_description forbidden (quote from CONTRIBUTING.md Tooling), prior_approval not-required (quote from Process), pr template .gitlab/merge_request_templates/default.md, no build, no generated files, max_lines 500, no risk paths. Nothing in the CI or contribution files changed.
- Diff between snapshot and profile.md is exactly one line, a hand-written edit: the Known traps row
  `| Flaky test_cache on CI | shared tmp dir | rerun once |` (snapshot had `| none yet | | |`).

## Gate / question
Before saving I show the result. Question I would ask: "Nothing in CI or contribution files changed since the last run, and your hand-written 'Flaky test_cache on CI' trap is kept. Save this (effectively unchanged) profile?" Pre-supplied dev answer: approve.

## Proposed result (shown before saving)
Profile is identical to the current .pr-ready/profile.md, including the hand-written trap row:

| Symptom | Cause | What to do |
|---|---|---|
| Flaky test_cache on CI | shared tmp dir | rerun once |

All other sections unchanged (see list above).

## Saved
On approval, the save is a no-op for profile.md: I left it as is, so the hand edit is preserved and nothing was overwritten. The generated snapshot .profile.generated.md also needs no update since the freshly derived content equals it. No files modified.
