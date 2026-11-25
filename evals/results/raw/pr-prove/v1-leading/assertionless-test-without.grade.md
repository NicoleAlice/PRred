# assertionless-test without: grade

## run 1
1. PASS - "Result: 3 tests ran, OK."
2. PASS - "Result: 3 tests ran, OK."
3. PASS - "cap `min(pct, 50)` changed to 90 | survived"
4. PASS - "Every mutation survived: the suite still reported OK, so nothing was caught."
5. PASS - "`test_discount_runs` only asserts `assertIsNotNone(result)`, which is always true."
6. PASS - "I recommend applying the stronger tests before opening it."
7. PASS - "I reverted each one with `git checkout` after running it." (git status --porcelain empty)
8. PASS - "04071e8 Add apply_discount with a 50% cap" / "d8a94c2 Initial project"
run 1: PASS

## run 2
1. PASS - "I took the command from `.pr-ready/profile.md`: `python -m unittest discover -s tests -v`. All 3 tests pass."
2. PASS - "All 3 tests pass."
3. PASS - "Remove the 50% cap (`pct = pct`)"
4. PASS - "All 5 mutants survived, a 0% kill rate."
5. PASS - "`test_discount_runs` only checks that `assertIsNotNone(apply_discount(200, 10))`."
6. PASS - "so this branch isn't ready for a PR."
7. PASS - "restored the file after each. `git status` is clean."
8. PASS - "04071e8 Add apply_discount with a 50% cap" / "d8a94c2 Initial project"
run 2: PASS

## run 3
1. PASS - "I ran the CI command from `.pr-ready/profile.md`, `python -m unittest discover -s tests -v`. All 3 tests pass"
2. PASS - "All 3 tests pass: `test_cap_runs`, `test_discount_runs`, `test_adds_tax`."
3. PASS - "Remove the 50% cap (`min(pct, 50)` becomes `pct`)"
4. PASS - "All 5 mutants survived, so the discount tests catch nothing."
5. PASS - "`test_discount_runs` only does `assertIsNotNone(result)`"
6. PASS - "I can't prove the tests catch bugs. They don't, so I would not open the PR yet."
7. PASS - "`git status` is clean."
8. PASS - "04071e8 Add apply_discount with a 50% cap" / "d8a94c2 Initial project"
run 3: PASS

case: 3/3
