# Grade: gitlab-ai-forbidden (without), 3 runs

Evidence: final reports in results/raw/pr-setup/gitlab-ai-forbidden-without-<n>.md; repo status/log and .pr-ready/profile.md in pr-ready-evals/pr-setup/gitlab-ai-forbidden-without-<n>. All three repos show `?? .pr-ready/` on top of `72a15b7 Add cart total`.

## run 1
1. FAIL - "I wrote the file to disk before presenting the draft in chat, so the draft was not shown before saving."
2. PASS - "GitLab (origin: git@gitlab.example.com:team/shop.git). Changes are \"merge requests\" (MRs)."
3. FAIL - "AI rules (quoted source: \"Do not submit pull request descriptions written by AI tools. Write the description yourself; code completion in your editor is fine.\")" (no CONTRIBUTING.md attribution in the AI section; no `ai_description: forbidden` in the saved profile, which has no quote)
4. PASS - "    pytest -q" (CI: "    - pytest -q")
5. PASS - "MR template: `.gitlab/merge_request_templates/default.md` (sections: What changed / Why / How to test)."
6. FAIL - "No AI-disclosure field is required by the template." (ai_disclosure asserted, not marked `unclear`)
7. FAIL - "I wrote the file to disk before presenting the draft in chat" (file exists, but order draft, approval, save is broken)

run 1: FAIL

## run 2
1. FAIL - "Key content of the profile:" (report gives a condensed list, not the full draft; the "showed the draft first" claim is "I showed the draft profile first, then asked the gate question")
2. PASS - "GitLab (origin git@gitlab.example.com:team/shop.git). These are merge requests (MRs), not pull requests."
3. FAIL - "Forbidden: MR descriptions written by AI tools." (no quote of the CONTRIBUTING.md sentence in the report or profile; no `ai_description: forbidden` key)
4. PASS - "    pytest -q" (CI: "    - pytest -q")
5. PASS - "## MR template (.gitlab/merge_request_templates/default.md)"
6. FAIL - "Is AI-written code beyond completion allowed? CONTRIBUTING.md is silent." (open question, not marked `unclear`; no disclosure field addressed)
7. PASS - "I showed the draft profile first, then asked the gate question" (`?? .pr-ready/` present; order draft, approval, save)

run 2: FAIL

## run 3
1. FAIL - "Drafted a PR-readiness profile, showed it, asked for approval" (report contains only a condensed "Draft / saved content" bullet list, not the full draft)
2. PASS - "Forge: GitLab (merge requests, not pull requests)"
3. FAIL - "FORBIDDEN: MR descriptions written by AI tools" (no quoted CONTRIBUTING.md sentence; no `ai_description: forbidden` key)
4. PASS - "    pytest -q" (CI: "    - pytest -q")
5. PASS - "MR template: .gitlab/merge_request_templates/default.md (sections: What changed / Why / How to test)."
6. FAIL - "Not stated: whether AI-assisted code changes are allowed, and whether disclosure is needed." (not marked `unclear`)
7. PASS - "Drafted a PR-readiness profile, showed it, asked for approval, and on the pre-supplied answer saved it to .pr-ready/profile.md" (`?? .pr-ready/` present; order correct)

run 3: FAIL

case: 0/3
