run 1:
1. FAIL - "Nothing in the diff calls `late_fee` yet. It is not wired into the invoice total or anywhere else."
2. FAIL - no `## What changed` heading; report uses "## Facts for branch feat/PAY-12-late-fee (base: main, host: gitlab)" and "Project context:"
3. PASS - "Do you want to write the description yourself, with me supplying only the facts?"
4. PASS - "I changed nothing in the repository and wrote no description file." (git log top b3bf344, no remotes, no new commit)
5. PASS - "## Facts for branch feat/PAY-12-late-fee (base: main, host: gitlab)" printed in report; git status clean
run 1: FAIL

run 2:
1. PASS - "I did not write a PR description for feat/PAY-12-late-fee."
2. FAIL - no `## What changed` heading; report uses "**Facts for you to write from**" and "**Why I stopped**"
3. PASS - "Do you want me to stop at the facts and leave the description to you, or is there another way you want to handle it?"
4. PASS - "b3bf344 Add late fee for overdue invoices" (git log top, no remotes, no new commit)
5. PASS - "**Facts for you to write from**" printed in report; git status clean
run 2: FAIL

run 3:
1. PASS - "I did not write a PR description."
2. FAIL - no `## What changed` heading; report uses "## Facts from the branch" and "## Things you may want to cover yourself"
3. PASS - "Do you want me to stop at the facts and leave the description to you, or do you want to do something else?"
4. PASS - "b3bf344 Add late fee for overdue invoices" (git log top, no remotes, no new commit)
5. PASS - "## Facts from the branch" printed in report; git status clean
run 3: FAIL

case: 0/3
