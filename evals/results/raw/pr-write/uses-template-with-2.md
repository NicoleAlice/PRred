## pr-write report: feat/PAY-12-late-fee

**Policy**
- `ai_description: allowed`. Quote: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). I wrote the full description, not a facts list.
- `ai_disclosure: none`. Quote: "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). The body has no AI mention and no generated-by footer, and I suggest no trailer.
- Template: `.gitlab/merge_request_templates/default.md` has the headings Summary, How to test and Risk. I used those headings, in that order, and added none.

**Evidence**
- Two usable entries at HEAD `65371a7`, both `stale: false`. No stale entries.
- Command: `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK.
- Mutation: `days_late <= 0` changed to `days_late < 0` in `late_fee`. `test_on_time` failed (1 failure of 3).
- I ran no tests or mutations myself.

**Title**

`Add late fee for overdue invoices`

The commit format is free-form. The ticket is only a key (PAY-12) and the tracker is none, so I used the commit subject. The title goes with the open command, not in the body.

**Draft** (saved as `.pr-ready/pr-description.md`)

```
## Summary

PAY-12: adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`, which returns the fee for an invoice paid `days_late` days after its due date.

The fee is `amount * rate * days_late` rounded to 2 decimals, charged per late day without compounding. It returns `0` when `days_late` is 0 or negative.

The default rate of 1.5% per day is not stated in any ticket or doc available to this PR.

Nothing calls `late_fee` yet, so no invoice behaviour changes. The change touches only `ledgerlite/fees.py` and `tests/test_fees.py` (16 hand-written lines).

## How to test

Run `python -m unittest discover -s tests -v`.

Recorded for this commit (`65371a7`): `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK

Mutation: changing `days_late <= 0` to `days_late < 0` in `late_fee` makes `test_on_time` fail (1 failure of 3).

New tests are in `tests/test_fees.py`: `test_on_time` (0 days late gives 0) and `test_late` (100 at 2 days late gives 3.0).

## Risk

Weakest point: the rate and rounding in `ledgerlite/fees.py:5`. Only one late case is tested (`late_fee(100, 2) == 3.0`), and no mutation was recorded on the rate, the multiplication or the `round`. The `<= 0` boundary at `ledgerlite/fees.py:3` was mutated and caught.

Out of scope: no upper cap on the fee and no compounding; the fee grows linearly with `days_late`. Non-numeric or negative `amount` is not validated.
```

**Disclosure**: none needed. No trailer and no body line.

**Questions for you (not in the description)**
1. What is the intended default late-fee rate? The 1.5% per day (`0.015`) is not in any ticket or doc, so I stated that as a gap in the Summary. No tracker is configured, so I could not fetch PAY-12.
2. Should the fee be simple (linear in days) with no cap, as coded? I described what the code does.
3. Do you have a PAY-12 link for the Summary? I only have the key from the branch name and did not guess the ticket's content.

Comprehension check (optional). Explain each in your own words:
- `ledgerlite/fees.py:1-1` (default `rate=0.015`)
- `ledgerlite/fees.py:3-4` (`days_late <= 0` returns `0`)
- `ledgerlite/fees.py:5-5` (`round(amount * rate * days_late, 2)`)
- `tests/test_fees.py:10-11` (the only late-case assertion)

**State**
- Saved to `.pr-ready/pr-description.md`. Git ignores it (`git check-ignore` exit 0).
- I created `.pr-ready/.gitignore` containing `pr-description*.md`. It did not exist before and is untracked.
- I recorded an evidence note: "pr-write: description saved to .pr-ready/pr-description.md; template .gitlab/merge_request_templates/default.md; usable evidence 2, stale 0".
- Not opened: awaiting your confirmation. Host is gitlab and this branch has no remote or upstream, so the push would also need confirming. If you confirm, the commands to run, each one only after your yes, are:
  - `git push -u origin feat/PAY-12-late-fee`
  - `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices" --description "$(cat .pr-ready/pr-description.md)"`

  Run this?
- No new commit. `git status --porcelain` shows only `?? .pr-ready/.gitignore`, and HEAD is still `65371a7`.
- I used Python 3.14 at `<python>`.
