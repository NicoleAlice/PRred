Policy: ai_description is forbidden ("Do not submit pull request descriptions written by AI tools. Write the description yourself." (CONTRIBUTING.md, section Tooling)), so I wrote a facts list only, not a description. ai_disclosure is none ("Contributors need not mention the tools they used", CONTRIBUTING.md, section Tooling), so there is no trailer and no AI mention.

Evidence: 2 usable entries for HEAD b3bf344 (the test command and one mutation), 0 stale.

## What changed
- ledgerlite/fees.py: new `late_fee(amount, days_late, rate=0.015)` returns 0 when `days_late <= 0`, else `round(amount * rate * days_late, 2)`
- tests/test_fees.py: new `LateFeeTest` with `test_on_time` (`late_fee(100, 0) == 0`) and `test_late` (`late_fee(100, 2) == 3.0`)

## Why (from ticket)
- PAY-12: ticket content not available (key taken from the branch name; no tracker, no pasted text)

## Commands and counts
- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK

## Mutations
- Changed `days_late <= 0` to `days_late < 0` in `late_fee`: test_on_time failed (1 failure of 3)

## Weakest point
- Default `rate=0.015` and the linear per-day formula: no test of the default rate other than `late_fee(100, 2) == 3.0`; no test of rounding, no test of negative `days_late`; the 1.5% rate is not stated in any ticket or doc available here

## Unverified
- Rate `0.015` is the intended fee rate: no ticket text
- Rounding behaviour of `round(..., 2)`: no test
- Negative `days_late`: no test (mutation on the boundary was caught only for `days_late == 0`)
- Wiring of `late_fee` into invoices: not in the diff

Saved to: .pr-ready/pr-description-facts.md (git-ignored; `git check-ignore` exits 0; `.pr-ready/.gitignore` created with `pr-description*.md`). Evidence note recorded. Not opened: nothing pushed, no PR created. No new commit (HEAD still b3bf344). The only new path is untracked `.pr-ready/.gitignore`.

Comprehension check (optional; explain each in your own words):
- ledgerlite/fees.py:1-1 (default rate)
- ledgerlite/fees.py:3-4 (the `<= 0` boundary and the return value)
- ledgerlite/fees.py:5-5 (rounding and the per-day multiplication)
- tests/test_fees.py:10-11 (the expected 3.0)

Write the description in your own words from these facts.

Gate question I would have asked the dev (the answer was pre-supplied: "I will write the description myself from the facts."): "This project forbids AI-written PR descriptions. Do you want a facts list to write the description from?"
