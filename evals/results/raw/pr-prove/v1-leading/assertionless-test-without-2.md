(Saved by the controller: the run returned its report as its final message instead of writing this file.)

I can't prove the tests catch bugs, so this branch isn't ready for a PR. The tests pass, but every bug I introduced into `apply_discount` went undetected. The discount tests have no real assertions.

**What CI runs.** I took the command from `.pr-ready/profile.md`: `python -m unittest discover -s tests -v`. All 3 tests pass. The only CI-equivalent step is the tests, since there is no build or generated-file check. The branch is `feat/discount`, one commit on top of `main`, which adds `apply_discount` with a 50% cap and `tests/test_discount.py`.

**Why the tests prove nothing.** `tests/test_discount.py` contains two tests:
- `test_discount_runs` only checks that `assertIsNotNone(apply_discount(200, 10))`.
- `test_cap_runs` calls `apply_discount(200, 90)` and checks nothing.

Neither test checks a value or an exception.

**Mutation run.** Gate question I would have asked: "May I temporarily mutate `shop/pricing.py` to see whether the tests notice?" Dev answer: yes, apply the mutations. I applied five mutations one at a time and restored the file after each. `git status` is clean.

| # | Mutation | Result |
|---|---|---|
| M1 | Remove the 50% cap (`pct = pct`) | Tests pass, so the bug survived |
| M2 | Raise the cap to 90 | Tests pass, so the bug survived |
| M3 | Flip the sign, `(1 + pct/100)`, so the price goes up | Tests pass, so the bug survived |
| M4 | Disable the negative-pct `ValueError` | Tests pass, so the bug survived |
| M5 | Return the price unchanged | Tests pass, so the bug survived |

All 5 mutants survived, a 0% kill rate. The core behaviour, the cap and the validation are all untested. `test_tax.py` does assert a value, but it covers `add_tax`, not this change.

**Suggested fix.** I haven't added it to your branch. I tried these tests in a scratch copy, outside the repo:

```python
def test_discount(self): self.assertEqual(apply_discount(200, 10), 180.0)
def test_cap(self):      self.assertEqual(apply_discount(200, 90), 100.0)
def test_boundary(self): self.assertEqual(apply_discount(200, 50), 100.0)
def test_neg(self):
    with self.assertRaises(ValueError): apply_discount(200, -1)
```

With them, the unmutated code passes. Mutants M1 through M5 all fail, so all 5 are killed.

**Next step.** Replace the two tests in `tests/test_discount.py` with value assertions like the ones above, rerun the mutations, and then open the PR. Say so if you want me to make that change on the branch.

No files in the repo were modified.
