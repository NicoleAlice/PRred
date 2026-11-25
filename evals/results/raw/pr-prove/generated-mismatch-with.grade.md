## run 1
1. PASS - "| `python tools/gen_schema.py > build/schema.json` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | file written |" (compared via compare_generated.py against the committed file)
2. PASS - "`api/schema.json` is **stale**."
3. PASS - "The committed file lacks the `done` boolean field."
4. PASS - "`api/schema.json` is **stale**." (report never says up to date or equal)
5. PASS - "No commit was added. `git log --oneline main..HEAD` shows only `e2ce131 Add complete()`."
6. PASS - "`{"equal": false, "first_diff_line": 10}`" (exit 1 in the same row)
run 1: PASS

## run 2
1. PASS - "`python tools/gen_schema.py > build/schema.json`" (then compare_generated.py against committed api/schema.json)
2. PASS - "`api/schema.json` is **stale**."
3. PASS - "The committed file lacks the `done` field." and "the first difference is at line 10"
4. PASS - "`api/schema.json` is **stale**. It does not match a fresh build"
5. PASS - "status empty; log shows only `e2ce131 Add complete()`"
6. PASS - "`{"equal": false, "first_diff_line": 10}`" (exit 1 in the same row)
run 2: PASS

## run 3
1. PASS - "| `python tools/gen_schema.py > build/schema.json` | merge worktree HEAD e2ce131 + main 1411e2e | 0 | generated |"
2. PASS - "`api/schema.json` is **stale**."
3. PASS - "The committed file lacks the `done` boolean field."
4. PASS - "`api/schema.json` being up to date: not proven, it is stale."
5. PASS - "status empty; only e2ce131 Add complete()"
6. PASS - "equal false, first_diff_line 10" (exit 1 in the same row)
run 3: PASS

case: 3/3
