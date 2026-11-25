Policy: ai_description is forbidden ("Do not submit pull request descriptions written by AI tools. Write the description yourself." CONTRIBUTING.md, section Tooling), so I produced the facts list only. ai_disclosure is none ("Contributors need not mention the tools they used", CONTRIBUTING.md, section Tooling), so there is no trailer and no AI mention.

Human gate: none came up. The dev's pre-supplied answer ("I will write the description myself from the facts") matches the facts-list output, so I continued with that.

Evidence: 2 usable entries for HEAD b3bf344, 0 stale. I ran no tests or mutations myself.

Saved to: .pr-ready/pr-description-facts.md (git-ignored; `git check-ignore` exit 0). I created the untracked `.pr-ready/.gitignore` with the line `pr-description*.md`. I recorded the evidence note. No commit was made, HEAD is still b3bf344, and the only new untracked path is `.pr-ready/.gitignore`. Host is gitlab and I did not open or push anything.

Facts list, as saved:

```
## What changed
- ledgerlite/fees.py: new function `late_fee(amount, days_late, rate=0.015)`
- ledgerlite/fees.py:3-4: returns 0 when `days_late <= 0`
- ledgerlite/fees.py:5: otherwise returns `round(amount * rate * days_late, 2)`
- tests/test_fees.py: new `LateFeeTest` with `test_on_time` and `test_late`
- Diff size: 16 hand-written lines in 2 files, budget 500

## Why (from ticket)
- PAY-12: ticket text not available (tracker none, nothing pasted); content not guessed

## Commands and counts
- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK (recorded for b3bf344)

## Mutations
- Changed `days_late <= 0` to `days_late < 0` in late_fee: test_on_time failed (1 failure of 3)

## Weakest point
- Default rate 0.015 (ledgerlite/fees.py:1): no ticket or doc states it; `test_late` uses the default rate only; no test passes a custom rate or a fractional-cent amount that exercises rounding

## Unverified
- Rate 0.015 per day: expected value not stated in any ticket or doc
- Rounding to 2 decimals (ledgerlite/fees.py:5): no test covers a result that needs rounding
- Negative `days_late`: no test; only `days_late == 0` is covered
- No caller of `late_fee` in the diff
```

Comprehension check (optional, explain each in your own words):
- ledgerlite/fees.py:1-1
- ledgerlite/fees.py:3-4
- ledgerlite/fees.py:5-5
- tests/test_fees.py:10-11

Write the description in your own words from these facts.
