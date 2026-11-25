Report: the PR is not ready. The tests pass, but the generated schema `api/schema.json` is stale.

What I ran (from the repo's `.pr-ready/profile.md`):

1. CI command: `python -m unittest discover -s tests -v`
   - Result: 2 tests ran, both OK (test_complete, test_make_task), exit code 0.

2. Generated-file check:
   - I ran `python tools/gen_schema.py > build/schema.json` (exit 0), then `diff api/schema.json build/schema.json`.
   - Result: they differ (diff exit 1). The committed `api/schema.json` lacks the `done` field that the generator now emits:

```
9a10,13
>     },
>     {
>       "name": "done",
>       "type": "boolean"
```

The committed schema lists only `id` and `title`. The generator produces `id`, `title` and `done` (boolean).

Conclusion: the tests pass, but `api/schema.json` was not regenerated, so the generated-file check fails. This is a real mismatch, not a formatting difference.

I did not modify any tracked file. `build/` is gitignored, and `git status` is clean. To fix it, run `python tools/gen_schema.py > api/schema.json`, then commit the result. I left that to you, since you asked me to prove the branch works, not to change it. No human gate came up, so I asked no questions.
