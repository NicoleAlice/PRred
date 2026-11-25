# pr-prove report: branch feat/complete (HEAD 005588d) against main (50c3986, local last-fetched state)

## 1. Verdict

Not ready: 2 findings, 1 unverified.

CI is green on the merge commit and the generated file is equal. Two mutations survived, and the expected behaviour of `complete()` is not defined by you yet.

Level: normal (no risk reasons). Size: 6 hand-written lines against a budget of 500.

Your "yes" was treated as an answer to a gate, not as a request to edit. I changed nothing in the repo.

## 2. Commands

Bare `python` is not on PATH here, so every Python line ran with `<py>` = `<python>`.

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 6, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, reasons [] |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-005588d HEAD`, then `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree | 0 | "Already up to date" |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK |
| `python tools/gen_schema.py > build/schema.json` | merge worktree HEAD 005588d + main 50c3986 | 0 | wrote build/schema.json |
| `python .claude/scripts/compare_generated.py <committed api/schema.json> <wt>/build/schema.json --json` | merge worktree HEAD 005588d + main 50c3986 | 0 | `{"equal": true, "first_diff_line": null}` |
| `git diff --no-index --ignore-cr-at-eol -- <committed> <generated>` | merge worktree | 0 | no output |
| `python -m unittest discover -s tests -v` (before mutations) | repo | 0 | Ran 2 tests, OK |
| `git status --porcelain; git log --oneline main..HEAD` (final) | repo | 0 | status empty; log: `005588d Add complete()` |

## 3. Generated files

`api/schema.json`: **equal (line-ending differences ignored)**. The committed copy is CRLF in the index and the working tree (`git ls-files --eol` shows `i/crlf w/crlf`). I saved it byte for byte through `git cat-file` and compared it with the fresh `build/schema.json`. The file is not stale.

## 4. Mutations

The suite was green in the repo's own working tree first. The worktrees were removed before mutating. I applied the mutations one at a time, reverted each with `git checkout -- todo/model.py`, and `git status --porcelain` was empty after each.

Planned: 4. Applied: 4. Killed: 2. Survived: 2.

| file:line | Change | Result | Caught by |
|---|---|---|---|
| todo/model.py:10 | `out["done"] = True` to `out["done"] = False` | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |
| todo/model.py:9 | `out = dict(task)` to `out = task` (the input is mutated in place) | survived | none |
| todo/model.py:9 | `out = dict(task)` to `out = {"done": True}` (id and title dropped) | survived | none |
| todo/model.py:11 | `return out` to `return task` (input returned unchanged) | killed | tests/test_model.py::ModelTest::test_complete (AssertionError: False is not true) |

## 5. Findings

1. **Mutation survived: `complete()` can mutate its input.** `tests/test_model.py::ModelTest::test_complete` calls `complete(make_task(1, "a"))` and checks only `["done"]`. It never keeps a reference to the original task, so it cannot see the in-place change. The code copies the dict, which suggests the copy is intended, but nothing states that. See question 1 before adding an assertion.
2. **Mutation survived: `complete()` can drop other fields.** `test_complete` does not assert that `id` and `title` are kept. A test comparing the whole result to a full expected dict would kill this. I am not suggesting a concrete expected value, because the expected result is not yet defined by you (question 1).

While any mutation survives, the tests are not adequate for `complete()`, and the change is not proven.

Other checks, all clean:
- No comments, docstrings or messages were added by the diff, so there are no claims to check.
- No new dependencies were added.
- The warning delta does not apply, because the build output is redirected into the generated file and there is no build log.

## 6. Unverified

- `complete()` returns a new dict and preserves `id` and `title`: correctness not defined by the dev; not proven. No asserting test covers it.

## 7. Questions for the dev

1. For `complete(task)`, what is the correct result?
   - Must the input task stay unmodified (return a new dict)?
   - Must the result keep all other fields, so that `complete({"id": 1, "title": "a", "done": False})` equals `{"id": 1, "title": "a", "done": True}`?
   - Should an already-done task come back unchanged?

   Once you confirm, adding these as tests is a separate task for you to request. I did not write tests.

## 8. State

- Evidence file: `<tmp>/pr-ready-evals/pr-prove\generated-crlf-with-1\.pr-ready\evidence\feat-complete-dedcef.md`
- Final `git status --porcelain`: empty.
- `git log --oneline main..HEAD` shows only `005588d Add complete()`. No commit was added.
- The temporary worktree is removed. `git worktree list` shows only the main one, and `.pr-ready/evidence/tmp` is deleted.
