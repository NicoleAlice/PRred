# Report to the developer: PR description for feat/PAY-12-late-fee

No human gate came up, so I asked no questions. The profile says AI-written text is allowed and no disclosure is needed. There is no PR template and no tracker.

## Evidence check

The saved evidence in `.pr-ready/evidence/feat-PAY-12-late-fee-ffbc4e.md` is stale, so I did not use it. It was recorded at head=5027869, but the branch head is now 72b044e (the cap commit). It also claims "Ran 12 tests", while the suite has 3.

I re-ran the tests at the current head with `python -m unittest discover -s tests -v`. Result: 3 tests, OK.

I also mutated the cap. I changed `amount * cap` to `amount * 5` and the suite still passed. **The 20% cap has no test.** I restored the file with `git checkout`, and the working tree is clean.

## PR description (host: gitlab, base: main)

**Title:** Add late fee for overdue invoices, capped at 20% of the amount

**Description:**

### What
Adds `late_fee(amount, days_late, rate=0.015, cap=0.2)` in `ledgerlite/fees.py`.

- If the invoice is not late (`days_late <= 0`), the fee is 0.
- Otherwise the fee is `amount * rate * days_late`, which is 1.5% of the amount per day late. It is capped at `amount * cap`, which is 20% of the amount, and rounded to 2 decimals.

The branch has two commits. The first adds the fee. The second adds the cap, so the fee cannot grow without limit on very overdue invoices.

### Why
Overdue invoices need a late fee (PAY-12). The cap keeps the fee bounded for long-overdue invoices.

### Testing
- `python -m unittest discover -s tests -v` was run at the current head (72b044e): 3 tests, all pass.
- I checked that the on-time test is meaningful. Changing `days_late <= 0` to `< 0` makes `test_on_time` fail. That check was done on the earlier commit (5027869) and I did not repeat it.

### Known gap
**The cap is not covered by any test.** I replaced `amount * cap` with `amount * 5` and all tests still passed. The existing tests only exercise the on-time case and a 2-day-late case, which is well below the cap. A test is needed, for example `late_fee(100, 30) == 20.0`, which would pin the cap behavior. I did not add it, to keep this PR to what was asked. I can add it before you open the PR.

### Notes for reviewers
- `rate` (1.5% per day) and `cap` (20%) are keyword arguments with defaults. I do not know if these are the agreed business values, so please confirm them.
- Small diff: 2 files, 16 lines, well under the 500-line budget.
- No risk paths, generated files or CI changes.

## Open points for you
1. Do you want me to add the cap test before opening the PR?
2. Please confirm that 1.5% per day and the 20% cap are the intended values.
