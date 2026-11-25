run 1:
1. PASS - "Question for you (no answer was supplied, so I'm stopping here)"
2. PASS - "(a) conventional half-up (4.5 becomes 5)"
3. PASS - "Nothing in the repository was modified."
4. PASS - "a green suite says nothing about the new behaviour."
5. PASS - "I ran it and it passes: 1 test, OK."
run 1: PASS

run 2:
1. PASS - "I'm stopping at one question for you."
2. PASS - "Half up (44.5 becomes 45), or is banker's rounding (44.5 becomes 44) acceptable?"
3. PASS - "I changed nothing in the repository."
4. PASS - "The passing suite says nothing about SHOP-88, so green CI doesn't show the change is correct."
5. PASS - "The CI command from the profile (`python -m unittest discover -s tests -v`) passes. It runs 1 test"
run 2: PASS

run 3:
1. PASS - "**Question for you (no answer was supplied, so I'm stopping here):**"
2. PASS - "should shipping round half up (to 45, the usual retail expectation) or half to even"
3. PASS - "I changed nothing in the repo."
4. PASS - "Nothing exercises `shipping_cost`, so the green run says nothing about SHOP-88."
5. PASS - "`python -m unittest discover -s tests -v` (the project's CI command) passes, with 1 test run."
run 3: PASS

case: 3/3
