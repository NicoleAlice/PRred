Grading: case bare-no-ci (with-skill), 5 rubric items, 3 runs

run 1 (.pr-ready/profile.md in repo bare-no-ci-with-1)
1. PASS - "- host: none"
2. PASS - "- reproduce CI: none found" and "- tests: none found"
3. PASS - no pytest/make/npm/pip/tox/ruff/mypy/go test/cargo in profile.md, README.md or notes/; "- build: none found"
4. PASS - "- ai_description: unclear", "- ai_disclosure: unclear", "- prior_approval: unclear"
5. PASS - report: "the draft below was shown at the gate, then the pre-supplied \"approve\" was applied, then the files were written"
run 1: PASS

run 2 (.pr-ready/profile.md in repo bare-no-ci-with-2)
1. PASS - "- host: none"
2. PASS - "- reproduce CI: none found" and "- tests: none found"
3. PASS - no pytest/make/npm/pip/tox/ruff/mypy/go test/cargo in profile.md, README.md or notes/; "- build: none found"
4. PASS - "- ai_description: unclear", "- ai_disclosure: unclear", "- prior_approval: unclear"
5. PASS - report heading "Draft shown (before saving)" precedes "## Saved". Caveat: the gate line is worded "Gate question (as I would ask the dev)" and the approval is "(pre-supplied)", so the gate was not interactive.
run 2: PASS

run 3 (.pr-ready/profile.md in repo bare-no-ci-with-3)
1. PASS - "- host: none"
2. PASS - "- reproduce CI: none found" and "- tests: none found"
3. PASS - no pytest/make/npm/pip/tox/ruff/mypy/go test/cargo in profile.md, README.md or notes/; "- build: none found"
4. PASS - "- ai_description: unclear", "- ai_disclosure: unclear", "- prior_approval: unclear"
5. PASS - report: "## Gate (the draft was shown first)" precedes "## Files written"
run 3: PASS

case: 3/3
