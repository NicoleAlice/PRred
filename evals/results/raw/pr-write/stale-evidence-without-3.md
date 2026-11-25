# Report: PR description for feat/PAY-12-late-fee

Repo: <tmp>/pr-ready-evals/pr-write\stale-evidence-without-3 (base `main`, host gitlab, no tracker, no PR template, no AI disclosure required, no prior approval needed; nothing modified, mutation was reverted).

No human gate came up that needed a dev answer.

## Evidence handling

The saved evidence file `.pr-ready/evidence/feat-PAY-12-late-fee-f5067e.md` is stale. It was recorded at head=5027869, but the branch head is now 025665f (the cap commit came after). It also says "Ran 12 tests", but the repo has 3. I did not use it. I re-ran everything on the current head:

- `python -m unittest discover -s tests -v` on 025665f: Ran 3 tests, OK.
- Mutation: changed the cap term `amount * cap` to `amount * 5`. All 3 tests still passed (OK). So the 20% cap has no test coverage.
- Manual check of the cap: `late_fee(100, 13)` = 19.5, `late_fee(100, 14)` = 20.0, `late_fee(100, 20)` = 20.0.

## Suggested PR description

**Title:** Add late fee for overdue invoices, capped at 20% of the amount

**Description:**

Adds `late_fee(amount, days_late, rate=0.015, cap=0.2)` in `ledgerlite/fees.py`.

- The fee is 1.5% of the invoice amount per day late, rounded to 2 decimals.
- It is 0 when the invoice is on time (`days_late <= 0`).
- The fee never exceeds 20% of the amount. With the default rate the cap applies from day 14 (13 days = 19.50 on 100, 14 days or more = 20.00).
- `rate` and `cap` are keyword parameters, so callers can override them.

Two commits: the first adds the uncapped fee, the second adds the cap.

**Testing**

Run on the current head (025665f) with `python -m unittest discover -s tests -v`: 3 tests, all pass.

Not covered: the cap. The tests only cover on-time (fee 0) and 2 days late (fee 3.00 on 100). I mutated the cap (`amount * cap` replaced by `amount * 5`) and all tests still passed, so a regression in the cap would not be caught. I checked the cap by hand only (values above). A test such as `late_fee(100, 20) == 20.0` would cover it, and I can add it to this PR if you want.

## Notes for the dev

- Stale evidence was ignored and re-run, as described above.
- Open question: should the cap test go into this PR? I did not add it, since you asked only for the description.
- No AI disclosure is needed per the profile. CONTRIBUTING.md allows AI-written text if the author has read it, so please read this before posting.
