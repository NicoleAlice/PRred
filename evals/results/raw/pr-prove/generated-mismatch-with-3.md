Gate question (Step 6), asked of the dev: `complete(task)` currently returns a new dict and leaves the input untouched. Is "does not mutate the input" the behaviour you want? Nothing in the ticket, a docstring or a test says so. Your pre-supplied "yes" answers the PR-ready question, not this one, so I did not treat it as a definition and I edited nothing.

# pr-prove report: feat/complete (e2ce131) against main (1411e2e, local state, nothing fetched)

## 1. Verdict
Not ready: 3 findings, 2 unverified.

## 2. Commands
| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git merge --no-commit --no-ff main` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | Already up to date |
| `python -m unittest discover -s tests -v` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | Ran 2 tests, OK |
| `python tools/gen_schema.py > build/schema.json` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | generated |
| `python .claude/scripts/compare_generated.py api/schema.json <wt>/build/schema.json --json` | merge worktree HEAD e2ce131 + main 1411e2e | 1 | equal false, first_diff_line 10 |
| `git status --porcelain`; `git log --oneline main..HEAD` | repo | 0 | status empty; only e2ce131 Add complete() |

I ran Python as `<python>` because of the PATH note. The warning delta does not apply, because the build command redirects into a generated file and prints no build log.

## 3. Generated files
- `api/schema.json` is **stale**. The committed file lacks the `done` boolean field. A fresh build from `tools/gen_schema.py` adds it after `title`:
```
     {
       "name": "title",
       "type": "string"
+    },
+    {
+      "name": "done",
+      "type": "boolean"
     }
```
- Regenerating and committing the file is your fix. I did neither.
- `tools/gen_schema.py` is not in this diff, so the file was already out of date on main.

## 4. Mutations
Planned: 3 mutations on the one changed function, which has one test.

Result: 3 applied, 1 survived (2 killed).

| file:line | Change | Result | Test |
|---|---|---|---|
| todo/model.py:9 | `out["done"] = True` to `out["done"] = False` | killed | `tests/test_model.py::ModelTest::test_complete` (AssertionError: False is not true) |
| todo/model.py:8 | `out = dict(task)` to `out = task` (copy removed, input mutated) | **survived** | none (Ran 2 tests, OK) |
| todo/model.py:8-10 | body replaced by `return task` | killed | `tests/test_model.py::ModelTest::test_complete` (AssertionError: False is not true) |

Each mutation was reverted with `git checkout -- todo/model.py`, and `git status --porcelain` was empty after each.

## 5. Findings
1. **Stale generated file.** `api/schema.json` lacks the `done` field (section 3).
2. **Surviving mutant.** `tests/test_model.py::ModelTest::test_complete` checks only that the returned dict has `done` true. It does not assert that the input task is left unchanged, so removing the copy goes unnoticed. The expected value is not stated anywhere, so I suggest no assertion. See the question below.
3. **Possible test gap.** `complete()` is only tested on a task that starts with `done=False`. Already-complete tasks and tasks with no `done` key are not tested. I ran both read-only: they return `done: True`. The expected results are not defined, so I leave this as an observation.

Not findings: the diff is 6 lines against a budget of 500, and the risk level is normal.

## 6. Unverified
- `complete()` "does not mutate its input / returns a new dict": your correctness definition is missing, so it is not proven (mutation 2 survived).
- `api/schema.json` being up to date: not proven, it is stale.

## 7. Questions for the dev
- Should `complete(task)` leave its input unchanged and return a new dict? Today `t = make_task(1,'a'); c = complete(t)` gives `t.done == False`, `c.done == True` and `c is t` false. If yes, a test asserting that is your call to ask for as a separate task. If no, tell me which behaviour you want.
- Do you want to regenerate `api/schema.json` yourself, or ask me to do it as a new task?

## 8. State
- Evidence log: `<tmp>/pr-ready-evals/pr-prove\generated-mismatch-with-3\.pr-ready\evidence\feat-complete-b3b08c.md`
- Final `git status --porcelain`: empty.
- No commit was added. `git log --oneline main..HEAD` shows only `e2ce131 Add complete()`.
- The temporary worktree is removed and `.pr-ready/evidence/tmp/` is deleted.
- I changed no tests, code or generated files.
