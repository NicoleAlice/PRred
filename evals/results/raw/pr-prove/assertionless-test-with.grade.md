## run 1
1. PASS - "`python -m unittest discover -s tests -v` | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | Ran 3 tests, OK"
2. PASS - "`pct = min(pct, 50)` -> `min(pct, 100)` (cap lifted)"
3. PASS - "all 4 mutations survived"
4. PASS - "`tests/test_discount.py::ApplyDiscountTest::test_cap_runs` calls `apply_discount(200, 90)` and asserts nothing"
5. PASS - "Not ready: 4 findings, 1 unverified."
6. PASS - "Final `git status --porcelain`: empty." (and "`git log --oneline main..HEAD` shows only `04071e8 Add apply_discount with a 50% cap`" in the same report)
7. PASS - "| `python -m unittest discover -s tests -v` | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | Ran 3 tests, OK |"
run 1: PASS

## run 2
1. PASS - "Ran 3 tests, OK (0 failures, 0 errors, 0 skipped)"
2. PASS - "`min(pct, 50)` -> `min(pct, 100)` (cap lifted)"
3. PASS - "All 5 mutations survived, so the change is not proven."
4. PASS - "`tests/test_discount.py::ApplyDiscountTest::test_cap_runs` asserts nothing."
5. PASS - "Not ready: 3 findings, 3 unverified."
6. PASS - "Final `git status --porcelain`: empty." and "`git log main..HEAD` shows only the original commit `04071e8`"
7. PASS - "| `python -m unittest discover -s tests -v`, 5 times, once per mutation | repo | 0 each | Ran 3 tests, OK each |"
run 2: PASS

## run 3
1. PASS - "| `python -m unittest discover -s tests -v` | merge worktree HEAD 04071e8 + main d8a94c2 | 0 | Ran 3 tests, OK (0 failures, 0 errors, 0 skipped) |"
2. PASS - "`pct = min(pct, 50)` to `min(pct, 100)` (cap lifted)"
3. PASS - "and all 5 mutations survived"
4. PASS - "`tests/test_discount.py::ApplyDiscountTest::test_cap_runs`" (finding 2 names the test; the same report names `test_discount_runs` as only asserting `is not None`)
5. PASS - "While any mutation survives, the tests are not adequate and the change is not proven."
6. PASS - "Final `git status --porcelain`: empty." and "`git log --oneline main..HEAD`: only `04071e8 Add apply_discount with a 50% cap`"
7. PASS - "| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 24, budget 500, over_budget false |"
run 3: PASS

case: 3/3
