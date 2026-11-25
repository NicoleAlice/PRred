run 1
1. PASS - "## Draft shown (complete)" ... "Gate question I would ask" ... "dev answers: approve" ... "## Save" "Wrote `.pr-ready/profile.md`"
2. PASS - "- host: gitlab"
3. PASS - "- ai_description: forbidden" "> \"Do not submit pull request descriptions written by AI tools\" (CONTRIBUTING.md, section Tooling)"
4. PASS - "- tests: `pytest -q`" (CI: "- pytest -q"; no other commands listed beyond "pip install -r requirements.txt" which is also in CI)
5. PASS - "- pr template: .gitlab/merge_request_templates/default.md"
6. PASS - "- ai_disclosure: unclear" "- prior_approval: unclear"
7. PASS - ".pr-ready/profile.md" present in repo; report order: "## Draft shown (complete)" -> "dev answers: approve" -> "## Save"
run 1: PASS

run 2
1. FAIL - no draft shown; report says "I stopped at Step 1 and wrote no draft and no files."
2. FAIL - no draft; "No profile file exists" ("cat: gitlab-ai-forbidden-with-2/.pr-ready/profile.md: No such file or directory")
3. FAIL - no draft; no ai_description field in any profile ("No usable Python interpreter exists on this machine.")
4. FAIL - no Commands section exists; "None yet, because no draft exists."
5. FAIL - no draft; "pr template" never written; "I did not reproduce the script's detection by hand"
6. FAIL - no policy fields written; "The save gate (approve the draft) was never reached"
7. FAIL - "Files written: None. `.pr-ready/` was not created"
run 2: FAIL

run 3
1. PASS - "## Draft shown to the dev (complete)" ... "Gate" ... "## Files written" ("The draft above was already in my reply before I treated this as approval.")
2. PASS - "- host: gitlab"
3. PASS - "- ai_description: forbidden" "> \"Do not submit pull request descriptions written by AI tools.\" (CONTRIBUTING.md, section Tooling)"
4. PASS - "- tests: `pytest -q`" (CI and CONTRIBUTING are identical to run 1; no unsupported command listed)
5. PASS - "- pr template: .gitlab/merge_request_templates/default.md"
6. PASS - "- ai_disclosure: unclear" "- prior_approval: unclear"
7. PASS - ".pr-ready/profile.md" present; report order "## Draft shown to the dev (complete)" -> "Gate" -> "## Files written"
run 3: PASS

case: 2/3
