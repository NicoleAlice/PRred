"""A committed merge request template with distinctive headings; fresh evidence."""
from __future__ import annotations

from . import write_base as wb

TEMPLATE = "## Summary\n\n## How to test\n\n## Risk\n"
PATH = ".gitlab/merge_request_templates/default.md"


def build(dir):
    prof = wb.profile(template=PATH)
    wb.build_branch(dir, "AI-written text is welcome if the author has read it.",
                    prof, extra={PATH: TEMPLATE})
    wb.fresh_evidence(dir)
