# pr-cold-review eval results

Runs: 3 per case per mode. A run passes when every rubric item passes; a case passes at ≥ 2/3.
Runner model: Sonnet. Grader model: Haiku. Raw reports and grades: `raw/pr-cold-review/`.

| case | without | with |
|------|---------|------|
| false-comment | 1/3 | 3/3 |
| secret-in-build-step | 0/3 | 3/3 |
| clean-diff | 0/3 | 3/3 |

Notes:
- Without the skill the agent usually spots the real defects; it fails on evidence: findings without file:line, and minor remarks with no location. The skill's difference here is verified, located findings, not detection alone.
- With the skill, all 9 runs used a separate reviewer subagent (none fell back to "not cold").
- One with-skill run (false-comment, run 3) also cited a line range that does not exist in a test file (`tests/test_read.py:24-33`, file has 22 lines); its rubric-relevant findings were correct. Verification of every cited line is a rule in the skill; this run shows it is not always followed.
- After the review fix (92ac4fd, ae440c9) that made citation checks concrete, false-comment was re-run with the skill: 3/3. In all three runs the cold reviewer again cited lines past the end of a test file, and each time the skill rejected the citation as "location does not exist" instead of reporting it — the verification step working as intended. Pre-fix runs are in `raw/pr-cold-review/pre-fix/`.
