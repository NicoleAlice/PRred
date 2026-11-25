# Report: SHOP-88 pre-PR check (branch feat/round-shipping)

## Verdict: not yet verified as good to go. I stopped at a human gate with no pre-supplied dev answer.

## What I checked
- The diff against main is one commit, "Round shipping cost". It adds `shipping_cost(weight_kg)` to `shop/shipping.py`:

```python
def shipping_cost(weight_kg):
    """Shipping cost rounded to a whole currency unit (SHOP-88)."""
    return round(base_cost(weight_kg))
```

- The project profile gives the test command `python -m unittest discover -s tests -v`. I ran it and it passes: 1 test, OK.
- That one test only covers the existing `base_cost` (`base_cost(2) ≈ 6.7`). **The branch adds no test for `shipping_cost`**, so a green suite says nothing about the new behaviour.
- The diff is small (5 lines), well under the 500-line budget. There are no risk paths and no generated files.

## Findings from running the new function
| weight_kg | base_cost | shipping_cost |
|---|---|---|
| 0 | 4.0 | 4 |
| 0.5 | 4.675 | 5 |
| 1 | 5.35 | 5 |
| 2 | 6.7 | 7 |
| 10/27 (about 0.370) | 4.5 | **4** |

- Python's `round()` rounds exact halves to the nearest even number. So `round(4.5)` returns 4 and `round(2.5)` returns 2, while `round(3.5)` returns 4.
- A customer whose cost is exactly x.5 can therefore be charged down or up depending on parity. For example 4.5 becomes 4, but 5.5 becomes 6.
- Float representation makes the behaviour hard to predict near halves.
- Negative weights are not rejected: -1 kg gives 3. This is probably out of scope, but it is unguarded.

## Gate: question for the dev (no pre-supplied answer, so I am stopping here)
"SHOP-88 says 'round the shipping cost'. What is the intended rule for a cost that falls exactly on .5?
- (a) conventional half-up (4.5 becomes 5)
- (b) banker's rounding, which is what `round()` does now (4.5 becomes 4)
- (c) always round up (ceil), so the customer never pays less than cost
- (d) always round down

Also, is the ticket's intended result the whole currency unit, as the docstring says, or should it round to 2 decimals?"

## Suggested next steps once the dev answers
1. Implement the chosen rule explicitly. For half-up, use `decimal.Decimal` with `ROUND_HALF_UP`, or `math.floor(x + 0.5)`. For (c), use `math.ceil`.
2. Add tests for `shipping_cost`, including an exact-half boundary and zero weight, and a mutation check that the tests fail if the rounding rule is changed.
3. Re-run `python -m unittest discover -s tests -v` and then open the PR.

Nothing in the repository was modified.
