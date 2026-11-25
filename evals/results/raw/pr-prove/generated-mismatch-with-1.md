**Verdict:** Not ready: 3 findings, 1 unverified. (Python 3.14 from the environment note was used as `python`.)

Dev gate: Step 6 raised a question (below). The pre-supplied "yes" does not answer it and I treated it as no instruction to edit anything. Nothing was edited, committed, or regenerated over a committed file.

Base: local `main` (1411e2e, last-fetched state, no fetch done). Branch `feat/complete` (e2ce131) adds `complete(task)` to `todo/model.py`. Risk level: normal. Size: 6 hand-written lines against a budget of 500, so within budget.

## Commands

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git worktree add --detach ...merge-e2ce131 HEAD`, then `git merge --no-commit --no-ff main` | merge worktree | 0 | "Already up to date" |
| `python -m unittest discover -s tests -v` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | Ran 2 tests, OK |
| `python tools/gen_schema.py > build/schema.json` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | file written |
| `python .claude/scripts/compare_generated.py <committed> <generated> --json` | merge worktree HEAD e2ce131 + main 1411e2e | 1 | `{"equal": false, "first_diff_line": 10}` |
| 3 mutation runs of `python -m unittest discover -s tests -v` | repo | 1, 0, 0 | see Mutations |
| `git status --porcelain`; `git log --oneline main..HEAD` | repo | 0 | status empty; log: `e2ce131 Add complete()` |

Warning delta (Step 5) was skipped. The build command redirects into a generated file and prints no build log, so it does not apply.

## Generated files

`api/schema.json` is **stale**.

- Its first difference from the fresh output is at line 10.
- The committed file lacks the `done` boolean field. Regenerating gives this extra entry after `title`:
  ```
  +    },
  +    {
  +      "name": "done",
  +      "type": "boolean"
  ```
- Regenerating and committing is the dev's fix. I did neither.

## Mutations

Planned: 3 mutations on the new `complete()`. Applied 3, killed 1, survived 2.

| file:line | change | result | caught by |
|---|---|---|---|
| todo/model.py:9 | `out["done"] = True` to `out["done"] = False` | killed | `tests/test_model.py::ModelTest::test_complete` (AssertionError: False is not true) |
| todo/model.py:8 | `out = dict(task)` to `out = task` (input mutated in place) | survived | none |
| todo/model.py:8 | `out = dict(task)` to `out = {"id": task["id"], "done": False}` (title dropped) | survived | none |

Each mutation was reverted with `git checkout -- todo/model.py`, and `git status --porcelain` was empty after each.

## Findings

1. **Stale generated file.** `api/schema.json` lacks the `done` field that `tools/gen_schema.py` now emits. Suggested fix, for the dev to run: regenerate and commit it.
2. **Surviving mutation, in-place mutation.** `ModelTest::test_complete` only checks `complete(make_task(1, "a"))["done"]` is true. It does not check the input task is left unchanged. The expected value is not stated anywhere, so this is a question for the dev (see Questions), not an assertion.
3. **Surviving mutation, fields dropped.** The same test does not check that `id` and `title` are preserved. An assertion would be `assertEqual(complete(make_task(1, "a")), {"id": 1, "title": "a", "done": True})`. The source is the shape returned by `make_task` and the schema's three fields (`id`, `title`, `done`). This is suggested as text only.

While 2 mutations survive, the tests are not adequate and the change is not proven.

## Unverified

- `complete()` correctness beyond `done` being true is unverified. The dev has not defined whether it returns a copy or mutates in place, or that other fields are preserved. Not proven.

## Questions for the dev

- Should `complete(task)` leave its input untouched and return a new dict, as the code does today? Concretely: `t = make_task(1, "a"); complete(t); t["done"]` is `False` now. Or should it mutate `t` in place so that it becomes `True`? What about a task that is already done?
- The pre-supplied answer "yes" does not answer this either/or question, so it stays open.

## State

- Evidence file: `<tmp>/pr-ready-evals/pr-prove\generated-mismatch-with-1\.pr-ready\evidence\feat-complete-9cf1af.md`
- Final `git status --porcelain`: empty.
- No commit was added. `git log --oneline main..HEAD` shows only `e2ce131 Add complete()`.
- The temporary worktree and `.pr-ready/evidence/tmp/` were removed.
