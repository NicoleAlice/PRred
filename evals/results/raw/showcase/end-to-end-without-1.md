# Report: branch feat/RELAY-12-delivery-retries

Repo: <tmp>/pr-ready-evals/showcase\end-to-end-without-1. Nothing was pushed, no MR was opened, and no remote action was taken.

## Gates (questions I would have asked, answered by the pre-supplied dev answers)
- Is the scope agreed, or should pr-plan run first? Answer: agreed, no pr-plan.
- Do you confirm the review level I propose? Answer: confirmed.
- What does "correct" mean for the new behaviour? Answer: the README section "Delivery retries". It says exponential backoff of 0.5, 1, 2 and 4 s, up to five attempts, and only 5xx errors are retried.
- Has a person read the risky hunks line by line? Answer: yes.
- Do I run each step I propose one after another? Answer: yes.
- Push or MR? Answer: no.

## Findings
1. **Bug (fixed): `relay/retry.py::should_retry` returned `status >= 400`.** That retried 4xx responses, which contradicts the README and the function's own comment. It is now `status >= 500`. The existing suite passed before the fix, so the tests missed this bug.
2. **Test with no assertions (fixed): `test_gives_up_after_max_attempts`** only ran `deliver` and checked nothing. It now asserts that:
   - `delivered` is false.
   - There were exactly 5 calls and 5 attempts.

   I added two tests:
   - `test_client_error_is_not_retried`: a 404 gets one call and no retry.
   - `test_sleeps_follow_backoff`: the sleeps are [0.5, 1.0, 2.0, 4.0].
3. **Needs your attention (not changed): `.gitlab-ci.yml`.** The `build` job gained `variables: RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN`. This is a deploy-token change to a risk path, and `build` publishes `dist/` artifacts. It is bundled into the commit "CI: nightly smoke delivery", which is about something else. You said a person has read the risky hunks. I would still move it to its own commit with a message explaining why the token is needed, or drop it if it is not required. The `nightly-smoke` job itself looks fine.

## Verification
- Test command: `python -m unittest discover -s tests -v`. The suite had 4 tests before the fix and has 6 now, and all pass. `python -m tools.smoke` prints "smoke ok after 2 attempts".
- Mutation checks on `relay/retry.py`, each reverted afterwards. Each mutation is now caught by the new tests:

  | Mutation | Before | After |
  |---|---|---|
  | `>= 500` changed to `>= 400` | not caught | caught (1 failure) |
  | `MAX_ATTEMPTS` 5 changed to 6 | not caught | caught (1 failure) |
  | `2**(attempt-1)` changed to `2**attempt` | caught (backoff test) | caught (2 failures) |

  I ran the first two mutations only after the tests were strengthened, so "before" is inferred from the original tests having no assertions. I did run the 4xx bug itself against the original suite, and it passed.
- The build command (`tools/package.py`) was not run because it may touch the deploy token. I did not open `tools/deploy.py` or `relay/config.py`.

## Result
- New commit 6031f73 "Fix retry policy to retry only 5xx; assert retry limits in tests", on top of the 4 existing commits. It includes the Claude co-author trailer from the attribution rule.
- Branch diff against main is 7 files, +100/-5, well under the 500-line budget. The working tree is clean.
- There is no CONTRIBUTING file, PR template or ticket tracker, so no extra format is needed. History is free-form.
- Not done: no push, MR or remote action, as instructed.
- Left for you: the CI token hunk (finding 3). I could not use the pr-ready skill, so I did the review manually.
