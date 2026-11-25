## Policy
- ai_description: allowed ("AI-written text is welcome if the author has read it", CONTRIBUTING.md, Tooling). Output chosen: full description.
- ai_disclosure: none ("Contributors need not mention the tools they used", CONTRIBUTING.md, Tooling). No AI mention or footer in the body, no trailer.

## Evidence
Evidence missing: `evidence.py show --json` returned zero entries for HEAD `5027869`. No test counts or "passes" claims were made. Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again.

## Title
Add late fee for overdue invoices

## Draft (saved as .pr-ready/pr-description.md)

```
## Ticket

PAY-12 (no tracker configured and no ticket text provided, so only the key is known)

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: it returns 0 when `days_late` is 0 or negative, otherwise `amount * rate * days_late` rounded to 2 decimals.

## Why

Overdue invoices had no late fee calculation, and the branch is named for PAY-12. The ticket text was not available, so the acceptance criteria are not restated here.

## Impact

Reaches nothing beyond the two files added: `late_fee` is a new function that nothing in the repo calls yet, `ledgerlite/invoice.py` is unchanged, and there is no config or contract change.

## Focus

The 1.5% default rate (`ledgerlite/fees.py:1`) is not stated in any ticket or doc I could read, so it is the least certain part; I checked it by reading the diff only. The fee is simple (not compounded) per day late and rounded with Python's `round` on a float (`ledgerlite/fees.py:5`); the two new tests cover only 0 days and 2 days late on an amount of 100.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.

New tests: `LateFeeTest.test_on_time` and `LateFeeTest.test_late` in `tests/test_fees.py`.
```

## Disclosure
None required (ai_disclosure: none).

## Questions for you (not in the description)
- What is the PAY-12 ticket text or link? The profile has tracker: none, so I only have the key. The Ticket line has no link and Why does not state acceptance criteria.
- Where does the 1.5% default daily rate come from? It is not in any ticket or doc I read.
- Is the fee meant to be simple per-day (rate x days) rather than compounded, and is `round()` on a float acceptable for money? The description states what the code does.

Comprehension check (optional, explain each in your own words):
- `ledgerlite/fees.py:1-1` (default `rate=0.015`)
- `ledgerlite/fees.py:3-4` (`days_late <= 0` returns 0)
- `ledgerlite/fees.py:5-5` (`round(amount * rate * days_late, 2)`)
- `tests/test_fees.py:15-16` (`late_fee(100, 2) == 3.0`)

## State
- Saved: `.pr-ready/pr-description.md` (git-ignored via `.pr-ready/.gitignore` line `pr-description*.md`; `git check-ignore` exit 0). Note recorded with `evidence.py add --kind note`.
- Not opened: no remote configured and no `glab` CLI (detect_platform reports host `none`, though the profile says gitlab), so the dev opens the MR by hand with the text above.
- Tree: no new commit (HEAD still `5027869`). Only new untracked path is `.pr-ready/.gitignore`.
