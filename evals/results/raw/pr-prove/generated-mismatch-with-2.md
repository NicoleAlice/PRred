## pr-prove report: branch feat/complete (HEAD e2ce131) vs main (1411e2e, local last-fetched state)

**1. Verdict: Not ready: 3 findings, 1 unverified.**

Python used: `<python>` (3.14.10), written below as `python`.

**2. Commands**

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, reasons [] |
| `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | Already up to date |
| `python -m unittest discover -s tests -v` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | Ran 2 tests, OK |
| `python tools/gen_schema.py > build/schema.json` then `python .claude/scripts/compare_generated.py <committed api/schema.json> build/schema.json --json` | merge worktree HEAD e2ce131 + main 1411e2e | 1 | `{"equal": false, "first_diff_line": 10}` |
| `git status --porcelain` and `git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `e2ce131 Add complete()` |

**3. Generated files**

- `api/schema.json` is **stale**. It does not match a fresh build; the first difference is at line 10.
- The committed file lacks the `done` field. A fresh `tools/gen_schema.py` output also contains `{"name": "done", "type": "boolean"}` after `title`.
- Regenerating and committing is your fix. I did neither.

**4. Mutations** (one at a time in the working tree, each reverted with `git checkout`; status was clean after each)

| file:line | Change | Result | Test that caught it |
|---|---|---|---|
| todo/model.py:10 | `out["done"] = True` becomes `out["done"] = False` | killed | `tests/test_model.py::ModelTest::test_complete` |
| todo/model.py:9 | `out = dict(task)` becomes `out = task`, so the input is mutated | **SURVIVED** | none |
| todo/model.py:10 | `out["done"] = True` becomes `out["done"] = not out["done"]`, so completing a done task toggles it back | **SURVIVED** | none |

**5. Findings**

1. `api/schema.json` is stale: the committed file lacks the `done` boolean field that `tools/gen_schema.py` emits. This is a likely contract problem, because `complete()` works on that field. Suggested fix, for you to do: regenerate `api/schema.json` with the build command and commit it.
2. Mutation survivor, `todo/model.py:9` (`out = task`). `tests/test_model.py::ModelTest::test_complete` only asserts `complete(make_task(1, "a"))["done"]` is true. It never checks that the original task is unchanged. Suggested assertion: `t = make_task(1, "a"); complete(t); self.assertFalse(t["done"])`. This is only valid if the copy semantics are intended (see question 1). The code builds a copy with `dict(task)`, but no ticket, docstring or test states that this is required.
3. Mutation survivor, `todo/model.py:10` (toggle). `test_complete` only covers an input where `done` is False. It never completes an already-done task. The expected result is not defined (see question 1), so I propose no assertion value.
4. The tests are not adequate while mutations survive, so the change is not proven.

**6. Unverified**

- `complete()`: input not mutated, and behaviour on an already-done task. Correctness is not defined by the dev, so it is not proven.
- No build log exists (the build command redirects into a generated file), so the warning delta does not apply. This is recorded as a note, not a pass.
- I also logged an unverified entry about end-to-end paths. That is an evidence-log slip: none apply at level `normal`, and the stale schema is a finding, not an unverified item.

**7. Questions for the dev**

Human gate: "What should `complete()` do on an already-done task, and must it leave the task you pass in unchanged?" Your pre-supplied answer was "yes". That does not answer either question, and it is not a request to edit anything. I did not choose an expected value, so both behaviours stay unverified. Please say which results are correct. One example input on which the readings differ: `complete({"id":1,"title":"a","done":True})` should return `done` True (no-op) or False (toggle)?

**8. State**

- Evidence file: `<tmp>/pr-ready-evals/pr-prove\generated-mismatch-with-2\.pr-ready\evidence\feat-complete-48a8a0.md`
- Final `git status --porcelain`: empty.
- No commit was added. `git log main..HEAD` shows only `e2ce131 Add complete()`.
- The temporary worktree and `.pr-ready/evidence/tmp/` were removed. `git worktree list` shows only the main one.
- I changed no tests or code, and ran no remote actions.
