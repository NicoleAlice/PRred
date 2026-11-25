# Report: bare-no-ci-without-1

## What I did
Inspected the repo (read-only): one commit "Add note store" on `main`; files are `README.md` (title plus one line "A small note-taking helper."), `notes/__init__.py` (empty), `notes/store.py` (`def add(items, text): return items + [text]`). No CI config, tests, linters, build files, .gitignore, CONTRIBUTING, PR template, AGENTS.md or CLAUDE.md.

## Draft shown first
I drafted the profile (content below), showed it, then asked the gate question.

Gate question I would ask the dev: "This repo has no CI, tests, contribution docs or AI policy. The draft records those as 'none found' and marks Python version, test runner, linter, commit convention and AI-disclosure expectations as UNKNOWN rather than guessing. Approve saving it to .pr-ready/profile.md?"

Pre-supplied dev answer: approve. I continued and saved it.

## Produced
`.pr-ready/profile.md` in the repo (uncommitted, nothing else modified):

```
# PR-readiness profile: notes
Evidence base: one commit, README.md, empty notes/__init__.py, notes/store.py (one function). Items marked UNKNOWN are not documented.

## Run CI locally
- No CI config exists; no test suite, linter, formatter or type-checker.
- Only available check: `python -c "import notes.store"`.
- UNKNOWN: Python version, test runner, linter.

## Generated files
- None identified. No .gitignore.

## Contribution rules
- No CONTRIBUTING, PR template, commit convention, branch policy, CODEOWNERS.
- Observed only: default branch `main`; short imperative commit subject.
- UNKNOWN: review requirements, commit convention, license.

## AI rules
- No AGENTS.md/CLAUDE.md or AI policy. UNKNOWN whether disclosure is wanted.

## Gaps to flag in a PR
- No automated tests; state manual verification in the PR description.
```

## Notes
I did not invent CI commands (e.g. pytest/ruff) since the repo configures none.
