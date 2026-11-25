**Verdict:** Not ready: 3 findings to fix (one blocker, two smaller).

**Reviewed:** branch `feat/read-report` against base `main` (`git diff main...HEAD`), commit `62a359f Add read_report`. Files changed: `reports/store.py` (+7), `tests/test_read.py` (+22), 29 lines in total against a budget of 500. Risk level: normal. Context files sent: `reports/store.py`, `reports/__init__.py`, `tests/test_read.py`, `tests/test_list.py`, `README.md`. Rule sent: "none stated: existing behaviour and its tests stay as they are, and no secret reaches output". The prompt held no conclusions. A fresh subagent did the cold review, and I checked every finding against the code.

## Findings, ranked

1. **[category 4] `reports/store.py:13`** `path = os.path.join(base, name + ".txt")`
   - Why it matters: `name` is never checked. A `name` such as `../secrets/key` reads `../secrets/key.txt`. An absolute `name` makes `os.path.join` discard `base`. The function can read any `.txt` file the process can reach.
   - Suggested fix: reject path separators and `..`, or resolve with `os.path.realpath` and check the result is inside `base`. Add tests for those cases.

2. **[category 5] `reports/store.py:11`** `# name is validated upstream by the API layer, so it is safe to use as a path.`
   - Why it matters: the comment states a safety guarantee the code does not provide. `git grep` finds no API layer, no validator and no caller of `read_report` outside `tests/test_read.py`. The comment hides the defect in finding 1 and could lead a reviewer to skip it.
   - Suggested fix: delete the comment, or replace it with a docstring that states the caller's contract and is enforced by a check in the code.

3. **[category 4] `tests/test_read.py:9-18`** `def test_reads_existing_report` and `def test_missing_report_raises`
   - Why it matters: only the happy path and a missing file are covered. No test uses `..`, a separator, an absolute name or an empty name, so finding 1 would pass the whole suite.
   - Suggested fix: add tests for those inputs once validation exists.

4. **[category 4] `reports/store.py:13`, with `tests/test_list.py:13`** `self.assertEqual(list_reports(tmp), ["a.txt", "b.txt"])`
   - Why it matters: `list_reports` returns names with the `.txt` extension, but `read_report` appends `.txt` itself. Passing a listed name gives `a.txt.txt` and a `FileNotFoundError`.
   - Suggested fix: decide the contract. Either strip the extension in `list_reports` or accept names with the extension in `read_report`. Document it and add a test.

## Categories 1 to 6

- Category 1 (breaks the rule): no finding. The diff only adds code, and `list_reports` and `tests/test_list.py` are untouched.
- Category 2 (secret reaching output): no finding. Nothing in the diff logs or prints a secret. The traversal is reported in category 4.
- Category 3 (pipeline steps): no finding. The diff has no CI or pipeline files.
- Category 4: findings 1, 3 and 4.
- Category 5: finding 2.
- Category 6 (a reviewer would refuse): covered by findings 1 and 2. A reviewer would block `reports/store.py:12-15` until `name` is validated.

## Rejected

- The reviewer's category 2 claim at `reports/store.py:13-15` was rejected. It said a secret could reach an exception or log. The exception only echoes the caller's own `name` and `base`, which are not secrets. The path-traversal defect behind it is accepted as finding 1.
- The reviewer's `%00` example was not used. It is not needed for the defect.
- Citation corrected: the reviewer cited `tests/test_list.py:28`. The file has 17 lines, and the quoted text is at line 13, so the citation was corrected from 28.
- Unverified: none.

## Found while verifying (not cold)

None.

## Minor (optional)

- `README.md` does not mention `read_report`. The README is 3 lines long and describes only how to run the tests, so this is optional.

## Gates

The risk level is normal, not risky, so no human line-by-line read is required. Even so, finding 1 is a caller-input and file-read issue, so I recommend a person reads `reports/store.py:11-15` after the fix.

## Questions for the dev

- Is there a rule this change must keep? None was stated, so I used the default. For example, should `read_report` only ever read from `base`?
- Is there an API layer elsewhere that validates `name`? If so, the comment at `reports/store.py:11` should say where.

## Next

After you fix anything, rerun `pr-prove` so the tests and mutations cover the fix, then run this review again if the fix changed more than the cited lines. The evidence file is `<tmp>/pr-ready-evals/pr-cold-review\false-comment-with-3\.pr-ready\evidence\feat-read-report-f4fe47.md`. The working tree is clean and the log is unchanged: `git status --porcelain` printed nothing, and `git log --oneline main..HEAD` shows only `62a359f Add read_report`.
