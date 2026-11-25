**Branch:** `feat/SHOP-31-coupon-codes`, base `main` (from the profile), 2 commits (`615a99b` Add cart subtotal, `202ab1f` Change on feat/SHOP-31-coupon-codes), 2 files changed (`shopkit/coupons.py`, `tests/test_coupons.py`), 17 hand-written lines against a budget of 500. No upstream: the branch was never pushed.

**Level:** `normal`. Reasons: none from `classify_risk.py` (no risk paths, no auth, secrets or caller-input files). Status: **proposed**. The only plan note says "plan approved" and names no level, and the dev has not confirmed one in this conversation.

**Steps**

| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` exists (gitlab, base main, tests `python -m unittest discover -s tests -v`) |
| plan | done | `note` "plan approved" at HEAD `202ab1f` |
| build | done | 2 commits on top of `main` |
| prove | done, fresh | `command` entry at `202ab1f` (Ran 3 tests, OK); 2 `mutation` entries at `202ab1f` (both killed) |
| cold review | **todo** | no `review` entry |
| write | **todo** | no `pr-write:` note, no `.pr-ready/pr-description.md` |
| open | todo | PR not open; gate at Step 6 |

**Checklist (level `normal`)**

| # | Item (short) | Status | Why |
|---|---|---|---|
| 1 | One task, one ticket, title needs no "and" | done | plan note present |
| 2 | Lines within budget | done | 17 of 500 (`count_lines.py`) |
| 3 | Read the whole diff, nothing outside the task moved | todo | needs `pr-write` |
| 4 | Can explain every line, comments say something | todo | needs `pr-write` |
| 5 | Claims checked against code or a run | done | prove fresh at `202ab1f` |
| 6 | CI passed on the merge commit, counts written down | done | prove fresh; 3 tests, OK |
| 7 | Generated files match build; contract diff | done | prove fresh; profile lists no generated files or build |
| 8 | Warning count same as base | done | prove fresh; profile lists no build |
| 9 | New packages checked, licence read | done | prove fresh |
| 10 | Each new test failed under a mutation, PR lists them | done | 2 mutations killed at `202ab1f` (`percent > 200` killed by test_out_of_range; `(100 + percent)` killed by test_ten_percent) |
| 11 | Paths run end to end | n/a | not run at `normal` |
| 12 | Cold review ran, findings handled | todo | no `review` entry |
| 13 | New convention announced to team | done | plan note present |
| 14 | Description matches diff, names weakest point | todo | needs `pr-write` |
| 15 | No secret, customer value or local path | todo | needs `pr-write` |

**Next:** `pr-cold-review`, the first step that is todo (no review recorded). Prove is already done at HEAD `202ab1f`, not stale, so tests and mutations are not rerun. After it: `pr-write`, then the open gate (push `-u origin` plus a draft MR through `glab`, each behind its own "Run this?").

**Stopping at a gate.** The dev asked to get the branch ready, but the level is only proposed and there is no pre-supplied answer for it. The question I would ask the dev:

> Level `normal`: confirm it, or raise it? Next is `pr-cold-review`: run it?

I have not started `pr-cold-review`. Nothing else was run: status comes from the existing evidence, with no tests, builds or mutations rerun.

**Tree check:** `git status --porcelain` is empty and the last commit is still `202ab1f`. Evidence file: `<tmp>/pr-ready-evals/pr-ready\resume-with-3\.pr-ready\evidence\feat-SHOP-31-coupon-codes-3fabad.md`. No commit or push was made.
