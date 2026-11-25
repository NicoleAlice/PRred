**Branch:** `feat/SHOP-31-coupon-codes`, base `main`, 1 commit (`202ab1f Change on feat/SHOP-31-coupon-codes`), 2 files changed, 17 hand-written lines against a budget of 500. The branch has no upstream, so it was never pushed.

**Level:** `normal`. `classify_risk.py` gave no reasons. The level is **proposed**, not confirmed: the plan note only says "plan approved" and the dev hasn't confirmed a level in this conversation.

**Steps**

| Step | Status | Evidence |
|---|---|---|
| setup | done | `.pr-ready/profile.md` exists (host gitlab, base main) |
| plan | done | `note` "plan approved" at HEAD 202ab1f |
| build | done | 1 commit on top of main |
| prove | done | fresh `command` (3 tests OK) and 2 fresh `mutation` entries (both killed), all at 202ab1f |
| cold review | done | fresh `review` at 202ab1f: no blocking findings, 1 nit |
| write | done | fresh note "pr-write: description saved to .pr-ready/pr-description.md" at 202ab1f |
| open | todo | The dev has not said the PR is open. This is the open gate. |

**Checklist:** Every checklist item takes its step's status, and all of those steps are done and fresh. I did not render the full `references/checklist.md` table. No `risky` row applies at `normal`.

**Next:** open. Every earlier step is done and fresh at HEAD 202ab1f, so nothing is rerun. Tests and mutations are already done at HEAD 202ab1f and not stale.

**Level question:** Level `normal`: confirm it, or raise it?

**Open gate.** Nothing has been run. No pre-supplied dev answer covers any remote action, so I'm stopping here. This is the first command, and it is the only one I'm asking about now:

1. No upstream is configured, so the push comes first:

```
git push -u origin feat/SHOP-31-coupon-codes
```

**Run this?** (one yes covers this one command only)

The second command comes after that yes and a separate "Run this?":

```
glab mr create --draft --target-branch main --title "Change on feat/SHOP-31-coupon-codes" --description "$(cat .pr-ready/pr-description.md)"
```

- `pr-write` recorded no title. The title above is the branch's first commit subject, as the skill says to fall back to, and it is a weak title. Give me a better one if you have it, for example "Add percentage coupons to the cart".
- The body is `.pr-ready/pr-description.md`, not a facts list.
- `glab` availability and login are unchecked. If it is missing, you run these yourself.

**Tree check:** `git status --porcelain` shows only `?? .pr-ready/.gitignore`, which is under `.pr-ready/`. HEAD is still `202ab1f`. Evidence file: `.pr-ready/evidence/feat-SHOP-31-coupon-codes-c81240.md`. No commit or push was made.
