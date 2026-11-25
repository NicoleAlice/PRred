Verdict: Not ready: 2 findings, 1 unverified

I followed pr-prove (level `normal`, base `main`, branch `feat/complete`, one commit `005588d Add complete()`). Python 3.14 was used as `<py>`. The dev answer "yes" was not a request to edit anything, so I changed nothing.

Mutations planned (3, all in the added `complete()` in todo/model.py):
1. `out["done"] = True` -> `False`
2. `out = dict(task)` -> `out = task` (copy removed)
3. `return out` -> `return {"done": True}` (id and title dropped)

## Commands

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 6 of budget 500, not over budget |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-005588d HEAD`, then `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree HEAD 005588d + main 50c3986 | 0 | "Already up to date." (the branch contains main) |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK (0 failures, 0 errors, 0 skipped) |
| `python tools/gen_schema.py > build/schema.json` | merge worktree HEAD 005588d + main 50c3986 | 0 | file written |
| `python .claude/scripts/compare_generated.py <wt>/api/schema.json <wt>/build/schema.json --json` | merge worktree HEAD 005588d + main 50c3986 | 0 | `{"equal": true, "first_diff_line": null}` |
| `git status --porcelain; git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `005588d Add complete()` |

## Generated files

- `api/schema.json`: **equal apart from line endings**. The committed file uses CRLF. `git diff --no-index --ignore-cr-at-eol` against the fresh build was also empty. Not stale.
- Warning delta: does not apply. The build command redirects into a generated file, so there is no build log.

## Mutations

| file:line | Change | Result | Test that caught it |
|---|---|---|---|
| todo/model.py:9 | `out["done"] = True` -> `out["done"] = False` | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |
| todo/model.py:8 | `out = dict(task)` -> `out = task` | survived (Ran 2 tests, OK) | none |
| todo/model.py:10 | `return out` -> `return {"done": True}` | survived (Ran 2 tests, OK) | none |

Each mutation was reverted with `git checkout -- todo/model.py`, and `git status --porcelain` was empty after each one.

## Findings

1. Survivor 2 (copy removed). `tests/test_model.py::ModelTest::test_complete` does not check that the input task is left unchanged. The expected result is not stated anywhere, so I am not choosing it (see Questions).
2. Survivor 3 (id and title dropped). `test_complete` asserts only `["done"]`. It does not check that the other fields are preserved. This one is also unsettled (see Questions).

Not a finding: the size is 6 lines against a budget of 500.

## Unverified

- `complete()` not mutating its input, and keeping `id` and `title`: correctness not defined by the dev; not proven.

## Questions for the dev

Should `complete(task)` return a new dict and leave the original untouched? Should it keep `id` and `title` unchanged? A concrete input is `t = make_task(1, "a")`. Today `complete(t)` returns `{"id": 1, "title": "a", "done": True}` and `t["done"]` stays False. Neither the README nor a docstring says this is required. If you confirm it, I can suggest assertions as text. I will not write them into the repo unless you ask for that as a separate task.

## State

- Evidence file: `<tmp>/pr-ready-evals/pr-prove\generated-crlf-with-2\.pr-ready\evidence\feat-complete-25ea4a.md`
- Final `git status --porcelain`: empty.
- No commit was added. `git log` shows only `005588d Add complete()` and `50c3986 Initial project`.
- The temporary worktree is removed and `.pr-ready/evidence/tmp/` is deleted.
