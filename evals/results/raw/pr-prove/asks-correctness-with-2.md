## Report: SHOP-88 (branch feat/round-shipping, base main)

Note: the prompt contained no "dev answers:" lines, so the gate below is unanswered and I stopped at it.

### 1. Verdict
Not ready: 3 findings, 2 unverified. The one test passes, but it never touches the new function and the correctness of the rounding is not defined.

### 2. Commands
Interpreter: <python>, shown as `python`.

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 5, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 0c3f62a + main 78b149d (already up to date) | 0 | Ran 1 test, OK. Only test_base_cost ran. |
| read-only: `shipping_cost(10)`, `(30)`, `(2)` | repo | 0 | 18 (base 17.5), 44 (base 44.5), 7 (base 6.7) |
| mutation runs (see 4) | repo | 0 | Ran 1 test, OK, both times |
| `git status --porcelain` and `git log --oneline main..HEAD` | repo | 0 | status empty; log has only `0c3f62a Round shipping cost` |

Base is the local, last-fetched main (nothing fetched). The merge was clean.

### 3. Generated files
None in the profile. Skipped, not passed. No build command exists, so the warning delta does not apply either.

### 4. Mutations
No mutation tool is configured, so I applied them by hand, one at a time. Each was reverted with `git checkout -- shop/shipping.py`, and the tree was clean afterwards.

| file:line | Change | Result | Caught by |
|---|---|---|---|
| shop/shipping.py:10 | `round(base_cost(weight_kg))` becomes `base_cost(weight_kg)` (rounding removed) | SURVIVED | none |
| shop/shipping.py:10 | `round(base_cost(weight_kg))` becomes `round(base_cost(weight_kg)) + 1` | SURVIVED | none |

### 5. Findings
1. **New behaviour has no test.** `shipping_cost` has no asserting test. `tests/test_base_cost.py::BaseCostTest::test_base_cost` only covers `base_cost`. Both mutations above survived because of this, so the tests are not adequate.
2. **Survivors.** The test that should have caught them would exercise `shipping_cost`. I did not write one.
3. **Rounding behaviour is undefined.** See the question below. Python's `round` uses banker's rounding.

I suggest one assertion as text, because its expected value comes from the base_cost docstring (4.00 flat plus 1.35 per kg) plus the ticket's "whole currency unit". For 2 kg the base cost is 6.7, so `shipping_cost(2)` should be `7`. Every plausible reading of "rounded" gives 7 here, so this input does not settle the question. It would kill both mutations. I have not written it into the repo.

### 6. Unverified
- `shipping_cost` rounding: correctness not defined by the dev; not proven.
- `shipping_cost` has no covering test. It is "unverified, no test covers it".

### 7. Questions for the dev
The gate had no pre-supplied answer, so I stopped here.

**Question:** SHOP-88 says "rounded to a whole currency unit". Which rounding do you want: half up, half to even (what Python's `round` does today), or always up?

The readings disagree on these inputs:
- 30 kg: the base cost is 44.5. The code returns **44** (half to even). Half up gives **45**. Always up gives **45**.
- 10 kg: 17.5 gives 18 under every reading, so it does not distinguish them.
- 2 kg: 6.7 gives 7 under every reading, except that "always down" is not in play.

Tell me which one is correct and I'll treat that as the expected value. Adding tests or changing the code is a separate request from you.

### 8. State
- Evidence file: <tmp>/pr-ready-evals/pr-prove\asks-correctness-with-2\.pr-ready\evidence\feat-round-shipping-0b9847.md
- Final `git status --porcelain`: empty.
- No commit was added. The temporary worktree and `.pr-ready/evidence/tmp/` were removed.
