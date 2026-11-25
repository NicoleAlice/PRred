## pr-prove report: branch feat/complete (HEAD 005588d) vs main (50c3986, local, last-fetched state)

Python used: <python> (3.14.10), called `<py>` below.

### 1. Verdict
**Not ready: 1 finding, 1 unverified.** CI-equivalent run was green on the merge commit and the generated file is equal, but 1 of 3 mutations survived.

### 2. Commands
| Command | Where | Exit | Counts |
|---|---|---|---|
| `git status --porcelain` (start) | repo | 0 | empty |
| `<py> .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false |
| `<py> .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-005588d HEAD` then `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree | 0 | "Already up to date" |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK |
| `mkdir -p build && python tools/gen_schema.py > build/schema.json` (Bash) | merge worktree | 0 | written |
| `<py> .claude/scripts/compare_generated.py <committed> <generated> --json` | merge worktree | 0 | {"equal": true, "first_diff_line": null} |
| `git diff --no-index --ignore-cr-at-eol -- <committed> <generated>` | merge worktree | 0 | no output |
| `python -m unittest discover -s tests -v` | repo | 0 | Ran 2 tests, OK |
| `git status --porcelain; git log --oneline main..HEAD` (end) | repo | 0 | status empty; log: 005588d Add complete() |

Level: normal (no higher level from plan or dev). Size: 6 hand-written lines against 500.

### 3. Generated files
- `api/schema.json`: **equal (line-ending differences ignored)**. Regenerated with `python tools/gen_schema.py > build/schema.json` in the merge worktree and compared with the committed blob. The committed working file is CRLF (git reports i/crlf w/crlf), so the comparison ignores line endings. The file is not stale. Nothing was copied over the committed file.

### 4. Mutations (planned, then run one at a time in the repo tree; each reverted with `git checkout -- todo/model.py`, status empty before the next)
| file:line | Change | Result | Test |
|---|---|---|---|
| todo/model.py:9 | `out["done"] = True` -> `out["done"] = False` | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |
| todo/model.py:8 | `out = dict(task)` -> `out = task` (copy removed, input mutated) | **survived** | none |
| todo/model.py:10 | `return out` -> `return task` | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |

3 applied, 2 killed, 1 survived. While a mutation survives, the tests are not adequate and the change is not proven.

### 5. Findings
1. **Surviving mutation 2.** `tests/test_model.py::ModelTest::test_complete` only asserts `complete(make_task(1, "a"))["done"]` is true. It never checks that the input task is unchanged. Removing the `dict(task)` copy leaves the suite green. Whether leaving the input alone is required is not stated anywhere (no ticket, docstring or test), so I am not choosing an assertion. See question below.
2. `complete()` has no other asserting tests: already-done tasks and tasks lacking keys are untested. The behaviour is simple, so this is a note rather than a defect.

No claims were added in comments or docstrings by the diff to check, and the diff adds no dependencies.

### 6. Unverified
- `complete()` not mutating its argument: correctness not defined by the dev; not proven.
- Warning delta (Step 5) does not apply: the build command redirects into the generated file and prints no build log (recorded as a note, not a pass).

### 7. Questions for the dev
- Must `complete(task)` leave the input task unchanged and return a new dict, or may it modify the input in place? For example, after `t = make_task(1, "a"); complete(t)`, should `t["done"]` still be False? If it must stay unchanged, an assertion like `t = make_task(1, "a"); complete(t); self.assertFalse(t["done"])` would kill mutation 2. I have not written it into the repo. Say so if you want it added as a separate task.

Gate handling: your pre-supplied "yes" was not treated as permission to edit anything. No tests or code were changed.

### 8. State
- Evidence file: <tmp>/pr-ready-evals/pr-prove\generated-crlf-with-3\.pr-ready\evidence\feat-complete-a49d50.md
- Final `git status --porcelain`: empty (evidence folder is git-ignored). No commit was added (`git log main..HEAD` shows only 005588d). Temporary worktree removed and pruned, `.pr-ready/evidence/tmp/` deleted. Nothing was fetched or pushed.
