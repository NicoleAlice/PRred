## pr-write report: feat/PAY-12-late-fee (HEAD 5027869, base main)

**1. Policy**
- ai_description: allowed. Quote: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: a description, not a facts list.
- ai_disclosure: none. Quote: "Contributors need not mention the tools they used". The body has no AI mention and no generated-by footer.
- No PR template (profile: `pr template: none`), so the pr-format.md sections are used.

**2. Evidence**
- Evidence missing. `evidence.py show --json` returned no entries for HEAD 5027869, and there are no stale entries either.
- Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again.
- I ran no tests myself. The Tests section says only that evidence is missing, and the body gives no test count and no "passes", "tested" or "verified".

**3. Title**

`Add late fee for overdue invoices`

(Commit-subject shape, free-form commit format. It matches the branch's only commit subject.)

**Draft** (saved as is):

```
PAY-12

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: it returns 0 when `days_late` is 0 or negative, otherwise `amount * rate * days_late` rounded to 2 decimals.

## Why

Overdue invoices had no late fee. The PAY-12 ticket text was not available, so this reason comes from the commit subject only, and the 1.5% default rate is not stated in any ticket or doc I could read.

## Impact

Adds a new module and a new test file and changes no existing file. Nothing in the diff calls `late_fee` yet, so no invoice total or other caller changes.

## Focus

The weakest point is the default `rate=0.015`: it is applied per day late, grows linearly with `days_late`, and its source is not stated anywhere. The rounding to 2 decimals and the `days_late <= 0` boundary were checked by reading only; the new tests in `tests/test_fees.py` (`test_on_time`, `test_late`) cover `days_late` of 0 and 2 and no other value.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.
```

Size: 16 hand-written lines (budget 500), 2 files.

**4. Disclosure**
None required (`ai_disclosure: none`), so there is no trailer and no body mention.

**5. Questions for you (not in the description)**
1. What does PAY-12 say? The branch name gives the key only, the tracker is `none`, and no ticket text was pasted. Paste it so Why can state the real problem. The first line of the body is just `PAY-12`, not a link.
2. Where does the 1.5% per day default rate come from? No ticket or doc states it. The draft names the gap in Why and Focus. If it is a business rule, say so and I will cite it. If it is a placeholder, say so.
3. Should the fee scale linearly per day (`amount * rate * days_late`) with no cap? That is what the code does and what the draft says. Tell me if the ticket says otherwise.

Comprehension check (optional; explain each in your own words):
- `ledgerlite/fees.py:1-1` (default `rate=0.015`)
- `ledgerlite/fees.py:3-4` (`days_late <= 0` returns 0)
- `ledgerlite/fees.py:5-5` (`round(..., 2)` on the product)
- `tests/test_fees.py:10-11` (`late_fee(100, 2) == 3.0`)

**6. State**
- Saved to `.pr-ready/pr-description.md`. It is git-ignored: `.pr-ready/.gitignore` was untracked, so I created it with the line `pr-description*.md`, and `git check-ignore` exits 0 for the draft.
- Evidence note recorded: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 0".
- No new commit. HEAD is still 5027869. `git status --porcelain` shows only `?? .pr-ready/.gitignore`. The profile and evidence files are not listed because the repo's ignore rules cover them or they were already present.
- Not opened: awaiting confirmation. Host is gitlab and `glab` is the adapter. Nothing has been run. The commands I would show, each behind its own "Run this?":
  1. `git push -u origin feat/PAY-12-late-fee` (the branch has no upstream)
  2. `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices" --description "$(cat .pr-ready/pr-description.md)"`

Recommendation: run `pr-prove` first, then `pr-write` again, so the Tests section carries real evidence before the MR goes up.

Gate note: no human gate needed a pre-supplied answer. The ticket content question is reported above instead of stopping the draft.
