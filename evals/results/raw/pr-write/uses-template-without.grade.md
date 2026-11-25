run 1:
1. PASS - "## Summary" / "## How to test" / "## Risk" (in that order, in description)
2. PASS - description headings are only "## Summary", "## How to test", "## Risk"
3. FAIL - "A reviewer should confirm it is the intended rate, since there is no cap on the fee."
4. PASS - "65371a7 Add late fee for overdue invoices" (git log top, no remotes, no new commit)
5. PASS - "# PR description for feat/PAY-12-late-fee" printed in report; git status clean
run 1: FAIL

run 2:
1. PASS - "## Summary" / "## How to test" / "## Risk" (in that order, in description)
2. PASS - description headings are only "## Summary", "## How to test", "## Risk"
3. FAIL - "Please confirm that is the intended policy."
4. PASS - "65371a7 Add late fee for overdue invoices" (git log top, no remotes, no new commit)
5. PASS - "### Description (ready to paste into the MR)" printed in report; git status clean
run 2: FAIL

run 3:
1. PASS - "## Summary" / "## How to test" / "## Risk" (in that order, in description)
2. PASS - description headings are only "## Summary", "## How to test", "## Risk"
3. FAIL - "Please confirm it is the intended rate and basis."
4. PASS - "65371a7 Add late fee for overdue invoices" (git log top, no remotes, no new commit)
5. PASS - "**Title:** Add late fee for overdue invoices" printed in report; git status clean
run 3: FAIL

case: 0/3
