"""A normal code change; prove is done (fresh evidence), no review yet."""
from __future__ import annotations

from . import ready_base as rb


def build(dir):
    rb.build_branch(dir, rb.FEATURE_FILES)
    rb.prove_evidence(dir)
