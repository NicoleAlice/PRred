## Policy
- ai_description: allowed ("AI-written text is welcome if the author has read it", CONTRIBUTING.md, Tooling). Output chosen: full description.
- ai_disclosure: none ("Contributors need not mention the tools they used", CONTRIBUTING.md, Tooling). No AI mention and no trailer.
- No PR template (profile: none; detect_platform found none), so the pr-format.md sections are used.

## Evidence
Evidence missing: `evidence.py show --json` returned no entries for HEAD `5027869`. Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again. I ran no tests myself. The Tests section says the evidence is missing, and the description gives no test count.

## Title
Add late fee for overdue invoices

## Draft (saved to `.pr-ready/pr-description.md`)

```
Ticket: PAY-12

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`, which returns 0 when `days_late` is 0 or negative, and otherwise `amount * rate * days_late` rounded to 2 decimals.

## Why

Ticket PAY-12. No tracker is configured and its text was not available, so the reason is not restated here.

## Impact

Reaches nothing beyond the two files added: no existing code changes and nothing in the repo calls `late_fee` yet. The fee is linear in days late (no compounding) and the default rate is 0.015 per day.

## Focus

The default `rate=0.015` is the weakest point: it is not stated in any ticket or doc available here, and nothing was checked about it beyond reading the code. Rounding with `round(..., 2)` was also only read, not exercised at a rounding boundary.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.

New test file `tests/test_fees.py` with `test_on_time` and `test_late` in `LateFeeTest`.
```

## Disclosure
None needed (ai_disclosure: none).

## Questions for you (not in the description)
- What does PAY-12 say? The tracker is `none` and no ticket text was pasted, so only the key is used. Paste the ticket and I will fill in Why.
- Is 1.5% per day (simple, not compounding) the rate the ticket asks for? It is not stated anywhere I can read.
- Is returning `0` (an int) for on-time invoices and a float otherwise intended?
- The profile says host `gitlab`, but the repo has no remote and no `glab`, so there is no ticket link to build.

Comprehension-check hunks (optional; explain each in your own words):
- `ledgerlite/fees.py:1-5` (whole function), specifically:
  - `ledgerlite/fees.py:1` default `rate=0.015`
  - `ledgerlite/fees.py:3-4` the `days_late <= 0` early return of `0`
  - `ledgerlite/fees.py:5` `round(amount * rate * days_late, 2)`

## State
- Saved to `<tmp>/pr-ready-evals/pr-write/no-evidence-with-1/.pr-ready/pr-description.md`. `check-ignore` exits 0, so it is git-ignored.
- I created `.pr-ready/.gitignore` (it was not tracked) with the line `pr-description*.md`.
- Evidence note recorded.
- Not opened. There is no `glab` or remote, so the dev opens the MR by hand with the title and body above.
- No new commit. HEAD is still `5027869`, and the only new path is untracked `.pr-ready/.gitignore`.
