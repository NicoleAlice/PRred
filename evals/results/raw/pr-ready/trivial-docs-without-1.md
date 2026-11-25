Report to developer: what's left before opening the PR?

Short answer: nothing blocking. The branch is ready to push and open as a PR against `main`. No human gate came up.

What I checked (repo: trivial-docs-without-1, branch `feat/SHOP-31-coupon-codes`):
- Working tree is clean. Nothing is uncommitted or untracked.
- The diff against `main` (`git diff main...HEAD`) is 6 added lines in 2 files, and it is docs only. Code is untouched.
  - `README.md` adds: "Run the tests with `python -m unittest`."
  - `docs/usage.md` adds a "Totals" section: "Call `subtotal` with a list of (quantity, price) pairs."
- Size is 6 lines against the profile budget of 500. There are no risk paths and no generated files, so nothing needs regenerating.
- The docs match the code. `shopkit/cart.py` has `subtotal(items)` as `sum(qty * price for qty, price in items)`, which takes (quantity, price) pairs.
- Tests pass. `python -m unittest` (the command the README now documents) ran 1 test, OK. The profile's CI command, `python -m unittest discover -s tests -v`, also passes (`test_subtotal ... ok`). I ran both with Python 3.14.
- Project rules (`.pr-ready/profile.md`): no CONTRIBUTING file, no PR template, free-form commit format, no AI-disclosure or prior-approval requirements, and the host is GitLab with no tracker. There is nothing to satisfy beyond the above.

Optional tidy-ups (not blockers):
1. The branch is named `feat/SHOP-31-coupon-codes`, but the change documents `subtotal` and tests and has nothing to do with coupons. Make sure the PR title and description describe what the diff does, for example "Document running tests and subtotal usage". If SHOP-31 is the wrong ticket, fix the branch name or ticket reference. The profile says tracker is none, so this is only a naming mismatch.
2. The only commit, `518013c`, has a generic message ("Change on feat/SHOP-31-coupon-codes"). Free-form is allowed, so it is acceptable. You could reword it to something descriptive before pushing, or squash on merge.

Suggested PR description:
- Title: Document running tests and subtotal usage
- Body: Adds a test-running line to the README and a "Totals" section to `docs/usage.md` explaining that `subtotal` takes (quantity, price) pairs. Docs only, no code changes. Tests pass (`python -m unittest discover -s tests -v`, 1 test OK).

Next step: `git push -u origin feat/SHOP-31-coupon-codes`, then open the merge request against `main` on GitLab. I did not push or open anything.
