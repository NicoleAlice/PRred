# pr-write report: feat/PAY-12-late-fee

## 1. Policy
- `ai_description: allowed`: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: full description (not a facts list).
- `ai_disclosure: none`: "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). No AI mention, no footer, no trailer.

## 2. Evidence
- Evidence missing for this HEAD. Usable entries: 0. Stale entries: 2.
- The recorded evidence is from commit `5027869`, older than HEAD `67b10cf`, so it is not used. (Two entries: one command run and one mutation. Their counts are not quoted anywhere.)
- Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again.

## 3. Title
Add late fee for overdue invoices, capped at 20 percent of the amount

## Draft (saved)
```
Ticket: PAY-12

## What

Adds `late_fee(amount, days_late, rate=0.015, cap=0.2)` in `ledgerlite/fees.py`: an invoice paid on time or early (`days_late <= 0`) owes 0, and a late one owes `amount * rate * days_late`, limited to `amount * cap` and rounded to 2 decimals.

## Why

Overdue invoices had no late fee. The second commit caps the fee at 20 percent of the invoice amount so a long delay cannot grow the fee past that share. The ticket text was not available, so this is taken from the branch name and the commit messages.

## Impact

Nothing else is reached: `late_fee` is a new function with no caller in the repository, and the diff touches only `ledgerlite/fees.py` and `tests/test_fees.py`, with no config, contract or pipeline change.

## Focus

The cap is the weakest point. `min(amount * rate * days_late, amount * cap)` at `ledgerlite/fees.py:5` has no test that reaches it: `test_late` uses `late_fee(100, 2)`, which gives 3.0, well under the cap of 20. The cap was checked by reading only. The default rate of 1.5 percent per day and the 20 percent cap are not stated in any ticket or doc available here.

## Out of Scope

Negative or non-numeric `amount` is not handled; the function does no input validation.

## Tests

Evidence missing for `67b10cf`: no recorded run for this commit. Run `pr-prove` before review. New tests are in `tests/test_fees.py`: `test_on_time` and `test_late`.
```

## 4. Disclosure
None required (`ai_disclosure: none`). Nothing to add.

## 5. Questions for you (not in the description)
- What do PAY-12 and the tracker say? No tracker is configured (`tracker: none`) and no ticket text was pasted, so I gave the key only and did not guess its content.
- Are the 1.5 percent per-day rate and the 20 percent cap the agreed values? Neither is stated in a ticket or doc I could see; the description says so in Focus.
- Should the cap be exercised by a test? Nothing in the test file reaches it, so the cap is unproven at this HEAD.
- Is the missing input validation (Out of Scope) intended?

Comprehension check (optional; explain each in your own words):
- `ledgerlite/fees.py:3-4`
- `ledgerlite/fees.py:5`
- `tests/test_fees.py:10-11`

## 6. State
- Saved: `.pr-ready/pr-description.md` (git-ignored: `.pr-ready/.gitignore` created with `pr-description*.md`; `git check-ignore -q` exits 0).
- Evidence note recorded: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 2".
- Not opened: host is `gitlab`, but `glab` is not installed, so by the none adapter fallback I print the text and stop; you open the MR by hand. No push or remote action was run, and no confirmation was given.
- Tree: no new commit (HEAD still `67b10cf`); the only new path is untracked `.pr-ready/.gitignore`.
