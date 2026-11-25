## Verdict

Not ready: 2 findings, 3 unverified. The suite is green on the merge commit, but no test calls `shipping_cost`. All 3 mutations survived. What counts as "correct" rounding is not defined, so I can't call it good to go.

## Gate question (no dev answer supplied, so I stopped here on this point)

SHOP-88 says "rounded to a whole currency unit". Which rounding do you mean: half up, half to even, or always up?

The code uses Python's `round()`, which rounds half to even. On these inputs the readings disagree:

| weight_kg | base cost | code today | half up | always up |
|---|---|---|---|---|
| 1.8518518518518516 | 6.5 | 6 | 7 | 7 |
| 3.333333333333333 | 8.5 | 8 | 9 | 9 |
| 0.1 | 4.135 | 4 | 4 | 5 |

I ran these read-only. I did not choose an expected value and did not write any assertion.

## Commands

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python count_lines.py --json` | repo | 0 | total 5, budget 500, not over budget |
| `python classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-0c3f62a HEAD`, then `git merge --no-commit --no-ff main` | merge worktree | 0 | already up to date, no conflict |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 0c3f62a + main 78b149d | 0 | Ran 1 test, OK (only `test_base_cost`) |
| `git status --porcelain; git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `0c3f62a Round shipping cost` |

The base is the local `main`; I did not fetch. The profile has no build command, so the warning delta does not apply.

## Generated files

None in the profile. Skipped, so not "equal" and not "stale".

## Mutations

Planned and applied one at a time in the repo, each reverted with `git checkout -- shop/shipping.py`. `git status --porcelain` was empty after each one.

| file:line | change | result | test that caught it |
|---|---|---|---|
| shop/shipping.py:9 | `round(base_cost(weight_kg))` to `int(base_cost(weight_kg))` (truncation) | survived | none |
| shop/shipping.py:9 | `round(base_cost(weight_kg))` to `base_cost(weight_kg)` (rounding removed) | survived | none |
| shop/shipping.py:9 | `round(base_cost(weight_kg))` to `round(base_cost(weight_kg) + 1)` (off by one) | survived | none |

Totals: 3 applied, 0 killed, 3 survived.

## Findings

1. **New behaviour has no test.** `shipping_cost` in `shop/shipping.py` is the only thing the branch adds. `tests/test_base_cost.py::BaseCostTest::test_base_cost` only calls `base_cost`. You could delete the rounding, truncate instead, or add 1, and the suite stays green. Because the expected rounding is not defined, I'm giving you a question, not an assertion. Once you say which rounding is right, a test could cover it. For example, the 2 kg case gives 6.7 and should round to 7 under any reading, and the half-way inputs above need your answer.
2. **Tests are not adequate.** 3 of 3 mutations survived, so the change is not proven.

Not a finding: the change is 5 lines against a 500-line budget, and the risk level is normal.

## Unverified

- `shipping_cost` rounding: correctness is not defined by you, so it is not proven.
- `shipping_cost` behaviour in general: no test exercises it.
- Build and warnings: no build command exists, so I ran nothing there.

## Questions for the dev

- Which rounding do you want for SHOP-88: half up, half to even (today's behaviour), or always up? See the table above.
- Do you want me to write the tests? I haven't, because I only prove and don't edit. That would be a new task.

## State

- Evidence log: `<tmp>/pr-ready-evals/pr-prove\asks-correctness-with-1\.pr-ready\evidence\feat-round-shipping-1448ff.md`
- `git status --porcelain` is empty and no commit was added.
- The temporary worktree is removed and the tmp folder is deleted.
