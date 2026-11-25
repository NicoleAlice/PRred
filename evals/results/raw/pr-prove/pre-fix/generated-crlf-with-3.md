# pr-prove report: branch feat/complete (HEAD 005588d) vs main (50c3986, local, last-fetched; no fetch done)

Gate note: the only pre-supplied answer was "yes", which does not answer any specific question. I did not treat it as permission to edit anything. No files were edited, and the Step 6 question below is still open.

## 1. Verdict

Not ready: 2 findings, 1 unverified. CI passes on the merge commit and the generated file is up to date. Two hand mutations survived, and the expected behaviour of `complete()` is not defined.

## 2. Commands

`python` is Python 3.14 at <python>. `python3` and `python` on PATH are Windows Store aliases and do not work.

| Command | Where | Exit | Counts |
|---|---|---|---|
| `git status --porcelain` | repo | 0 | empty (clean) |
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false (todo/model.py +6) |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, reasons [] |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-005588d HEAD`, then `git merge --no-commit --no-ff main` | merge worktree HEAD 005588d + main 50c3986 | 0 | "Already up to date" |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK (0 failures, 0 errors, 0 skipped) |
| `python tools/gen_schema.py > build/schema.json`, then `compare_generated.py api/schema.json <wt>/build/schema.json --json` | merge worktree HEAD 005588d + main 50c3986 | 0 | `{"equal": true, "first_diff_line": null}`; `git diff --no-index --ignore-cr-at-eol` printed nothing |
| `git worktree remove --force`, `git worktree prune`, `git status --porcelain`, `git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `005588d Add complete()` |

Risk level is normal. The warning delta does not apply, because the build command redirects into a generated file and prints no build log. I recorded that as a note.

## 3. Generated files

`api/schema.json`: **equal apart from line endings** to a fresh `tools/gen_schema.py` output built in the merge worktree. It is not stale. It is committed with CRLF line endings. The comparison ignores that, and I did not check bytes.

## 4. Mutations

Planned: 3, applied one at a time to `todo/model.py`, each reverted with `git checkout -- todo/model.py`. `git status --porcelain` was empty after each.

Result: 3 applied, 1 killed, 2 survived.

| file:line | Change | Result | Caught by |
|---|---|---|---|
| todo/model.py:9 | `out["done"] = True` -> `out["done"] = False` | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |
| todo/model.py:8 | `out = dict(task)` -> `out = task` (the input is mutated, no copy) | survived (Ran 2 tests, OK) | none |
| todo/model.py:8 | `out = dict(task)` -> `out = {"done": task["done"]}` (id and title dropped) | survived (Ran 2 tests, OK) | none |

## 5. Findings

1. **Survivor: input mutation.** `tests/test_model.py::ModelTest::test_complete` is `self.assertTrue(complete(make_task(1, "a"))["done"])`. It checks only that the returned `done` is truthy. It never checks that the original task is left unchanged, so `complete()` could mutate its argument and the test would still pass. I will not suggest an assertion, because the expected behaviour is not stated anywhere (see section 7).
2. **Survivor: other fields.** The same test never checks that `id` and `title` are kept. The expected result is again not stated anywhere (see section 7).

I have not edited any test. Writing these assertions is a separate task for you to ask for.

## 6. Unverified

- `complete()`: whether it must leave the input unmodified and keep `id` and `title`. Correctness was not defined by the dev, so this is not proven, and no test asserts it.

## 7. Questions for the dev

For `complete(task)` in `todo/model.py`, there is no ticket, docstring or existing test that states the intended result. Today the code does this:

- `complete({"id": 1, "title": "a", "done": False})` returns a new dict `{"id": 1, "title": "a", "done": True}`.
- The original dict stays `done: False`.

Which of these is correct?

1. Return a new dict and leave the input untouched, which is what the code does now.
2. Mutate the input in place.
3. Something else, for example what should happen when the task is already done.

Also confirm that `id` and `title` must be preserved. Once you answer, I can propose assertions with that source quoted. I will not write them into the repo unless you ask.

## 8. State

- Evidence file: `<tmp>/pr-ready-evals/pr-prove\generated-crlf-with-3\.pr-ready\evidence\feat-complete-a49d50.md`
- Final `git status --porcelain`: empty.
- No commit was added. `git log main..HEAD` shows only `005588d Add complete()`.
- The temporary worktree is removed and `.pr-ready/evidence/tmp/` is deleted.
- Nothing was pushed or fetched.
