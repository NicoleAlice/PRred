"""Trivial fixture used to test the harness itself."""
from __future__ import annotations

from .lib import make_repo


def build(dir):
    make_repo(dir, [
        {"files": {"README.md": "# hello\n"}, "commit": "initial"},
    ])
