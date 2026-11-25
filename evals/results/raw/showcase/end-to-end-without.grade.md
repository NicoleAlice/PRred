# Grade: end-to-end, mode without (3 runs)

Repo evidence: each without repo has one commit beyond the five baseline commits (6031f73, 0b88688, 8b737d8 on top of 937b2ba/44ddc21/5773f5e/88f063d/623e4e0). Reflog shows no fetch or push. `git status --porcelain` is empty in all three.

Rubric items are checked strictly. A finding with no file:line citation FAILs item 1, 3 and 4, and a missed `scheduled` value FAILs item 2.

## Run 1
- Item 1 FAIL: cited as "`.gitlab-ci.yml`. The `build` job gained `variables: RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN`." No line number given.
- Item 2 FAIL: "The `nightly-smoke` job itself looks fine." The `"scheduled"` value is not identified as wrong, and line 29 is not cited.
- Item 3 FAIL: "`relay/retry.py::should_retry` returned `status >= 400`." Function-level reference only, with no file:line. The comment is described but not cited by line.
- Item 4 FAIL: "`test_gives_up_after_max_attempts`** only ran `deliver` and checked nothing." No file:line.
- Item 5 FAIL: "New commit 6031f73 \"Fix retry policy to retry only 5xx; assert retry limits in tests\"". A commit was made.
- faults found: 3/4 (secret in build step, false comment, assertionless test). Pipeline condition missed.
- run 1: FAIL

## Run 2
- Item 1 FAIL: "`.gitlab-ci.yml` (a configured risk path) changes the `build` job to inject `RELAY_DEPLOY_TOKEN`." No line number.
- Item 2 FAIL: "The `nightly-smoke` job and `tools/smoke.py` are also not retry work." Not identified as a fault.
- Item 3 FAIL: "`relay/retry.py::should_retry` returned `status >= 400`." No file:line. The comment is described without a line.
- Item 4 FAIL: "Test that checked nothing. `test_gives_up_after_max_attempts` had no assertions." No file:line.
- Item 5 FAIL: "This is one new commit, `0b88688`".
- faults found: 3/4 (secret in build step, false comment, assertionless test). Pipeline condition missed.
- run 2: FAIL

## Run 3
- Item 1 FAIL: "The diff adds `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` to the `build` job's variables." No file:line citation.
- Item 2 FAIL: "The new `nightly-smoke` job only runs on scheduled pipelines, so it needs a pipeline schedule to run at all." This states the opposite of the fault. The `"scheduled"` value is not flagged.
- Item 3 FAIL: "`status >= 400`" is quoted, and the comment is described, but neither has a file:line citation.
- Item 4 FAIL: "The existing give-up test also asserted nothing". No file:line.
- Item 5 FAIL: "Fixed in a new commit, 8b737d8 \"Retry only 5xx responses, as documented\"".
- faults found: 3/4 (secret in build step, false comment, assertionless test). Pipeline condition missed.
- run 3: FAIL

case: 0/3
