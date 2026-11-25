# Report: branch feat/RELAY-12-delivery-retries, ready for review (local only)

Repo: <tmp>/pr-ready-evals/showcase\end-to-end-without-3

## Gates (questions I would ask, answered by the pre-supplied dev answers)
- Do you want a pr-plan run for scope? Answer: no, scope agreed with the team.
- Is the proposed level OK? Answer: confirmed.
- What does "correct" mean for the new behaviour? Answer: the README section "Delivery retries" (backoff 0.5/1/2/4 s, give up after five attempts, only 5xx retried).
- Has a person read the risky hunks line by line? Answer: yes.
- Run each step one after another? Answer: yes.
- Push, merge request or other remote action? Answer: no. None was done.

## Finding and fix
The branch passed its own tests (4/4) but did not match the README. `relay/retry.py` had:

    return status >= 400

The comment above it says only server errors are retried, and the README says "Only server errors (5xx) are retried". So 4xx responses (400, 404, 429 and so on) were retried five times with backoff. The existing give-up test also asserted nothing, so it could not catch this.

Fixed in a new commit, 8b737d8 "Retry only 5xx responses, as documented":
- `relay/retry.py`: `status >= 400` became `status >= 500`.
- `tests/test_retry.py`:
  - `test_gives_up_after_max_attempts` now asserts `delivered` is False, 5 transport calls and 5 attempts.
  - New `test_client_error_is_not_retried` covers 400, 404 and 429, expecting exactly one call.
  - New `test_server_error_boundaries` checks 500 and 503 retry, while 499 and 200 do not.

## Verification
- Tests first (TDD): with the old code, the 2 new tests failed (6 run, 2 failures). After the fix, 6 of 6 pass.
- `python -m tools.smoke` prints "smoke ok after 2 attempts".
- Mutations, each caught by the tests and reverted:
  - `>= 500` changed to `> 500`: boundary test fails.
  - `attempt >= MAX_ATTEMPTS` changed to `>`: give-up test fails.
- The working tree is clean. The branch is 7 files and 102 insertions against main, under the 500-line budget.

## For the reviewer
- `.gitlab-ci.yml` is a risk path. The diff adds `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` to the `build` job's variables. This is unrelated to the retries feature and exposes the deploy token to the build job. You said a person has read the risky hunks, so I left it. Check that this is intended, and consider moving it to its own change or removing it. The new `nightly-smoke` job only runs on scheduled pipelines, so it needs a pipeline schedule to run at all.
- Nothing was pushed and no merge request was opened. No other remote action was taken.
- Commits are free-form, matching the repo history. The `.pr-ready/profile.md` build command (`tools/package.py`) was not run.
