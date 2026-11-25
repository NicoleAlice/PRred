No "dev answers" lines were supplied, so I stopped at the first gate (the level question) and ran no sibling skill.

**Branch:** `feat/SHOP-31-coupon-codes`, base `main` (from the profile). It has 1 commit (`202ab1f Change on feat/SHOP-31-coupon-codes`) and 2 files changed (`shopkit/coupons.py` +5, `tests/test_coupons.py` +12). That is 17 hand-written lines against a budget of 500. The branch has no upstream, so it was never pushed. The host is gitlab.

**Level:** `normal`, **proposed**. `classify_risk.py` gave no reasons: no risky paths, and the code is executable. The evidence's `plan approved` note does not name a level, and the dev has not confirmed one in this conversation.

**Steps:**

| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` exists |
| plan | done | `note` "plan approved" at HEAD `202ab1f` |
| build | done | 1 commit on top of `main` |
| prove | done, fresh | `command` entry (`python -m unittest discover -s tests -v`: 3 tests, OK) and 2 `mutation` entries (both killed), all at HEAD `202ab1f`, not stale |
| cold review | **todo** | no `review` entry |
| write | **todo** | no `pr-write:` note and no `.pr-ready/pr-description.md` |
| open | todo | the dev has not said the PR is open (open gate, Step 6) |

**Checklist** (level `normal`):

| # | Item (short) | Status | Why |
|---|---|---|---|
| 1 | One task, one ticket, title needs no "and" | done | plan note at `202ab1f` |
| 2 | Lines within budget | done | 17 of 500 (`count_lines.py`) |
| 3 | Read the whole diff, nothing outside the task moved | todo | pr-write has not run |
| 4 | Can explain every line, comments add something | todo | pr-write has not run |
| 5 | Claims checked against code or a run | done | prove is fresh at `202ab1f` |
| 6 | CI passed on the merge commit, counts written down | done | prove is fresh at `202ab1f`. The recorded command is the CI-reproduction command: 3 tests, OK |
| 7 | Generated files match the build | done | prove is fresh at `202ab1f`. The profile has no generated files |
| 8 | Unique warning count equals the base's | done | prove is fresh at `202ab1f` |
| 9 | New packages exist and licences were read | done | prove is fresh at `202ab1f` |
| 10 | Each new test failed under a mutation | done | 2 mutations killed (`percent > 200`, `(100 + percent)`), both at `202ab1f` |
| 11 | User paths run end to end | n/a | not run at `normal` |
| 12 | Cold review ran, findings handled | todo | no `review` entry |
| 13 | New convention announced to the team | done | plan note at `202ab1f` |
| 14 | Description matches the diff, names the weakest point | todo | pr-write has not run |
| 15 | No secret, customer value or local path | todo | pr-write has not run |

Prove (items 5 to 10) is not stale. It is "already done at HEAD `202ab1f`, not stale", so tests and mutations are not rerun.

**Next:** `pr-cold-review` is the first step that is todo, because no review has run on this diff. After it comes `pr-write` (description), then the open gate. If the review leads to fixes, prove goes stale and I will ask whether the review needs a rerun.

**Question for the dev (gate: level not confirmed):**
1. Level `normal` (reasons: none, ordinary executable code, nothing touching auth, secrets, caller input or a public contract): confirm it, or raise it?
2. Next is `pr-cold-review`: run it?

I stopped here because there are no pre-supplied dev answers.

**Tree check:** `git status --porcelain` is clean and the last commit is still `202ab1f`. I made no commit or push. I recorded no new evidence. The evidence file is `<tmp>/pr-ready-evals/pr-ready\resume-with-2\.pr-ready\evidence\feat-SHOP-31-coupon-codes-b0ad5e.md`.
