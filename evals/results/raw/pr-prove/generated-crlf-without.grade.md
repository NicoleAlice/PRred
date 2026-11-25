run 1:
1. PASS - "Build: `python tools/gen_schema.py > build/schema.json`"
2. FAIL - "`cmp` reported them byte-identical, so the generated file is not stale." (says identical, not equal apart from line endings)
3. PASS - "so the generated file is not stale."
4. PASS - "2 tests ran, both passed (test_complete, test_make_task). Result: OK."
5. PASS - "`git status` is clean again."
6. PASS - "It exited 0."
run 1: FAIL

run 2:
1. PASS - "I ran `python tools/gen_schema.py > build/schema.json`"
2. FAIL - "The two files are byte-identical (`cmp` reported no difference)." (not stated as equal apart from line endings)
3. PASS - "so it needs no regeneration"
4. PASS - "ran 2 tests, both OK (`test_make_task`, `test_complete`)"
5. PASS - "I deleted `build/` afterwards, and the tree is clean again."
6. PASS - "`cmp` reported no difference" (with "2 tests, both OK")
run 2: FAIL

run 3:
1. PASS - "I ran `python tools/gen_schema.py > build/schema.json` and compared it to the committed api/schema.json."
2. PASS - "a byte-level comparison would show a difference even though the content is the same (it matches once CRs are stripped)."
3. PASS - "so the generated file is not stale."
4. PASS - "`python -m unittest discover -s tests -v` ran 2 tests, both OK"
5. PASS - "I deleted the build/ directory afterwards (it is gitignored anyway)." (repo status shows only ignored entries)
6. PASS - "`cmp` returned 0"
run 3: PASS

case: 1/3
