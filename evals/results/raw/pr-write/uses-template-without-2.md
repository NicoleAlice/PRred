## Report to developer

No human gate came up, so no questions were needed.

What I used:
- The repo's MR template at `.gitlab/merge_request_templates/default.md` (sections: Summary, How to test, Risk), so the description follows it.
- Evidence in `.pr-ready/evidence/feat-PAY-12-late-fee-b42b1a.md`. It was recorded at head=65371a7, which is the current head. I re-ran the tests myself on this head: 3 tests, OK.
- Profile: GitLab, no tracker, so no issue link. CONTRIBUTING.md says AI-written text is fine and needs no disclosure, so I added none. The diff is 16 lines against a 500-line budget.

Branch `feat/PAY-12-late-fee` against `main`: one commit, which adds `ledgerlite/fees.py` and `tests/test_fees.py`.

### Title

Add late fee calculation for overdue invoices

### Description (ready to paste into the MR)

```markdown
## Summary

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`. It returns the fee for an invoice paid `days_late` days after its due date: simple (non-compounding) interest of `amount * rate * days_late`, rounded to 2 decimals. The default rate is 1.5% per day. Invoices paid on time or early (`days_late <= 0`) get a fee of 0.

This only adds the function. Nothing calls it yet, and `invoice.total` is unchanged, so applying the fee to an invoice is left for a follow-up.

## How to test

    python -m unittest discover -s tests -v

On the branch head this runs 3 tests, all passing: the existing `test_total` plus the new `test_on_time` and `test_late` (`late_fee(100, 2) == 3.0`).

To check that the on-time boundary is covered, change `days_late <= 0` to `days_late < 0` in `late_fee`. `test_on_time` fails (1 failure out of 3).

## Risk

Low. The change is purely additive: one new function and its tests, with no existing code touched or called.

Open points for review:
- The 1.5% default rate is per day and does not compound. Please confirm that is the intended policy.
- Tests cover only 0 days and 2 days late. Negative `days_late` (paid early) is handled by the same `<= 0` branch but has no test of its own.
- There is no validation of negative `amount`.
```

### Notes
- Only the two tests listed above plus the existing one were run; there is no build or generated-file check in this repo.
- I did not commit, push or modify anything in the repo.
