## 1. Policy

- `ai_description: allowed`: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: full description.
- `ai_disclosure: none`: "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). No AI mention and no footer in the body, and no trailer.
- Template: none (profile). I used the pr-format.md sections.

## 2. Evidence

Evidence missing for this HEAD: run `pr-prove`.

- The recorded evidence is from commit `5027869`, older than HEAD `c1e1d67`, so it is not used. This covers 2 entries: a test command and a mutation.
- Usable entries: 0. Stale entries: 2.
- The Tests section therefore gives no counts and no "passes" claim.
- Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again.

## 3. Title and draft

Title: `Add late fee for overdue invoices, capped at 20 percent of the amount`

Draft, saved as written:

```
## Ticket

PAY-12 (from the branch name; no tracker is configured and no ticket text was provided)

## What

Adds `late_fee(amount, days_late, rate=0.015, cap=0.2)` in `ledgerlite/fees.py`. It returns 0 when `days_late` is 0 or negative, otherwise `amount * rate * days_late` capped at `amount * cap` (20% of the amount), rounded to 2 decimals.

## Why

Overdue invoices had no late fee. The 20% cap keeps the fee from growing past a fifth of the invoice amount however late the payment is. The 1.5% daily rate and the 20% cap are not stated in any ticket or doc available here.

## Impact

Adds a new module and a new test file only. `late_fee` is not called from anywhere yet, and `ledgerlite/invoice.py` is unchanged, so no existing behaviour changes.

## Focus

The cap path (`min(..., amount * cap)` in `ledgerlite/fees.py:5`) is the least-covered part: the two tests cover `days_late` of 0 and 2 only, and none reaches the cap. It was checked by reading only.

## Tests

Evidence missing for `c1e1d67`: no recorded run for this commit. Run `pr-prove` before review.

New tests are in `tests/test_fees.py` (`test_on_time`, `test_late`).
```

## 4. Disclosure

Nothing to add. `ai_disclosure` is `none`.

## 5. Questions for you (not in the description)

1. What does PAY-12 say? There is no tracker and no pasted text, so I only have the key from the branch name. I need the ticket link or text for the Ticket line and the Why.
2. Where do the 1.5% per-day rate and the 20% cap come from? The description says they are not stated in any ticket or doc I could see.
3. Should `late_fee` be wired into invoicing in this PR? Nothing calls it today, and the Impact section says so.
4. Should the cap path get a test? No test reaches the cap, so I named that as the Focus. Both `pr-prove` and a new test would help.

Comprehension check (optional). Explain each in your own words:

- `ledgerlite/fees.py:1-1`: the default `rate=0.015` and `cap=0.2`
- `ledgerlite/fees.py:3-4`: the `days_late <= 0` boundary returns 0
- `ledgerlite/fees.py:5-5`: `min(amount * rate * days_late, amount * cap)` applies the cap
- `ledgerlite/fees.py:5-5`: `round(..., 2)` on the result
- `tests/test_fees.py:10-11`: `late_fee(100, 2) == 3.0`

## 6. State

- Saved to `.pr-ready/pr-description.md`.
- I created `.pr-ready/.gitignore` with the line `pr-description*.md`.
- `git check-ignore` exits 0 for the draft.
- I recorded an evidence note: `pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 2`.
- Not opened: awaiting confirmation. Host is gitlab and the branch has no remote configured. If you want to open it, the command from the adapter is below. I have not run it, and I need your confirmation for each remote step, including a push.
  `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices, capped at 20 percent of the amount" --description "$(cat .pr-ready/pr-description.md)"`
- No new commit: HEAD is still `c1e1d67`.
- The only new path is the untracked `.pr-ready/.gitignore`.
- I did not run tests or mutations myself.
