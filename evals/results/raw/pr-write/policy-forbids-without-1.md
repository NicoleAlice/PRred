I did not write the PR description. This repo's CONTRIBUTING.md (section Tooling) says: "Do not submit pull request descriptions written by AI tools. Write the description yourself; editor completion is fine." The `.pr-ready/profile.md` records this as `ai_description: forbidden`.

Gate question I would ask: "CONTRIBUTING.md forbids PR descriptions written by AI tools. Do you want to write the description yourself, with me supplying only the facts?"

Dev answer (pre-supplied): "I will write the description myself from the facts."

So I am handing over facts only, with no drafted prose, title or section structure.

## Facts for branch feat/PAY-12-late-fee (base: main, host: gitlab)

Commits on the branch relative to main:
- b3bf344 "Add late fee for overdue invoices". This is the only commit ahead of main. Main is at 220cad6 "Add invoice total".

Diff (2 files, 16 lines added, nothing removed or modified):
- `ledgerlite/fees.py` (new, 5 lines) adds `late_fee(amount, days_late, rate=0.015)`.
  - It returns 0 when `days_late <= 0`.
  - Otherwise it returns `round(amount * rate * days_late, 2)`. That is a simple (non-compounding) fee of 1.5% of the amount per day late, rounded to 2 decimals.
  - The docstring reads: "Fee for an invoice paid days_late days after the due date."
- `tests/test_fees.py` (new, 11 lines) adds `LateFeeTest`.
  - `test_on_time`: `late_fee(100, 0) == 0`.
  - `test_late`: `late_fee(100, 2) == 3.0`.

Nothing in the diff calls `late_fee` yet. It is not wired into the invoice total or anywhere else.

Verification I observed:
- The recorded evidence in `.pr-ready/evidence/feat-PAY-12-late-fee-07100d.md` shows `python -m unittest discover -s tests -v` passing (3 tests, OK) at head b3bf344.
- That evidence also records a mutation check. Changing `days_late <= 0` to `days_late < 0` made `test_on_time` fail (1 failure of 3).
- I re-ran the tests just now and got 3 tests, OK.

Not covered by tests:
- Negative `days_late` is not tested.
- A custom `rate` is not tested.
- Rounding behaviour is not tested beyond the single case.

Project context:
- Tracker: none. The branch name mentions PAY-12, but no tracker is configured.
- PR template: none.
- Prior approval is not required for small fixes ("Small fixes may be sent without an issue").
- AI disclosure: none required.
- Size is 16 lines, well under the 500-line budget.
- No risk paths and no generated files.

I changed nothing in the repository and wrote no description file.
