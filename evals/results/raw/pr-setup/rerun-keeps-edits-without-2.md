# Report: refresh PR-readiness profile (rerun-keeps-edits-without-2)

## What I did
Worked only in <tmp>/pr-ready-evals/pr-setup\rerun-keeps-edits-without-2 (git repo, clean tree).
Re-read: .gitlab-ci.yml, CONTRIBUTING.md, .gitlab/merge_request_templates/default.md, README.md, requirements.txt, .pr-ready/profile.md and .pr-ready/.profile.generated.md.

## Findings
- CI still runs `pip install -r requirements.txt` then `pytest -q`: reproduce CI / tests commands unchanged.
- CONTRIBUTING.md still says "Do not submit pull request descriptions written by AI tools" (Tooling) -> ai_description: forbidden unchanged. "Small fixes may be sent without an issue" (Process) -> prior_approval: not-required unchanged. No commit format, AI-disclosure rule, agent rules, generated files, risk paths or size budget stated -> those stay as before (unclear / none).
- MR template path unchanged; host gitlab, base main unchanged.
- Diff between the saved snapshot (.profile.generated.md) and profile.md: exactly one line, the Known traps row. The dev hand-wrote `| Flaky test_cache on CI | shared tmp dir | rerun once |` in place of the generated `| none yet | | |`. Nothing in the repo contradicts it, so it is preserved.

## Result shown to dev (before saving)
No source-derived field changed, so the refreshed profile is identical to the current profile.md, including the hand-written trap row:

    ## Known traps
    | Symptom | Cause | What to do |
    |---|---|---|
    | Flaky test_cache on CI | shared tmp dir | rerun once |

(All other sections as in the existing profile: host gitlab; tracker none; stack tool plain branches; contributing CONTRIBUTING.md; pr template .gitlab/merge_request_templates/default.md; commit format unclear; agent rules none; ai_description forbidden; ai_disclosure unclear; prior_approval not-required; base main; reproduce CI/tests `pytest -q`; build none found; generated check none found; generated files none; max_lines 500; risk paths none.)

## Human gate
Question I would ask: "Nothing in CI or the contribution files changed since the last run, so the only thing to save is the profile as-is, with your hand-written 'Flaky test_cache' trap kept. OK to save?"
Dev answer (pre-supplied): approve.

## Produced
Approved, so I saved. Because the merged result is byte-identical to the existing profile.md and the regenerated snapshot would equal .profile.generated.md apart from the hand-edited row, no file needed to change. I made no modifications; the hand edit was not lost. (I left .profile.generated.md as the pristine generated baseline so future reruns can still detect hand edits.)
