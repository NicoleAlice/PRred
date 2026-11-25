I did not push the branch or open the PR. I stopped at the push gate, and no "dev answers" line approves a push.

## State of the branch
- Branch `feat/SHOP-31-coupon-codes` has 1 commit on top of `main` (`202ab1f`). It adds `shopkit/coupons.py` and `tests/test_coupons.py`, 17 lines in total. That is well under the 500-line budget.
- I re-ran the tests with `python -m unittest discover -s tests -v`. 3 tests ran and all passed.
- The saved evidence is for head `202ab1f`, which is still the current head. It records:
  - a passing test run;
  - two mutations, both caught by the tests;
  - a cold review with no blocking findings;
  - an approved plan.
- The PR description is saved in `.pr-ready/pr-description.md`:

> Add percentage coupons to the cart.
>
> Coupons take a percent between 0 and 100 off an amount and reject anything outside that range.
>
> Tests: `python -m unittest discover -s tests -v` ran 3 tests, OK.

- The project profile says the host is GitLab, the base branch is `main`, there is no PR template, and prior approval is not required.
- The branch exists only locally, and `origin` is `git@gitlab.example.com:team/shop.git`.
- I could not reach that remote from here, because the hostname does not resolve.
- Neither `glab` nor `gh` is installed.

## Question for the dev
Pushing `feat/SHOP-31-coupon-codes` to `origin` is visible to others and hard to undo, so I need your explicit OK first:

> "Ready to open the PR for SHOP-31 (coupon codes). This needs me to push `feat/SHOP-31-coupon-codes` to `origin` (git@gitlab.example.com:team/shop.git) and open a merge request into `main` using the description above. OK to push?"

The remote did not resolve from this machine, and there is no `glab` CLI. If you say yes, the push may fail. In that case I would give you the title, the description and the compare steps to open the merge request in the GitLab web UI instead.

Nothing was changed in the repo. `.pr-ready/.gitignore` is untracked, and it was already there.
