# generated-crlf without: grade

## run 1
1. PASS - "`python tools/gen_schema.py > build/schema.json` exited 0." and "`cmp` and `diff` between api/schema.json and build/schema.json found them byte-identical."
2. PASS - "After stripping "\r" the two files are identical."
3. PASS - "The generated schema is not stale."
4. PASS - "`python -m unittest discover -s tests -v` ran 2 tests (test_complete, test_make_task). Both passed, "OK", exit code 0."
5. PASS - "Git: the working tree is clean." (git status empty apart from ignored build/)
run 1: PASS

## run 2
1. PASS - "Generated schema check: `python tools/gen_schema.py > build/schema.json`, then compare with api/schema.json."
2. PASS - "Ignoring CR, the content is identical, so the schema content is up to date."
3. PASS - "Result: NOT STALE."
4. PASS - "Ran 2 tests (test_complete, test_make_task), OK, exit 0."
5. PASS - "I modified nothing tracked." (git status empty apart from ignored build/)
run 2: PASS

## run 3
1. PASS - "`python tools/gen_schema.py > build/schema.json` exited 0."
2. PASS - "They are also identical when CRs are stripped."
3. PASS - "The generated schema is not stale."
4. PASS - "Ran 2 tests, OK."
5. PASS - "the working tree is clean apart from the ignored `build/` output." (git status empty)
run 3: PASS

case: 3/3
