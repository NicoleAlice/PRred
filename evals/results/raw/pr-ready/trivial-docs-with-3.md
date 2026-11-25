**Branch:** `feat/SHOP-31-coupon-codes`, base `main` (from the profile). 1 commit (`518013c Change on feat/SHOP-31-coupon-codes`). 2 files changed (`README.md`, `docs/usage.md`). 6 hand-written lines against a budget of 500. There is no upstream: the branch was never pushed.

**Level:** `trivial`. Reasons: only non-executable files changed, and `classify_risk.py` returned no reasons. The level is **proposed**, not confirmed.

**Steps**

| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` exists (gitlab, base main, tests command, budget 500) |
| plan | todo | No `plan` note in the evidence log |
| build | done | 1 commit on top of `main` |
| prove | todo | Only the `count_lines.py` size check is needed at `trivial`, and no `command` entry is recorded. The log is empty at HEAD `518013c`. |
| cold review | n/a | docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review |
| write | todo | No `pr-write:` note and no `.pr-ready/pr-description.md` |
| open | todo | The dev has not said the PR is open |

**Checklist** (level `trivial`)

| # | Item (short) | Status | Why |
|---|---|---|---|
| 1 | One task, one ticket, no "and" in the title | todo | plan has no evidence |
| 2 | Hand-written lines within budget | todo | The 6/500 lines fit, but the `count_lines.py` command is not recorded yet. `pr-prove` records it. |
| 3 | I read the whole diff, nothing outside the task moved | todo | write not run |
| 4 | I can explain every line, comments say something new | todo | write not run |
| 5 | Every claim checked against code or a run | n/a | not run at `trivial` |
| 6 | CI passed on the merge commit | n/a | not run at `trivial` |
| 7 | Generated files match the build | n/a | not run at `trivial` |
| 8 | Build warning count unchanged | n/a | not run at `trivial` |
| 9 | New packages checked | n/a | not run at `trivial` |
| 10 | Each new test failed under a mutation | n/a | docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review |
| 11 | User paths run end to end | n/a | not run at `trivial` |
| 12 | Cold review ran | n/a | docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review |
| 13 | New convention announced | n/a | not run at `trivial` |
| 14 | Description matches the diff, names the weakest point, asks nothing | todo | write not run |
| 15 | No secret, customer value or local path | todo | write not run |

**Next:** `pr-plan`. The branch already has a commit but there is no plan note. You can run `pr-plan`, or tell me the scope was agreed. In that case I record `plan: scope agreed by the dev, no pr-plan run: <your words>` and move on. After it come `pr-prove` (size check only), `pr-write`, then the open gate. The cold review and the mutations are n/a at this level.

**Questions for you**
1. Level `trivial`: confirm it, or raise it?
2. Next is `pr-plan`. Shall I run it now, or was the scope already agreed?

When the PR is opened, the steps will be `git push -u origin feat/SHOP-31-coupon-codes` and then `glab mr create --draft --target-branch main ...`. Each needs its own "Run this?" yes from you. I have not run either.

Tree check: `git status --porcelain` is clean and the last commit is still `518013c`. I ran no tests, builds or mutations. Evidence file: `<tmp>/pr-ready-evals/pr-ready\trivial-docs-with-3\.pr-ready\evidence\feat-SHOP-31-coupon-codes-68fb73.md`. No commit or push was made.
