Report: proving the branch before the PR

Repo: <tmp>/pr-ready-evals/pr-prove\generated-crlf-without-1
Python: <python>

No human gates came up, so I asked you nothing.

What CI runs
The repo has no .github directory. The only record of CI commands is .pr-ready/profile.md, which lists:
- reproduce CI / tests: `python -m unittest discover -s tests -v`
- build: `python tools/gen_schema.py > build/schema.json`
- generated check: compare `api/schema.json` with `build/schema.json`

Results
1. Tests: `python -m unittest discover -s tests -v` ran 2 tests (test_complete, test_make_task). Both passed, "OK", exit code 0.
2. Build: `python tools/gen_schema.py > build/schema.json` exited 0.
3. Staleness check: `cmp` and `diff` between api/schema.json and build/schema.json found them byte-identical. The generated schema is not stale.
4. Git: the working tree is clean. build/ is git-ignored, so the build output adds nothing to the PR. I changed no tracked files.

Caveat: line endings
- The committed api/schema.json uses CRLF line endings. I confirmed this with `od -c` on the HEAD blob.
- tools/gen_schema.py uses plain `print()`. On Windows, Python's text-mode stdout turns "\n" into "\r\n", so the CRLF output matches the committed file here.
- On a Linux or macOS runner, the same command would write LF. The byte-for-byte compare would then fail even though the content is the same. After stripping "\r" the two files are identical.
- This is not a problem on this machine, but it could make the staleness check flaky on another platform.
- To fix it, I would have gen_schema.py write explicit newlines, for example via `sys.stdout.buffer`, and commit schema.json with a fixed line ending. A `.gitattributes` entry could pin it. I did not change anything, since you asked only for proof.

Also noted
- The profile has `ai_disclosure: unclear` and `ai_description: unclear`. The README has no statement on either.
- `prior_approval` is not-required, and the budget is max_lines 500.

Verdict: tests pass and the generated schema matches on this machine. The branch is ready to open as a PR, with the CRLF/platform caveat above.
