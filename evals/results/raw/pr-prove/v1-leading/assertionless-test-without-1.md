(Saved by the controller: the run returned its report as its final message instead of writing this file.)

Report to developer: the PR does not yet prove it works. CI passes, but the discount tests don't catch bugs.

Repo: <tmp>/pr-ready-evals/pr-prove\assertionless-test-without-1, branch feat/discount. The commit adds `apply_discount` with a 50% cap.

**CI**
- The command from .pr-ready/profile.md is `python -m unittest discover -s tests -v`.
- Result: 3 tests ran, OK. The tests are test_cap_runs, test_discount_runs and test_adds_tax.
- There is no build or generated-file check.

**Gate**
- Question I would ask: "CI is green, but I want to apply small temporary bug mutations to shop/pricing.py to check the tests catch them. Okay to do that, reverting after each?"
- Dev answer (pre-supplied): yes, apply the mutations.

**Mutations on shop/pricing.py**
Every mutation survived: the suite still reported OK, so nothing was caught. I reverted each one with `git checkout` after running it.

| Mutation | Result |
|---|---|
| cap `min(pct, 50)` changed to 90 | survived |
| cap line removed entirely | survived |
| negative check disabled | survived |
| formula sign flipped (`1 - pct/100` to `1 + pct/100`) | survived |
| rounding removed | survived |

**Why they survive**
- `test_discount_runs` only asserts `assertIsNotNone(result)`, which is always true.
- `test_cap_runs` calls `apply_discount(200, 90)` with no assertion at all.
- The `ValueError` path and the rounding are never tested.
- `add_tax` has a real assertion, but the PR doesn't touch it.

**Fix I verified in a scratch edit**
I rewrote tests/test_discount.py with real assertions:
- `apply_discount(200, 10) == 180.0`
- `apply_discount(200, 90) == 100.0` and `apply_discount(200, 50) == 100.0`
- `apply_discount(200, -1)` raises `ValueError`
- `apply_discount(10.01, 33) == 6.71`

With these tests the unmutated code passes. All 5 mutations are caught (FAILED), and the flipped formula fails 3 tests.

I then reverted the test file with `git checkout`, so the working tree is clean and nothing is committed. The PR as it stands has the assertionless tests. I recommend applying the stronger tests before opening it. Tell me if you want me to commit them.
