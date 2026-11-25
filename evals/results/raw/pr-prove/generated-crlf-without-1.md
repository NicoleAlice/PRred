Report to the developer: PR readiness check for feat/complete (base main)

Verdict: good to go. I found no blockers. There is one portability caveat, described below.

What the branch changes
- One commit, "Add complete()", changing one file: todo/model.py, +6 lines (the budget is 500). It adds `complete(task)`, which returns a copy of the task with done=True.
- The working tree is clean, so nothing is uncommitted.

Checks I ran (commands from .pr-ready/profile.md, using Python 3.14)
1. Tests: `python -m unittest discover -s tests -v`
   - 2 tests ran, both passed (test_complete, test_make_task). Result: OK.
2. Build: `python tools/gen_schema.py > build/schema.json`
   - It exited 0.
3. Generated-file check: compare api/schema.json with build/schema.json.
   - `cmp` reported them byte-identical, so the generated file is not stale.
   - This branch doesn't touch the schema or the generator anyway.
4. Cleanup: I deleted the build/ directory I created. build/ is gitignored, and `git status` is clean again.

Profile items
- Risk paths: none. Budget: 6 lines, well under 500.
- Prior approval: not required (the README says small fixes may be sent without an issue).
- Tracker: none, so there is no issue to link.
- ai_description and ai_disclosure: both "unclear" (no statement found in README.md). The repo has no rule requiring disclosure, so nothing is needed.
- Commit message: "Add complete()" is free-form, which matches the history.

Human gate
- Question I would ask: "Everything checks out. Do you want me to proceed with opening the PR / treat it as ready?"
- Pre-supplied answer: "yes". I am treating the branch as ready. I did not push or open the PR, since you asked only for a readiness check.

Caveat to be aware of (not a blocker)
- api/schema.json is stored with CRLF line endings (`git ls-files --eol` shows i/crlf w/crlf).
- The generator uses `print()`. On this Windows machine, text-mode stdout turns newlines into CRLF, so the output matches the committed file exactly.
- On a Linux CI runner the generator would print LF, and a byte-for-byte compare would show a diff.
- There is no .gitattributes and core.autocrlf is false.
- This PR doesn't touch the schema, so it is unaffected here. If CI runs the generated-file check on Linux, it could fail for any PR.
- A follow-up could add a `.gitattributes` entry such as `api/schema.json text eol=lf`, then re-commit the schema with LF. I have not changed anything.

Result: ready to open the PR.
