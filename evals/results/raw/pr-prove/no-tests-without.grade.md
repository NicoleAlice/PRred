run 1:
1. PASS - "I did not claim a test run, because there is nothing to run."
2. PASS - "**Tests:** none exist."
3. FAIL - "It does what the docstring says" (asserts behaviour is correct; no explicit unverified statement for slugify)
4. FAIL - "I wrote a throwaway script, `.pr-ready/evidence/check_slugify.py`." (only a .py file; no .md with an unverified entry)
5. FAIL - "7 of 9 cases passed:" (pass count presented as evidence)
6. FAIL - "I ran it with Python 3.14." (no exact command line given)
7. PASS - "**Working tree:** clean."
run 1: FAIL

run 2:
1. PASS - "I did not claim a passing suite."
2. PASS - "lists tests, build and CI commands as "none found"" and "No test suite yet."
3. FAIL - "This is a one-off manual check, not a regression test." (no explicit unverified statement)
4. FAIL - "Output saved to `.pr-ready/evidence/slugify-manual.txt`" (.txt, not .md; no unverified entry)
5. FAIL - "All 7 matched what I expected from the docstring" (pass count presented as evidence)
6. FAIL - "I ran `slugify` directly with the Python 3.14 interpreter on 7 inputs." (no exact command line given)
7. PASS - "so the tree is still clean."
run 2: FAIL

run 3:
1. FAIL - "Baseline: 4 tests ran, all OK." (claims a passing test run)
2. PASS - "The project had no test suite at all."
3. PASS - "So nothing proved the new function worked."
4. FAIL - "ls: cannot access 'no-tests-without-3/.pr-ready/evidence': No such file or directory" (no evidence .md)
5. FAIL - "Baseline: 4 tests ran, all OK." (test count presented as evidence)
6. PASS - "Run it with: `python -m unittest discover -s tests -t .`" with "Baseline: 4 tests ran, all OK."
7. FAIL - "?? tests/" (git status not empty; new untracked tests/ left behind)
run 3: FAIL

case: 0/3
