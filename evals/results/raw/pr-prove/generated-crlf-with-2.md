## pr-prove report: feat/complete vs main

Python: `<python>` (the PATH `python` is the Windows Store alias, so it was not used). Base `main` is the local, last-fetched state. Nothing was fetched.

### 1. Verdict
Not ready: 1 finding, 1 unverified. The suite is green on the merge commit and the generated file is equal. One mutation survived, because no test checks that `complete()` leaves its input unchanged.

### 2. Commands
| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree | 0 | Already up to date |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK |
| `python tools/gen_schema.py > build/schema.json` (Bash) plus `compare_generated.py <committed> <generated> --json` | merge worktree HEAD 005588d + main 50c3986 | 0 | `{"equal": true, "first_diff_line": null}`. `git diff --no-index --ignore-cr-at-eol` printed nothing. |
| `python -m unittest discover -s tests -v` | repo, before mutations | 0 | Ran 2 tests, OK |
| `git status --porcelain`; `git log --oneline main..HEAD` | repo, final | 0 | status empty; log is `005588d Add complete()` only |

The level is `normal`, so the full process ran.

### 3. Generated files
`api/schema.json`: **equal (line-ending differences ignored)**. The committed file uses CRLF and the regenerated output uses LF. The files match apart from line endings, so the file is not stale.

### 4. Mutations
These were planned and then run one at a time in the repo tree. Each was reverted at once, and `git status --porcelain` was empty after each.

| file:line | Change | Result | Caught by |
|---|---|---|---|
| todo/model.py:8 | `out = dict(task)` to `out = task` (copy removed, input mutated) | **survived** (Ran 2 tests, OK) | none |
| todo/model.py:9 | `out["done"] = True` to `False` | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |
| todo/model.py:10 | `return out` to `return task` | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |

Result: 3 applied, 2 killed, 1 survived.

### 5. Findings
1. **Surviving mutation, `todo/model.py:8`.** `tests/test_model.py::ModelTest::test_complete` only asserts `complete(make_task(1, "a"))["done"]` is true. It does not check that the input task is left unchanged. Removing the copy, so `complete` mutates its argument, goes unnoticed. The expected behaviour is not stated anywhere (see question 1), so I suggest no assertion. Once the dev answers, the test could be, if "no mutation" is wanted:
   `t = make_task(1, "a"); complete(t); self.assertFalse(t["done"])`
   I have not written it, because adding it is a separate task.

Other checks:
- Over budget: no (6 of 500 lines).
- Claims: the diff adds no comments or docstrings that state behaviour.
- New dependencies: none.
- Warning delta: does not apply. The build command redirects into a generated file and prints no build log.

### 6. Unverified
- `complete()` does not mutate its input: correctness not defined by the dev; not proven, and no test asserts it.

### 7. Questions for the dev
1. Should `complete(task)` leave its argument unchanged, as the current code does by returning a copy? Or is mutating the argument acceptable? Neither the ticket, a docstring nor a test says. With the line `out = task`, `t = make_task(1, "a"); complete(t)` turns `t["done"]` into True. With the current code, `t["done"]` stays False.

Human gates: I asked the question above and you supplied only "yes". That is not an answer to the question, so it stays open and the behaviour stays unverified. "Yes" was not taken as a request to edit anything. I changed no tests and no code.

### 8. State
- Evidence file: `<tmp>/pr-ready-evals/pr-prove\generated-crlf-with-2\.pr-ready\evidence\feat-complete-25ea4a.md`
- Final `git status --porcelain`: empty.
- No commit was added: `git log main..HEAD` shows only `005588d Add complete()`.
- The temporary worktree and `.pr-ready/evidence/tmp/` are removed, and `git worktree list` shows only the repo.
