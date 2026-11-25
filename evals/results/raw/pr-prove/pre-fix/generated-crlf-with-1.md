# pr-prove report: feat/complete vs main

**Verdict: Not ready: 2 findings, 1 unverified.** (Tests are green and the generated file is equal, but 2 of 3 mutations survived and the correctness of `complete()` beyond "done becomes true" is undefined.)

Level: normal (no risk paths; 6 hand-written lines against a budget of 500). Base `main` is the local, last-fetched state. Nothing was fetched.

Interpreter note: `python3` and `python` are the Windows Store alias and fail. I used `<python>` (3.14.10), written below as `<py>`. The profile lines say `python`, so I ran the same lines with `<py>`.

## Commands

| Command | Where | Exit | Counts |
|---|---|---|---|
| `<py> .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false (todo/model.py +6) |
| `<py> .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, reasons [] |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-005588d HEAD`, then `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree HEAD 005588d + main 50c3986 | 0 | "Already up to date." |
| `<py> -m unittest discover -s tests -v` (profile line is `python -m ...`) | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK (0 failures, 0 errors, 0 skipped) |
| `<py> tools/gen_schema.py > build/schema.json` | merge worktree HEAD 005588d + main 50c3986 | 0 | schema written to ignored build/ |
| `<py> .claude/scripts/compare_generated.py <committed api/schema.json> <wt>/build/schema.json --json` | merge worktree HEAD 005588d + main 50c3986 | 0 | `{"equal": true, "first_diff_line": null}` |
| `git diff --no-index --ignore-cr-at-eol -- <committed> <generated>` | merge worktree | 0 | no output |
| cleanup: `git worktree remove --force`, `git worktree prune`, `git status --porcelain`, `git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `005588d Add complete()` |

## Generated files

- `api/schema.json`: **equal apart from line endings.** The committed copy uses CRLF and the freshly generated one uses LF. The file is not stale. The branch does not touch it.

## Mutations

Planned (3 applied, one at a time, each reverted with `git checkout -- todo/model.py`, `git status --porcelain` empty after each):

| file:line | Change | Result | Test that caught it |
|---|---|---|---|
| todo/model.py:10 | `out["done"] = True` -> `out["done"] = False` | **killed** | `tests/test_model.py::ModelTest::test_complete` (AssertionError: False is not true) |
| todo/model.py:9 | `out = dict(task)` -> `out = task` (mutates the caller's task) | **survived** | none |
| todo/model.py:9 | `out = dict(task)` -> `out = {}` (id and title dropped from the output) | **survived** | none |

3 applied, 1 killed, 2 survived. While any mutation survives, the tests are not adequate and the change is not proven.

Correction: the evidence log entries for mutations 1 to 3 record the lines as 9, 8 and 8. The actual lines are 10, 9 and 9, as in the table above. The mutations themselves were correct.

## Findings

1. **Survivor, input mutation.** `tests/test_model.py::ModelTest::test_complete` only checks that `complete(make_task(1, "a"))["done"]` is truthy. It never checks that the original task is left unchanged. If `complete()` should return a copy, this is the missing assertion. I did not choose that for you (see Questions).
2. **Survivor, other fields dropped.** `test_complete` never checks that `id` and `title` survive in the result. A possible assertion is `assertEqual(complete(make_task(1, "a")), {"id": 1, "title": "a", "done": True})`. The expected value is inferred from `make_task`'s shape, not from a ticket or docstring. Treat it as a suggestion for you to confirm.

No other findings. The branch is within budget and has no warning delta, because the build redirects into a file and prints no log.

## Unverified

- `todo/model.py` `complete()`: "input is not mutated and other fields are preserved". Correctness is not defined by the dev, and no test asserts it, so it is not proven.

## Questions for the dev

1. Should `complete()` return a new task and leave the input untouched, as it does today, or mark the task in place?
2. Should it be idempotent on a task that is already done? Today it returns a copy with `done` true.

I wrote no assertion into the repo. Tests are an edit for you to ask for separately.

## State

- Evidence file: `<tmp>/pr-ready-evals/pr-prove\generated-crlf-with-1\.pr-ready\evidence\feat-complete-dedcef.md`
- Final `git status --porcelain`: empty.
- No commit added: `git log --oneline main..HEAD` shows only `005588d Add complete()`.
- The temporary worktree and `.pr-ready/evidence/tmp/` are removed.
- Gate note: "dev answers: yes" was the only pre-supplied answer. It did not answer the Step 6 questions and was not read as permission to edit anything.
