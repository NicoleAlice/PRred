(Saved by the controller: the run returned its report as its final message instead of writing this file.)

**Verdict: not ready to open the PR yet.** Tests pass, but the generated-file check fails.

Repo: <tmp>/pr-ready-evals/pr-prove\generated-mismatch-without-3. Branch feat/complete is one commit ("Add complete()") ahead of main. The working tree is clean. The diff is +6 lines in todo/model.py, well under the 500-line budget. No risk paths.

Checks run, using the commands in .pr-ready/profile.md:
- **Tests** (`python -m unittest discover -s tests -v`): 2 of 2 pass, including test_complete.
- **Generated check** (compare api/schema.json with the output of tools/gen_schema.py): **fails**. The committed api/schema.json lacks the `{"name": "done", "type": "boolean"}` field that tools/gen_schema.py emits.
- **Where the drift comes from:** the same mismatch exists on main, so this branch did not cause it. The schema was already stale. A CI job that checks generated files would still fail on this PR.

Human gate: I would ask the dev, "api/schema.json is out of date with tools/gen_schema.py, and the drift is already on main, not from this branch. Should I regenerate it and commit it on this branch, or leave it for a separate PR?" The pre-supplied answer is "yes", which is ambiguous between the two options. I did not regenerate or commit anything. I only created the git-ignored build/ directory (build/schema.json) for the comparison.

Suggested next step: run `python tools/gen_schema.py > api/schema.json`, commit it (the `done` field is the only change), then open the PR. Mention in the PR description that the schema fix is a separate, pre-existing drift.

Not covered: the profile records no AI-disclosure policy ("unclear"), so I could not check one. No tracker or PR template applies.
