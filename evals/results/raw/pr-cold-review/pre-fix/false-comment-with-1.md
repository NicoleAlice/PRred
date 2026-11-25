**Verdict:** Not ready: 2 findings to fix (one path traversal, one false comment hiding it).

**Reviewed:** branch `feat/read-report` against base `main` (`git diff main...HEAD`), 1 commit (`62a359f Add read_report`), 2 files, 29 lines added (`reports/store.py`, `tests/test_read.py`). Risk level: normal. There are no uncommitted changes. Context files sent: `reports/store.py`, `reports/__init__.py`, `tests/test_list.py`, `tests/test_read.py`, `README.md`. Rule sent: "none stated: existing behaviour and its tests stay as they are, and no secret reaches output". The prompt held no conclusions or hints. The review was cold: a fresh subagent did it, and I verified each finding myself.

## Findings

**1. [category 1/2] `reports/store.py:13`** `path = os.path.join(base, name + ".txt")`
- Why it matters: `name` is never checked. `read_report("../../secrets/api_key")` returns any `.txt` file outside `base`. An absolute `name` makes `os.path.join` drop `base` entirely, so `read_report("/etc/creds")` reads `/etc/creds.txt`. `read_report` returns the file contents, so anything it reads can reach the caller's output. A missing file also raises `FileNotFoundError` carrying the full path.
- Suggested fix: reject names that contain a path separator or `..`, or that are absolute. For example, require `os.path.basename(name) == name`, or check that the `realpath` of the result stays inside the `realpath` of `base`. Add tests for `../x`, an absolute name and a name with a separator.

**2. [category 5, and 4] `reports/store.py:11`** `# name is validated upstream by the API layer, so it is safe to use as a path.`
- Why it matters: nothing in the repo supports this. `git grep -n -i "validat\|api"` finds only this comment itself. There is no API layer, no caller of `read_report`, and no validation. The comment makes the missing guard in finding 1 look deliberate, so a reviewer may skip it. It is also untested: `tests/test_read.py` covers only the happy path (line 13) and a missing file (line 17), with no traversal case.
- Suggested fix: remove the comment and enforce the check in `read_report` (see finding 1). If a validating layer really exists, name it, link it and test the contract.

## Categories 1 to 6
1. Rule: `reports/store.py:13` (finding 1). `list_reports` (`reports/store.py:8`) and `tests/test_list.py` are unchanged and untouched.
2. Secrets: `reports/store.py:13` (the same traversal, which would let a secret file be read). The tests use temp directories and fixed strings only, so there is no leak in test output.
3. Pipeline: no finding. There is no pipeline; CI is only `python -m unittest discover -s tests -v`.
4. Premises: `reports/store.py:11` (finding 2), and no traversal test in `tests/test_read.py`.
5. Comments: `reports/store.py:11` (finding 2).
6. Reviewer would refuse: `reports/store.py:13` and `reports/store.py:11` (the same two findings).

## Rejected
- Category 3, extension mismatch: the reviewer said `list_reports` returns names with `.txt` (`tests/test_list.py:13` asserts `["a.txt", "b.txt"]`) while `read_report` appends `.txt` (`reports/store.py:13`), so feeding one into the other gives `a.txt.txt`. The code does behave that way, but it is a design inconsistency, not a step that fails to do what it says. It is not a category 3 finding. Cited line corrected from `tests/test_list.py:11` to `:13`. I list it as optional minor below.
- The reviewer's claim that `list_reports` returns code files for the default `base` is true (`reports/store.py:4`, `:8`), but it is existing behaviour and not part of this diff. It is not a finding.

Unverified: none.

## Minor (optional)
- `reports/store.py:13` vs `tests/test_list.py:13`: `list_reports` returns names with `.txt` and `read_report` expects them without. You may want to align them.

## Gates
Risk is normal, not risky, so no line-by-line human read is required by the gate. Finding 1 does concern caller input, though, so a person should look at the fix.

## Questions for the dev
- Is there a rule this change must keep? None was stated, so I used "existing behaviour and its tests stay as they are, and no secret reaches output".
- Is there an API layer that calls `read_report`? If so, where? If not, the comment at `reports/store.py:11` is false.

## Next
After you fix anything, rerun `pr-prove` so the tests and mutations cover the fix, then run this review again if the fix changed more than the cited lines. Evidence is recorded at `<tmp>/pr-ready-evals/pr-cold-review\false-comment-with-1\.pr-ready\evidence\feat-read-report-1be1cc.md`. The tree (`git status --porcelain`, empty) and the log (`62a359f Add read_report`) are unchanged from Step 1. I made no edits.
