# Showcase: one branch, with and without pr-ready

Fresh agents were given the same invented branch and the same prompt: "Get this branch ready for review." plus the pre-supplied gate answers shown below. Three runs had no plugin and three had pr-ready. This page reports what each run caught, quoted from its report. The result was **0/3 runs passing without the plugin and 1/3 with it.**

## The branch

`hookrelay` is an invented service that relays webhooks to subscriber URLs. The branch `feat/RELAY-12-delivery-retries` adds delivery retries in four commits:

- a retry policy;
- the sender that uses it;
- a CI change with a nightly smoke job;
- a README section.

The repo has a committed `.pr-ready/profile.md` (host GitLab) and no evidence log, so every step starts from scratch.

The fixture is [`evals/fixtures/showcase.py`](../evals/fixtures/showcase.py). The case, with its rubric, is [`evals/showcase/cases.json`](../evals/showcase/cases.json). The local test suite passes on the branch. Four faults are planted, one for each cold-review category from 2 to 5:

| # | Category | Where | The fault |
|---|---|---|---|
| 1 | A secret reaches a step that does not need it | `.gitlab-ci.yml:15-16` | The `build` job is given `RELAY_DEPLOY_TOKEN`; only `deploy` uses it. |
| 2 | A pipeline step that does not behave as written | `.gitlab-ci.yml:29` | `nightly-smoke` runs only when `CI_PIPELINE_SOURCE == "scheduled"`. GitLab sets `schedule`, so the job never runs. |
| 3 | An untested premise | `tests/test_retry.py:21-24` | `test_gives_up_after_max_attempts` asserts nothing, so giving up is untested. |
| 4 | A comment that says what the code does not | `relay/retry.py:12-15` | The comment says a 4xx is never retried; `should_retry` retries every status from 400 up. |

None of these fails a local test run.

## How it was run

The runs followed the procedure in [`evals/README.md`](../evals/README.md):

- a fresh fixture for each run;
- the runner prompt from `python evals/setup.py showcase end-to-end {with,without} <OUT_DIR>`;
- a fresh subagent for each run;
- a grader that scores the final report, `git status --porcelain` and `git log --oneline` against the rubric.

The prompt also carries the dev's pre-supplied answers to the gates, the same in both modes: scope agreed, level confirmed, "correct" as the README states it, a person has read the risky hunks, run each step, and no remote actions. A finding passes its rubric item only with a `file:line` citation.

## Results

| Rubric item | without 1 | without 2 | without 3 | with 1 | with 2 | with 3 |
|---|---|---|---|---|---|---|
| Secret on the build job, with file:line | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| Smoke rule never fires, with file:line | FAIL | FAIL | FAIL | FAIL | FAIL | PASS |
| False comment on 4xx, with file:line | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| Test with no assertion, with file:line | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| No commits and no remote actions | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| Faults found (any form) | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 | 4/4 |
| **Run passes** | FAIL | FAIL | FAIL | FAIL | FAIL | PASS |

The case result was **0/3 without pr-ready and 1/3 with it.** Under the eval rule a case passes at 2/3, so the showcase case **does not pass** in either mode.

Without the plugin, every run found three of the four faults but cited none of them by line. Every run also committed a fix on its own. With the plugin, every finding came with a verified `file:line`, nothing was committed or pushed, and the reports said "not ready" with surviving mutants listed. But two of the three runs missed the pipeline condition, the same fault every run without the plugin missed.

## What each run caught

### Without the plugin

All three runs found the token on the build job, the false 4xx comment and the empty test, each without a line number. None caught that the `"scheduled"` value never matches. All three created a commit on their own.

- **Run 1:** fixed the 4xx rule and the test, then committed: "New commit 6031f73 "Fix retry policy to retry only 5xx; assert retry limits in tests"". It said of the CI change: "The `nightly-smoke` job itself looks fine."
- **Run 2:** made the same kind of fix and committed it: "This is one new commit, `0b88688`". It treated the smoke job as a scope question, not a fault: "The `nightly-smoke` job and `tools/smoke.py` are also not retry work."
- **Run 3:** committed a fix: "Fixed in a new commit, 8b737d8 "Retry only 5xx responses, as documented"". On the smoke job it said the opposite of the fault: "The new `nightly-smoke` job only runs on scheduled pipelines, so it needs a pipeline schedule to run at all."

### With the plugin

Every run went through the status table, `pr-prove` (CI reproduced on the merge commit, then mutations) and `pr-cold-review`. Each stopped before `pr-write` with a "not ready" verdict. Nothing was edited, committed or pushed.

- **Run 1 (3/4, fail):** "Verdict: not ready for review." It ran 7 mutations: 1 killed, 6 survived. It tied the survivors to the empty test: "`tests/test_retry.py:21-24` (`test_gives_up_after_max_attempts`) asserts nothing. Mutations 2, 6 and 7 survived because of it." It raised the smoke job only as an unverified remark ("it only runs in scheduled pipelines, so there is no CI proof of it"), not as a wrong value.
- **Run 2 (3/4, fail):** "VERDICT: NOT READY for review." It reported "7 mutations run, 3 killed, 4 survived". It cited `.gitlab-ci.yml:28-29`, but only to ask whether a scheduled pipeline also reaches `deploy`. It never said `"scheduled"` is wrong.
- **Run 3 (4/4, pass):** "Verdict: not ready for review." It ran 7 mutations: 1 killed, 6 survived. It caught the pipeline fault: "`.gitlab-ci.yml:29` `$CI_PIPELINE_SOURCE == \"scheduled\"`: GitLab's value is `\"schedule\"` ... so `nightly-smoke` would never run and stay silently green."

## What this shows

- **The skills changed discipline and evidence.** Findings were located and verified at `file:line`, nothing was committed without asking, and mutation runs proved the tests weak (4 to 6 survivors per run) instead of leaving that as an opinion.
- **They did not make the review catch everything.** A subtle CI value typo (`scheduled` for `schedule`) was missed in 2 of 3 runs with the plugin, and in all 3 without it.
- **A person still reads CI and security-relevant changes line by line.** That is one of the method's gates ([human-gates.md](../references/human-gates.md)), and this result is why it stays a person's job.

## Notes

- The runs answered "a person has read the risky hunks" from the pre-supplied answers. Without the plugin, run 1 used that answer to leave the token change as it was ("You said a person has read the risky hunks").
- The grader checked each cited line against the fixture. All three runs with the plugin cite the false comment as `relay/retry.py:13-14` and the code as `:15`, which fall inside the planted range.

Raw reports and grades: [`evals/results/raw/showcase/`](../evals/results/raw/showcase/). Summary: [`evals/results/showcase.md`](../evals/results/showcase.md).
