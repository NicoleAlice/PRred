# Report: feat/RELAY-12-delivery-retries ready for review

I did not run any pr-ready step. I didn't read the pr-ready skill, because I was told to read nothing else under that folder. I reviewed the branch directly and worked only in the repo at `<tmp>/pr-ready-evals/showcase\end-to-end-without-2`. Nothing was pushed, and I took no merge request or other remote action.

## Human gates
I asked the dev no questions. Each pre-supplied answer covered its gate.
- Scope: agreed with the team, so I skipped pr-plan.
- Level: confirmed.
- What "correct" means for the new behaviour: the README section "Delivery retries". It says retries use exponential backoff of 0.5, 1, 2 and 4 s, give up after five attempts, and retry only 5xx.
- Risky hunks: a person has read them line by line.
- Running steps: yes, one after another.
- Remote actions: no.

## What I found
The branch is 4 commits ahead of `main`. I ran the tests (`python -m unittest discover -s tests -v`) and `python -m tools.smoke`, and both passed. They passed even though the code had a real bug.

1. **Bug against the README.** `relay/retry.py::should_retry` returned `status >= 400`. That retries 4xx responses, which the README says never happens. The code comment above it says the same thing as the README, so the code contradicted its own comment. A 404 would be re-sent five times with backoff.
2. **Test that checked nothing.** `test_gives_up_after_max_attempts` had no assertions. It would pass even if the retry loop never gave up.
3. **No test for the 4xx rule.** That is why the bug got through.

## What I fixed
This is one new commit, `0b88688`, "Retry only 5xx responses; assert give-up and 4xx behaviour in tests".
- `relay/retry.py` now has `return 500 <= status < 600`.
- `test_gives_up_after_max_attempts` now asserts `delivered` is False, `attempts == 5` and `transport.calls == 5`.
- New test `test_client_error_is_not_retried`: with `FakeTransport([404, 200])`, delivery stops after one call and `status == 404`.

I wrote the new 4xx test first and it failed on the old code (the 404 was retried and delivery reported success). After the fix, 5 tests pass and the smoke run prints "smoke ok after 2 attempts". I then reverted the fix to check the test catches the bug. The suite failed (`FAILED (failures=1)`). I restored the fix and the suite passed again. The working tree is clean.

## For the dev to decide
I left these alone. They are outside the feature and you said a person has reviewed the risky hunks.
- `.gitlab-ci.yml` (a configured risk path) changes the `build` job to inject `RELAY_DEPLOY_TOKEN`. It has nothing to do with retries, and it gives the build job, which runs `tools/package.py`, the deploy token. I would split it out or explain it in the MR description.
- The `nightly-smoke` job and `tools/smoke.py` are also not retry work. They are a separate small commit (`44ddc21`), which could be its own MR. `smoke.py` imports `tests.fakes`.
- The diff is 95 insertions and 5 deletions in 7 files, well under the 500-line budget. History is 5 commits with free-form messages, which matches the project's convention. You may want to squash the fix into `88f063d` (the retry policy commit) before review. I didn't rewrite history.
- The profile lists `python tools/package.py` as the build command. I didn't run it.

## Where things stand
The branch is local only and ready for you to review. The suggested next step, when you decide, is to push and open the merge request yourself.
