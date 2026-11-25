## pr-write report: feat/PAY-12-late-fee

**1. Policy**
- `ai_description: allowed`, quote: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: full description.
- `ai_disclosure: none`, quote: "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). The body has no AI mention and no footer, and no trailer is needed.

**2. Evidence**
- Evidence missing: `evidence.py show --json` returned no entries for HEAD `5027869`. No test counts or "passes" claims are used. Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again.
- I ran no tests or mutations myself.

**3. Title**

`Add late fee for overdue invoices`

(Free-form commit format, using the wording of the branch commit. The ticket text was not available.)

**Draft** (saved as is)

```
Ticket: PAY-12

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: it returns 0 when `days_late` is 0 or negative, and otherwise `amount * rate * days_late` rounded to two decimals, a simple per-day rate with no compounding and no cap.

## Why

PAY-12 asks for a late fee on overdue invoices. The ticket text was not available when this was written, so only the key is cited.

## Impact

Reaches nothing beyond the two files in this change: `late_fee` is new and no existing code calls it, so invoice totals and every other caller are unchanged.

## Focus

The default `rate=0.015` (1.5% per day late) and the per-day multiplication are the weakest point: no ticket or doc in the repo states the expected rate or whether it is per day. The two tests in `tests/test_fees.py` pin only `late_fee(100, 0) == 0` and `late_fee(100, 2) == 3.0`; the negative `days_late` branch and the rounding are not covered by a test, and no mutation was recorded against them.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.

The change adds `tests/test_fees.py` with `test_on_time` and `test_late`.
```

**4. Disclosure**

None needed (`ai_disclosure: none`).

**5. Questions for you (the dev, not in the description)**
- What is the intended late-fee rate: 1.5% per day late, or something else such as per month? The default `0.015` is stated in no ticket or doc. The description says only what the code does.
- Can you paste the PAY-12 ticket text or a link? There is no tracker connector (`tracker: none`) and no pasted ticket, so the Why section cites only the key. I did not guess its content.
- Is the `.pr-ready/.gitignore` I created fine? It was missing, so I created it with the line `pr-description*.md`.

Comprehension-check hunks (optional). Explain each in your own words:
- `ledgerlite/fees.py:1-1`: the default `rate=0.015`.
- `ledgerlite/fees.py:3-4`: the `days_late <= 0` branch returns 0.
- `ledgerlite/fees.py:5-5`: the rounding to two decimals and the per-day multiplication.
- `tests/test_fees.py:10-11`: the `late_fee(100, 2) == 3.0` expectation.

**6. State**
- Saved to `.pr-ready/pr-description.md`. It is git-ignored (`git check-ignore` exit 0) and not committed.
- Evidence note recorded: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 0".
- Open command: not opened. Host is `gitlab`, but `glab` is not installed and no remote is configured, so I print the text and stop. You open it by hand.
- No new commit (HEAD is still `5027869`). `git status --porcelain` shows only the new untracked `.pr-ready/.gitignore`.
