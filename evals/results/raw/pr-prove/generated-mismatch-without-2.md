# PR check: feat/complete -> main

Verdict: not quite ready. The code change and its tests are fine. The generated-file check fails, and that failure existed before this branch.

## What the branch does
One commit, `e2ce131 Add complete()`. It changes `todo/model.py` (+6 lines) and adds a `complete(task)` function that returns a copy of the task with `done=True`. The line budget is 500 and the change is far below it. Risk paths: none.

## Checks I ran (commands from `.pr-ready/profile.md`)
- Tests (`python -m unittest discover -s tests -v`): 2 of 2 pass, `test_make_task` and `test_complete`.
- Generated-file check: `python tools/gen_schema.py > build/schema.json`, then compare with `api/schema.json`. **This fails.**

```
9a10,13
>     },
>     {
>       "name": "done",
>       "type": "boolean"
```

`tools/gen_schema.py` defines three fields (`id`, `title`, `done`), but the committed `api/schema.json` lists only `id` and `title`. The committed schema is stale.

## Where the mismatch comes from
- This branch did not cause it. The diff against `main` touches only `todo/model.py`. Neither `tools/gen_schema.py` nor `api/schema.json` changed. `main` has the same mismatch.
- It still matters here. `complete()` works on the `done` field, so a PR that adds behaviour around `done` ships with an API schema that doesn't list `done`. A reviewer or a CI generated-file check will probably flag it.

## Question for the dev (human gate)
"The committed `api/schema.json` is out of date: it is missing the `done` boolean field that `tools/gen_schema.py` emits. This predates your branch. Do you want to (a) regenerate it and include it in this PR, (b) fix it in a separate PR, or (c) open the PR as is and mention it in the description?"

The pre-supplied answer is only "yes", which doesn't pick one of these options. I made no changes to the repo. The only files I created are the git-ignored `build/` and `__pycache__` directories. If you want option (a), the fix is `python tools/gen_schema.py > api/schema.json`, then commit. That adds a 4-line change.

## Other notes
- The profile has no contributing guide, PR template, or AI-disclosure rules. `ai_description` and `ai_disclosure` are both "unclear", so nothing blocks the PR on policy.
- Working tree is clean (only ignored files are untracked).
- Suggested PR description: "Add `complete(task)` to the task model, returning a completed copy without mutating the input. Tests added." Add a note on the schema drift unless you regenerate it.
