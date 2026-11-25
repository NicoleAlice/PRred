# Report: SHOP-88 PR readiness check (branch feat/round-shipping)

**Verdict: not ready to call good to go. I'm stopping at one question for you.**

## What I checked
- The branch has one commit (`0c3f62a Round shipping cost`) on top of `main`. It adds `shipping_cost(weight_kg)` to `shop/shipping.py`:

  ```python
  def shipping_cost(weight_kg):
      """Shipping cost rounded to a whole currency unit (SHOP-88)."""
      return round(base_cost(weight_kg))
  ```
- The working tree is clean. The diff is 5 lines, well under the 500-line budget. There are no risk paths and no generated files.
- The CI command from the profile (`python -m unittest discover -s tests -v`) passes. It runs 1 test, `test_base_cost`, which only covers the existing `base_cost`.

## Problems
1. **The new function has no tests.** `shipping_cost` is not exercised anywhere. The passing suite says nothing about SHOP-88, so green CI doesn't show the change is correct.
2. **Python's `round()` rounds halves to the nearest even number (banker's rounding), which may not be what the ticket wants.** I ran it:

   | weight_kg | base_cost | shipping_cost |
   |---|---|---|
   | 10 | 17.5 | 18 |
   | 30 | 44.5 | **44** |
   | 50 | 71.5 | 72 |

   A 30 kg parcel at 44.50 rounds down to 44, while a 10 kg parcel at 17.50 rounds up to 18. If "round" means the usual shop convention (half up, so 44.5 becomes 45), this is a customer-visible bug. Float representation adds some risk too. The ticket text I have says only "round the shipping cost", so I can't tell which behaviour is intended.

## Question for you (no answer was supplied, so I'm stopping here)
**For SHOP-88, how should exact halves round? Half up (44.5 becomes 45), or is banker's rounding (44.5 becomes 44) acceptable? And should the result be a whole unit, or two decimals?**

## What I'd do once you answer
- If half up is wanted, change the implementation. For example, use `decimal.Decimal` with `ROUND_HALF_UP`, or `math.floor(x + 0.5)`.
- Add tests for `shipping_cost` covering a normal value (weight 20 gives 31), a half case at 10 kg (17.5) and at 30 kg (44.5), and weight 0 (gives 4).
- Re-run the suite, then confirm the PR is ready.

I changed nothing in the repository.
