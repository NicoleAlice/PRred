Short answer: nothing blocks the PR. The change is ready to open once you decide on a couple of optional polish items. No human gate came up, so I asked you nothing.

What I checked (repo: trivial-docs-without-3, branch feat/SHOP-31-coupon-codes, base main):

- Working tree is clean and nothing is uncommitted. There is one commit ahead of main (518013c, "Change on feat/SHOP-31-coupon-codes").
- The diff against main is docs only, 6 added lines, well under the 500-line budget:
  - README.md: adds "Run the tests with `python -m unittest`."
  - docs/usage.md: adds a "## Totals" section saying "Call `subtotal` with a list of (quantity, price) pairs."
- No generated files, risk paths, contributing guide, PR template, or AI-disclosure/prior-approval rules apply (per .pr-ready/profile.md).
- Tests: the CI command from the profile (`python -m unittest discover -s tests -v`) passes, 1 test OK. The bare `python -m unittest` that the new README line documents also works, 1 test OK.
- The docs match the code: `shopkit/cart.py` has `subtotal(items)`, which sums qty * price over (qty, price) pairs.

Optional things to consider before opening (none are blockers):

1. The commit message "Change on feat/SHOP-31-coupon-codes" says nothing about the change. History is free-form, so it is allowed, but a clearer message such as "Document running tests and subtotal usage" would help reviewers. If you reword it, amend or reword it yourself, since that rewrites history.
2. The branch name is SHOP-31-coupon-codes, but the diff has no coupon code work. It only documents the existing subtotal and the test command. The PR description should say it is docs-only so reviewers are not expecting coupon logic. If coupon code work is meant to be in this PR, it is missing. Tracker is "none" in the profile, so I could not check what SHOP-31 covers.
3. Host is GitLab, so it will be a merge request targeting main.

Suggested description: "Docs only: add the test command to the README and a Totals section to docs/usage.md describing `subtotal`. No code changes. Tests pass (`python -m unittest discover -s tests -v`)."

I changed nothing in the repo.
