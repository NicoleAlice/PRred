# pr-write report: feat/PAY-12-late-fee

## 1. Policy
- ai_description: allowed. Quote: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: full description.
- ai_disclosure: none. Quote: "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). The body has no AI mention and no generated-by footer.
- Template: `.gitlab/merge_request_templates/default.md` (headings `## Summary`, `## How to test`, `## Risk`). I used those headings in that order and added none. The template has no HTML comments or checkboxes.

## 2. Evidence
Both entries are usable (head 65371a7 equals HEAD, stale: false). There are no stale entries.
- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK
- Mutation: changed `days_late <= 0` to `days_late < 0` in late_fee: test_on_time failed (1 failure of 3)

I did not run anything myself. I did not put the mutation in the description (see question 1).

## 3. Title
Add late fee for overdue invoices

The profile's commit format is free-form. This matches the branch's commit subject, and the ticket text was not available to word it differently.

## Draft (saved as written)

```
## Summary

Ticket: PAY-12

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: the fee for an invoice paid `days_late` days after its due date, charged as `amount * rate * days_late` per day late and rounded to 2 decimals. It returns `0` when `days_late` is 0 or negative.

Why: overdue invoices had no fee calculation in ledgerlite. The PAY-12 text was not available when this was written, so the reason beyond that is not stated here.

Impact: nothing else is reached. The function is new, nothing in `ledgerlite/invoice.py` or elsewhere calls it yet, and no existing file changes.

## How to test

`python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK

New tests in `tests/test_fees.py`: `test_on_time` (0 days late gives 0) and `test_late` (100 invoiced, 2 days late gives 3.0).

## Risk

Weakest point: the default `rate=0.015` (1.5% per day late) is not stated in any ticket or doc available here. The only check on it is `test_late`, which restates the same value, so it confirms the arithmetic and not that 1.5% is the right rate.

The boundary at `days_late == 0` and the treatment of negative `days_late` as no fee are covered by `test_on_time` for 0 only. Negative values and fractional-cent rounding have no test.
```

## 4. Disclosure
Nothing to add. ai_disclosure is none, so there is no trailer and no body mention.

## 5. Questions for you (not in the description)
1. The recorded mutation looks wrong. With `days_late < 0`, `late_fee(100, 0)` falls through to `round(100 * 0.015 * 0, 2)`, which is `0.0`. `assertEqual(0.0, 0)` passes, so `test_on_time` should not fail. The log says it did. I left the mutation out of "How to test" rather than quote a result I doubt, and I did not rerun it (pr-write may not). Please re-run `pr-prove` on that mutation. If it survives, the `days_late == 0` boundary is untested and Risk should say so. If it really fails, tell me how, and I will add the line.
2. Is 1.5% per day the intended rate, and is the fee meant to be per day late (simple, not compounding)? Neither is stated anywhere I could read. The description says so under Risk and does not ask the reviewer.
3. What does PAY-12 say? There is no tracker, and the branch name gives only the key. The "Why" is limited to what the diff shows. If you paste the ticket text, I will put the real motivation in and add a link.
4. Is the missing ticket link acceptable? The line `Ticket: PAY-12` is key only, with no URL.

Comprehension check (optional; explain each in your own words):
- `ledgerlite/fees.py:1-1` (default `rate=0.015`)
- `ledgerlite/fees.py:3-4` (`<= 0` returns the int `0`, so negatives get no fee)
- `ledgerlite/fees.py:5-5` (rounding to 2 decimals after multiplying by `days_late`)
- `tests/test_fees.py:8-8` (assertion that carries the boundary at 0)

## 6. State
- Saved: `.pr-ready/pr-description.md`. It is git-ignored (`git check-ignore` exits 0). I created `.pr-ready/.gitignore` with the line `pr-description*.md`.
- Evidence note added to `.pr-ready/evidence/feat-PAY-12-late-fee-6b3143.md`. It records that the description was saved, the template path, and usable evidence 2, stale 0.
- Open command (GitLab, `glab`). Not run, awaiting your confirmation for each step.
  - Push (the branch has no upstream): `git push -u origin feat/PAY-12-late-fee`. Run this?
  - Create the draft MR: `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices" --description "$(cat .pr-ready/pr-description.md)"`. Run this?
- Tree check: HEAD is still 65371a7 with no new commit. The only new path is untracked `.pr-ready/.gitignore`, which is under `.pr-ready/`.
