# PR description: feat/PAY-12-late-fee -> main

No human gate came up, so there were no questions for the dev. The profile says `ai_description: allowed`, `prior_approval: not-required` and `tracker: none`. The repo has no PR template.

I did not change the repo. I ran the profile's test command, `python -m unittest discover -s tests -v`. All 3 tests passed, including the 2 new ones. Nothing else was run.

## Title

Add late_fee helper for overdue invoices

## Description

Adds `ledgerlite.fees.late_fee(amount, days_late, rate=0.015)`. It returns the fee for an invoice paid `days_late` days after its due date.

- The fee is simple, not compounding: `round(amount * rate * days_late, 2)`.
- The default rate is 1.5% per day late.
- It returns `0` when `days_late <= 0`, so on-time and early payments cost nothing.

This is a standalone function. Nothing calls it yet. `invoice.total` is unchanged, so late fees do not show up in any invoice total.

### Testing

I ran `python -m unittest discover -s tests -v`. All 3 tests passed: the 2 new ones and the existing `test_total`.

The new tests, in `tests/test_fees.py`, cover only two cases:
- on time: `late_fee(100, 0)` returns `0`
- 2 days late: `late_fee(100, 2)` returns `3.0`

I did not test or decide the following:
- negative or zero `amount`
- a custom `rate`
- fractional days
- float rounding at the half-cent boundary

### Review notes

- The change is 16 added lines in 2 files (`ledgerlite/fees.py`, `tests/test_fees.py`). It is well under the 500-line budget.
- Please confirm that a simple (non-compounding) 1.5% per day is the intended policy. Nothing in the repo records the source of that rate.

## Notes to the developer (not for the PR body)

- I only described what the diff and the test run show. I did not claim anything about behavior I did not run, such as edge cases, integration with invoices, or the origin of the 1.5% rate. The branch name mentions PAY-12, but the profile says there is no tracker. I did not add an issue link, because I could not verify one.
- `.pr-ready/profile.md` quotes "Contributors need not mention the tools they used" as the source for `ai_disclosure: none`. That sentence is not in `CONTRIBUTING.md`, whose Tooling section only says "AI-written text is welcome if the author has read it." So the disclosure rule is not backed by the cited text. I added no AI disclosure, and I did not add anything claiming one is required. Please check that setting.
- `CONTRIBUTING.md` says AI-written text is welcome if the author has read it, so read this description before posting it.
- The host is GitLab, so this is a merge request, not a PR. The description above works in either.
