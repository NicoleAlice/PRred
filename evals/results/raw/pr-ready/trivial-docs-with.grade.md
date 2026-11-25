## run 1
1. PASS - "2 files changed (`README.md`, `docs/usage.md`), 6 hand-written lines against a budget of 500."
2. PASS - "Mutations are n/a for the same reason: docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review."
3. PASS - "After that: `pr-prove` (size check only), `pr-write`, then the open gate."
4. PASS - "**Tree check:** `git status --porcelain` was empty and HEAD is still `518013c`."
run 1: PASS

## run 2
1. PASS - "2 files changed (`README.md`, `docs/usage.md`), 6 hand-written lines against a budget of 500."
2. PASS - "mutations and the cold review are **n/a: docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review**."
3. PASS - "`pr-write` (description), then the open gate"
4. PASS - "`git status --porcelain` is clean and the last commit is still `518013c`."
run 2: PASS

## run 3
1. PASS - "2 files changed (`README.md`, `docs/usage.md`). 6 hand-written lines against a budget of 500."
2. PASS - "| cold review | n/a | docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review |"
3. PASS - "After it come `pr-prove` (size check only), `pr-write`, then the open gate."
4. PASS - "`git status --porcelain` is clean and the last commit is still `518013c`."
run 3: PASS

case: 3/3
