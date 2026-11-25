## Status: CI is green, but I could not prove the new behaviour is right. I need one answer from you first.

### What CI runs
`python -m unittest discover -s tests -v` (from `.pr-ready/profile.md`; there is no `.github` directory).

```
test_base_cost (test_base_cost.BaseCostTest.test_base_cost) ... ok
Ran 1 test in 0.000s
OK
```

That pass says nothing about SHOP-88. The only test covers `base_cost`, which this branch did not change. The branch adds `shipping_cost` (`round(base_cost(weight_kg))`) and no test calls it. Running CI therefore does not exercise the new behaviour. I did not add a test, because I can't write the expected values until you answer the question below.

### What I observed by calling `shipping_cost` directly

| kg | base_cost | shipping_cost |
|---|---|---|
| 0 | 4.0 | 4 |
| 0.5 | 4.675 | 5 |
| 1 | 5.35 | 5 |
| 2 | 6.7 | 7 |
| 2.5 | 7.375 | 7 |
| 3 | 8.05 | 8 |
| 4 | 9.4 | 9 |
| 10 | 17.5 | 18 |
| 30 | 44.5 | **44** |
| 50 | 71.5 | 72 |
| 70 | 98.5 | **98** |

Ordinary values round as expected. Exact .5 costs do not round consistently. Python's `round()` uses banker's rounding (half to even), so 17.5 becomes 18 but 44.5 becomes 44 and 98.5 becomes 98. A customer shipping 30 kg is charged 44, and one shipping 50 kg is charged 72, even though both costs sit exactly halfway.

### Gate: what is correct?
Question I would ask you, and I have no pre-supplied answer, so I'm stopping here:

> For SHOP-88, what should a cost that lands exactly on .5 round to? Python's `round()` gives 44.5 -> 44 and 71.5 -> 72 (half to even). Is that intended, or should halves always round up (44.5 -> 45), which is the usual meaning of "round the shipping cost"? Also, should the result stay an `int` as it is now (`18`) or be a float (`18.0`)?

### Next step once you answer
- Add tests for `shipping_cost` covering the ordinary cases above and the .5 boundaries (10, 30, 50 kg), with expectations set by your answer.
- If half-up is wanted, change `shipping_cost` to a half-up rounding (for example `decimal` with `ROUND_HALF_UP`, or `math.floor(x + 0.5)`).
- Re-run CI and show the results.

I changed nothing in the repo (`git status` is clean).
