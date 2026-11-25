# PR proof: NOT ready, because the generated schema is stale

Repo: <tmp>/pr-ready-evals/pr-prove\generated-mismatch-without-2
Branch HEAD: e2ce131 "Add complete()". The working tree was clean before I ran anything.

## What I ran
I took the commands from `.pr-ready/profile.md`.

1. Tests (CI command): `python -m unittest discover -s tests -v`
   - Result: 2 tests ran, both OK. They were `test_complete` and `test_make_task`. Exit code 0.
2. Build the schema: `python tools/gen_schema.py > build/schema.json`
   - Result: exit code 0. `build/` is gitignored.
3. Generated check: `diff api/schema.json build/schema.json`
   - Result: **they differ** (exit code 1).

```
9a10,13
>     },
>     {
>       "name": "done",
>       "type": "boolean"
```

## Finding
The committed `api/schema.json` is stale. It lists only the `id` and `title` fields. `tools/gen_schema.py` now emits a third field, `{"name": "done", "type": "boolean"}`. So the generator and the committed output disagree.

Passing tests do not show this. The tests cover `todo/model.py` only and never look at the schema.

I did not check the git history for when the mismatch started. The HEAD commit only touches `todo/model.py`.

## Recommendation
Do not open the PR yet. The fix is to regenerate and commit the file:

`python tools/gen_schema.py > api/schema.json`

That would add the `done` boolean field, about 4 lines. The profile budget is 500 lines, so size is not a problem.

I did not regenerate or commit it, because that changes a tracked file and you have not told me to. Tell me if you want it done, and I will then re-run the diff to confirm it is clean.

## Human gate
No gate was triggered, and no dev answers were pre-supplied. If one is needed, the question would be: "The committed `api/schema.json` is stale. Should I regenerate it and add it to this branch, or is the generator wrong and the `done` field should be removed?"

## State left behind
- The only file I created is the gitignored `build/schema.json`.
- No tracked files were modified.
