## Report to developer

No human gate came up that needed an answer, so nothing was blocked.

I read the branch `feat/PAY-12-late-fee` against `main`. It has one commit, "Add late fee for overdue invoices", and adds 16 lines in two files. I ran the CI command from the profile, `python -m unittest discover -s tests -v`. All 3 tests passed, and the working tree stayed clean.

### Things to check before you submit

1. **The profile has a disclosure quote that is not in CONTRIBUTING.md.** The profile says `ai_disclosure: none` and quotes "Contributors need not mention the tools they used". `CONTRIBUTING.md` only says "AI-written text is welcome if the author has read it." I could not confirm that disclosure is unnecessary. I added no AI-disclosure line and no tool mention. You may want to re-check the profile.
2. **I did not run the new code by hand.** The evidence is only the two unit tests below. I did not try fractional days, large amounts or float rounding.
3. **I did not invent a tracker link.** The profile says the tracker is `none`. "PAY-12" appears only in the branch name, so I left it out of the body. Add the link yourself if PAY-12 exists somewhere.
4. **I did not confirm intent for the 1.5% rate.** I could only describe what the code does.

### PR title

Add late_fee helper for overdue invoices

### PR description (ready to paste)

```markdown
## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`.

- It returns `0` when `days_late <= 0`.
- Otherwise it returns `round(amount * rate * days_late, 2)`. That is simple interest at 1.5% per day late by default, and the caller can override the rate.

This only adds the function. Nothing calls it yet. `ledgerlite/invoice.py` is unchanged, so `total()` still does not include any late fee.

## Why

Overdue invoices need a way to compute a late fee. This is the calculation on its own, so it can be reviewed apart from wiring it into invoices.

## Testing

`python -m unittest discover -s tests -v` runs 3 tests and all pass: the 2 new ones and the existing `total` test.

- `test_on_time`: `late_fee(100, 0)` returns `0`.
- `test_late`: `late_fee(100, 2)` returns `3.0`.

Not covered by tests: negative `days_late`, a custom `rate`, and rounding of fractional cents.

## Review notes

- The default rate of 1.5% per day is a policy choice. Please confirm it is the one you want.
- The fee is not capped, so a long delay can produce a fee larger than the invoice.
```

### Self-check

- The size is 16 added lines, well under the profile's 500-line budget.
- There are no generated files or risk paths to flag.
- Every claim in the description comes from the diff or the test run I did. The one exception is the sentence in Why, which is my inference from the commit title.
