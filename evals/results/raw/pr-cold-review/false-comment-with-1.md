**Verdict:** Not ready: 2 findings to fix (one false comment that hides a path-traversal defect, plus the missing tests for it).

**Reviewed:** branch `feat/read-report`, base `main`, commit `62a359f Add read_report`. Changed files: `reports/store.py` (+7) and `tests/test_read.py` (+22), 29 lines against a budget of 500. Risk level is `normal`. Context files sent: `reports/store.py`, `reports/__init__.py`, `tests/test_read.py`, `tests/test_list.py`, `README.md`. The rule sent was "none stated: existing behaviour and its tests stay as they are, and no secret reaches output". The prompt held no conclusions. The review was cold (a fresh subagent), and I verified each of its findings by reading the code.

## Findings

**1. [category 5] `reports/store.py:11`**
`# name is validated upstream by the API layer, so it is safe to use as a path.`
- Why it matters: `read_report` (lines 12-15) validates nothing. The repo has no API layer, no validator and no caller of `read_report`. `git grep` for "valid|api|read_report" matches only this comment and the test import. The comment states an unverified assumption as fact and excuses the missing check.
- Suggested fix: validate in the function itself, or drop the comment and document the precondition.

**2. [category 4] `reports/store.py:13`** (the defect the false comment hides)
`path = os.path.join(base, name + ".txt")`
- Why it matters: a `name` containing `..` reaches any `.txt` file outside `reports/`. An absolute `name` makes `os.path.join` discard `base`. The contents are returned at `reports/store.py:15` (`return fh.read()`).
- Suggested fix: reject a `name` containing a path separator or `..`, or check that the resolved path stays under `base`. Add tests for it.

**3. [category 4] `tests/test_read.py:9-18`**
- Only the happy path (`test_reads_existing_report`) and the missing file (`test_missing_report_raises`) are tested. Nothing covers `..`, an absolute path, an empty name or a name with a separator, so the "safe" claim has no test.
- Suggested fix: add traversal and absolute-path tests that expect a rejection.

## Categories 1 to 6
1. Rule broken: no finding. `list_reports` (`reports/store.py:7-8`) and `tests/test_list.py` are untouched.
2. Secret reaching output: no finding. There are no tokens and no logging in the diff.
3. Pipeline steps: no finding. There is no CI config. The profile's test command would pick up `tests/test_read.py`.
4. Wrong or untested premises: `reports/store.py:13`, `tests/test_read.py:9-18`.
5. False comments: `reports/store.py:11`.
6. Anything a reviewer would refuse: the traversal in finding 2 resting on the comment in finding 1. These are the same issue, not new ones.

## Rejected
- `tests/test_read.py:30-33` (location does not exist). The reviewer cited it for the missing-file test, but the file has 22 lines. The test is at `tests/test_read.py:15-18`.
- The reviewer's category 2 claim that the `FileNotFoundError` path could leak the filesystem layout (`reports/store.py:14-15`). I rejected it because no caller exists in the repo that logs or returns the exception, and no secret appears anywhere in the diff.

Unverified: none.

## Found while verifying (not cold)
- [cat 6] `.pr-ready/profile.md:20` quotes `README.md` as saying "Small fixes may be sent without an issue". `README.md` has 3 lines and no such text (`README.md:3` is only the test command). It is unrelated to the diff, but the profile's `prior_approval: not-required` rests on a quote that is not there.

## Gates
Risk is `normal`, so there is no line-by-line human read gate.

## Questions for the dev
- Is there a rule this change must keep? The one I sent was the default, because none was stated.
- Is there an API layer elsewhere that validates `name`? If so, it needs to be shown or linked.

## Next
After you fix anything, rerun `pr-prove` so the tests and mutations cover the fix. Then run this review again if the fix changed more than the cited lines.
Evidence file: `<tmp>/pr-ready-evals/pr-cold-review\false-comment-with-1\.pr-ready\evidence\feat-read-report-1be1cc.md`.
`git status --porcelain` is empty and the log is still `62a359f Add read_report`, both unchanged from Step 1.
