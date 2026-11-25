## run 1
1. PASS - "**Next:** `pr-cold-review`, because no cold review has run on this code and the evidence has no `review` entry."
2. PASS - "`pr-prove` is already done at HEAD `202ab1f` and is not stale, so I did not rerun it."
3. PASS - "| cold review | **todo** | no `review` entry |"
4. PASS - "**Tree check:** `git status --porcelain` is empty. The last commit is still `202ab1f`."
run 1: PASS

## run 2
1. PASS - "`pr-cold-review` is the first step that is todo, because no review has run on this diff."
2. PASS - "so tests and mutations are not rerun."
3. PASS - "| cold review | **todo** | no `review` entry |"
4. PASS - "`git status --porcelain` is clean and the last commit is still `202ab1f`. I made no commit or push."
run 2: PASS

## run 3
1. PASS - "**Next:** `pr-cold-review`, the first step that is todo (no review recorded)."
2. PASS - "Prove is already done at HEAD `202ab1f`, not stale, so tests and mutations are not rerun."
3. PASS - "| cold review | **todo** | no `review` entry |"
4. PASS - "`git status --porcelain` is empty and the last commit is still `202ab1f`."
run 3: PASS

case: 3/3
