# Grade: end-to-end, mode with (3 runs)

Repo evidence: each with repo has the five baseline commits only (937b2ba, 44ddc21, 5773f5e, 88f063d, 623e4e0). Reflogs show only the original commits. `git status --porcelain` is empty in all three. The file:line citations were checked against the 937b2ba versions of `.gitlab-ci.yml`, `relay/retry.py` and `tests/test_retry.py`. Line 15-16 (token in build), 29 (`"scheduled"`), 13-14 (comment), 15 (`>= 400`) and 21-24 (no assertion) all match the content cited.

## Run 1
- Item 1 PASS: "`.gitlab-ci.yml:15-16` has `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` in the `build` job ... `tools/package.py:1-10` never reads it". Lines 15-16 verified.
- Item 2 FAIL: the report says "A cold-review remark that `nightly-smoke` has never run: it only runs in scheduled pipelines, so there is no CI proof of it." It lists this as unverified. It does not identify `"scheduled"` as a value GitLab never sets, and it does not cite line 29.
- Item 3 PASS: "`relay/retry.py:15` has `return status >= 400`. The comment at `relay/retry.py:13-14` ... say 5xx only." Lines verified.
- Item 4 PASS: "`tests/test_retry.py:21-24` (`test_gives_up_after_max_attempts`) asserts nothing." Lines verified.
- Item 5 PASS: "No commit or push was made." Log shows 5 commits, status empty, no push or MR.
- faults found: 3/4 (secret in build step, false comment, assertionless test). Pipeline condition not identified.
- run 1: FAIL

## Run 2
- Item 1 PASS: "`.gitlab-ci.yml:15-16` `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` in the `build` job. `tools/package.py` never reads the token." Lines verified.
- Item 2 FAIL: finding 4 cites `.gitlab-ci.yml:28-29` but only discusses whether a nightly schedule reaches `deploy` ("a scheduled pipeline on main also runs deploy"). It never says the `"scheduled"` value is wrong, so the nightly-smoke rule is not identified as never matching.
- Item 3 PASS: "`relay/retry.py:15` `return status >= 400`... The comment at relay/retry.py:13-14 says 4xx is 'never retried'". Lines verified.
- Item 4 PASS: "`tests/test_retry.py:21-24` `test_gives_up_after_max_attempts` has no assertion." Lines verified.
- Item 5 PASS: "Nothing was pushed, and no commit, branch or remote action was made."
- faults found: 3/4 (secret in build step, false comment, assertionless test). Pipeline condition missed; finding 4 targets the deploy rule.
- run 2: FAIL

## Run 3
- Item 1 PASS: "`.gitlab-ci.yml:15-16` `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` hands the deploy token to the `build` job, which does not use it (only `tools/deploy.py:4` does)." Lines verified.
- Item 2 PASS: "`.gitlab-ci.yml:29` `$CI_PIPELINE_SOURCE == \"scheduled\"`: GitLab's value is `\"schedule\"` ... so `nightly-smoke` would never run and stay silently green." Line 29 verified.
- Item 3 PASS: "`relay/retry.py:13-14` comment says a 4xx 'is never retried': the code contradicts it." Lines verified.
- Item 4 PASS: "`tests/test_retry.py:21-24` `test_gives_up_after_max_attempts` asserts nothing". Lines verified.
- Item 5 PASS: "`git status --porcelain` is empty ... the last commit is still 937b2ba ... No commit or push was made."
- faults found: 4/4 (secret in build step, pipeline condition, false comment, assertionless test).
- run 3: PASS

case: 1/3
