# pr-ready profile

Invented example: a small Python library with no git host CLI, no CI pipeline and a maintainer who wants an issue agreed before any pull request. Copy it to `.pr-ready/profile.md` only as a starting point; `pr-setup` builds the real one from your repo.

## Platform

- host: none
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: CONTRIBUTING.md
- pr template: none
- commit format: free-form (observed in history)
- agent rules: none
- ai_description: unclear
  > "Please write your own words in the pull request" (CONTRIBUTING.md, section Pull requests)
- ai_disclosure: unclear
  > "no statement found" (CONTRIBUTING.md)
- prior_approval: required
  > "Open an issue and wait for a maintainer to agree before sending a pull request" (CONTRIBUTING.md, section Before you start)

`ai_description` is `unclear` on purpose: "your own words" could forbid an assistant's prose or only ask for care. `pr-write` hands the dev a facts list and asks.

## Base branch

- base: main

## Commands

- setup: none found
- reproduce CI: none found
- tests: `python -m unittest discover -s tests -v`
- build: none found
- generated check: none found

## Generated files

- none

## Budget

- max_lines: 300

## Risk paths

- `easy_tz/parse.py`

## Known traps

| Symptom | Cause | What to do |
|---|---|---|
| Tests pass on one machine and fail on another | The tests read the system time zone database | Run them with `TZ=UTC` and with one non-UTC zone |
