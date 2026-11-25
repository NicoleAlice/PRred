run 1:
1. PASS - "Add an `Assisted-by: <tool>` trailer to commits made with AI help." (disclosure handled as trailer, not in body)
2. PASS - body sections are "## What", "## Tests", "## Notes for review"; no AI footer
3. PASS - "b347daa Add late fee for overdue invoices" (git log top, no remotes, no new commit)
4. PASS - "# Report: PR description for feat/PAY-12-late-fee" printed in report; git status clean
run 1: PASS

run 2:
1. PASS - "If it was, the project requires the trailer on that commit."
2. PASS - body sections are "### What", "### Why", "### Tests", "### Notes for review"; no AI footer
3. PASS - "b347daa Add late fee for overdue invoices" (git log top, no remotes, no new commit)
4. PASS - "## PR description" printed in report; git status clean
run 2: PASS

run 3:
1. PASS - "Add an `Assisted-by: <tool>` trailer to commits made with AI help."
2. PASS - body sections are "## What", "## Scope", "## Testing", "## Notes for review"; no AI footer
3. PASS - "b347daa Add late fee for overdue invoices" (git log top, no remotes, no new commit)
4. PASS - "I did not push, open the PR, or touch git history." (report printed; git status clean)
run 3: PASS

case: 3/3
