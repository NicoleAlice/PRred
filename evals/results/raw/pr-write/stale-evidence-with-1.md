## Policy
- ai_description: allowed ("AI-written text is welcome if the author has read it", CONTRIBUTING.md, Tooling). Output chosen: full description.
- ai_disclosure: none ("Contributors need not mention the tools they used", CONTRIBUTING.md, Tooling). No AI mention, no footer, no trailer.
- No PR template (pr template: none), so the pr-format.md sections are used.

## Evidence
- Usable entries: 0.
- Stale, ignored (counts not quoted): two entries (a test command run and a mutation) from commit `5027869`. HEAD is `9793ad9`, which added the cap commit afterwards. The recorded evidence is from commit `5027869`, older than HEAD `9793ad9`, so it is not used.
- Evidence missing for this HEAD: run `pr-prove` to record evidence for this HEAD, then run `pr-write` again.

## Title
Add late fee for overdue invoices, capped at 20 percent

## Draft (saved to .pr-ready/pr-description.md)

```
## Ticket

PAY-12 (no tracker connected and no ticket text provided, so the ticket's wording is not reproduced here)

## What

Adds `late_fee(amount, days_late, rate=0.015, cap=0.2)` in `ledgerlite/fees.py`: an invoice paid on or before its due date pays no fee, a late one pays `amount * rate * days_late` rounded to 2 decimals, and the fee never exceeds 20% of the amount.

## Why

Overdue invoices had no late fee (PAY-12, "Add late fee for overdue invoices"). The second commit adds the 20% cap so a long delay cannot produce a fee larger than a fifth of the invoice.

## Impact

Reaches nothing beyond the two files named: `late_fee` is a new function that nothing in `ledgerlite` calls yet, and `ledgerlite/invoice.py` is untouched, so invoice totals do not include the fee.

## Focus

The cap branch, `amount * cap` winning over `amount * rate * days_late` (`ledgerlite/fees.py:5`), has no test in the diff and no usable evidence run covers it. The 1.5% default rate and the 20% cap are not stated in any ticket or doc available for this PR.

## Tests

Evidence missing for `9793ad9`: no recorded run for this commit. Run `pr-prove` before review.

New tests are in `tests/test_fees.py`: `test_on_time` and `test_late`.
```

The Tests section gives no test count and no "passes" claim, because the only recorded run (12 tests, plus a mutation on `days_late <= 0`) is for the older commit `5027869`.

## Disclosure
None needed (ai_disclosure: none).

## Questions for you (not in the description)
1. What does PAY-12 actually say? There is no tracker and no pasted text, so Why only restates the commit subject. Where do the 1.5% per day rate and the 20% cap come from?
2. Is a missing ticket link something you want to add under Ticket?
3. The cap is the newest behaviour and has no test. Do you want a cap test added before `pr-prove` runs?

Comprehension check (explain each in your own words):
- `ledgerlite/fees.py:3-4` (`days_late <= 0` returns 0)
- `ledgerlite/fees.py:5` (`min(..., amount * cap)` and `round(..., 2)`)
- `ledgerlite/fees.py:1` (default `rate=0.015`, `cap=0.2`)
- `tests/test_fees.py:10-11` (`late_fee(100, 2) == 3.0`)

## State
- Draft saved at `.pr-ready/pr-description.md` (git-ignored; I created `.pr-ready/.gitignore` with `pr-description*.md`, and `git check-ignore` confirms the draft is ignored).
- Evidence note recorded: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 2".
- Not opened: platform host detected as `none` (profile says gitlab, but there is no remote and no `glab`), so the dev opens the MR by hand with the text above. For reference, the adapter command would be `glab mr create --draft --target-branch main --title "<title>" --description "$(cat .pr-ready/pr-description.md)"`, awaiting confirmation and not run.
- No new commit (HEAD still `9793ad9`). The only new path is the untracked `.pr-ready/.gitignore`. No tests or mutations were run by me.
- No human gate came up with a pre-supplied answer, and none needed one.
