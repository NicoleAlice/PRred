# Grade: bare-no-ci (without skill)

## run 1
1. FAIL - no `host` field anywhere in report or profile; "host: none" never appears
2. FAIL - "No CI configuration exists; no test suite, linter, formatter or type-checker is configured." (no `none found`)
3. FAIL - "Only available check: `python -c \"import notes.store\"`." (check listed under Run CI locally; no repo file supports it)
4. FAIL - "UNKNOWN whether maintainers want it." (no ai_description/ai_disclosure/prior_approval fields; value is UNKNOWN, not `unclear`)
5. PASS - "I drafted the profile (content below), showed it, then asked the gate question."
run 1: FAIL

## run 2
1. FAIL - no `host` field anywhere in report or profile; "host: none" never appears
2. FAIL - "Local command: none defined." (not `none found`)
3. FAIL - "`python -c \"import notes.store\"` (a sanity check, not a project-defined gate)" (check listed under Running CI locally; no repo file supports it)
4. FAIL - "None documented: no CLAUDE.md, AGENTS.md, .cursorrules, or similar. No AI-disclosure or attribution policy." (no `unclear`, no policy field names)
5. PASS - "Draft shown, then the gate" and "The pre-supplied dev answer was \"approve\", so I treated the draft as approved and saved it as-is."
run 2: FAIL

## run 3
1. FAIL - no `host` field anywhere in report or profile; "host: none" never appears
2. FAIL - "No tests, linter, formatter, or type-checker are configured." (no `none found`)
3. FAIL - "`python -m compileall notes` (syntax) and `python -c \"import notes.store\"` (import)" (checks listed under Running CI locally; no repo file supports them)
4. FAIL - "UNKNOWN: whether AI-assisted changes need disclosure, and any limits on them." (value is UNKNOWN, not `unclear`; no policy field names)
5. PASS - "Gate: I showed the draft and asked \"Approve this draft profile?...\" The pre-supplied answer was \"approve\", so I saved it."
run 3: FAIL

case: 0/3
