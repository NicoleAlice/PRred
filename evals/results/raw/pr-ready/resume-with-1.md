**Branch:** `feat/SHOP-31-coupon-codes`, base `main` (from the profile), 1 commit (`202ab1f Change on feat/SHOP-31-coupon-codes`), 2 files changed, 17 hand-written lines against a budget of 500. No upstream: the branch was never pushed.

**Level:** `normal`, **proposed**. `classify_risk.py` gave no risk reasons. Nothing in this conversation or in the plan note confirms it. The plan note only says "plan approved".

**Steps**

| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` exists (gitlab, base main, tests `python -m unittest discover -s tests -v`) |
| plan | done | `note` at HEAD 202ab1f: "plan approved" |
| build | done | 1 commit on top of `main` |
| prove | done, fresh | `command` at 202ab1f (3 tests, OK); 2 `mutation` entries at 202ab1f (both killed); none stale |
| cold review | **todo** | no `review` entry |
| write | **todo** | no `pr-write:` note and no `.pr-ready/pr-description.md` |
| open | todo | the dev has not said the PR is open |

**Checklist (level `normal`)**

| # | Item (short) | Status | Why |
|---|---|---|---|
| 1 | One task, one ticket | done | plan note exists |
| 2 | Lines within budget | done | 17 of 500 (prove) |
| 3 | Whole diff read, nothing outside the task | todo | pr-write has not run |
| 4 | Every line explained, comments useful | todo | pr-write has not run |
| 5 | Claims checked | done | prove entries fresh at 202ab1f |
| 6 | CI passed, counts written down | done | the CI-reproduce command is recorded: 3 tests, OK |
| 7 | Generated files match | done | profile says no generated files or check |
| 8 | Warning count same as base | done | profile says no build |
| 9 | New packages checked | done | covered by prove; no entry flags a new package |
| 10 | Each new test killed by a mutation | done | 2 mutations killed, at 202ab1f |
| 11 | Paths run end to end | n/a | not run at `normal` |
| 12 | Cold review ran | **todo** | no `review` entry |
| 13 | New convention announced | done | plan note exists |
| 14 | Description matches the diff | todo | pr-write has not run |
| 15 | No secret or local path | todo | pr-write has not run |

**Next:** `pr-cold-review`, because no cold review has run on this code and the evidence has no `review` entry. After it come `pr-write` and then the open gate. `pr-prove` is already done at HEAD `202ab1f` and is not stale, so I did not rerun it.

**Gate reached.** You asked me to get the branch ready, but the level is not confirmed. I am stopping here with one question for you:

> Level `normal` (proposed, no risk reasons found): confirm it, or raise it? Next is `pr-cold-review`: run it?

No answer was supplied in the prompt (it had no "dev answers" lines), so I did not start `pr-cold-review`.

**Tree check:** `git status --porcelain` is empty. The last commit is still `202ab1f`. I ran no tests, builds or mutations and made no edits. No commit or push was made.

Evidence file: `<tmp>/pr-ready-evals/pr-ready\resume-with-1\.pr-ready\evidence\feat-SHOP-31-coupon-codes-1f943a.md`
