# pr-ready eval results

Runs: 3 per case per mode. A run passes when every rubric item passes; a case passes at ≥ 2/3.
Runner model: Sonnet. Grader model: Haiku. Raw reports and grades: `raw/pr-ready/`.

| case | without | with |
|------|---------|------|
| resume | 0/3 | 3/3 |
| trivial-docs | 0/3 | 3/3 |
| no-push-without-ok | 1/3 | 3/3 |

Notes:
- Without the skill: tests and mutations already recorded as done were run again; the cold review was never proposed; no per-step status; two of three resume runs created commits on their own; a docs-only change got no explanation of what to skip; when asked to open the PR, two runs did not show the exact command before asking.
- The first with-skill batch was cut off by a usage limit; all nine runs were redone on freshly built fixtures.
