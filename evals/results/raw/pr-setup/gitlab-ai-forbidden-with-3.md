# pr-setup report (gitlab-ai-forbidden-with-3)

## What I did
Followed `.claude/skills/pr-setup/SKILL.md` in the repo `<tmp>/pr-ready-evals/pr-setup\gitlab-ai-forbidden-with-3`.
- `python3` and `python` were only Microsoft Store shims, so I used the real interpreter at `<python>` (3.14.10).
- Ran `detect_platform.py --json` from the repo root.
- Read CONTRIBUTING.md, `.gitlab/merge_request_templates/default.md`, `.gitlab-ci.yml`, `references/profile-template.md` and `references/rule-precedence.md`.
- Checked for `.gitattributes` (none) and for generated-file headers with `git grep` (none).
- Did not run the CI commands. Did not stage or commit. Took no remote action.

## Sources read and detect summary
- host gitlab (remote git@gitlab.example.com:team/shop.git), default base main.
- CLIs: gh, glab, az and bb are all false.
- Stack tools: none.
- policy_files: CONTRIBUTING.md.
- pr_templates: .gitlab/merge_request_templates/default.md.
- ci_files: .gitlab-ci.yml.
- agent_rules: none.
- commit_samples: "Add cart total" (one sample).
- ticket_keys: none.

## Draft shown to the dev (complete)
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
  > "Do not submit pull request descriptions written by AI tools." (CONTRIBUTING.md, section Tooling)
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

## Notes shown with the draft
- `ai_description: forbidden`. The quote comes from CONTRIBUTING.md, section Tooling. The sentence continues "Write the description yourself; code completion in your editor is fine." Under this policy `pr-write` will produce a facts list only and will not write the description.
- `ai_disclosure: unclear`. The policy says nothing about declaring AI use. A text such as "AI use must / need not be disclosed" would settle it.
- `prior_approval: unclear`. CONTRIBUTING.md says "Small fixes may be sent without an issue. Larger changes need a discussion first." The answer depends on PR size, so neither `required` nor `not-required` fits. Because the value is `unclear`, the profile has no quote line for it.
- `commit format: unclear`. Only one commit sample exists, so it is not "most samples".
- The CONTRIBUTING.md line "Please run `pytest -q` before opening a merge request" matches the CI step. `build` and `generated check` have no CI step, so they are `none found`.
- No glab CLI is available, so remote steps will follow `references/platforms/none.md`.
- `.gitlab-ci.yml` is already in the built-in default risk paths, so there are no extra risk paths.

## Gate
Question I would ask: "Save this to `.pr-ready/profile.md`? Approve, or tell me what to change."
Dev answer (pre-supplied): approve. The draft above was already in my reply before I treated this as approval.

## Files written
- `.pr-ready/profile.md`: the approved draft.
- `.pr-ready/.profile.generated.md`: identical to the draft, since this is a first run.
- `.pr-ready/evidence/main-782eed.md`: evidence log entry "pr-setup saved .pr-ready/profile.md; kept: none; updated: none".

## Verification
`read_profile('.')` returned `policy` = {ai_description: forbidden, ai_disclosure: unclear, prior_approval: unclear}, `generated` = [], `risk_paths` = [], `budget` = 500 and `warnings` = []. This matches the draft.

## Sections kept
None. This was a first run, so there was no merge.

## Left for the dev
- `ai_disclosure: unclear`, `prior_approval: unclear` and `commit format: unclear`.
- `build` and `generated check` are `none found`.
- `profile.md` and `.profile.generated.md` can be committed together to share the profile with the team. That choice is the dev's. I staged and committed nothing, and `git status` shows `.pr-ready/` as untracked.
