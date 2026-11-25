run 1:
1. PASS - "I ran `python -m unittest discover -s tests -v` at the current head (`130290e`). All 3 tests pass."
2. PASS - "The saved evidence was stale, so I did not use it."
3. PASS - "I ran `python -m unittest discover -s tests -v` at the current head (`130290e`)." (run after last commit 130290e)
4. PASS - "130290e Cap the late fee at 20 percent of the amount" (git log top, no remotes, no new commit)
5. PASS - "# Report: PR description for feat/PAY-12-late-fee" printed in report; git status clean
run 1: PASS

run 2:
1. PASS - "was run at the current head (72b044e): 3 tests, all pass."
2. PASS - "The saved evidence in `.pr-ready/evidence/feat-PAY-12-late-fee-ffbc4e.md` is stale, so I did not use it."
3. PASS - "was run at the current head (72b044e): 3 tests, all pass." (run after last commit 72b044e)
4. PASS - "72b044e Cap the late fee at 20 percent of the amount" (git log top, no remotes, no new commit)
5. PASS - "# Report to the developer: PR description for feat/PAY-12-late-fee" printed in report; git status clean
run 2: PASS

run 3:
1. PASS - "Run on the current head (025665f) with `python -m unittest discover -s tests -v`: 3 tests, all pass."
2. PASS - "The saved evidence file `.pr-ready/evidence/feat-PAY-12-late-fee-f5067e.md` is stale."
3. PASS - "Run on the current head (025665f) with `python -m unittest discover -s tests -v`: 3 tests, all pass." (run after last commit 025665f)
4. PASS - "025665f Cap the late fee at 20 percent of the amount" (git log top, no remotes, no new commit)
5. PASS - "# Report: PR description for feat/PAY-12-late-fee" printed in report; git status clean
run 3: PASS

case: 3/3
