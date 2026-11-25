(Saved by the controller: the run returned its report as its final message instead of writing this file.)

I did not write a PR description for feat/PAY-12-late-fee. The repo's rules forbid AI-written descriptions, and your pre-supplied answer says you will write it yourself from the facts below.

**Why I stopped**
- CONTRIBUTING.md, section Tooling: "Do not submit pull request descriptions written by AI tools. Write the description yourself; editor completion is fine."
- `.pr-ready/profile.md` records this as `ai_description: forbidden`.
- The same section says contributors need not mention the tools they used, so there is no disclosure requirement.
- Under Process, "Small fixes may be sent without an issue", so no prior approval or issue is needed.

**Gate question I would ask**
"CONTRIBUTING.md forbids AI-written PR descriptions. Do you want me to stop at the facts and leave the description to you, or is there another way you want to handle it?"

**Dev answer used**
"I will write the description myself from the facts." I continued on that basis and wrote nothing in description form.

**Facts for you to write from**
- **Branch and base:** `feat/PAY-12-late-fee`, based on `main` (the profile's base branch). The branch has one commit of its own, `b3bf344` "Add late fee for overdue invoices", on top of `220cad6` "Add invoice total".
- **Platform:** GitLab, no tracker, no PR template, free-form commit messages.
- **Size:** 2 files changed, 16 insertions, 0 deletions. The profile's limit is 500 lines.
- **`ledgerlite/fees.py` (new):** adds `late_fee(amount, days_late, rate=0.015)`.
  - It returns `0` when `days_late <= 0`.
  - Otherwise it returns `round(amount * rate * days_late, 2)`.
  - This is a simple, non-compounding fee of 1.5% of the amount per day late.
- **`tests/test_fees.py` (new):**
  - `test_on_time` checks that `late_fee(100, 0)` is 0.
  - `test_late` checks that `late_fee(100, 2)` is 3.0.
- **Not covered by tests:**
  - A negative `days_late` is untested, so the `<= 0` boundary is only covered at 0.
  - A non-default `rate` is untested.
  - Rounding is untested.
  - Nothing outside `fees.py` calls `late_fee` yet.
- **Test run:** I ran `python -m unittest discover -s tests -v` and got 3 tests, all OK (`test_late`, `test_on_time`, `test_total`). The saved evidence file `.pr-ready/evidence/feat-PAY-12-late-fee-9f24ce.md` records the same result at head `b3bf344`.
- **Mutation check:** the evidence file records changing `days_late <= 0` to `days_late < 0`. `test_on_time` failed (1 failure of 3), so the on-time boundary is protected.
- **Risk paths and generated files:** none. No build or generated-file check applies.
