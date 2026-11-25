1. Policy
- ai_description: allowed ("AI-written text is welcome if the author has read it", CONTRIBUTING.md, Tooling). Output chosen: a full description.
- ai_disclosure: none ("Contributors need not mention the tools they used", CONTRIBUTING.md, Tooling). The body has no AI mention and no generated-by footer, and there is no trailer.

2. Evidence
Evidence missing: run `pr-prove`. The log for HEAD `5027869` has no entries, so no usable entries and no stale ones. The description gives no test counts and no "passes", "tested" or "verified".

3. Title
Add late fee for overdue invoices

Draft, saved to `.pr-ready/pr-description.md`:

```
Ticket: PAY-12

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`. It returns 0 when `days_late` is 0 or negative, and otherwise `amount * rate * days_late` rounded to 2 decimals. The fee is simple, not compounded: it grows linearly with the days late.

## Why

Overdue invoices had no way to compute a late fee. PAY-12 is the only ticket reference available (taken from the branch name), so the problem statement here comes from the code alone.

## Impact

Reaches nothing beyond the two files named: `fees.py` is a new module and nothing in the repo imports it yet, so no existing caller changes behaviour. The 1.5% default rate is hard-coded as the `rate` default and is not read from config.

## Focus

The weakest point is the 1.5% per-day default rate and the rounding in `round(amount * rate * days_late, 2)`. The 1.5% value is not stated in any ticket or doc available here, and no recorded evidence covers it. The `days_late <= 0` boundary and the rounding were read in the diff only. The tests in `tests/test_fees.py` (`test_on_time`, `test_late`) check a whole-number case (100 at 2 days late) and the on-time case, not a fractional-cent rounding case.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.
```

4. Disclosure
None needed. The policy is `none`, so there is no trailer and no AI line.

5. Questions for you (the dev, not in the description)
- The tracker is `none` and no ticket text was pasted, so the description has only the key PAY-12 and no link. Can you paste the ticket text or its link? I did not guess its content.
- The ticket doesn't state the 1.5% default rate, and I couldn't find it in any doc I read. Is it the intended default, and is it per day? The code applies it per day late, and the description says so as a fact, not a question.
- The diff makes no change to `README.md` or to any caller. If the late fee is meant to feed the invoice total in `ledgerlite/invoice.py`, that is not in this branch, and the description does not claim it.

Comprehension check (optional). Explain each of these in your own words:
- `ledgerlite/fees.py:1-1`: the 0.015 default `rate`.
- `ledgerlite/fees.py:3-4`: the `days_late <= 0` branch returning 0 (an int, not 0.0).
- `ledgerlite/fees.py:5-5`: `round(amount * rate * days_late, 2)`, meaning linear per-day accrual and rounding to cents.

6. State
- Saved: `.pr-ready/pr-description.md`. It is git-ignored (`git check-ignore -q` exits 0). I created `.pr-ready/.gitignore` with the line `pr-description*.md`, because that file was not tracked.
- An evidence note was recorded: `pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 0`.
- Not opened: the host is gitlab and I have not been asked to push or open anything. No push or MR command has been run, and nothing is awaiting a confirmation yet. When you want to open it, I will show the exact commands: `git push -u origin feat/PAY-12-late-fee`, then the GitLab draft MR create command with this body.
- Tree state: no new commit (HEAD is still `5027869`). The only new path is the untracked `.pr-ready/.gitignore`.
- Pre-supplied dev answers: there were none, and no gate blocked the work. The ticket-content question above is not a blocker (the skill allows key-only), so I carried on.
