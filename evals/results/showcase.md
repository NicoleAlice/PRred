# showcase eval results

Runs: 3 per case per mode. A run passes when every rubric item passes; a case passes at ≥ 2/3.
The case runs `pr-ready` end to end (`evals/showcase/cases.json`). Raw reports and grades: `raw/showcase/`. Write-up: `docs/showcase.md`.

| case | without | with |
|------|---------|------|
| end-to-end | 0/3 | 1/3 |

Faults found per run (of 4 planted):

| mode | run 1 | run 2 | run 3 |
|------|-------|-------|-------|
| without | 3, none with file:line | 3, none with file:line | 3, none with file:line |
| with | 3, with file:line | 3, with file:line | 4, with file:line |

Notes:
- The case does not pass in either mode.
- Without the skill: each run found the token on the build job, the false 4xx comment and the assertionless test, but cited none of them by file:line. All three runs created a commit on their own (6031f73, 0b88688, 8b737d8). None caught the pipeline condition that never fires (`$CI_PIPELINE_SOURCE == "scheduled"` at `.gitlab-ci.yml:29`; GitLab's value is `"schedule"`).
- With the skill: no commits and no remote actions in any run. Each report gave a "not ready" verdict and listed the surviving mutants (6, 4 and 6 of 7). Runs 1 and 2 missed the same pipeline-condition fault; run 2 cited `.gitlab-ci.yml:28-29` for a different concern.
- The prompt carries the same pre-supplied gate answers in both modes, including "a person has read the risky hunks line by line".
