# Mutations

A mutation is one deliberate bug that a test should catch. If the tests still pass, the mutation **survived**: the tests do not prove the behaviour it broke. Survivors are findings.

## Project tool first

If the profile's `Commands`, the CI files or the build config name a mutation tool (mutmut, Stryker, PIT, cargo-mutants, infection, go-mutesting), run it scoped to the changed files, exactly as configured, and record its command and its killed/survived/timeout counts as a `command` entry. Each survivor it reports becomes a finding. Hand mutations are then only for behaviour the tool did not cover.

## Choosing hand mutations

Target the code the branch added or changed, never test files. Propose 2 or 3 per new or changed test, and at least one per new behaviour that no test covers (it will survive; that is the point). Choose changes a test of that behaviour should notice:

- remove a check or a guard (`if pct < 0: raise` deleted, a cap like `min(pct, 50)` lifted to `min(pct, 100)`);
- flip a sign, a comparison or a boundary (`1 - x` to `1 + x`, `<` to `<=`, `> 0` to `>= 0`);
- change a constant or a rounding (`round(x)` to `int(x)`, `2` decimals to `1`);
- drop a field, a key or an argument from an output;
- reword an expected message or error type;
- return early with a plausible value (the input unchanged, `None`, an empty list).

List the planned mutations in the report before their results. Proposing them needs no answer from the dev.

## Running each one

Start from a clean tree (`git status --porcelain` empty), with the temporary worktrees already removed, and a green suite **in the repo's own working tree**: run the tests command there once and record it, even though it passed in the merge worktree. If it is not green there, do not mutate; report why. Then, for each mutation, one at a time:

1. Make the single edit in the source file with the edit tool. Change nothing else.
2. Run the profile's `tests` command (else `reproduce CI`) from the repo root, exactly as in Step 3.
3. Read the output: **killed** if any test failed or errored because of the change (name it, `file::Class::test`, and the assertion); **survived** if the run is green. An import or syntax error you caused counts as neither: revert, fix the mutation, and retry it once.
4. Revert: `git checkout -- <file>` (or `git restore <file>`).
5. Run `git status --porcelain`. It must be empty (ignored paths do not appear). If it lists anything else, such as untracked files the test run created (a report, a cache, a database file), delete the files your run created, restore any other tracked file with `git checkout -- <file>`, and run it again. Do not start the next mutation until it is empty; if you cannot make it empty, stop mutating and report it.
6. Record it:

   ```
   <py> <scripts>/evidence.py add --kind mutation --stdin <<'EOF'
   mutation 2/4: shop/pricing.py:9 `pct = min(pct, 50)` -> `pct = min(pct, 100)` (cap removed)
   cmd: python -m unittest discover -s tests -v
   exit: 0
   counts: Ran 3 tests, OK
   result: survived (no test failed; tests/test_discount.py::test_cap_runs calls the code but asserts nothing)
   reverted: git checkout -- shop/pricing.py; git status --porcelain empty
   EOF
   ```

   For a killed mutation, `result: killed by tests/test_x.py::XTest::test_y (AssertionError: 100.0 != 180.0)`.

Never leave a mutation in place, never combine two, and never touch tests to make one die.

## Reading the result

- A survivor's finding names the test that exercises the code (or says none does) and what it fails to assert, for example "`test_cap_runs` calls `apply_discount(200, 90)` and checks nothing; `assertEqual(apply_discount(200, 90), 100.0)` would kill the cap mutation (the 50% cap is stated in the docstring)".
- When the expected value is not stated anywhere, the suggestion is a question for the dev, not an assertion (SKILL.md, Step 7).
- Read survivors that look harmless too: if a mutation cannot change any observable result (an equivalent mutant), say why, and do not count it as a finding.
- Report the counts: N applied, K killed, S survived. While S > 0, the tests are not adequate.
