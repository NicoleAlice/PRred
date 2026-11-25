# pr-setup report: bare-no-ci-with-2

Repo: <tmp>/pr-ready-evals/pr-setup\bare-no-ci-with-2

## Sources read
SKILL.md, profile-template.md, rule-precedence.md. The `policy_files`, `pr_templates`, `ci_files` and `agent_rules` lists were all empty, so there was nothing further to read. I also looked at README.md (one line: "A small note-taking helper.") and notes/store.py to check for risk paths and generated files.
Python: `python3` and `python` are Windows Store stubs and failed. I used `%LOCALAPPDATA%\Programs\Python\Python314\python.exe`.
detect_platform summary: host none (no remote), base main, no CLIs (gh, glab, az, bb all false), no stack tools, commit_samples ["Add note store"], no ticket keys.

## Draft shown (before saving)

```markdown
# pr-ready profile

## Platform

- host: none
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: none
- pr template: none
- commit format: unclear
- agent rules: none
- ai_description: unclear
- ai_disclosure: unclear
- prior_approval: unclear

## Base branch

- base: main

## Commands

- reproduce CI: none found
- tests: none found
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
- ai_description, ai_disclosure and prior_approval are unclear. The repo has no CONTRIBUTING, AI policy, PR template or agent rules. Silence is not a value, so none of them is `none`, `allowed` or `not-required`. A CONTRIBUTING.md or AI policy sentence would settle them.
- commit format is unclear. There is only one commit sample, so no format is "most samples".
- All four Commands are `none found` because there are no CI files. No tests, build or CI commands appear anywhere in the repo, so I suggest none.
- No host CLI is available, and the host is none. Remote steps will follow references/platforms/none.md.
- Generated files: no `.gitattributes`, and `git grep` for generated-file headers found nothing.
- Risk paths: only notes/store.py and notes/__init__.py exist. There is nothing auth-, secrets- or migration-related beyond the defaults.

## Gate question (as I would ask the dev)
"Save this to `.pr-ready/profile.md`? Approve, or tell me what to change."

## Dev answer (pre-supplied)
approve

## Saved
- .pr-ready/profile.md (the approved draft, written with LF line endings)
- .pr-ready/.profile.generated.md (identical, since this is a first run with no merge)
- Parse check with read_profile: found true, policy all `unclear`, budget 500, warnings [] (empty).
- Evidence log: `evidence.py add --kind note` exited 0 and wrote .pr-ready/evidence/main-1ff971.md.
- Nothing staged or committed. `git status` shows only `?? .pr-ready/`. The dev can commit profile.md and .profile.generated.md together to share the profile with the team, and that choice is theirs.

## Sections kept / updated
First run, so none were kept or updated.

## Fields left unclear for the dev
ai_description, ai_disclosure, prior_approval, commit format.
