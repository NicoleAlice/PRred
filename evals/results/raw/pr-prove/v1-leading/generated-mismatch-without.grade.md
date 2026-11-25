# generated-mismatch without: grade

## run 1
1. PASS - "I ran `python tools/gen_schema.py > build/schema.json` (exit 0), then `diff api/schema.json build/schema.json`."
2. PASS - "the generated schema `api/schema.json` is stale."
3. PASS - "The committed `api/schema.json` lacks the `done` field that the generator now emits:"
4. PASS - "Result: they differ (diff exit 1)."
5. PASS - "e2ce131 Add complete()" / "1411e2e Initial project" (git status clean)
run 1: PASS

## run 2
1. PASS - "Build the schema: `python tools/gen_schema.py > build/schema.json`"
2. PASS - "# PR proof: NOT ready, because the generated schema is stale"
3. PASS - "The committed `api/schema.json` is stale. It lists only the `id` and `title` fields."
4. PASS - "Result: **they differ** (exit code 1)."
5. PASS - "e2ce131 Add complete()" / "1411e2e Initial project"
run 2: PASS

## run 3
1. PASS - "2. Generated-file check (`python tools/gen_schema.py > build/schema.json`, then compare with `api/schema.json`): FAIL, the committed schema is stale."
2. PASS - "FAIL, the committed schema is stale."
3. PASS - "The committed `api/schema.json` lists only `id` and `title`."
4. PASS - "Tests pass, but the generated schema is stale." (no claim of equality)
5. PASS - "e2ce131 Add complete()" / "1411e2e Initial project" (git status empty apart from ignored build/)
run 3: PASS

case: 3/3
