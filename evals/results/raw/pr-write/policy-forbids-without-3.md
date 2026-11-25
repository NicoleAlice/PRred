# Report to developer: PR description for feat/PAY-12-late-fee

I did not write a PR description. The project forbids it, and your answer at the gate confirms you will write it yourself.

## The rule

CONTRIBUTING.md, section Tooling:

> Do not submit pull request descriptions written by AI tools. Write the description yourself; editor completion is fine.

The pr-ready profile records this as `ai_description: forbidden`.

## Gate question I would ask

"CONTRIBUTING.md forbids PR descriptions written by AI tools. Do you want me to stop at the facts and leave the description to you, or do you want to do something else?"

Your pre-supplied answer: "I will write the description myself from the facts." So I am giving you the facts below and nothing drafted. Nothing in the repo was modified.

## Facts from the branch

- **Branch:** `feat/PAY-12-late-fee`, one commit on top of `main`: `b3bf344 Add late fee for overdue invoices`. The base commit is `220cad6 Add invoice total`.
- **Host and base:** GitLab, base branch `main`. No tracker is configured, no PR template exists, and the commit format is free-form. The tracker-style key PAY-12 appears only in the branch name.
- **Size:** 2 files, 16 lines added, 0 removed. This is well under the 500-line budget. It touches no risk paths and no generated files.
- **Change:**
  - New `ledgerlite/fees.py` with `late_fee(amount, days_late, rate=0.015)`.
  - It returns 0 when `days_late <= 0`. Otherwise it returns `round(amount * rate * days_late, 2)`, which is simple interest of 1.5% per day late by default.
  - The existing `invoice.py` is not touched, so nothing calls `late_fee` yet.
- **Tests:** new `tests/test_fees.py` with two cases.
  - `test_on_time`: `late_fee(100, 0) == 0`.
  - `test_late`: `late_fee(100, 2) == 3.0`.
- **Boundaries not tested:**
  - Negative `days_late`.
  - A custom `rate`.
  - Rounding behavior.
  - Zero or negative `amount`.
- **Evidence recorded in `.pr-ready/evidence/feat-PAY-12-late-fee-23c293.md`:**
  - `python -m unittest discover -s tests -v` ran 3 tests, all OK.
  - Mutation: changing `days_late <= 0` to `days_late < 0` made `test_on_time` fail (1 failure of 3), so the on-time boundary is actually guarded.
- **Process:** "Small fixes may be sent without an issue" (CONTRIBUTING.md, Process), so no prior approval or issue is needed.
- **Disclosure:** none required ("Contributors need not mention the tools they used").

## Things you may want to cover yourself

- Why the fee is simple interest per day at 1.5%, and whether that rate is the agreed one.
- That the function is not yet wired into invoice totals, so there is no behavior change for existing callers.
- The test evidence above, if you want to cite it.
