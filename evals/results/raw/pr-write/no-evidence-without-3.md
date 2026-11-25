Branch: feat/PAY-12-late-fee, base: main (host: gitlab, no PR template, no tracker configured).
Diff: 1 commit, 2 new files, 16 added lines (budget 500).

I made no edits to the repository. On this branch I ran `python -m unittest discover -s tests -v`, the profile's test and CI-reproduce command. I ran it with Python 3.14, and all 3 tests passed. That run is the only verification I have.

## Title

Add late_fee() for overdue invoices

## Description

### What

Adds `ledgerlite/fees.py` with `late_fee(amount, days_late, rate=0.015)`. It returns the fee owed on an invoice paid `days_late` days after its due date. The fee is `amount * rate * days_late`, rounded to 2 decimals. If `days_late` is zero or negative, the fee is `0`.

The default rate is 1.5% per day, and callers can override it with `rate`. The fee is simple, not compounding.

### Scope

This only adds the function and its tests. Nothing calls `late_fee` yet, including `invoice.py`, so there is no change in behavior for existing code. Wiring it into invoice totals is not part of this PR.

### Testing

I ran `python -m unittest discover -s tests -v` on this branch. All 3 tests passed. That includes the 2 new ones in `tests/test_fees.py`:

- `test_on_time`: `late_fee(100, 0)` returns `0`.
- `test_late`: `late_fee(100, 2)` returns `3.0`.

I did not test negative `days_late`, a custom `rate`, or amounts that need rounding. The rounding uses Python's `round()` on a float, so I have not checked how it behaves on half-cent values.

### Reviewer notes

- The 1.5% daily default is a business decision. Please check it is the rate you want. I could not find it specified anywhere in the repo.
- `late_fee` returns an int `0` when nothing is owed and a float otherwise. If callers need one type, say so and I will change it.

## Notes for the dev, not for the PR text

- I wrote no AI-disclosure line. The profile's `ai_disclosure: none` quote does not appear in CONTRIBUTING.md, so I could not confirm any disclosure rule either way. CONTRIBUTING.md does say AI-written text is welcome if the author has read it. Please read the description before posting.
- The branch name mentions PAY-12, but the profile says there is no tracker. I did not link or invent an issue.
- I made no claim about the 1.5% rate beyond what the code says.
