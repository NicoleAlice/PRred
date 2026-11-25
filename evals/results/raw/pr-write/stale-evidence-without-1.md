# Report: PR description for feat/PAY-12-late-fee

No human gate came up, so I asked no questions. I changed nothing in the repo. I temporarily edited `fees.py` for one mutation check and restored it with `git checkout`. The working tree is clean.

## Things you should know before opening the PR

1. **The saved evidence was stale, so I did not use it.** `.pr-ready/evidence/feat-PAY-12-late-fee-3aff2a.md` was recorded at head `5027869`. The branch head is now `130290e`, after the "Cap the late fee at 20 percent" commit. That file also claims "Ran 12 tests", but the suite has 3 tests. I re-ran everything against the current head instead.
2. **Fresh test run at 130290e:** `python -m unittest discover -s tests -v` ran 3 tests, all OK.
3. **The new 20% cap has no test.** I removed the cap in `fees.py` (replaced `min(...)` with the uncapped fee) and the suite still passed, 3 tests OK. The cap is the newest behavior and nothing protects it. I did not add a test, since you only asked for the description. Adding one is cheap, for example `late_fee(100, 20) == 20.0`, because the uncapped fee would be 30.
4. **Your CI is likely to pass.** It uses the same command I ran. I could not run it on GitLab from here.

## PR description

**Title:** Add late fee for overdue invoices, capped at 20% of the amount

**Body:**

### What

Adds `ledgerlite.fees.late_fee(amount, days_late, rate=0.015, cap=0.2)`.

- If the invoice is not late (`days_late <= 0`), the fee is 0.
- Otherwise the fee is 1.5% of the amount per day late, rounded to 2 decimals.
- The fee never exceeds 20% of the invoice amount. `rate` and `cap` are keyword arguments, so callers can override them.

Example: `late_fee(100, 2)` returns `3.0`. `late_fee(100, 20)` returns `20.0`, because the uncapped fee would be 30.

### Why

Overdue invoices need a late fee (PAY-12). The cap keeps the fee bounded on invoices that are very late.

### How it is organized

The change is two commits:

1. `Add late fee for overdue invoices` adds the function and its tests.
2. `Cap the late fee at 20 percent of the amount` adds the `cap` parameter.

### Testing

I ran `python -m unittest discover -s tests -v` at the current head (`130290e`). All 3 tests pass.

The tests cover only the on-time case and a 2-days-late case. **The 20% cap has no test.** I removed the cap locally and the suite still passed, so a regression there would not be caught. I would add a test before merging, or in a follow-up.

### Notes for reviewers

- The cap is a fraction of the invoice amount (`0.2` means 20%), not an absolute value.
- There is no tracker integration and no template for this repo. The description is plain text.
