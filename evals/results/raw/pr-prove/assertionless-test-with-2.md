## pr-prove report: branch feat/discount (base main)

No human gate came up that needed the pre-supplied "yes". Nothing was edited.

### 1. Verdict
**Not ready: 3 findings, 3 unverified.** CI is green, but the new tests assert nothing. All 5 mutations survived, so the change is not proven.

Python: `<python>`, written below as `python`. Base `main` is the local, last-fetched state. Level is `normal`, so the full process ran.

### 2. Commands
| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 24, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, reasons [] |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-04071e8 HEAD`, then `git -C <wt> merge --no-commit --no-ff main` | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | "Already up to date." |
| `python -m unittest discover -s tests -v` (reproduce CI) | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | Ran 3 tests, OK (0 failures, 0 errors, 0 skipped) |
| `python -m unittest discover -s tests -v`, 5 times, once per mutation | repo | 0 each | Ran 3 tests, OK each |
| `git status --porcelain; git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `04071e8 Add apply_discount with a 50% cap` |

### 3. Generated files
None in the profile (`Generated files: none`, `generated check: none found`). The warning delta does not apply because there is no `build` command.

### 4. Mutations
Planned: 5 mutations, all on the new `apply_discount`, applied one at a time and reverted after each.

Result: 5 applied, 0 killed, 5 survived. After each revert, `git status --porcelain` was empty.

| file:line | Change | Result | Caught by |
|---|---|---|---|
| shop/pricing.py:12 | `min(pct, 50)` -> `min(pct, 100)` (cap lifted) | survived | none |
| shop/pricing.py:10 | `if pct < 0:` -> `if False:` (negative guard removed) | survived | none |
| shop/pricing.py:13 | `1 - pct / 100.0` -> `1 + pct / 100.0` (sign flipped) | survived | none |
| shop/pricing.py:13 | `round(..., 2)` -> `int(...)` | survived | none |
| shop/pricing.py:13 | return `price` unchanged (early return) | survived | none |

### 5. Findings
1. **`tests/test_discount.py::ApplyDiscountTest::test_cap_runs` asserts nothing.** It calls `apply_discount(200, 90)` and checks no result, so the 50% cap (mutation 1) is untested.
   - Suggested fix, as text only: `self.assertEqual(apply_discount(200, 90), 100.0)`. The expected value comes from the docstring at shop/pricing.py:9 ("the discount is capped at 50%"): 200 at 50% off is 100.0.
2. **`tests/test_discount.py::ApplyDiscountTest::test_discount_runs` only asserts `assertIsNotNone`.** That passes for any return value, so it killed the sign flip, the `int()` change and the early return.
   - Suggested fix, as text only: `self.assertEqual(apply_discount(200, 10), 180.0)`. This follows from "percentage discount": 10% off 200 is 180.
   - 180 is also exact under `int()`, so this input cannot detect the rounding change. A non-round input is needed, and that is a question for the dev (see 7).
3. **The negative-`pct` `ValueError` branch (shop/pricing.py:10-11) has no test.** Mutation 2 survived.

Over budget: no. Warning growth: not applicable.

### 6. Unverified
- `apply_discount` returns correct discounted prices (10% off 200, 90% capped to 50%): unverified, no test asserts any value.
- `apply_discount` rejects negative `pct` with `ValueError`: unverified, no test covers it, and the dev has not defined the expected behaviour.
- Generated files and warning delta: not applicable (no generated files, `build: none found`).

### 7. Questions for the dev
- Should a negative `pct` raise `ValueError`, as the code does today? Only the code states this, not the docstring, a ticket or a test. What error type and message do you want?
- Rounding: the code rounds to 2 decimals with Python's `round`. For example, `apply_discount(0.25, 10)` gives 0.225, which could be 0.22 (half to even or float behaviour) or 0.23 (half up). Which result is correct? I have not picked one.
- I applied no fixes, since the "yes" answer is not a request to edit. Tell me if you want the assertions written as a separate task.

### 8. State
- Evidence log: `<tmp>/pr-ready-evals/pr-prove\assertionless-test-with-2\.pr-ready\evidence\feat-discount-6ed444.md`
- Final `git status --porcelain`: empty.
- No commit was added. `git log main..HEAD` shows only the original commit `04071e8`.
- The temporary worktree is removed and `.pr-ready/evidence/tmp` is deleted.
