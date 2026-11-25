# pr-setup report: bare-no-ci-with-1

Note on ordering: the draft below was shown at the gate, then the pre-supplied "approve" was applied, then the files were written.

## Sources read
- `.claude/skills/pr-setup/SKILL.md`, `references/profile-template.md`, `references/rule-precedence.md`.
- `detect_platform.py --json` output: host `none`, no remote, default_base `main`, no CLIs (gh/glab/az/bb all false), no stack tools, `policy_files`, `pr_templates`, `ci_files` and `agent_rules` all empty, one commit sample ("Add note store"), no ticket keys.
- No policy, template, CI or agent-rule files exist, so none were read. Tracked files are only README.md, notes/__init__.py and notes/store.py. No tracked file has a generated header.
- Python: the `python3`/`python` Store aliases and `py` failed. I used the real interpreter at `<python>` for the scripts.

## Complete draft (shown before saving)

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
- `ai_description`, `ai_disclosure` and `prior_approval` are `unclear`, and no quote lines are written. Text in a CONTRIBUTING.md, an AI policy, a PR template or agent rules would settle them. Silence is not recorded as `none` or `allowed`.
- `commit format` is `unclear` because there is only one commit sample.
- All four Commands are `none found` because the repo has no CI files. I suggested no commands from habit (pytest and the like).
- No host CLI is available and the host is `none`, so remote steps follow `references/platforms/none.md`.
- No tracker connector is available in the session and there are no ticket keys, so `tracker: none`.

## Gate question
Save this to `.pr-ready/profile.md`? Approve, or tell me what to change.

dev answers: approve (pre-supplied)

## Saved
- Wrote `.pr-ready/profile.md` and `.pr-ready/.profile.generated.md` (identical content, since this is a first run).
- The profile parse check passed: `policy` is unclear/unclear/unclear, `budget` 500, `generated` and `risk_paths` empty, `warnings` empty.
- The evidence log entry was added: `.pr-ready/evidence/main-3c30fa.md` ("pr-setup saved .pr-ready/profile.md; kept: none; updated: none").
- Nothing was staged or committed; `git status` shows only `?? .pr-ready/`. The dev can commit `profile.md` and `.profile.generated.md` together to share the profile with the team, and the choice is theirs.

## Final report
Draft shown, dev approved, files written (profile.md, .profile.generated.md, one evidence note), no sections kept because this was a first run. Fields left for the dev: `commit format`, `ai_description`, `ai_disclosure`, `prior_approval` (all `unclear`).
