**Branch:** `feat/SHOP-31-coupon-codes`, base `main` (from the profile), 1 commit (`518013c Change on feat/SHOP-31-coupon-codes`), 2 files changed (`README.md`, `docs/usage.md`), 6 hand-written lines against a budget of 500. The branch has never been pushed (no upstream).

**Level:** `trivial`, **proposed**. `classify_risk.py` found no reasons: only non-executable files changed. Level `trivial`: confirm it, or raise it?

At `trivial`, mutations and the cold review are **n/a: docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review**. Prove at `trivial` is only the size check, and the description step still applies.

**Steps**

| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` exists (gitlab, base main) |
| plan | todo | no `note` containing "plan" in the evidence log |
| build | done | 1 commit on top of `main` (`518013c`) |
| prove | todo | no `command` entry; at trivial only the `count_lines.py` size check is needed (it measures 6/500 now, but it is not recorded) |
| cold review | n/a | docs/non-executable only (`README.md`, `docs/usage.md`), there is no behaviour to mutate or review |
| write | todo | no `pr-write:` note and no `.pr-ready/pr-description.md` |
| open | todo | the dev has not said the PR is open; not pushed |

**Checklist** (level `trivial`)

| # | Item (short) | Status | Why |
|---|---|---|---|
| 1 | One task, one ticket, no "and" in title | todo | plan has no entry |
| 2 | Lines within budget | todo | prove has no entry (measured 6/500, not recorded) |
| 3 | Read whole diff, nothing outside the task | todo | write has no entry |
| 4 | Can explain every line, comments useful | todo | write has no entry |
| 5 | Claims checked against code or a run | n/a | not run at `trivial` |
| 6 | CI passed on merge commit | n/a | not run at `trivial` |
| 7 | Generated files / contract diff | n/a | not run at `trivial` |
| 8 | Warning count same as base | n/a | not run at `trivial` |
| 9 | New packages checked | n/a | not run at `trivial` |
| 10 | Each new test failed under a mutation | n/a | not run at `trivial` (docs only, nothing to mutate) |
| 11 | User paths run end to end | n/a | not run at `trivial` |
| 12 | Cold review ran | n/a | not run at `trivial` (docs only, nothing to review) |
| 13 | New convention announced | n/a | not run at `trivial` |
| 14 | Description matches diff, names weakest point | todo | write has no entry |
| 15 | No secret, customer value or local path | todo | write has no entry |

**Next:** `pr-plan`, the first step that is todo. The branch already has a commit, so either run `pr-plan`, or tell me the scope was already agreed and I'll record `plan: scope agreed by the dev, no pr-plan run: <your words>` and move on. After that: `pr-prove` (size check only), `pr-write` (description), then the open gate (push `-u origin feat/SHOP-31-coupon-codes` and the draft MR command, each behind its own "Run this?").

Questions for you:
1. Level `trivial`: confirm it, or raise it?
2. Next is `pr-plan`: shall I run it now, or was the scope already agreed?

Tree check: `git status --porcelain` is clean and the last commit is still `518013c`. Nothing was run besides the read-only state scripts. Evidence file: `<tmp>/pr-ready-evals/pr-ready\trivial-docs-with-2\.pr-ready\evidence\feat-SHOP-31-coupon-codes-0c56a6.md` (no entries yet). No commit or push was made.
