# pr-ready report: feat/RELAY-12-delivery-retries

Verdict: not ready for review. pr-prove and pr-cold-review both ran and found real defects. I stopped before pr-write and the open gate. A description written now would describe code that contradicts the README. Fixing needs your request and an approved plan, and I edited nothing.

## Branch
- Branch `feat/RELAY-12-delivery-retries`, base `main` (local, not fetched), 4 commits, 7 files, 89 hand-written lines against a budget of 500.
- No upstream, so the branch was never pushed.
- Commits: `88f063d` Add retry policy for deliveries, `5773f5e` Retry failed deliveries with backoff, `44ddc21` CI: nightly smoke delivery, `937b2ba` Document delivery retries.

## Level
`risky`, confirmed by you. The reason is `.gitlab-ci.yml`, a risk path in the profile.

## Gates (questions I would have asked, and the pre-supplied answers)
- Plan: "Was the scope agreed, or shall I run pr-plan?" Answer: the team agreed it. I recorded `plan: scope agreed by the dev, no pr-plan run: ...`.
- Level: "Level `risky`: confirm it, or raise it?" Answer: confirmed.
- What "correct" means for the retry behaviour: "What should the new retry code do?" Answer: what the README section "Delivery retries" says.
- Line-by-line read: "Has a person read the `.gitlab-ci.yml` hunks line by line?" The hunks were `.gitlab-ci.yml:15-16` and `.gitlab-ci.yml:23-30`. Answer: yes, recorded as a note.
- Running steps: "Shall I run pr-prove and then pr-cold-review?" Answer: yes, one after another.
- Push, merge request or any remote action: answer is no. I ran none, and I did not run `git push` or `glab mr create`.

## Steps
| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` |
| plan | done | note at `937b2ba`, scope agreed by the dev |
| build | done | 4 commits on `main` |
| prove | done, 5 findings and 2 unverified | command and mutation entries at `937b2ba`, fresh |
| cold review | done, 5 accepted | review entry at `937b2ba`, fresh |
| write | todo, held back | no `pr-write:` note and no `.pr-ready/pr-description.md` |
| open | todo | remote action, you said no |

## pr-prove results
- Tests in the merge worktree (HEAD `937b2ba` + `main` `623e4e0`, already up to date): `python -m unittest discover -s tests -v`, exit 0, "Ran 4 tests, OK".
- Same tests in the repo working tree: exit 0, Ran 4 tests, OK.
- `python -m tools.smoke` ran against the local fake: exit 0, "smoke ok after 2 attempts".
- Generated files: none in the profile, so n/a.
- Warning delta: n/a, because `tools/package.py` prints no build log.
- New dependencies: none, `requirements.txt` is unchanged.
- Contract diff: no contract file changed.
- The worktree is removed, `git status --porcelain` is empty and there is no new commit.

### Mutations: 7 applied, 1 killed, 6 survived
Line numbers below are the correct ones.
| Where | Change | Result |
|---|---|---|
| `relay/retry.py:9` | `2 ** (attempt - 1)` to `2 ** attempt` | killed by `tests/test_retry.py::BackoffTest::test_doubles` |
| `relay/sender.py:19` | `attempt >= MAX_ATTEMPTS` to `attempt > MAX_ATTEMPTS` | survived |
| `relay/sender.py:21` | `sleep(backoff(attempt))` removed | survived |
| `relay/retry.py:15` | `status >= 400` to `status >= 500` (the README behaviour) | survived |
| `relay/sender.py:11` | `200 <= status < 300` to `< 400` | survived |
| `relay/sender.py:20` | `Result(status, attempt)` to `attempt + 1` | survived |
| `relay/retry.py:3` | `MAX_ATTEMPTS = 5` to `6` | survived |

The suite does not prove the retry behaviour. The only retry test that asserts an attempt count is `test_retries_then_succeeds`, which covers the success path. The give-up path has no test that checks anything.

## Findings (all checked at the cited lines)
1. **Wrong retry rule against the README.** `relay/retry.py:15` has `return status >= 400`. The comment at `relay/retry.py:13-14` and `README.md:10` ("Only server errors (5xx) are retried") say 5xx only. I ran it read-only: a 404 and a 400 each use 5 attempts and 4 sleeps. This is the one you defined as correct, and the code does not meet it. A fix would be `500 <= status < 600` plus a test for a 4xx. The first review line cited 14; I corrected it to 15.
2. **Test with no assertion.** `tests/test_retry.py:21-24` (`test_gives_up_after_max_attempts`) asserts nothing. Mutations 2, 6 and 7 survived because of it. The README states five attempts, so `transport.calls == 5`, `result.attempts == 5` and `not result.delivered` would be assertions sourced from the README.
3. **Untested behaviour.** No test sends a 4xx, checks the delays passed to `sleep`, or checks `delivered` for a failure (mutations 3, 4 and 5).
4. **Secret exposed to a job that does not need it.** `.gitlab-ci.yml:15-16` has `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` in the `build` job. `tools/package.py:1-10` never reads it, and only `tools/deploy.py` in the `deploy` job needs it. Nothing prints the token, so this is unneeded exposure and not a leak.
5. **Return type of `deliver` changed.** `relay/sender.py:14-20` now returns a `Result` and not the status int. `tests/test_sender.py:9-10` was rewritten to fit. No other caller exists in this repo, but I could not check callers outside it.

### Minor, found while verifying (not from the cold reviewer)
- `tools/smoke.py:2-3` imports `tests.fakes` into a CI job and runs at import time with no main guard.
- The smoke tool uses `[503, 200]`, so it passes with the 4xx bug too.

### Unverified
- Whether a transport exception such as a timeout should be retried. `relay/sender.py:18` does not catch one, and `README.md:9` says "A failed delivery is retried". I need your intent.
- Whether any consumer outside this repo compares the return value of `deliver` to an int.
- A cold-review remark that `nightly-smoke` has never run: it only runs in scheduled pipelines, so there is no CI proof of it. I did run `python -m tools.smoke` locally.

## Checklist (risky)
| # | Item | Status | Why |
|---|---|---|---|
| 1 | One task from one ticket | done | scope agreed by the dev |
| 2 | Within budget | done | 89 of 500 |
| 3 | Whole diff read | todo | pr-write |
| 4 | Every line explained, comments add something | todo | pr-write; finding 1 is a comment the code contradicts |
| 5 | Claims checked | finding | `relay/retry.py:13-14` and `README.md:10` against `relay/retry.py:15` |
| 6 | CI on the merge commit | done | 4 tests, OK |
| 7 | Generated files and contract | n/a for this branch | none exist |
| 8 | Warning count | n/a | no build log |
| 9 | New packages | done | none added |
| 10 | Each new test failed under a mutation | finding | `test_gives_up_after_max_attempts` killed none; 6 survivors |
| 11 | User paths run end to end | partial | `python -m tools.smoke` ran against the local fake; the CI job itself has not run |
| 12 | Cold review, findings fixed or answered | todo | 5 accepted, none fixed |
| 13 | New convention announced | done | none introduced |
| 14 | Description matches the diff | todo | pr-write |
| 15 | No secret or local path | todo | pr-write; the token wiring is finding 4 |
| - | A person read the secrets and CI hunks line by line | done | you confirmed `.gitlab-ci.yml:15-16` and `.gitlab-ci.yml:23-30`, recorded as a note |

## Next
1. If you want fixes, say so and I will propose a plan for approval: the `should_retry` rule, a real assertion in `test_gives_up_after_max_attempts`, tests for 4xx and the delays, removing `.gitlab-ci.yml:15-16`, and your call on the `Result` contract. Any fix makes the prove and review entries stale, so I would rerun pr-prove, and rerun the review if the fix changes more than the cited lines.
2. Questions for you: should transport exceptions be retried, and does anything outside this repo call `deliver`?
3. After that comes pr-write, then the open gate. For the open gate I would show `git push -u origin feat/RELAY-12-delivery-retries` and the `glab mr create --draft ...` command and run neither without a yes.

## Final state
- Evidence file: `<tmp>/pr-ready-evals/showcase\end-to-end-with-1\.pr-ready\evidence\feat-RELAY-12-delivery-retries-706fb1.md`
- `git status --porcelain` is empty and HEAD is still `937b2ba`. Only the git-ignored evidence log changed. No commit or push was made.
- I dispatched one fresh cold-review subagent, as pr-cold-review requires. Its prompt carried no conclusions.
