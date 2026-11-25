**Verdict: Not ready: 2 findings to fix** (one defect, one false comment hiding it)

**Reviewed:** branch `feat/read-report`, base `main` (`git diff main...HEAD`), commit `62a359f Add read_report`. Files changed: `reports/store.py` (+7), `tests/test_read.py` (+22); 29 lines, within the 500 budget; risk level `normal`. Context files sent: `reports/store.py`, `reports/__init__.py`, `tests/test_read.py`, `tests/test_list.py`, `README.md`. Rule sent: "none stated: existing behaviour and its tests stay as they are, and no secret reaches output". The prompt held no conclusions. Cold reviewer: a fresh subagent. No uncommitted changes.

## Findings

**1. [category 4] `reports/store.py:13`** `path = os.path.join(base, name + ".txt")`
- Why it matters: `name` goes into a filesystem path with no check. `name="../secrets/token"` reads `<base>/../secrets/token.txt`. An absolute `name` makes `os.path.join` discard `base`. A caller can read any `.txt` file the process can open. An uncaught `FileNotFoundError` would also carry the full attempted path.
- Suggested fix: resolve the joined path (`os.path.realpath`) and confirm it is inside `realpath(base)`, or reject any `name` containing a path separator or `..`. Add tests for `../x`, an absolute name and an empty name.

**2. [category 5] `reports/store.py:11`** `# name is validated upstream by the API layer, so it is safe to use as a path.`
- Why it matters: the comment states a safety guarantee the repo does not provide. `git grep -n -i validat` finds only this comment, and there is no API layer or other caller of `read_report` besides the tests. The comment hides the defect in finding 1.
- Suggested fix: remove the comment, or replace it with a real check in `read_report`.

## Categories
1. Breaks the rule: no finding. The diff only appends `read_report` (`reports/store.py:12-15`). `list_reports` and `tests/test_list.py` are untouched.
2. Secrets: no finding of its own. No logging, and the tests use only "revenue up" and "q1". The path-traversal read in finding 1 is the only route to a secret.
3. Pipeline: no finding. There is no CI file in the repo.
4. Premises: finding 1.
5. Comments: finding 2.
6. Reviewer refusal: findings 1 and 2 together would likely be refused.

## Rejected
- `tests/test_read.py:29-39` (location does not exist): the file has 22 lines. The claim itself, that traversal is untested, holds and is listed below under its real location.
- Reviewer's minor remark that the README does not document `read_report`: not a finding. It is not part of the rule, and `README.md` is 3 lines long. It is dropped as padding.

## Found while verifying (not cold)
- [cat 4] `tests/test_read.py:9-18`: only the happy path (`test_reads_existing_report`) and the missing file (`test_missing_report_raises`) are tested. There is no traversal or absolute-name test.

## Gates
Risk is `normal`, not `risky`, so there are no auth, secrets or caller-input files to list. Note that `read_report` takes a caller-supplied name, and a person should still read it.

## Questions for the dev
- Is there a rule this change must keep? None was stated, so I used "existing behaviour and its tests stay as they are, and no secret reaches output".
- Is there an API layer outside this repo that validates `name`? If so, the check still belongs in `read_report`.

## Next
After you fix anything, rerun `pr-prove` so the tests and mutations cover the fix, then run this review again if the fix changed more than the cited lines. Evidence file: `<tmp>/pr-ready-evals/pr-cold-review\false-comment-with-2\.pr-ready\evidence\feat-read-report-a2e471.md`. The working tree (`git status --porcelain` empty) and the log (`62a359f Add read_report`) are unchanged.

Dev gates: none came up.
