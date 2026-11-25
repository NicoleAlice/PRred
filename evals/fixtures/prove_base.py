"""Shared pieces for the pr-prove fixtures: small unittest-only projects."""
from __future__ import annotations

from .lib import make_repo

GITIGNORE = ".pr-ready/evidence/\n__pycache__/\n*.pyc\nbuild/\n"


def profile(commands, generated=None):
    gen = "\n".join("- `%s`" % g for g in generated) if generated else "- none"
    return """# pr-ready profile

## Platform

- host: github
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: none
- pr template: none
- commit format: free-form (observed in history)
- agent rules: none
- ai_description: unclear
  > "no statement found" (README.md)
- ai_disclosure: unclear
  > "no statement found" (README.md)
- prior_approval: not-required
  > "Small fixes may be sent without an issue" (README.md)

## Base branch

- base: main

## Commands

%s

## Generated files

%s

## Budget

- max_lines: 500

## Risk paths

- none
""" % (commands, gen)


TESTED_COMMANDS = (
    "- reproduce CI: `python -m unittest discover -s tests -v`\n"
    "- tests: `python -m unittest discover -s tests -v`\n"
    "- build: none found\n"
    "- generated check: none found")

NO_COMMANDS = (
    "- reproduce CI: none found\n"
    "- tests: none found\n"
    "- build: none found\n"
    "- generated check: none found")


def build_repo(dir, base_files, feature_files, feature_msg, branch):
    files = dict(base_files)
    files[".gitignore"] = GITIGNORE
    make_repo(dir, [
        {"files": files, "commit": "Initial project"},
        {"files": feature_files, "commit": feature_msg, "branch": branch},
    ])
