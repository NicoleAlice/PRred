## Policy

- `ai_description: allowed`: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, section Tooling). Output chosen: full description.
- `ai_disclosure: required-in-trailer`: "Add an `Assisted-by: <tool>` trailer to commits made with AI help" (CONTRIBUTING.md, section Tooling). The body has no AI mention and no generated-by footer.

## Evidence

Two usable entries (not stale, head `b347daa` = HEAD), both used. No stale entries.
- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK
- Mutation: `days_late <= 0` to `days_late < 0` in `late_fee`: test_on_time failed (1 failure of 3)

I ran no tests or mutations myself.

## Title

Add late fee for overdue invoices

(Commit format is free-form, observed in history; this matches the branch's commit subject. No ticket text was available, so I could not use the ticket's own words.)

## Draft (saved as written)

```
## Ticket

PAY-12 (no tracker configured; ticket text not available)

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: no fee when `days_late` is 0 or negative, otherwise `amount * rate * days_late` rounded to 2 decimals.

## Why

Overdue invoices need a late fee (PAY-12).

## Impact

Reaches nothing beyond the two new files: `late_fee` has no callers yet and nothing else in the diff changes.

## Focus

The weakest point is the 1.5% default rate and the linear per-day accrual: neither is stated in any ticket or doc available here, and no test pins the default rate or the rounding apart from one 100 x 2 days case. The `days_late <= 0` boundary was checked by mutation (below).

## Tests

- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK
- Mutation: changed `days_late <= 0` to `days_late < 0` in `late_fee`; `test_on_time` failed (1 failure of 3)
```

No PR template exists, so I used the pr-format.md sections in order (Out of Scope omitted: no entry). Diff size is 16 hand-written lines (`ledgerlite/fees.py` +5, `tests/test_fees.py` +11), under the 500 budget.

## Disclosure (for you, not in the description)

Add this trailer to the commit(s) made with AI help. I did not amend anything:

```
Assisted-by: Claude Code
```

Replace the tool name if the project expects a different form (for example with a model name). Commit `b347daa` currently has no trailer.

## Questions for you (not in the description)

1. Dev gate: what is the PAY-12 text, and does it state the 1.5% default rate and per-day linear accrual? Nothing in the repo or ticket key gives it, so the description states the gap as a fact in Focus. (No pre-supplied answer, so I continued without it.)
2. Should a fee on a negative `days_late` return 0 (current behavior, as written) rather than raise? The description only states what the code does.
3. Do you want a test for the default rate and rounding (for example, an amount whose product needs rounding)? Only the 100 x 2 case exists.

Comprehension check (optional; explain each in your own words):
- `ledgerlite/fees.py:1-1` (default `rate=0.015`)
- `ledgerlite/fees.py:3-4` (`days_late <= 0` returns the integer 0, not 0.0 or a rounded value)
- `ledgerlite/fees.py:5-5` (linear accrual per day and `round(..., 2)`)
- `tests/test_fees.py:10-11` (`late_fee(100, 2) == 3.0` is the only late case)

## State

- Saved: `.pr-ready/pr-description.md` (git-ignored; `git check-ignore` exit 0 via the new `.pr-ready/.gitignore` containing `pr-description*.md`).
- Evidence note recorded: `pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 2, stale 0`.
- Not opened: awaiting confirmation. Host is `gitlab`, and the branch `feat/PAY-12-late-fee` has no upstream. If you want me to open it, I would show these and ask "Run this?" for each:
  1. `git push -u origin feat/PAY-12-late-fee`
  2. `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices" --description "$(cat .pr-ready/pr-description.md)"`
- Tree check: `git status --porcelain` shows only `?? .pr-ready/.gitignore` (new untracked file under `.pr-ready/`); HEAD is still `b347daa`, no new commit.
