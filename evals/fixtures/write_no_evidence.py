"""Policy allows AI descriptions, but nothing was ever run or recorded."""
from __future__ import annotations

from . import write_base as wb


def build(dir):
    wb.build_branch(dir, "AI-written text is welcome if the author has read it.",
                    wb.profile())
