# pr-setup report (gitlab-ai-forbidden-with-1)

## What I did
Followed SKILL.md. Python: the `python3`/`python` on PATH were Windows Store stubs and failed, so I used the real install at `<python>` (the skill's fallback chain `python3`, `python`, `py -3` did not work as written).

Ran `detect_platform.py --json`:
host gitlab, remote git@gitlab.example.com:team/shop.git, base main, no CLIs (gh/glab/az/bb all false), no stack tools, policy_files [CONTRIBUTING.md], pr_templates [.gitlab/merge_request_templates/default.md], ci_files [.gitlab-ci.yml], agent_rules [], commit_samples ["Add cart total"], ticket_keys [].

Read: CONTRIBUTING.md, the MR template, .gitlab-ci.yml, README.md, profile-template.md, rule-precedence.md. No .gitattributes and no generated-file headers. No existing profile, so not a re-run.

## Draft shown (complete)
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
- prior_approval: unclear

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
| none yet | | |
```

## Notes
- ai_disclosure unclear: CONTRIBUTING says nothing about declaring AI use. Silence is not "none".
- prior_approval unclear: "Small fixes may be sent without an issue. Larger changes need a discussion first." is mixed, so neither required nor not-required fits. A rule stating which applies would settle it.
- commit format unclear: only one commit sample ("Add cart total").
- CONTRIBUTING mentions `pytest -q`, which is also in CI, so it is covered. No build or generated-check step exists in CI.
- No `glab` CLI, so remote steps follow `references/platforms/none.md`.

## Gate question I would ask
"Save this to `.pr-ready/profile.md`? Approve, or tell me what to change."

dev answers: approve

## Save
Wrote `.pr-ready/profile.md` and `.pr-ready/.profile.generated.md` (identical, UTF-8, LF). Parse check with `read_profile('.')`:
`{"found": true, "generated": [], "risk_paths": [], "budget": 500, "policy": {"ai_description": "forbidden", "ai_disclosure": "unclear", "prior_approval": "unclear"}, "warnings": []}`
Policy matches the draft and warnings are empty. Evidence note added with `evidence.py add --kind note` (exit 0): `.pr-ready/evidence/main-03e357.md`. Nothing staged or committed (`git status`: only `?? .pr-ready/`). CI commands were not run.

The dev can commit `profile.md` and `.profile.generated.md` together to share the profile with the team. That choice is theirs.

## Final report
Draft shown, dev approved, files written (above), sections kept: none (first run), unclear fields left for the dev: ai_disclosure, prior_approval, commit format.
