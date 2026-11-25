run 1:
1. PASS - "| Flaky test_cache on CI | shared tmp dir | rerun once |"
2. PASS - "Known traps: kept (dev edited), because profile.md differs from .pr-ready/.profile.generated.md"
3. PASS - "ai_description: forbidden" with "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
4. PASS - "| none yet | | |" (.profile.generated.md exists, no Flaky row)
5. PASS - "dev answers: approve (pre-supplied; applied after the draft was shown above)."
run 1: PASS

run 2:
1. PASS - "| Flaky test_cache on CI | shared tmp dir | rerun once |"
2. PASS - "Known traps: kept (dev edited), because profile.md differs from .pr-ready/.profile.generated.md"
3. PASS - "ai_description: forbidden" with "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
4. PASS - "| none yet | | |" (.profile.generated.md exists, no Flaky row)
5. FAIL - "Draft shown (Step 4 reply, as it would have appeared)" (display is hedged, not shown as actual)
run 2: FAIL

run 3:
1. PASS - "| Flaky test_cache on CI | shared tmp dir | rerun once |"
2. PASS - "Known traps: kept (dev edited)" with "differs from .pr-ready/.profile.generated.md"
3. PASS - "ai_description: forbidden" with "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
4. PASS - "| none yet | | |" (.profile.generated.md exists, no Flaky row)
5. PASS - "Question I asked the dev: \"Save this to `.pr-ready/profile.md`?"
run 3: PASS

case: 2/3
