No human gates came up, so no dev questions were needed. The profile allows AI-written descriptions and requires no disclosure. Prior approval is not required.

I did not modify anything in the repo. The description follows the project's GitLab MR template (`.gitlab/merge_request_templates/default.md`: Summary / How to test / Risk). It is below, ready to paste.

Branch `feat/PAY-12-late-fee` is one commit (`65371a7`) on `main`, 16 lines added, no tracker.

---

**Title:** Add late fee for overdue invoices

## Summary

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`. It returns the fee for an invoice paid `days_late` days after its due date: `amount * rate * days_late`, rounded to 2 decimals. An invoice that is on time or early (`days_late <= 0`) gets a fee of 0. The default rate is 1.5% per day late.

This only adds the function. Nothing calls it yet, and `invoice.total` is unchanged, so no existing behavior changes.

Two tests are added in `tests/test_fees.py`: `late_fee(100, 0) == 0` and `late_fee(100, 2) == 3.0`.

## How to test

```
python -m unittest discover -s tests -v
```

Expected: 3 tests, OK (the 2 new ones plus the existing `test_total`).

On this branch (head `65371a7`) the suite ran 3 tests and passed. As a check that the tests catch a regression, I changed `days_late <= 0` to `days_late < 0` in `late_fee`. `test_on_time` then failed (1 failure of 3).

## Risk

Low. The change only adds new code, with no callers and no changes to existing code.

- The 1.5% default rate is per day late, applied as simple interest with no cap. I took this from the code, not from a spec. Please confirm it is the intended rate and basis.
- The float arithmetic and `round(..., 2)` follow the existing style. They could give off-by-a-cent results on some inputs, such as binary-float rounding. Only 2 cases are tested.
- Because the function is not wired in, a reviewer should expect a follow-up that applies the fee to invoices.

---

Notes for the dev:
- The Risk section flags the per-day, uncapped 1.5% rate as an open question. I could not confirm it from the repo, so I did not state it as settled.
- I left out any tracker reference. The profile says `tracker: none`, and the PAY-12 in the branch name has no link I could verify.
