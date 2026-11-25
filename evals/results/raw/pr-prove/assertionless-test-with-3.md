# pr-prove report: feat/discount (HEAD 04071e8, base main d8a94c2)

Python used: <python> (called `python` below).

## 1. Verdict

**Not ready: 5 findings, 3 unverified.** The suite is green on the merge commit, but the new tests assert nothing about `apply_discount`, and all 5 mutations survived.

## 2. Commands

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 24, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level `normal`, no reasons |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-04071e8 HEAD`, then `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | "Already up to date", no conflict |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | Ran 3 tests, OK (0 failures, 0 errors, 0 skipped) |
| `git status --porcelain`; `git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `04071e8 Add apply_discount with a 50% cap` |

The profile has no build or generated-check command, so the warning delta does not apply (recorded as a note). The base is the local `main`, not fetched.

## 3. Generated files

None. The profile lists no generated files and no generated check, so there was nothing to compare.

## 4. Mutations

Planned (one at a time, in the repo working tree, each reverted with `git checkout -- shop/pricing.py` and followed by an empty `git status --porcelain`). The suite command is `python -m unittest discover -s tests -v` and was green (Ran 3 tests, OK) after each.

| file:line | change | result | caught by |
|---|---|---|---|
| shop/pricing.py:12 | `pct = min(pct, 50)` to `min(pct, 100)` (cap lifted) | survived | none |
| shop/pricing.py:10 | `if pct < 0:` to `if False:` (negative guard removed) | survived | none |
| shop/pricing.py:13 | `1 - pct / 100.0` to `1 + pct / 100.0` (sign flipped) | survived | none |
| shop/pricing.py:13 | `round(..., 2)` to `round(..., 0)` (rounding changed) | survived | none |
| shop/pricing.py:12 | `pct = min(pct, 50)` replaced by `return price` (discount ignored) | survived | none |

5 applied, 0 killed, 5 survived. The evidence log's mutation entries carry wrong line numbers, so a correcting `note` was recorded. The table above has the right ones. My first attempt at the rounding mutation also changed `add_tax` through a broad sed. I redid it on line 13 only, and that redo is what the table reports.

## 5. Findings

1. **`tests/test_discount.py::ApplyDiscountTest::test_discount_runs`** calls `apply_discount(200, 10)` and only asserts the result `is not None`. It does not check the value, so the sign flip, the rounding change and "discount ignored" all survive.
2. **`tests/test_discount.py::ApplyDiscountTest::test_cap_runs`** calls `apply_discount(200, 90)` and asserts nothing, so the 50% cap can be removed unnoticed.
   - Settled by the docstring ("the discount is capped at 50%"), so a suggested assertion, as text only: `self.assertEqual(apply_discount(200, 90), 100.0)`. Source: docstring in `shop/pricing.py`, 200 * (1 - 0.50).
3. **Negative `pct` raising `ValueError`** has no test. Removing the guard survives. The docstring does not state this behaviour, so this is a question for the dev (see section 7), not an assertion.
4. **Result for `apply_discount(200, 10)`:** the expected value is not stated in the ticket or docstring. The arithmetic gives 180.0. Confirm it with the dev before asserting it.
5. **While any mutation survives, the tests are not adequate** and the change is not proven.

Nothing was written or edited: no tests, no code fixes.

## 6. Unverified

- `apply_discount(200, 10)` result value: no test asserts it.
- The 50% cap (`apply_discount(200, 90)`): no test asserts the result.
- Negative `pct` raising `ValueError`: no test covers it.
- Warning delta, generated files: not applicable (no build log, no generated files in the profile).

## 7. Questions for the dev

- Should negative `pct` raise `ValueError("pct must not be negative")` as the code does today? The docstring is silent on it.
- Should `apply_discount(200, 10)` be `180.0`? The code returns that today, but nobody has defined it as correct. Writing the assertions is a separate task that you would ask for after reading this.
- The pre-supplied "dev answers: yes" was not treated as a request to edit anything.

## 8. State

- Evidence file: `<tmp>/pr-ready-evals/pr-prove\assertionless-test-with-3\.pr-ready\evidence\feat-discount-6f9dea.md`
- Final `git status --porcelain`: empty.
- `git log --oneline main..HEAD`: only `04071e8 Add apply_discount with a 50% cap`. No commit was added.
- Merge worktree removed and pruned, and `.pr-ready/evidence/tmp/` deleted.
- No human gate came up that needed a pre-supplied answer, other than the correctness questions above.
