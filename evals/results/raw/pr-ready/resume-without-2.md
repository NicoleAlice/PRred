# Report: feat/SHOP-31-coupon-codes ready for review (stopped at the push/MR gate)

## Resumed state
The branch already had an evidence log (`.pr-ready/evidence/feat-SHOP-31-coupon-codes-847f75.md`, git-ignored). It recorded a passing test run, two killed mutations and "plan approved", all at head=202ab1f, base=615a99b. HEAD and main had not moved since, so I did not redo that work. I re-ran the tests once to confirm: 3 of 3 passed.

## Scope
Compared with `main`, the branch adds 17 lines in two files: `shopkit/coupons.py` (`apply_coupon`) and `tests/test_coupons.py`. That is far below the 500-line budget. No risk paths or generated files apply, and the working tree was clean. The profile says host gitlab, tracker none, free-form commit format, AI description allowed. No AI disclosure or prior-approval rules were found.

## Verification gap found and fixed
I tried two new mutations on `apply_coupon`, then reverted each:
- `percent < 0` changed to `percent < -50`: it survived, because no test covered negative percents. The bounds check was therefore untested on the low side.
- `percent > 100` changed to `percent > 100 and False`: it was killed.

I added `test_negative_percent` to `tests/test_coupons.py` and committed it as `dfa640b "Test that negative coupon percent is rejected"`. With the test in place, the tests pass (4 of 4) and the same `< -50` mutation now fails. The source is back to its original state.

## Open observations (not changed)
- `docs/usage.md` says nothing about coupons. The profile names no docs requirement, so I left it. A one-line mention of `apply_coupon` would be a reasonable follow-up.
- The boundary values 0 and 100 are untested. For example, `> 100` changed to `>= 100` would survive. I did not add tests for this.

## Human gate: push and open the merge request
Question I would ask the dev: "The branch is verified. Should I push `feat/SHOP-31-coupon-codes` to origin (git@gitlab.example.com:team/shop.git) and open a GitLab merge request against `main`? Here is the draft."

There is no pre-supplied answer for this gate, so I stopped here. I did not push and did not open an MR.

### Draft MR
Title: `SHOP-31: Add coupon codes (percent discount)`

Description:

> ## What
> Adds `shopkit.coupons.apply_coupon(amount, percent)`. It takes a percentage off an amount and rounds the result to 2 decimals. It raises `ValueError` if `percent` is outside 0-100.
>
> ## Why
> SHOP-31: coupon code support.
>
> ## Testing
> `python -m unittest discover -s tests -v` passes, 4 of 4. I mutation-checked the bounds checks and the discount formula. Changing `> 100` to `> 200` and `(100 - percent)` to `(100 + percent)` were each caught by a test. A weakened `< 0` check was not caught at first, so I added `test_negative_percent`, which now catches it.
>
> ## Notes
> `docs/usage.md` does not yet document coupons. The change is 2 source files, about 30 lines.

## Local state
Branch `feat/SHOP-31-coupon-codes` is 2 commits ahead of `main` (202ab1f and dfa640b). The working tree is clean. I also appended a mutation entry to the git-ignored evidence log, but it is not tracked.

Repo: `<tmp>/pr-ready-evals/pr-ready\resume-without-2`
