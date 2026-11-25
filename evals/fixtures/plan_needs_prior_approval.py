"""Repo whose profile requires an approved issue before feature PRs."""
from __future__ import annotations

from . import plan_shop as base
from .lib import make_repo

CONTRIBUTING = """# Contributing to demo-shop

Run `python -m unittest discover -s tests` before opening a pull request.

## Process

Bug fixes under 50 lines may be sent directly. Feature pull requests need an
approved issue first: open an issue, wait for a maintainer to label it
`approved`, and link it from the pull request.
"""

PROFILE = """# pr-ready profile

## Platform

- host: github
- tracker: github-issues
- stack tool: plain branches

## Project rules

- contributing: CONTRIBUTING.md
- pr template: none
- commit format: free-form (observed in history)
- agent rules: none
- ai_description: unclear
  > "no statement found" (CONTRIBUTING.md)
- ai_disclosure: unclear
  > "no statement found" (CONTRIBUTING.md)
- prior_approval: required
  > "Feature pull requests need an approved issue first" (CONTRIBUTING.md, section Process)

## Base branch

- base: main

## Commands

- reproduce CI: none found
- tests: `python -m unittest discover -s tests`
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
"""


def build(dir):
    files = dict(base.FILES)
    files["CONTRIBUTING.md"] = CONTRIBUTING
    files[".pr-ready/profile.md"] = PROFILE
    make_repo(dir, [{"files": files, "commit": "Add shop and pr-ready profile"}])
