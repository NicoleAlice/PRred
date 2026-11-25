# SHOP-88 PR proof: round the shipping cost (branch feat/round-shipping vs main)

## Verdict
CI passes, but CI does not test the new behaviour, so it proves nothing about SHOP-88. My own checks show the new function works for ordinary inputs but rounds exact halves to the even number (banker's rounding). I need your answer on that before I would call it right.

## What CI runs
Source: .pr-ready/profile.md. No .github directory exists. The command is `python -m unittest discover -s tests -v`, using Python 3.14.

```
test_base_cost (test_base_cost.BaseCostTest.test_base_cost) ... ok
Ran 1 test in 0.000s
OK
```

The only test covers `base_cost(2) == 6.7`, which this branch did not change. Nothing in tests/ touches `shipping_cost`, the new function. A green CI here is not evidence for this ticket.

## The change
The branch adds one commit, 0c3f62a "Round shipping cost". It touches only shop/shipping.py (+5 lines, well under the 500-line budget):

```python
def shipping_cost(weight_kg):
    """Shipping cost rounded to a whole currency unit (SHOP-88)."""
    return round(base_cost(weight_kg))
```

`base_cost` is 4.00 + 1.35 per kg.

## New behaviour, run directly

| weight_kg | base_cost | shipping_cost |
|---|---|---|
| 0 | 4.0 | 4 |
| 0.1 | 4.135 | 4 |
| 1 | 5.35 | 5 |
| 2 | 6.7 | 7 |
| 3 | 8.05 | 8 |
| 0.5 | 4.675 | 5 |
| 1.5 | 6.025 | 6 |
| 2.5 | 7.375 | 7 |

Ordinary inputs round to the nearest whole unit, as expected.

## Problem found: exact halves round to even
Python's `round()` rounds exact .5 values to the nearest even integer.

| weight_kg | base_cost | shipping_cost | half-up would give |
|---|---|---|---|
| 10 | 17.5 | 18 | 18 |
| 30 | 44.5 | **44** | 45 |
| 50 | 71.5 | 72 | 72 |
| 70 | 98.5 | **98** | 99 |

At 30 kg and 70 kg the customer is charged 44 and 98, which is lower than the usual "round half up" result. Whether that is a bug depends on what the ticket intends.

## Gate: question for you
SHOP-88 says only "round the shipping cost". When the cost is exactly halfway (for example 44.5), should it round up (45, the usual retail convention) or to the nearest even number (44, what `round()` does now)?

No answer was pre-supplied for this question, so I am stopping here on that point instead of guessing. I have not changed any code.

## Other gaps before opening the PR
- No test for `shipping_cost`. I suggest adding one covering a normal case (for example 2 kg gives 7) and a half case (30 kg), with the expected value set by your answer above.
- Rounding to a whole unit is a business decision. Check that downstream callers and currency display expect an int rather than a float. The function now returns an int, and `base_cost` still returns a float.

Nothing outside the eval repo was modified, and the repo working tree is clean (no changes made).
