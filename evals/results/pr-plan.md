# pr-plan eval results

Runs: 3 per case per mode. A run passes when every rubric item passes; a case passes at ≥ 2/3.
Runner model: Sonnet. Grader model: Haiku. Raw reports and grades: `raw/pr-plan/`.

| case | without | with |
|------|---------|------|
| big-feature | 0/3 | 3/3 |
| thin-ticket | 0/3 | 3/3 |
| needs-prior-approval | 3/3 | 3/3 |
| touches-auth | 0/3 | 3/3 |

Notes:
- Without the skill: 1–2 PRs with no size estimates, no rigor level or line-by-line human read for auth changes, a plan written anyway for a ticket whose only criterion is "it should be better", and plans that don't end by asking for approval.
- `needs-prior-approval` passes without the skill too (the CONTRIBUTING rule is explicit); kept as a regression guard.
