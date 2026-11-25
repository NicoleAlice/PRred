"""The branch changes only README.md and docs/usage.md; no evidence."""
from __future__ import annotations

from . import ready_base as rb


def build(dir):
    rb.build_branch(dir, rb.DOCS_FILES)
