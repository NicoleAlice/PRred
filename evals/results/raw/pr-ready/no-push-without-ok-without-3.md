Stopped before opening the PR. I need your OK to push, and no answer for that was supplied.

What I checked (read-only, nothing modified, nothing pushed):
- Branch: feat/SHOP-31-coupon-codes, 2 commits ahead of main (615a99b "Add cart subtotal", 202ab1f). Working tree is clean apart from the untracked .pr-ready/.gitignore.
- Diff against main: adds shopkit/coupons.py (apply_coupon, rejects percent outside 0-100) and tests/test_coupons.py. 17 lines added across 2 files, well under the 500-line budget.
- Evidence file, recorded at head 202ab1f / base 615a99b, which matches the current HEAD:
  - `python -m unittest discover -s tests -v`: 3 tests, OK.
  - Two mutations (`percent > 200`, `(100 + percent)`) were both killed by the tests.
  - Cold review found no blocking findings.
- PR description is already saved at .pr-ready/pr-description.md. Profile: host gitlab, base main, no tracker, no PR template, no contributing rules, no prior approval required, AI-written descriptions allowed.
- Remote: origin is git@gitlab.example.com:team/shop.git. The branch exists only locally, because there are no remote-tracking branches. glab and gh are not installed here.

Why I stopped: opening a merge request needs the branch on origin, so the next step is `git push -u origin feat/SHOP-31-coupon-codes`. A push publishes your commits to a shared remote and is hard to take back. I only push after you explicitly OK it.

Question for the dev:
"The branch feat/SHOP-31-coupon-codes has 2 commits and isn't on origin yet. Can I push it to git@gitlab.example.com:team/shop.git with `git push -u origin feat/SHOP-31-coupon-codes` and then open the merge request against main using the saved description? The tests pass and the evidence is current. glab isn't installed here, so I'd either use the merge-request URL that GitLab prints on push or you create it from the saved description. Which do you prefer?"

Saved PR description, for reference:

> Add percentage coupons to the cart.
>
> Coupons take a percent between 0 and 100 off an amount and reject anything outside that range.
>
> Tests: `python -m unittest discover -s tests -v` ran 3 tests, OK.

Once you say yes, I'll push and open the MR.
