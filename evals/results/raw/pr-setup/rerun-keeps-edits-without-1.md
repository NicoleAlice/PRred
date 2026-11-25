# Report: refresh of .pr-ready/profile.md (rerun-keeps-edits-without-1)

## What I did
Worked only in the temp repo `pr-ready-evals/pr-setup/rerun-keeps-edits-without-1`. I read the existing `.pr-ready/profile.md` and the saved baseline `.pr-ready/.profile.generated.md`. Then I re-read the sources: `.gitlab-ci.yml`, `CONTRIBUTING.md`, `.gitlab/merge_request_templates/default.md`, `README.md` and `requirements.txt`.

## Findings
- Re-deriving the profile from the sources gives exactly the baseline `.profile.generated.md`:
  - host gitlab
  - base main
  - CI and tests command `pytest -q`
  - ai_description forbidden, quoted from CONTRIBUTING.md "Tooling"
  - prior_approval not-required, quoted from "Process"
  - commit format unclear
  - budget 500
  - no generated files and no risk paths
- Nothing in the CI or contribution files changed since the last generation, so the generated sections need no update.
- The only difference between `profile.md` and the baseline is the hand-written Known traps row:

  | Flaky test_cache on CI | shared tmp dir | rerun once |

  The baseline has the placeholder row `none yet`. This row is the dev's own work and I kept it exactly as written.

## Gate
Question I would ask the dev: "Nothing changed in the CI or contributing files. The only difference is your hand-added Known traps row, which I keep as is. Save this unchanged profile?"
Pre-supplied answer: approve.

## Result shown before saving
The profile is identical to the current `.pr-ready/profile.md`, including the trap row (`Flaky test_cache on CI | shared tmp dir | rerun once`). Approval gave nothing to write, so I left both `profile.md` and `.profile.generated.md` untouched and made no commit. The baseline stays valid because the regenerated output equals it.

## Files changed
None.
