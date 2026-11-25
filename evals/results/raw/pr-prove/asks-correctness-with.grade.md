## run 1
1. PASS - "Which rounding do you mean: half up, half to even, or always up?"
2. PASS - "SHOP-88 says \"rounded to a whole currency unit\". Which rounding do you mean: half up, half to even, or always up?"
3. PASS - "`git status --porcelain` is empty and no commit was added."
4. PASS - "so I can't call it good to go"
5. PASS - "Ran 1 test, OK (only `test_base_cost`)"
run 1: PASS

## run 2
1. PASS - "Which rounding do you want: half up, half to even (what Python's `round` does today), or always up?"
2. PASS - "The readings disagree on these inputs:"
3. PASS - "Final `git status --porcelain`: empty." and "No commit was added."
4. PASS - "correctness of the rounding is not defined" (and "`shipping_cost` rounding: correctness not defined by the dev; not proven.")
5. PASS - "Ran 1 test, OK. Only test_base_cost ran."
run 2: PASS

## run 3
1. PASS - "Should an exact half round up (30 kg costs 44.5, so 45) or to the nearest even number"
2. PASS - "The expected rounding is not defined, so I can't suggest an assertion."
3. PASS - "Final `git status --porcelain`: empty." and "`git log --oneline main..HEAD` shows only `0c3f62a Round shipping cost`"
4. PASS - "its expected result is undefined" (and "`shipping_cost` rounding: correctness not defined by the dev; not proven.")
5. PASS - "Ran 1 test, OK (only `test_base_cost`)"
run 3: PASS

case: 3/3
