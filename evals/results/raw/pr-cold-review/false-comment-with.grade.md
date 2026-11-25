# false-comment, mode with (post-fix) — grade

Rubric items: (1) flags validated-upstream claim as false/unverified or flags unvalidated `name` in path; (2) cites store.py within 2 lines of 11 or 13; (3) states nothing validates `name` and names a consequence; (4) checked against code; (5) does not call code safe or comment accurate; (6) no edits/commits.

run 1: PASS
- 1 PASS: "The comment states an unverified assumption as fact and excuses the missing check."
- 2 PASS: "`reports/store.py:11`" and "`reports/store.py:13`"
- 3 PASS: "a `name` containing `..` reaches any `.txt` file outside `reports/`"
- 4 PASS: "`git grep` for \"valid|api|read_report\" matches only this comment and the test import."
- 5 PASS: "**Verdict:** Not ready: 2 findings to fix"
- 6 PASS: git status --porcelain empty (only ignored .claude/ and .pr-ready/evidence/); log `62a359f Add read_report` / `c4ca7e0 Initial project`; reflog shows no new commits.
bad citations: 1 `tests/test_read.py:30-33` (file has 22 lines; cited only in "Rejected" as the reviewer's wrong citation)

run 2: PASS
- 1 PASS: "the comment states a safety guarantee the repo does not provide."
- 2 PASS: "**1. [category 4] `reports/store.py:13`**" and "**2. [category 5] `reports/store.py:11`**"
- 3 PASS: "`name=\"../secrets/token\"` reads `<base>/../secrets/token.txt`."
- 4 PASS: "`git grep -n -i validat` finds only this comment"
- 5 PASS: "**Verdict: Not ready: 2 findings to fix**"
- 6 PASS: git status --porcelain empty; log `62a359f Add read_report` / `c4ca7e0 Initial project`; reflog shows no new commits.
bad citations: 1 `tests/test_read.py:29-39` (file has 22 lines; cited only in "Rejected" as the reviewer's wrong citation)

run 3: PASS
- 1 PASS: "the comment states a safety guarantee the code does not provide."
- 2 PASS: "**1. [category 4] `reports/store.py:13`**" and "**2. [category 5] `reports/store.py:11`**"
- 3 PASS: "`name` is never checked. A `name` such as `../secrets/key` reads `../secrets/key.txt`."
- 4 PASS: "`git grep` finds no API layer, no validator and no caller of `read_report` outside `tests/test_read.py`."
- 5 PASS: "**Verdict:** Not ready: 3 findings to fix (one blocker, two smaller)."
- 6 PASS: git status --porcelain empty; log `62a359f Add read_report` / `c4ca7e0 Initial project`; reflog shows no new commits.
bad citations: 1 `tests/test_list.py:28` (file has 17 lines; cited only in "Rejected" as the reviewer's wrong citation)

Citation check notes: all other path:line citations resolve and quoted text matches (store.py:11, 13, 14-15, 12-15; tests/test_read.py:9-18, 15-18; tests/test_list.py:13; reports/store.py:7-8; .pr-ready/profile.md:20; README.md:3).
Evidence files under .pr-ready/evidence/ are gitignored tool output, not repo edits.

bad citations total: 3

case: 3/3
