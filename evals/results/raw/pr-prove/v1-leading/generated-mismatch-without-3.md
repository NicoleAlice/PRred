Report: the branch is NOT ready to open as a PR. Tests pass, but the generated schema is stale.

Repo: <tmp>/pr-ready-evals/pr-prove\generated-mismatch-without-3
Branch has one commit on top of the initial one: e2ce131 "Add complete()". The working tree was clean before I ran anything.

Commands come from .pr-ready/profile.md. There is no CI config in the repo, so the profile's "reproduce CI" command is what I ran.

1. Tests (`python -m unittest discover -s tests -v`): PASS
   - test_complete ... ok
   - test_make_task ... ok
   - Ran 2 tests, OK

2. Generated-file check (`python tools/gen_schema.py > build/schema.json`, then compare with `api/schema.json`): FAIL, the committed schema is stale.
   The generator has a `done` boolean field that `api/schema.json` lacks:

   ```
   9a10,13
   >     },
   >     {
   >       "name": "done",
   >       "type": "boolean"
   ```

   The committed `api/schema.json` lists only `id` and `title`. `tools/gen_schema.py` emits `id`, `title` and `done`.

What I did not do:
- I did not regenerate or edit `api/schema.json`. You asked me to prove the branch, not change it. The fix is `python tools/gen_schema.py > api/schema.json`, committed on this branch. That is a generated file whose diff you should review.
- The only thing I created is `build/`, which is gitignored. `git status` is otherwise unchanged.

Question for you: should I regenerate `api/schema.json` and commit it? You gave no pre-supplied answer for this, so I stopped at the report.

Recommendation: regenerate and commit the schema, then re-run the comparison before opening the PR.
