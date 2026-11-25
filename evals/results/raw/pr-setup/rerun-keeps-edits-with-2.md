# Report: pr-setup re-run (rerun-keeps-edits-with-2)

Repo: <tmp>/pr-ready-evals/pr-setup\rerun-keeps-edits-with-2

## What I did
1. Read SKILL.md. Plain `python3`/`python` are Windows Store stubs and `py` is absent, so I used the real interpreter at `%LOCALAPPDATA%\Programs\Python\Python314\python.exe` (deviation noted).
2. Ran `detect_platform.py --json`: host gitlab, base main, no CLIs (gh/glab/az/bb all false), no stack tools, policy_files [CONTRIBUTING.md], pr_templates [.gitlab/merge_request_templates/default.md], ci_files [.gitlab-ci.yml], agent_rules [], commit_samples ["Add pr-ready profile", "Add cart total"], ticket_keys [].
3. Read all those files, profile-template.md, rule-precedence.md, the existing profile.md and .profile.generated.md.

## Draft shown (Step 4 reply, as it would have appeared)

Sources read: CONTRIBUTING.md, .gitlab/merge_request_templates/default.md, .gitlab-ci.yml, references/profile-template.md, references/rule-precedence.md, .pr-ready/profile.md, .pr-ready/.profile.generated.md. Detect: host gitlab, base main, CLIs none installed.

```markdown
# pr-ready profile

## Platform

- host: gitlab
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: CONTRIBUTING.md
- pr template: .gitlab/merge_request_templates/default.md
- commit format: unclear
- agent rules: none
- ai_description: forbidden
  > "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
- ai_disclosure: unclear
- prior_approval: not-required
  > "Small fixes may be sent without an issue" (CONTRIBUTING.md, section Process)

## Base branch

- base: main

## Commands

- reproduce CI: `pip install -r requirements.txt && pytest -q`
- tests: `pytest -q`
- build: none found
- generated check: none found

## Generated files

- none

## Budget

- max_lines: 500

## Risk paths

- none

## Known traps

| Symptom | Cause | What to do |
|---|---|---|
| Flaky test_cache on CI | shared tmp dir | rerun once |
```

Sections:
- Platform: unchanged
- Project rules: unchanged
- Base branch: unchanged
- Commands: updated (reproduce CI was `pytest -q`; .gitlab-ci.yml script runs `pip install -r requirements.txt` then `pytest -q`; profile.md matched the old generated text, so the new text replaces it)
- Generated files: unchanged
- Budget: unchanged
- Risk paths: unchanged (`.gitlab-ci.yml` is already in the built-in defaults)
- Known traps: kept (dev edited), because profile.md differs from .pr-ready/.profile.generated.md (your hand-written "Flaky test_cache on CI" row). The new generated section is still `none yet`, so there is no conflict.

Notes:
- `ai_disclosure: unclear`: no sentence in CONTRIBUTING.md says whether AI use must be disclosed or whether a trailer is forbidden. A sentence on disclosure would settle it.
- `commit format: unclear`: the two commit samples do not show a convention.
- `pytest -q` also appears in CONTRIBUTING.md; it matches the CI step, so nothing was written from outside CI.
- No host CLI (glab not installed): remote steps will follow references/platforms/none.md.

Gate question: "Save this to `.pr-ready/profile.md`? Approve, or tell me what to change."

dev answer (pre-supplied): approve.

## Saved (Step 5)
- `.pr-ready/profile.md`: the merged draft above (LF, UTF-8; 0 CR characters).
- `.pr-ready/.profile.generated.md`: the unmerged generated draft, identical except that Known traps is `| none yet | | |` and Commands has the new reproduce CI line.
- Parse check via prlib.profile.read_profile: `{"found": true, "generated": [], "risk_paths": [], "budget": 500, "policy": {"ai_description": "forbidden", "ai_disclosure": "unclear", "prior_approval": "not-required"}, "warnings": []}`. Policy matches the draft, warnings empty.
- Evidence log: `evidence.py add --kind note --text "pr-setup saved .pr-ready/profile.md; kept: Known traps; updated: Commands"` exited 0 (wrote .pr-ready/evidence/main-793ee2.md).
- Nothing staged or committed; git status shows only the two profile files modified. `profile.md` and `.profile.generated.md` can be committed together to share the profile with the team; that choice is the dev's.

## Final summary
Draft shown, approval received, two files written. Kept: Known traps (hand-written row preserved). Updated: Commands (reproduce CI now includes the pip install step). Unclear fields left for the dev: ai_disclosure, commit format.
