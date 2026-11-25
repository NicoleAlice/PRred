"""GitLab repo with a saved profile the dev hand-edited after generation."""
from __future__ import annotations

from . import setup_gitlab_ai_forbidden as base
from .lib import make_repo

GENERATED = """# pr-ready profile

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

- reproduce CI: `pytest -q`
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
"""

TRAP = "| Flaky test_cache on CI | shared tmp dir | rerun once |\n"
EDITED = GENERATED.replace("| none yet | | |\n", TRAP)


def build(dir):
    make_repo(dir, [
        {"files": base.FILES, "commit": "Add cart total"},
        {"files": {".pr-ready/.profile.generated.md": GENERATED,
                   ".pr-ready/profile.md": EDITED},
         "commit": "Add pr-ready profile"},
    ], remote=base.REMOTE)
