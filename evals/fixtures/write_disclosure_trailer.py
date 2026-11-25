"""Project requires AI disclosure as a commit trailer; policy allows AI text."""
from __future__ import annotations

from . import write_base as wb


def build(dir):
    prof = wb.profile(
        ai_disclosure="required-in-trailer",
        disclosure_quote='"Add an `Assisted-by: <tool>` trailer to commits made with AI help" '
                         '(CONTRIBUTING.md, section Tooling)')
    wb.build_branch(
        dir, "AI-written text is welcome if the author has read it. "
             "Add an `Assisted-by: <tool>` trailer to commits made with AI help.", prof)
    wb.fresh_evidence(dir)
