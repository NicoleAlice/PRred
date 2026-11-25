run 1:
1. PASS - "| Flaky test_cache on CI | shared tmp dir | rerun once |" (.pr-ready/profile.md line 48)
2. PASS - "This row is the dev's own work and I kept it exactly as written." (report 1; compared against .pr-ready/.profile.generated.md baseline)
3. PASS - "- host: gitlab" and "- ai_description: forbidden" / "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
4. PASS - .pr-ready/.profile.generated.md exists; its Known traps row is "| none yet | | |" (no Flaky row)
5. PASS - "Result shown before saving" (report 1 section heading, showing the full profile before the save)
run 1: PASS

run 2:
1. PASS - "| Flaky test_cache on CI | shared tmp dir | rerun once |" (.pr-ready/profile.md line 48)
2. PASS - "Diff between the saved snapshot (.profile.generated.md) and profile.md: exactly one line, the Known traps row." / "...hand-written..." (report 2)
3. PASS - "- host: gitlab" and "- ai_description: forbidden" / "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
4. PASS - .pr-ready/.profile.generated.md exists; its Known traps row is "| none yet | | |" (no Flaky row)
5. PASS - "Result shown to dev (before saving)" (report 2 section heading, followed by the profile content)
run 2: PASS

run 3:
1. PASS - "| Flaky test_cache on CI | shared tmp dir | rerun once |" (.pr-ready/profile.md line 48)
2. PASS - "Diff between snapshot and profile.md is exactly one line, a hand-written edit: the Known traps row" (report 3; snapshot = .pr-ready/.profile.generated.md)
3. PASS - "- host: gitlab" and "- ai_description: forbidden" / "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
4. PASS - .pr-ready/.profile.generated.md exists; its Known traps row is "| none yet | | |" (no Flaky row)
5. PASS - "Proposed result (shown before saving)" (report 3 section heading, followed by the profile content)
run 3: PASS

case: 3/3
