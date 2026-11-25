# PR readiness check: feat/discount

Verdict: NOT ready as committed. The tests pass, but they prove nothing about the new behavior. I strengthened them (uncommitted) after the gate below.

## What the branch does
feat/discount adds 2 commits over main: `apply_discount(price, pct)` in shop/pricing.py (50% cap, rejects negative pct) and tests/test_discount.py. Diff is 24 lines, well under the 500-line budget.

## Test run (as committed)
`python -m unittest discover -s tests -v`: 3 tests, all OK.

## Problem: the discount tests have no real assertions
- `test_discount_runs` only does `assertIsNotNone(result)`.
- `test_cap_runs` calls `apply_discount(200, 90)` and checks nothing.

I mutated the source to see whether the tests notice. Every mutation passed all 3 tests:

| Mutation | Result |
|---|---|
| Remove the 50% cap | tests still pass |
| Cap at 90 instead of 50 | tests still pass |
| `1 - pct` changed to `1 + pct` (wrong math) | tests still pass |
| Drop the negative-pct ValueError | tests still pass |

So the PR's headline claim ("50% cap") is unverified by its own tests. Source files were restored after each mutation.

## Gate (question to dev)
"The discount tests would pass even if the cap, the math, and the negative check were all broken. Do you want me to replace them with real assertions before you open the PR?"
Dev answer: yes.

## Fix applied (uncommitted, tests/test_discount.py only)
Replaced the tests with value assertions:
- `apply_discount(200, 10) == 180.0`
- `apply_discount(200, 90) == 100.0` (cap)
- `apply_discount(200, 50) == 100.0` (exactly at cap)
- `apply_discount(200, 0) == 200.0`
- negative pct raises `ValueError`

Result: 6 tests pass. Re-running mutations (remove cap, cap 90, cap 49, wrong math, drop negative check): all 5 now FAIL the suite, so the tests detect them. Source (shop/pricing.py) is unchanged.

## Remaining before opening the PR
- The test change is in the working tree, not committed. Review and commit it (I did not commit or push).
- Other checks: the branch is rebased on main (main is the parent), no generated files, no risk paths, no AI-disclosure or prior-approval requirement in the profile or README (disclosure "unclear", approval "not-required").
- Minor note: `add_tax` has no negative or rate validation; out of scope for this PR.
