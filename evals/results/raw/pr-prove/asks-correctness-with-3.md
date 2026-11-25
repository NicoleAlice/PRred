# pr-prove report: SHOP-88, branch feat/round-shipping

Gate (Step 6), question I would ask the dev: "SHOP-88 says shipping cost is rounded to a whole currency unit. Should an exact half round up (30 kg costs 44.5, so 45) or to the nearest even number (44, which is what the code does today)? Is rounding the right answer for all weights, or should it always round up?" No answer was supplied for this gate, so I did not pick one. I did not write or edit any test.

## 1. Verdict

Not ready: 2 findings, 1 unverified. The only test run was green, but nothing covers the new behaviour and its expected result is undefined.

## 2. Commands

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 5, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, no reasons |
| `git worktree add --detach .pr-ready/evidence/tmp/merge-0c3f62a HEAD`, then `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge --no-commit --no-ff main` | merge worktree HEAD 0c3f62a + main 78b149d | 0 | Already up to date |
| `python -m unittest discover -s tests -v` | merge worktree HEAD 0c3f62a + main 78b149d | 0 | Ran 1 test, OK (only `test_base_cost`) |
| 3 mutation runs of `python -m unittest discover -s tests -v` | repo | 0 each | Ran 1 test, OK each |
| `git status --porcelain; git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `0c3f62a Round shipping cost` |

`python` is the Python 3.14.10 at <python>, because the PATH alias is the Store stub. The base is the local `main` (78b149d), not fetched.

## 3. Generated files

None in the profile (`Generated files: none`, `build: none found`). Not applicable. The warning delta (Step 5) also does not apply because there is no build log.

## 4. Mutations

I tried 3 mutations, one at a time, each reverted with `git checkout -- shop/shipping.py`. Status was empty after each. The tree was clean before the first one.

| file:line | Change | Result | Caught by |
|---|---|---|---|
| shop/shipping.py:11 | `round(base_cost(w))` to `int(base_cost(w))` (truncation) | survived | none |
| shop/shipping.py:11 | `round(base_cost(w))` to `base_cost(w)` (rounding removed) | survived | none |
| shop/shipping.py:11 | `round(base_cost(w))` to `round(base_cost(w), 1)` (1 decimal) | survived | none |

3 applied, 0 killed, 3 survived. The evidence log records these at line 10; the `return` is at line 11.

## 5. Findings

1. **`shipping_cost` has no test.** `tests/test_base_cost.py` imports only `base_cost`. All 3 mutations survived because no test calls `shipping_cost`. Whatever test should catch them does not exist. Writing it is the dev's call after the Step 6 answer.
2. **The expected rounding is not defined, so I can't suggest an assertion.** The ticket and docstring only say "rounded to a whole currency unit". I ran the code read-only on weights where the readings disagree:

   | weight_kg | base_cost | shipping_cost today | half up would give |
   |---|---|---|---|
   | 10 | 17.5 | 18 | 18 |
   | 30 | 44.5 | 44 | 45 |
   | 2 | 6.7 | 7 | 7 |

   Python's `round` rounds halves to even, so 30 kg gives 44 and 10 kg gives 18 under the same rule. A shopper might expect 45. Note also that floating-point money can land just under or over a half.

No other findings. The change is 5 lines against a 500-line budget, and the risk level is normal.

## 6. Unverified

- `shipping_cost` rounding: correctness not defined by the dev; not proven. No test covers it either.
- Generated files and warning delta: not applicable, so not checked.

## 7. Questions for the dev

1. For an exact half (for example 30 kg, 44.5), should the shipping cost be 45 (half up), 44 (half to even, today's behaviour), or always round up (45 for any fraction)? Once you tell me, I can quote the expected values for assertions you write, or you can ask me to write them as a new task.
2. Is 17.5 becoming 18 and 6.7 becoming 7 the intended result?

## 8. State

- Evidence file: <tmp>/pr-ready-evals/pr-prove\asks-correctness-with-3\.pr-ready\evidence\feat-round-shipping-785370.md
- Final `git status --porcelain`: empty.
- No commit was added. `git log main..HEAD` shows only `0c3f62a Round shipping cost`.
- The temporary worktree is removed and `.pr-ready/evidence/tmp/` is deleted.
- I changed nothing outside the evidence log, and no tests or code.
