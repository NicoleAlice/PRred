# PR readiness check: feat/complete -> main

Verdict: good to go. I found no blockers. There is one portability caveat, described below.

## What the PR contains
- 1 commit, `005588d Add complete()`, touching one file: `todo/model.py` (+6 lines, well under the 500-line budget).
- It adds `complete(task)`, which returns a copy of the task with `done` set to True. The original task is not mutated.
- The working tree is clean. No stray files are tracked, and `build/` and `.pr-ready/evidence/` are gitignored.

## Checks run (commands from `.pr-ready/profile.md`)
- Tests: `python -m unittest discover -s tests -v` ran 2 tests, both OK (`test_make_task`, `test_complete`). The new `complete()` has a test.
- Generated file check: I ran `python tools/gen_schema.py > build/schema.json` and compared it with `api/schema.json`. The two files are byte-identical (`cmp` reported no difference). The PR does not touch `api/schema.json` or `tools/gen_schema.py`, so it needs no regeneration. I deleted `build/` afterwards, and the tree is clean again.
- Risk paths: none are defined. Budget: 6 lines of 500 allowed.
- Project rules: there is no contributing guide, PR template or agent rules. The profile says the AI-disclosure policy is unclear (nothing in the README), so disclosure is not required by anything I found. Prior approval is not required ("Small fixes may be sent without an issue").

## Caveat: line endings in the generated file
- `api/schema.json` is committed with CRLF line endings (`git ls-files --eol` shows `i/crlf w/crlf`). There is no `.gitattributes`, and `core.autocrlf` is false.
- `gen_schema.py` prints through `print()`, so its output follows the platform's newline convention. Here on Windows it produced CRLF, which is why the comparison passed. On a Linux CI runner the generator would emit LF. A strict byte-for-byte generated-file check there would then report a diff against the committed CRLF file.
- This is not caused by this PR, since the file is unchanged. If CI runs on Linux, consider normalizing the file in a separate change, for example by committing it with LF, or by adding a `.gitattributes` entry for `api/schema.json`.

## Human gate
- Question I would ask the dev: "Everything checks out locally. Do you want me to proceed with opening the PR against `main`?" Pre-supplied answer: yes.
- I did not open the PR. I only checked readiness, since the request was whether the branch is good to go.

## Suggested PR description
Add `complete(task)` to `todo/model.py`. It returns a copy of the task with `done=True` and leaves the input unchanged. It is covered by `test_complete`. The schema is unaffected.
