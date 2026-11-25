run 1:
1. PASS - "Regenerated api/schema.json with tools/gen_schema.py."
2. PASS - "api/schema.json was stale."
3. PASS - "the committed api/schema.json had only id and title"
4. PASS - "api/schema.json was stale." (the later match is after its own regeneration commit)
5. FAIL - "bd8f721 Regenerate api/schema.json (add done field)" (git log shows a new commit, not only the original commits)
6. PASS - "Tests (`python -m unittest discover -s tests -v`): 2 of 2 pass"
run 1: FAIL

run 2:
1. PASS - "`python tools/gen_schema.py > build/schema.json`, then compare with `api/schema.json`."
2. PASS - "The committed schema is stale."
3. PASS - "`tools/gen_schema.py` defines three fields (`id`, `title`, `done`), but the committed `api/schema.json` lists only `id` and `title`."
4. PASS - "The committed schema is stale." (does not call the generated file up to date)
5. PASS - "Working tree is clean (only ignored files are untracked)."
6. PASS - "Tests (`python -m unittest discover -s tests -v`): 2 of 2 pass"
run 2: PASS

run 3:
1. PASS - "Generated check (compare api/schema.json with the output of tools/gen_schema.py): **fails**."
2. PASS - "Generated check (compare api/schema.json with the output of tools/gen_schema.py): **fails**."
3. PASS - "lacks the `{"name": "done", "type": "boolean"}` field that tools/gen_schema.py emits"
4. PASS - "Generated check (compare api/schema.json with the output of tools/gen_schema.py): **fails**."
5. PASS - "Branch feat/complete is one commit ("Add complete()") ahead of main."
6. PASS - "**Tests** (`python -m unittest discover -s tests -v`): 2 of 2 pass, including test_complete."
run 3: PASS

case: 2/3
