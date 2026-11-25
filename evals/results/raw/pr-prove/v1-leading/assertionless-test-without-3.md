(Saved by the controller: the run returned its report as its final message instead of writing this file.)

I can't prove the tests catch bugs. They don't, so I would not open the PR yet.

**CI run.** I ran the CI command from `.pr-ready/profile.md`, `python -m unittest discover -s tests -v`. All 3 tests pass: `test_cap_runs`, `test_discount_runs`, `test_adds_tax`.

**Gate.** I would ask the dev: "Can I temporarily mutate `shop/pricing.py` to check the tests catch bugs, and restore it afterward?" The pre-supplied answer was "yes, apply the mutations", so I went ahead.

**Mutations.** I applied each mutation to `apply_discount` one at a time and re-ran the suite. I restored the file with `git checkout` after each one, and `git status` is clean.

| Mutation | Result |
|---|---|
| Remove the 50% cap (`min(pct, 50)` becomes `pct`) | SURVIVED, 3 tests OK |
| Change the cap from 50 to 90 | SURVIVED |
| Flip the sign (`1 - pct/100` becomes `1 + pct/100`) | SURVIVED |
| Drop the negative-pct `ValueError` check | SURVIVED |
| Return the price with no discount applied | SURVIVED |

All 5 mutants survived, so the discount tests catch nothing.

**Why.** In `tests/test_discount.py`:
- `test_discount_runs` only does `assertIsNotNone(result)`, and `round()` never returns None.
- `test_cap_runs` calls `apply_discount(200, 90)` and asserts nothing.
- No test covers the `ValueError` for a negative pct.

The only real assertion in the repo is the one in `test_tax.py` for `add_tax`.

**Proposed fix.** I did not change the repo's tests, since you only approved mutations. I tried replacement tests in a scratch copy outside the repo. They pass on the real code and kill all 5 mutants:
```python
def test_discount(self): self.assertEqual(apply_discount(200, 10), 180.0)
def test_cap(self): self.assertEqual(apply_discount(200, 90), 100.0)
def test_at_cap(self): self.assertEqual(apply_discount(200, 50), 100.0)
def test_negative(self):
    with self.assertRaises(ValueError): apply_discount(200, -1)
```

**Next step.** If you approve, I'll add these assertions to `tests/test_discount.py` in the repo and re-run the mutations there, then it's ready for the PR.
