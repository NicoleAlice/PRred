## pr-write report: feat/PAY-12-late-fee

**1. Policy**
- `ai_description: allowed` ("AI-written text is welcome if the author has read it", CONTRIBUTING.md, section Tooling). Output chosen: full description.
- `ai_disclosure: none` ("Contributors need not mention the tools they used", CONTRIBUTING.md, section Tooling). No AI mention and no footer in the body.

**2. Evidence**
Evidence missing. `evidence.py show --json` returned no entries for HEAD `5027869`. Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again. No test counts are quoted anywhere in the draft.

**3. Title**
`Add late fee calculation for overdue invoices (PAY-12)`

**Draft** (saved to `.pr-ready/pr-description.md`):

```
## Ticket

PAY-12 (key from the branch name; no tracker is configured and the ticket text was not available).

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`, which returns 0 when `days_late` is 0 or negative and otherwise `amount * rate * days_late` rounded to 2 decimals.

## Why

Invoices paid after their due date had no fee calculation. The ticket text was not available, so no further motivation is stated here.

## Impact

Reaches nothing beyond the two files added: no other module imports `late_fee`, and `invoice.py`, config and pipelines are untouched.

## Focus

The 1.5% default rate (`rate=0.015`) is not stated in any ticket or doc available to this description, and the fee is simple (not compounded) per day late, rounded with Python's `round` to 2 decimals. These were checked by reading the code only; no mutation is recorded for them.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review. New tests are `test_on_time` and `test_late` in `tests/test_fees.py`.
```

No PR template exists (`pr template: none`), so the default pr-format sections were used. Out of Scope was omitted because it has no entry.

**4. Disclosure**
None needed (`ai_disclosure: none`).

**5. Questions for you (the dev, not in the description)**
- Gate question, with no pre-supplied answer, so I did not act on it. I asked nothing that blocked the draft.
- What is the ticket text for PAY-12 (problem, acceptance criteria, link)? The Why section is thin without it, and the Ticket line has no link.
- Is the 1.5% per-day simple rate (`0.015`) the agreed rate? No ticket or doc states it.
- Is the fee meant to be 0 (int) when on time and a float otherwise? The code returns int `0` on time; I stated only what the code does.

Comprehension-check hunks (explain each in your own words; optional, does not block):
- `ledgerlite/fees.py:1-1` (default `rate=0.015`)
- `ledgerlite/fees.py:3-4` (`days_late <= 0` returns 0)
- `ledgerlite/fees.py:5-5` (`round(amount * rate * days_late, 2)`)
- `tests/test_fees.py:10-11` (`late_fee(100, 2) == 3.0`)

**6. State**
- Saved: `.pr-ready/pr-description.md`. `.pr-ready/.gitignore` created with `pr-description*.md`. `git check-ignore -q` exits 0.
- Evidence note recorded: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 0".
- Not opened: awaiting confirmation. Host is gitlab and the branch has no upstream. Commands I would show, each needing "Run this?":
  1. `git push -u origin feat/PAY-12-late-fee`
  2. `glab mr create --draft --target-branch main --title "Add late fee calculation for overdue invoices (PAY-12)" --description "$(cat .pr-ready/pr-description.md)"`
- No new commit. `git log --oneline -1` is still `5027869 Add late fee for overdue invoices`. The only new untracked path is `.pr-ready/.gitignore`, under `.pr-ready/`. The draft and evidence files are ignored.
- Diff size: 16 hand-written lines (budget 500).
