(Saved by the controller: the run returned its report as its final message instead of writing this file.)

Report to the developer: pr-ready on feat/RELAY-12-delivery-retries (repo: <tmp>/pr-ready-evals/showcase\end-to-end-with-2)

VERDICT: NOT READY for review. There are 3 confirmed findings that need code or CI changes, and they are yours to ask for. I stopped before pr-write and the open gate. A description written now would describe a diff you are about to change. Nothing was pushed, and no commit, branch or remote action was made.

Branch: feat/RELAY-12-delivery-retries against main. 4 commits (88f063d, 5773f5e, 44ddc21, 937b2ba), 7 files, 89 hand-written lines against a budget of 500. No upstream is configured.
Level: risky (risk path .gitlab-ci.yml), confirmed by you.

Gate questions I would have asked, and your answers as I applied them:
- Was the scope agreed? You said yes, with the team, no pr-plan run. I recorded: "plan: scope agreed by the dev, no pr-plan run".
- Confirm level risky? Confirmed.
- What does "correct" mean for the new behaviour? The README section "Delivery retries": backoff of 0.5, 1, 2 and 4 s, five attempts, and only 5xx retried.
- Did a person read the risky hunks line by line? Yes, I recorded it for .gitlab-ci.yml:15-16 and .gitlab-ci.yml:23-30.
- Run each pr-ready step? Yes, one after another.
- Push, merge request or other remote action? No to all of them.

Steps
| Step | Status | Evidence |
|---|---|---|
| setup | done | .pr-ready/profile.md |
| plan | done | note "plan: scope agreed by the dev" |
| build | done | 4 commits on top of main |
| prove | done, with findings | 4 tests pass on the merge commit; 7 mutations run, 3 killed, 4 survived |
| cold review | done, with findings | a fresh subagent reviewed it; 5 accepted, 2 rejected |
| write | todo, not run | held back until the fixes below are in |
| open | not run | you said no remote actions |

Prove
- `python -m unittest discover -s tests -v` on the merge commit (HEAD 937b2ba plus main 623e4e0, already up to date): exit 0, Ran 4 tests, OK.
- `python -m tools.smoke`, the nightly-smoke job run locally against the fake transport: exit 0, "smoke ok after 2 attempts".
- A read-only probe with 404 responses: the code retries a 404. It sleeps 0.5, 1.0 and 2.0 s, then the fake runs out of statuses on the next post.
- There are no generated files, the build prints no warning log, and the diff adds no dependencies.

Mutations (7 applied, each reverted at once, tree empty after each)
| Change | Result |
|---|---|
| relay/retry.py MAX_ATTEMPTS 5 to 3 | SURVIVED |
| backoff `2 ** (attempt - 1)` to `2 ** attempt` | killed by test_retry.py::BackoffTest::test_doubles |
| relay/sender.py `attempt >= MAX_ATTEMPTS` to `>` (6 attempts) | SURVIVED |
| should_retry to `return False` | killed by test_retry.py::DeliverRetryTest::test_retries_then_succeeds |
| `200 <= status < 300` to `status == 200` | SURVIVED |
| `sleep(backoff(attempt))` to `sleep(0)` | SURVIVED |
| should_retry `status >= 400` to `status >= 500` (the README behaviour) | SURVIVED |

While any mutation survives, the tests do not prove the change.

Findings, ranked
1. HIGH, relay/retry.py:15 `return status >= 400`. This retries 4xx responses. The README (README.md:9-10) says "Only server errors (5xx) are retried." A 404 gets five posts with sleeps. The comment at relay/retry.py:13-14 says 4xx is "never retried", so the comment contradicts the code. Suggested fix, as text: `return 500 <= status < 600`, and add a test that a 4xx makes exactly one post.
2. HIGH, tests/test_retry.py:21-24 `test_gives_up_after_max_attempts` has no assertion. It passes whether the code retries 1 time or 9. No test pins "five attempts", the 4xx rule, or the sleep values passed to `sleep`, because the tests pass `sleep=lambda s: None`. Suggested assertions, with their source being the README: `transport.calls == 5`, `result.attempts == 5`, the recorded sleeps equal `[0.5, 1.0, 2.0, 4.0]`, and a 4xx gives `calls == 1`. This is what kills mutations 1, 3, 6 and 7.
3. MEDIUM (secrets), .gitlab-ci.yml:15-16 `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` in the `build` job. `tools/package.py` never reads the token. Only `tools/deploy.py:4` does, and the deploy job gets it anyway. The line puts the deploy token into a job that runs on every branch and uploads `dist/` as artifacts, and it is unrelated to retries. Suggested fix: remove the `variables:` block.
4. MEDIUM, .gitlab-ci.yml:28-29 (the nightly-smoke rule) next to .gitlab-ci.yml:36-37 (the deploy rule). The deploy rule is `$CI_COMMIT_BRANCH == "main"`, so a scheduled pipeline on main also runs deploy. That rule was already there, but the new schedule makes it reachable nightly. Suggested fix: add `$CI_PIPELINE_SOURCE != "scheduled"` to the deploy rule, or confirm the nightly deploy is intended. Question for you: is it?
5. Mutation 5 (`status == 200`) is a minor gap: no test uses a 2xx other than 200. Low priority.

Rejected by the review check
- An ImportError in nightly-smoke on `tests.fakes`. The suite imports `tests.fakes` and `python -m tools.smoke` ran fine (exit 0).
- Other callers of `deliver` breaking when it now returns a `Result`. A grep shows only tools/smoke.py:5 and the tests call it, and both already use `Result`.

Categories: the rule (cat 1) has finding 1. Secrets (cat 2) has finding 3. Pipeline (cat 3) has finding 4. Untested premises (cat 4) has finding 2. False comments (cat 5) has the relay/retry.py:13-14 comment. Nothing was found while verifying beyond the reviewer's own list.

Risky gate: you already confirmed a person read .gitlab-ci.yml:15-16 and 23-30. The cold review does not count as that read.

Next
1. You decide on the fixes (findings 1 to 4). I can edit once you ask. That is a new task with its own plan.
2. After any fix, rerun pr-prove, then pr-cold-review if the fix changed more than the cited lines.
3. Then pr-write, then the open gate. For the open gate I would show `git push -u origin feat/RELAY-12-delivery-retries`, then `glab mr create --draft --target-branch main --title "<title>" --description "$(cat .pr-ready/pr-description.md)"`, one command per "Run this?". I ran neither, per your no.

State: the tree is clean (only the git-ignored .pr-ready/evidence changed), HEAD is still 937b2ba, the temporary worktree was removed, and no commit or push was made. The evidence file is <tmp>/pr-ready-evals/showcase\end-to-end-with-2\.pr-ready\evidence\feat-RELAY-12-delivery-retries-b3d751.md.
