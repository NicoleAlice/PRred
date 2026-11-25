I can't yet say SHOP-88 is proven right. CI passes, but it never calls the new function. The new function also rounds exact halves in a way that needs your decision. I stopped at that question and made no changes to the repo.

## What CI runs

The profile (`.pr-ready/profile.md`) gives this as the CI command. There is no `.github` directory.

```
python -m unittest discover -s tests -v
```

Result:

```
test_base_cost (test_base_cost.BaseCostTest.test_base_cost) ... ok
Ran 1 test in 0.000s
OK
```

That test only covers `base_cost(2) == 6.7`, and `base_cost` is unchanged by this branch. The branch adds `shipping_cost` in `shop/shipping.py` (+5 lines, no test changes). Nothing in CI executes it. A green run says nothing about the new behaviour.

## What the new behaviour does

I called `shipping_cost` directly. The function is `round(base_cost(w))`, where `base_cost(w) = 4.0 + 1.35*w`.

| weight (kg) | base_cost | shipping_cost |
|---|---|---|
| 0 | 4.0 | 4 |
| 1 | 5.35 | 5 |
| 2 | 6.7 | 7 |
| 5 | 10.75 | 11 |
| 20 | 31.0 | 31 |
| 0.37 | 4.4995 | 4 |
| 0.5 | 4.675 | 5 |
| 10 | 17.5 | 18 |
| 30 | 44.5 | 44 |
| 50 | 71.5 | 72 |
| 70 | 98.5 | 98 |

Ordinary values round as expected. Exact halves do not all round the same way.

- **Half-even rounding:** Python's `round` rounds halves to the nearest even integer. 17.5 becomes 18, but 44.5 becomes 44 and 98.5 becomes 98. At exactly .5, the cost goes up for some weights and down for others.
- **Float noise:** 90 kg gives 125.50000000000001, which rounds to 126. That is only because of float noise. Mathematically it is a half, and it does not follow the half-even pattern.

## Gate: what does "round" mean in SHOP-88?

Question for you: should shipping cost round halves up (17.5 becomes 18, 44.5 becomes 45), or is half-to-even acceptable? Billing code usually wants half-up. Also, is whole-unit rounding of a float right for money, or should this use `Decimal`?

There was no pre-supplied "dev answers" line for this, so I stopped here. I did not pick an interpretation and call it correct.

## Open points

- **No test covers `shipping_cost`.** Once you answer, I'd add tests for ordinary values (1 kg gives 5, 2 kg gives 7), the half cases (10 kg, 30 kg) and zero weight. I did not add them because I didn't want to guess the expected value for the half cases.
- **Negative weights:** these are not handled. They give base costs below 4, which is probably out of scope.
- **Scope:** the diff is 5 lines, well under the 500-line budget. The ticket has no tracker link, and the README says small fixes need no prior approval.
