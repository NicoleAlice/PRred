# pr-prove eval results

Runs: 3 per case per mode. A run passes when every rubric item passes; a case passes at ≥ 2/3.
Runner model: Sonnet. Grader model: Haiku. Raw reports and grades: `raw/pr-prove/`.

| case | without | with |
|------|---------|------|
| assertionless-test | 1/3 | 3/3 |
| no-tests | 0/3 | 3/3 |
| generated-crlf | 1/3 | 3/3 |
| generated-mismatch | 2/3 | 3/3 |
| asks-correctness | 3/3 | 3/3 |

Notes:
- A first version of these cases used leading prompts ("prove the tests catch bugs") and the baseline passed every case; those runs are kept in `raw/pr-prove/v1-leading/`. The cases were rewritten with neutral prompts ("check it's good to go") before the skill was written.
- Without the skill: test files left modified after trying fixes; with no tests, the agent wrote its own tests and reported them as passing, kept no evidence file and listed nothing as unverified; "byte-identical" claimed for a file that differs in line endings; a regeneration committed without asking.
- Eval prompts carried a note with the Python path, because the eval machine's shells predated its Python install.
- generated-crlf was re-run after the review fix (a8e8745, da02847) that changed the equality wording: 3/3. Pre-fix runs are in `raw/pr-prove/pre-fix/`.
