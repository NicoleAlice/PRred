# pr-setup eval results

Runs: 3 per case per mode. A run passes when every rubric item passes; a case passes at ≥ 2/3.
Runner model: Sonnet. Grader model: Haiku. Raw reports and grades: `raw/pr-setup/`.

| case | without | with |
|------|---------|------|
| gitlab-ai-forbidden | 0/3 | 2/3 |
| bare-no-ci | 0/3 | 3/3 |
| rerun-keeps-edits | 3/3 | 2/3 |

Notes:
- `gitlab-ai-forbidden` with, run 2: the run stopped because no Python interpreter was reachable from its shell (the eval machine had Python installed mid-session, so the session's PATH predated it). It followed the skill's rule to stop rather than redo the script by hand; counted as a failure.
- `rerun-keeps-edits` with, run 2: the report described the draft instead of showing it in full.
- `rerun-keeps-edits` passes without the skill too; it is kept as a regression guard for the section-merge behaviour.
