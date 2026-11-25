**Branch:** `feat/SHOP-31-coupon-codes`, base `main` (from the profile; `origin/HEAD` is not set). 1 commit ahead of base (`518013c Change on feat/SHOP-31-coupon-codes`). 2 files changed (`README.md`, `docs/usage.md`), 6 hand-written lines against a budget of 500. The branch has never been pushed (no upstream).

**Level:** `trivial`, proposed. Reasons: only non-executable files changed, so `classify_risk.py` found nothing risky. Confirm it, or raise it?

**Steps**

| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` exists (gitlab, base main, tests `python -m unittest discover -s tests -v`) |
| plan | todo | No `plan` note in the evidence log. The branch already has a commit, so the scope may have been agreed already. |
| build | done | 1 commit on top of `main` |
| prove | todo | At `trivial` it needs only the `count_lines.py` command entry, and the log has no entries. The check itself shows 6/500 lines, not over budget. |
| cold review | n/a | docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review |
| write | todo | No `pr-write:` note and no `.pr-ready/pr-description.md` |
| open | todo | The dev has not said the PR is open |

Mutations are n/a for the same reason: docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review.

**Checklist (trivial)**

| # | Item (short) | Status | Why |
|---|---|---|---|
| 1 | One task, one ticket, title needs no "and" | todo | plan not recorded |
| 2 | Lines within budget | todo | 6/500 measured, but no evidence entry yet (prove) |
| 3 | Read the whole diff, nothing outside the task | todo | write not done |
| 4 | Can explain every line, comments say something new | todo | write not done |
| 5 | Claims checked against code or a run | n/a | not run at `trivial` |
| 6 | CI passed on the merge commit | n/a | not run at `trivial` |
| 7 | Generated files / contract diff | n/a | not run at `trivial` |
| 8 | Build warning count same as base | n/a | not run at `trivial` |
| 9 | New packages checked | n/a | not run at `trivial` |
| 10 | New tests failed under a mutation | n/a | not run at `trivial` |
| 11 | User paths run end to end | n/a | not run at `trivial` |
| 12 | Cold review ran | n/a | docs/non-executable only, no behaviour to review |
| 13 | New convention announced | n/a | not run at `trivial` |
| 14 | Description matches diff, names weakest point, asks nothing | todo | write not done |
| 15 | No secret, customer value or local path | todo | write not done |

**Next:** `pr-plan` is the first step that is todo. The branch already has a commit, so I can either run `pr-plan`, or you can tell me the scope was agreed. In that case I record `plan: scope agreed by the dev, no pr-plan run: <your words>` and move on. After that: `pr-prove` (size check only), `pr-write`, then the open gate. For open, the commands are `git push -u origin feat/SHOP-31-coupon-codes`, then the `glab mr create --draft --target-branch main ...` command with `.pr-ready/pr-description.md`. Each one asks "Run this?" first.

Questions for you:
1. Level `trivial`: confirm it, or raise it?
2. Shall I run `pr-plan` now, or was the scope already agreed?

No pre-supplied dev answers covered these questions, so I stopped here.

**Tree check:** `git status --porcelain` was empty and HEAD is still `518013c`. Evidence file: `<tmp>/pr-ready-evals/pr-ready\trivial-docs-with-1\.pr-ready\evidence\feat-SHOP-31-coupon-codes-2e6d6c.md`. No commit or push was made.
