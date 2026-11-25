# PR description for feat/PAY-12-late-fee

No human gates came up, so I asked no questions. I read the repo profile and found the MR template at `.gitlab/merge_request_templates/default.md` (sections: Summary, How to test, Risk), and I used it. The profile says AI-written text is allowed and no AI disclosure is needed, so I added no disclosure line. Base is `main`. The branch has one commit on top of `d33b6ce`, and the evidence file matches head `65371a7`. I re-ran the tests and they pass.

## Title

Add late fee for overdue invoices

## Description (follows the repo's MR template)

```markdown
## Summary

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`. It returns the fee for an invoice paid `days_late` days after its due date.

- If `days_late <= 0`, the fee is 0.
- Otherwise the fee is `amount * rate * days_late`, rounded to 2 decimals. The default rate is 1.5% per day late, charged as simple interest, not compounded.

This only adds the function. Nothing calls it yet, so `invoice.total` is unchanged and invoice totals do not include the fee.

## How to test

    python -m unittest discover -s tests -v

Expected: 3 tests, all OK. The two new ones are in `tests/test_fees.py`:

- `test_on_time`: `late_fee(100, 0)` returns `0`.
- `test_late`: `late_fee(100, 2)` returns `3.0`.

I ran the suite on head `65371a7` and it passed (3 tests, OK). To check that `test_on_time` guards the boundary, I changed `days_late <= 0` to `days_late < 0`. `test_on_time` then failed (1 failure out of 3).

## Risk

Low. The change is one new function and its tests, with no edits to existing code and no callers.

- The 1.5% per day default is a business decision. A reviewer should confirm it is the intended rate, since there is no cap on the fee.
- Rounding uses Python's `round()`, which rounds half to even at the 2-decimal boundary.
- Nothing applies the fee to invoices yet. That would need a follow-up change.
```

## Notes for the dev

- The commit history is one commit ("Add late fee for overdue invoices"), and its message has no body.
- `.pr-ready/evidence/` is gitignored, so the evidence file will not be part of the PR.
- The tracker is `none`. The branch name suggests PAY-12, but the profile configures no tracker, so I added no issue link.
