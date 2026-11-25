**Not ready to open the PR yet.** The change has no test, and I found a rounding behavior that needs your decision.

**What the branch does:** `feat/round-shipping` has one commit, "Round shipping cost". It adds `shipping_cost(weight_kg)` to `shop/shipping.py`, which returns `round(base_cost(weight_kg))`. The diff is 5 lines against `main`, well under the 500-line budget.

**What I ran:** `python -m unittest discover -s tests -v` (the project's CI command) passes, with 1 test run. That test only covers the existing `base_cost` function. Nothing exercises `shipping_cost`, so the green run says nothing about SHOP-88.

**What I found:** Python's `round()` rounds exact halves to the nearest even number (banker's rounding), not up. I called the new function directly:

| weight_kg | base_cost | shipping_cost |
|---|---|---|
| 10 | 17.5 | 18 |
| 30 | 44.5 | **44** |
| 50 | 71.5 | 72 |
| 70 | 98.5 | **98** |

So 44.5 becomes 44 while 17.5 becomes 18. Customers would see inconsistent rounding at exact halves. The ticket says only "round the shipping cost", so I can't tell which behavior is intended.

**Question for you (no answer was supplied, so I'm stopping here):** At an exact half, such as 44.5, should shipping round half up (to 45, the usual retail expectation) or half to even (to 44, which is what the code does now)? Should it return an `int` (it does now) or a float like `44.0`?

**Before the PR:**
1. Once you answer, I'll change the rounding if needed. Half up would need something like `decimal` with `ROUND_HALF_UP`, or `math.floor(x + 0.5)`. Floats like 125.50000000000001 make exact-half handling fragile.
2. Add tests for `shipping_cost` in `tests/`: 0 kg, a below-half case (0.37 kg gives 4.4995, so 4), an above-half case, and the exact-half cases at 30 kg and 10 kg.
3. After that, rerun the tests and check that the new tests fail if the rounding line is changed (a mutation check). I'll do that and then confirm it's ready.

I changed nothing in the repo.
