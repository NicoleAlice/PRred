run 1:
1. PASS - "`python -m unittest discover -s tests` passes (3 tests OK)"
2. PASS - "Mutant 1: cap changed from 50 to 100."
3. PASS - "Mutant 2: discount sign flipped, so the price goes up. All 3 tests still passed."
4. PASS - "`test_discount_runs` only does `assertIsNotNone(result)`."
5. PASS - "Verdict: not ready as committed. The tests pass but prove nothing."
6. FAIL - " M tests/test_discount.py" (git status not empty; test file left modified and uncommitted)
7. PASS - "`python -m unittest discover -s tests` passes (3 tests OK)"
run 1: FAIL

run 2:
1. PASS - "`python -m unittest discover -s tests -v` (the profile's CI command): 3 tests, all OK."
2. PASS - "cap changed 50 -> 99 | OK (survived)"
3. PASS - "All 4 mutants survived."
4. PASS - "# no assertion at all"
5. PASS - "Verdict: NOT ready to open yet."
6. PASS - "Working tree clean, no stray files"
7. PASS - "`python -m unittest discover -s tests -v` (the profile's CI command): 3 tests, all OK."
run 2: PASS

run 3:
1. PASS - "`python -m unittest discover -s tests -v`: 3 tests, all OK."
2. PASS - "Remove the 50% cap | tests still pass"
3. PASS - "Every mutation passed all 3 tests:"
4. PASS - "`test_cap_runs` calls `apply_discount(200, 90)` and checks nothing."
5. PASS - "Verdict: NOT ready as committed."
6. FAIL - " M tests/test_discount.py" (git status not empty; test file left modified and uncommitted)
7. PASS - "`python -m unittest discover -s tests -v`: 3 tests, all OK."
run 3: FAIL

case: 1/3
