## Report: pr-write for feat/PAY-12-late-fee

Gate: no human gates came up and no pre-supplied answers were needed. The ticket is only a key (PAY-12), and `tracker: none` in the profile means there is no connector to fetch it.

### 1. Policy
- `ai_description: allowed`. Quote: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: full description.
- `ai_disclosure: none`. Quote: "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). The body has no AI mention and no generated-by footer.
- No PR template (`pr template: none`), so the pr-format.md sections are used.

### 2. Evidence
Evidence missing: `evidence.py show --json` returned HEAD `5027869` and zero entries, so nothing is usable or stale. I ran no tests. Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again. The Tests section says so and gives no counts.

### 3. Title and draft

Title: `Add late fee for overdue invoices`

Draft, saved as `.pr-ready/pr-description.md`:

```
Ticket: PAY-12

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: it returns 0 when `days_late` is 0 or negative, and otherwise `amount * rate * days_late` rounded to 2 decimals.

Adds `LateFeeTest` in `tests/test_fees.py` with `test_on_time` and `test_late`.

## Why

Overdue invoices had no late fee (PAY-12). The ticket text was not available when this was written, so only the key is cited.

## Impact

Reaches nothing beyond the two files named: `late_fee` is a new function, and nothing in the diff calls it, including `ledgerlite/invoice.py`.

## Focus

The weakest point is the 0.015 default rate, applied per day late without compounding: it is not stated in any ticket or doc available here, so the diff is its only source.

The `days_late <= 0` boundary and the `round(..., 2)` result for amounts that are not exact in floating point are covered by no recorded run. Only a read of the code was done on them.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.

The diff adds `test_on_time` and `test_late` in `tests/test_fees.py`.
```

Claim map (Step 6):
- `late_fee` signature and default rate 0.015: `ledgerlite/fees.py:1`
- Returns 0 for `days_late <= 0`: `ledgerlite/fees.py:3-4`
- Rounded product: `ledgerlite/fees.py:5`
- Two tests named: `tests/test_fees.py:7` and `tests/test_fees.py:10`
- Nothing calls it: `ledgerlite/invoice.py` only defines `total`, and the diff touches only 2 files (16 hand-written lines, budget 500).
- "Only a read of the code" about the boundary and rounding is true: I did nothing beyond reading.

Policy recheck: no AI mention, no trailer, no question to reviewers in the body.

### 4. Disclosure
None needed (`ai_disclosure: none`). No trailer to add.

### 5. Questions for you (not in the description)
1. What is the late-fee rate? 0.015 per day is a default in the code, and I found no ticket or doc stating it. Is it meant to be a flat 1.5% per day, with no cap and no compounding? The description states what the code does.
2. Can you paste the PAY-12 ticket text, or give me its link? The description cites only the key and has no link.
3. Do you want a grace period or a cap on the fee? The code has neither, and the description does not claim one.

Comprehension check (optional, explain each in your own words):
- `ledgerlite/fees.py:1-1` (the `rate=0.015` default)
- `ledgerlite/fees.py:3-4` (the `days_late <= 0` boundary returning 0)
- `ledgerlite/fees.py:5-5` (the `round(..., 2)` of a float product)
- `tests/test_fees.py:10-11` (`late_fee(100, 2) == 3.0`)

### 6. State
- Saved: `.pr-ready/pr-description.md` (git-ignored; `git check-ignore -q` exit 0).
- `.pr-ready/.gitignore` did not exist and was not tracked, so I created it with the line `pr-description*.md`. It shows as untracked (`?? .pr-ready/.gitignore`). It is not committed.
- Evidence note recorded: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 0".
- Not opened: awaiting confirmation. The branch has no upstream and `glab` is not installed, so by Step 7 it falls back to the `none.md` flow and the dev opens the MR by hand. For reference, the GitLab adapter commands, to run only after you confirm each one:
  - `git push -u origin feat/PAY-12-late-fee`
  - `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices" --description "$(cat .pr-ready/pr-description.md)"`
- Tree: HEAD is still `5027869`, with no new commit. The only new untracked path is `.pr-ready/.gitignore`; the draft and the evidence file are ignored.
