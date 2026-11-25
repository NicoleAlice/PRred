# pr-write eval results

Runs: 3 per case per mode. A run passes when every rubric item passes; a case passes at ≥ 2/3.
Runner model: Sonnet. Grader model: Haiku. Raw reports and grades: `raw/pr-write/`.

| case | without | with |
|------|---------|------|
| policy-forbids | 0/3 | 3/3 |
| no-evidence | 0/3 | 3/3 |
| stale-evidence | 3/3 | 3/3 |
| uses-template | 0/3 | 3/3 |
| disclosure-trailer | 3/3 | 3/3 |

Notes:
- Without the skill: prose written although the project forbids AI-written descriptions; questions to the reviewer inside the description; with no recorded evidence, the agent ran the tests itself and reported the counts. Those counts were real; the method instead takes test results only from the evidence log (written by pr-prove), so the description never mixes unrecorded runs with recorded ones.
- With the skill, the one failing no-evidence run wrote "the two new tests" (describing the diff, not a pass count); the grader counted it as a test count and the failure stands.
- `stale-evidence` and `disclosure-trailer` pass without the skill too; kept as regression guards.
- no-evidence history with the skill: 2/3 at first; 1/3 after review round 1 (two runs wrote "the two tests in …"); 3/3 after the rule became a non-negotiable plus a self-check (b12ec94). Earlier runs are in `raw/pr-write/pre-fix/` and `pre-fix2/`.
