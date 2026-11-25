## 1. Policy

- `ai_description: allowed`. Quote: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: a full description.
- `ai_disclosure: required-in-trailer`. Quote: "Add an `Assisted-by: <tool>` trailer to commits made with AI help" (CONTRIBUTING.md, Tooling). The body has no AI mention and no generated-by footer. The trailer goes on the commit instead (section 4).

## 2. Evidence

Two usable entries, both for HEAD `b347daa` (`stale: false`). No stale entries.
- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK
- Mutation: changed `days_late <= 0` to `days_late < 0` in `late_fee`: test_on_time failed (1 failure of 3)

I ran no tests myself.

## 3. Title and draft

Title: `Add late fee for overdue invoices (PAY-12)`

The draft below is saved, with no template (`pr template: none`), so it uses the pr-format sections.

```
Ticket: PAY-12 (from the branch name; no tracker connector and no ticket text available)

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: no fee when `days_late` is 0 or negative, otherwise `amount * rate * days_late` rounded to 2 decimals.

## Why

Overdue invoices had no way to compute a late fee; this adds the calculation for them (PAY-12).

## Impact

Reaches nothing beyond the two new files: `ledgerlite/fees.py` and `tests/test_fees.py`. No existing file changes and nothing calls `late_fee` yet.

## Focus

The weakest point is the `days_late <= 0` boundary and the 1.5% default `rate`, which no ticket or doc states. The boundary was checked with a mutation (`<=` changed to `<`), and `test_on_time` failed. The rate is covered only by the 2-day case in `test_late` and was not mutated.

## Tests

- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK
- Mutation: changed `days_late <= 0` to `days_late < 0` in `late_fee`: test_on_time failed (1 failure of 3)
```

Diff size: 16 hand-written lines across 2 files, under the 500 budget.

## 4. Disclosure (trailer for your commit)

The project requires the trailer on commits made with AI help. I did not amend or commit. If the commit `b347daa` ("Add late fee for overdue invoices") was made with AI help, add this line to its message:

```
Assisted-by: Claude Code
```

Use the tool name you actually used if it differs. The `<tool>` value is yours to confirm.

## 5. Questions for you (not in the description)

1. The ticket content for PAY-12 is not available (tracker: none, nothing pasted). I wrote Why from the diff and commit subject only. Paste the ticket text if you want Why to use its wording.
2. Neither a ticket nor a doc states the 1.5% default rate. The description says so in Focus as a fact. Is 1.5% per day the intended rate?
3. The `Out of Scope` section was omitted because there is no gap a reviewer would read as a bug. Say so if you want one.

Comprehension check (optional, does not block). Explain each in your own words:
- `ledgerlite/fees.py:1-1` (default `rate=0.015`)
- `ledgerlite/fees.py:3-4` (the `days_late <= 0` branch returns 0)
- `ledgerlite/fees.py:5-5` (`round(..., 2)` applied to `amount * rate * days_late`)
- `tests/test_fees.py:10-11` (the 2-day case expects `3.0`)

## 6. State

- Saved: `.pr-ready/pr-description.md`. `git check-ignore -q` exits 0, so it is ignored.
- I created `.pr-ready/.gitignore` (it did not exist) containing `pr-description*.md`. It is the only new untracked path, and it is under `.pr-ready/`.
- Evidence note recorded: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 2, stale 0".
- No commit, amend, stash or branch switch. HEAD is still `b347daa`.
- Not opened. The host is gitlab, but `glab` is not installed here and the branch has no upstream and no remote. When you have `glab` and a remote, the commands would be as follows. I have not run either, and each needs your confirmation ("Run this?"):
  1. `git push -u origin feat/PAY-12-late-fee`
  2. `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices (PAY-12)" --description "$(cat .pr-ready/pr-description.md)"`

  Without `glab`, open the MR by hand with the text above.
