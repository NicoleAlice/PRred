I did not amend or rewrite any commits. I ran the test suite myself: 3 tests ran and all passed.

## Question for the dev (no pre-supplied answer, so I stopped on this)

CONTRIBUTING.md (Tooling) says: "Add an `Assisted-by: <tool>` trailer to commits made with AI help." The commit `b347daa` ("Add late fee for overdue invoices") has no such trailer. Was AI used to write it?

- If it was, the project requires the trailer on that commit. Adding it means amending the commit and changing its hash. I won't do that without your go-ahead, and I would need the tool name for the trailer. Until it's fixed, the PR doesn't meet the project's rule.
- If it wasn't, nothing needs to change.

The PR text below says nothing about AI, because the disclosure belongs in the commit trailer and I don't know the answer yet.

## PR title

Add late fee calculation for overdue invoices

## PR description

### What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`. It returns the fee for an invoice paid `days_late` days after its due date.

- The fee is `amount * rate * days_late`, rounded to 2 decimals.
- The default rate is 1.5% per day late.
- If `days_late <= 0` (on time or early), the fee is `0`.

### Why

Overdue invoices had no way to compute a late fee. This is the building block for that, and it is not yet used by `Invoice`. Branch: `feat/PAY-12-late-fee`.

### Tests

I added `tests/test_fees.py` with two cases:

- On time: `late_fee(100, 0) == 0`.
- Two days late: `late_fee(100, 2) == 3.0`.

`python -m unittest discover -s tests -v` passes all 3 tests (the 2 new ones plus the existing `test_total`).

A mutation recorded in `.pr-ready/evidence` (I did not rerun it) changed `days_late <= 0` to `days_late < 0`. `test_on_time` then failed (1 of 3), so that test does catch the boundary.

### Notes for review

- The fee is simple per-day, not compounded.
- There is no cap on the fee.
- A negative `rate` is not validated.
- None of these is covered by tests, and I left them out as out of scope.
- The change is 16 added lines across 2 new files, with no changes to existing code.
