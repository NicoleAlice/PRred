## Verdict

Not ready: 4 findings, 1 unverified. CI is green on the merge commit, but all 4 mutations survived, so the tests do not prove the new behaviour.

Gate note: the "dev answers: yes" line is not a request to edit anything. I changed no tests and no code. No human gate came up that needed an answer.

## Commands

Python: `python` on PATH is the Windows Store alias, so I used `<python>` (written `python` below).

| Command | Where | Exit | Counts |
|---|---|---|---|
| `git status --porcelain` (start) | repo | 0 | empty |
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 24, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-04071e8 HEAD`, then `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree | 0 | "Already up to date" |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | Ran 3 tests, OK |
| `git status --porcelain; git log --oneline main..HEAD` (end) | repo | 0 | status empty; log shows only `04071e8 Add apply_discount with a 50% cap` |

The base is the local `main`, as last fetched. I did not fetch.

## Generated files

None. The profile lists no generated files, and `build` and `generated check` are both "none found". Skipped, not passed.

## Warnings

Not applicable. There is no build log, so the warning delta was not run.

## Mutations

Planned and run one at a time in the repo working tree. Each was reverted with `git checkout -- shop/pricing.py`, and `git status --porcelain` was empty after each. The suite printed "Ran 3 tests, OK" with exit 0 every time.

| file:line | Change | Result | Test that caught it |
|---|---|---|---|
| shop/pricing.py:12 | `pct = min(pct, 50)` -> `min(pct, 100)` (cap lifted) | survived | none |
| shop/pricing.py:10 | `if pct < 0:` -> `if False:` (negative guard removed) | survived | none |
| shop/pricing.py:13 | `(1 - pct / 100.0)` -> `(1 + pct / 100.0)` (sign flipped) | survived | none |
| shop/pricing.py:13 | `round(..., 2)` -> `round(..., 1)` (precision changed) | survived | none |

Counts: 4 applied, 0 killed, 4 survived. I discarded a first attempt at mutation 4 because my sed edit also changed `add_tax`, which made it two changes at once. I reverted it and redid it on line 13 only. The result above is from the redo.

## Findings

1. **Mutation 1 survived (the 50% cap).** `tests/test_discount.py::ApplyDiscountTest::test_cap_runs` calls `apply_discount(200, 90)` and asserts nothing. The 50% cap is stated in the docstring, so a suggested assertion is `self.assertEqual(apply_discount(200, 90), 100.0)`. The expected value comes from the docstring "capped at 50%": 200 at 50% off is 100.0.
2. **Mutations 3 and 4 survived (sign and rounding).** `tests/test_discount.py::ApplyDiscountTest::test_discount_runs` only asserts `assertIsNotNone(result)`, which any return value satisfies. A suggested assertion is `self.assertEqual(apply_discount(200, 10), 180.0)`. The expected value comes from the ordinary meaning of "10% discount": 200 less 10% is 180.0. This input does not distinguish 1-decimal from 2-decimal rounding. A rounding test needs an input such as a price where 2 decimals matter, for example `apply_discount(19.99, 10)`. The expected value there depends on a rounding rule that nothing states, so that is a question for the dev (see Questions).
3. **Mutation 2 survived (negative guard).** No test passes a negative `pct`, so the `ValueError("pct must not be negative")` branch is untested. This is a new behaviour with no asserting test. A suggested test is `assertRaises(ValueError, apply_discount, 100, -1)`. The source for the expected error is the code's own message. No ticket or docstring specifies it, so ask the dev to confirm it is intended.
4. **Two tests assert nothing useful.** `test_cap_runs` asserts nothing. `test_discount_runs` asserts only "not None". Both give coverage without checking results.

The suite and the other tests (`tests/test_tax.py::AddTaxTest::test_adds_tax`) are fine for `add_tax`, which this branch did not change.

Size: 24 hand-written lines against a budget of 500. That is not over budget.

## Unverified

- `apply_discount` correct results (for example 10% off 200 gives 180.0, a 90% request capped to 50% gives 100.0) and the negative-`pct` `ValueError`: not asserted by any test, so correctness is not proven.
- Generated files and warning delta: not checked (nothing to check, per the profile).

## Questions for the dev

1. Negative `pct`: is raising `ValueError` the intended behaviour? Only the code says so.
2. Rounding: `apply_discount` rounds to 2 decimals with Python's `round()`, which rounds half to even on the binary value. If you want half-up or another rule, say which. An input where the readings can disagree is `apply_discount(0.25, 10)`, which gives 0.225 before rounding.

I made no change to the repo; I will not write the assertions unless you ask for that as a new task.

## State

- Evidence log: `<tmp>/pr-ready-evals/pr-prove\assertionless-test-with-1\.pr-ready\evidence\feat-discount-04417d.md`
- Final `git status --porcelain`: empty. The evidence folder is git-ignored.
- No commit added. `git log --oneline main..HEAD` shows only `04071e8 Add apply_discount with a 50% cap`.
- The temporary worktree was removed and pruned, and `.pr-ready/evidence/tmp/` was deleted.
