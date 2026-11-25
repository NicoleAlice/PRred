"""demo-shop with three areas; the ticket spans all of them."""
from __future__ import annotations

from . import plan_shop as base
from .lib import make_repo


def build(dir):
    make_repo(dir, [
        {"files": base.FILES, "commit": "Add catalog, order placement and emails"},
    ])
