"""Evidence was recorded, then a new commit landed on top of it."""
from __future__ import annotations

from . import write_base as wb


def build(dir):
    wb.build_branch(dir, "AI-written text is welcome if the author has read it.",
                    wb.profile())
    wb.add_evidence(dir, "command",
                    "`python -m unittest discover -s tests -v`: Ran 12 tests in 0.004s, OK")
    wb.add_evidence(dir, "mutation",
                    "Changed `days_late <= 0` to `days_late < 0`: test_on_time failed")
    wb.add_followup_commit(dir)
