Policy: `ai_description: forbidden` — "Do not submit pull request descriptions written by AI tools. Write the description yourself." (CONTRIBUTING.md, section Tooling). Output chosen: facts list only. `ai_disclosure: none` — "Contributors need not mention the tools they used" (CONTRIBUTING.md, section Tooling), so no trailer and no AI mention.

Gate: the dev's answer was pre-supplied ("I will write the description myself from the facts."), so I continued with the facts list. No gate was left open.

Evidence: 2 usable entries (not stale, head b3bf344 = HEAD); 0 stale.

Saved to: `.pr-ready/pr-description-facts.md` (git-ignored via the new `.pr-ready/.gitignore` line `pr-description*.md`; `git check-ignore` exit 0). The evidence note was recorded. No new commit. Only new path: untracked `.pr-ready/.gitignore`.

Facts list, as saved:

```
## What changed
- ledgerlite/fees.py: new `late_fee(amount, days_late, rate=0.015)`; returns 0 when `days_late <= 0`, else `round(amount * rate * days_late, 2)`
- tests/test_fees.py: new `LateFeeTest` with `test_on_time` (`late_fee(100, 0) == 0`) and `test_late` (`late_fee(100, 2) == 3.0`)
- Diff size: 2 files, 16 lines added, 0 removed (budget 500)

## Why (from ticket)
- PAY-12: ticket text not available (no tracker, nothing pasted); only the key from the branch name is known

## Commands and counts
- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK

## Mutations
- Changed `days_late <= 0` to `days_late < 0` in late_fee: test_on_time failed (1 failure of 3)

## Weakest point
- The default rate 0.015 and the rounding to 2 decimals: no test passes `rate` explicitly or checks a rounding case, and the rate is not stated in any ticket or doc available; only the `<= 0` boundary was mutated

## Unverified
- Expected default rate (0.015): not stated in any available ticket or doc
- Rounding behaviour of `round(..., 2)`: no usable evidence entry covers it
- Explicit `rate` argument and negative `days_late`: no usable evidence entry covers them
```

Comprehension check (optional; explain each in your own words):
- ledgerlite/fees.py:1-1
- ledgerlite/fees.py:3-4
- ledgerlite/fees.py:5-5
- tests/test_fees.py:10-11

Write the description in your own words from these facts.
