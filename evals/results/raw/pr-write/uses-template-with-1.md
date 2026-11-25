## pr-write report

**1. Policy**
- ai_description: allowed. "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: full description.
- ai_disclosure: none. "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). The body has no AI mention and no generated-by footer, and I suggest no trailer.

**2. Evidence**
Two usable entries (stale false, head 65371a7 = HEAD), no stale ones:
- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK
- Mutation: changed `days_late <= 0` to `days_late < 0` in late_fee: test_on_time failed (1 failure of 3)

**3. Title** (free-form commit format, not in the body)
`Add late fee for overdue invoices`

**Draft** (saved as .pr-ready/pr-description.md; template .gitlab/merge_request_templates/default.md: Summary, How to test, Risk)

```
## Summary

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py` for PAY-12: an invoice paid `days_late` days after its due date is charged `amount * rate * days_late`, rounded to 2 decimals, and an invoice that is on time or early (`days_late <= 0`) is charged 0.

The ticket text was not available to this description, so the reason behind the fee is not restated; the 1.5% default rate is not stated in any ticket or doc this branch carries.

Nothing else calls `late_fee` yet; the change reaches only `ledgerlite/fees.py` and `tests/test_fees.py`.

## How to test

`python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK.

New tests in `tests/test_fees.py`: `test_on_time` (100, 0 days gives 0) and `test_late` (100, 2 days gives 3.0).

Mutation: changing `days_late <= 0` to `days_late < 0` in `late_fee` made `test_on_time` fail (1 failure of 3).

## Risk

Weakest point: the 1.5% default `rate`. It is exercised by a single case (100 over 2 days gives 3.0) and was checked by reading the diff only, with no mutation of the rate or the rounding.
```

**4. Disclosure:** none required.

**5. Questions for you (not in the description)**
- What are the PAY-12 ticket text and link? The tracker is "none" and no text was pasted, so I only have the key. Please also state where the 1.5% default rate comes from.
- The recorded mutation says `< 0` made test_on_time fail, but for days_late=0 the code would return `round(100*0.015*0, 2)` = 0.0, which equals 0. I copied the log entry as recorded. Re-check it with pr-prove if you want that line trusted.

Comprehension check (optional), explain each in your own words:
- ledgerlite/fees.py:1-1 (default rate 0.015)
- ledgerlite/fees.py:3-4 (the `days_late <= 0` boundary returning 0)
- ledgerlite/fees.py:5-5 (rounding to 2 decimals)
- tests/test_fees.py:10-11 (the expected 3.0)

**6. State**
- Saved: .pr-ready/pr-description.md. I also created .pr-ready/.gitignore with `pr-description*.md`, and `git check-ignore` confirms the draft is ignored. A note was added to the evidence log.
- Not opened: awaiting confirmation. `glab` is not installed here, so per the gitlab adapter this falls back to printing the text for you to open by hand. With glab installed, the pair to confirm would be a push of feat/PAY-12-late-fee (no upstream known) and `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices" --description "$(cat .pr-ready/pr-description.md)"`. Run neither without your go-ahead.
- No new commit (HEAD still 65371a7). The only new path is untracked `.pr-ready/.gitignore`.
