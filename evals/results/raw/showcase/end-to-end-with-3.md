# pr-ready report: feat/RELAY-12-delivery-retries

**Verdict: not ready for review. 6 accepted findings, 7 mutation survivors out of 7 applied minus 1 killed (6 survived), 2 unverified. I stopped before `pr-write` because the branch has a real bug that would make any description false. Nothing was edited, committed or pushed.**

## Gates (question I would ask, and the pre-supplied answer used)
- Plan: "Was the scope agreed, or shall I run pr-plan?" Dev: agreed with the team, no pr-plan run. Recorded note `plan: scope agreed by the dev, no pr-plan run: ...`.
- Level: "Level `risky` (risk path `.gitlab-ci.yml`): confirm it, or raise it?" Dev: confirmed.
- What "correct" means: "What should the retry behaviour be?" Dev: what README "Delivery retries" says (0.5, 1, 2, 4 s backoff; give up after five attempts; only 5xx retried).
- Line-by-line read: "Did a person read the risky hunks line by line?" Dev: yes. Recorded note for `.gitlab-ci.yml:15-16` and `.gitlab-ci.yml:23-30`.
- "Run each step one after another?" Yes. "Push / merge request / remote action?" No, none run.

## Branch
`feat/RELAY-12-delivery-retries`, base `main`, 4 commits (88f063d, 5773f5e, 44ddc21, 937b2ba), 7 files, 89 hand-written lines against a budget of 500. No upstream (never pushed). Level: **risky**, confirmed (`risk-path:.gitlab-ci.yml`).

## Steps
| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` |
| plan | done | note "plan: scope agreed by the dev" at 937b2ba |
| build | done | 4 commits on top of main |
| prove | done, with findings | command + mutation entries at 937b2ba (fresh) |
| cold review | done, with findings | review entry at 937b2ba (cold subagent) |
| write | todo | not run, see Next |
| open | todo | dev said no remote action |

## Prove
| Command | Where | Exit | Counts |
|---|---|---|---|
| `count_lines.py --json` | repo | 0 | 89 of 500, not over budget |
| `classify_risk.py --json` | repo | 0 | risky |
| `python -m unittest discover -s tests -v` | merge worktree 937b2ba + main 623e4e0 (already up to date) | 0 | Ran 4 tests, OK |
| same | repo, before mutations | 0 | Ran 4 tests, OK |
| `python -m tools.smoke` (local fake) | repo | 0 | "smoke ok after 2 attempts" |
| read-only `deliver()` with `[404, 200]` | repo | 0 | 2 calls, slept 0.5, status 200: **a 404 is retried** |
| read-only `deliver()` with `[503]*10` | repo | 0 | 5 calls, 5 attempts, status 503 |

Generated files: none in the profile. Warning delta: not applicable (`tools/package.py` prints no build log). New dependencies: none (`requirements.txt` untouched).

### Mutations (7 applied, 1 killed, 6 survived)
| File:line | Change | Result |
|---|---|---|
| relay/retry.py:15 | `status >= 400` to `>= 500` | survived (no test sends a 4xx) |
| relay/retry.py:4 | `MAX_ATTEMPTS = 5` to `3` | survived |
| relay/retry.py:9 | `2 ** (attempt - 1)` to `2 ** attempt` | killed by `tests/test_retry.py::BackoffTest::test_doubles` |
| relay/sender.py:19 | `attempt >= MAX_ATTEMPTS` to `>` | survived |
| relay/sender.py:9 | `200 <= status < 300` to `status < 300` | survived |
| relay/sender.py:21 | `sleep(backoff(attempt))` to `sleep(backoff(1))` | survived |
| relay/sender.py:7 | `self.attempts = attempts` to `1` | survived |

Each was reverted and `git status --porcelain` was empty after each. While any mutation survives, the tests are not adequate.

## Cold review (fresh subagent, rule: the README "Delivery retries" behaviour)
Accepted (I resolved every citation at its line):
1. [cat 1] `relay/retry.py:15` `return status >= 400`: retries every 4xx, README says only 5xx. My run confirms a 404 is retried.
2. [cat 5] `relay/retry.py:13-14` comment says a 4xx "is never retried": the code contradicts it.
3. [cat 2] `.gitlab-ci.yml:15-16` `RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN` hands the deploy token to the `build` job, which does not use it (only `tools/deploy.py:4` does). Remove it. No value is printed anywhere.
4. [cat 3] `.gitlab-ci.yml:29` `$CI_PIPELINE_SOURCE == "scheduled"`: GitLab's value is `"schedule"` (from GitLab docs, not run here), so `nightly-smoke` would never run and stay silently green.
5. [cat 3] `.gitlab-ci.yml:37` `$CI_COMMIT_BRANCH == "main"`: also true in a scheduled pipeline on main, so `deploy` would run nightly once a schedule exists. Suggested: add `&& $CI_PIPELINE_SOURCE != "schedule"`.
6. [cat 4] `tests/test_retry.py:21-24` `test_gives_up_after_max_attempts` asserts nothing; no test covers a 4xx, the delays passed to `sleep`, or `result.attempts`.

Rejected: the claim that `python -m tools.smoke` fails for lack of `tools/__init__.py` (I ran it: exit 0).
Unverified: transport exceptions are not retried (README is silent; needs your rule); the `test` job also running in scheduled pipelines (needs a GitLab run, harmless).

## Suggested assertions (text only, expected values from the README you named)
- `deliver(..., FakeTransport([503]*10), sleep=rec)`: `transport.calls == 5`, `result.attempts == 5`, `not result.delivered`, and recorded delays `== [0.5, 1.0, 2.0, 4.0]`.
- `deliver(..., FakeTransport([404, 200]), ...)`: `transport.calls == 1`, `result.status == 404`.
- Suggested fix for the code: `return 500 <= status < 600`.

## Checklist (risky)
| # | Item | Status | Why |
|---|---|---|---|
| 1 | One task | done | scope agreed note |
| 2 | Within budget | done | 89 of 500 |
| 3, 4, 14, 15 | Diff read, comments, description, no secrets | todo | `pr-write` not run |
| 5 | Claims checked | finding | comment and README claim vs `retry.py:15` |
| 6 | CI on merge commit | partly | local reproduction green (4 tests); real GitLab CI not run, no remote actions |
| 7 | Generated files | n/a in practice | none in profile |
| 8 | Warning count | n/a | no build log |
| 9 | New packages | done | none |
| 10 | Each new test failed under a mutation | **not met** | 6 of 7 mutations survived |
| 11 | User paths run end to end | partly | `tools.smoke` run locally; the pipeline jobs are unverified |
| 12 | Cold review | done, findings open | 6 accepted |
| 13 | Convention announced | todo/not applicable | no new convention found |
| row | Person read the risky hunks | done | `.gitlab-ci.yml:15-16`, `23-30`, recorded |

## Next
Not `pr-write` yet: the description would have to name a 4xx-retry bug and a never-running job. Suggested order, each only if you ask me to edit:
1. Fix `relay/retry.py:15`, the `scheduled` typo (line 29), the deploy rule (line 37) and remove the token variable (lines 15-16); strengthen the tests above.
2. Rerun `pr-prove` (prove goes stale after new commits), then decide whether the review needs rerunning.
3. Run `pr-write`, then the open gate (`git push -u origin feat/RELAY-12-delivery-retries` and `glab mr create --draft ...`, each behind "Run this?"; you said no to remote actions, so none was run).

Questions for you: should exceptions from the transport (timeouts) be retried? Do you want me to apply the fixes?

## State
Evidence file: `<tmp>/pr-ready-evals/showcase\end-to-end-with-3\.pr-ready\evidence\feat-RELAY-12-delivery-retries-b71c9a.md`. `git status --porcelain` is empty (the evidence folder is git-ignored), the last commit is still 937b2ba, the temporary worktree was removed. No commit or push was made.
