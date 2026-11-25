"""Committed api/schema.json is missing a field the generator produces."""
from __future__ import annotations

from . import prove_generated_crlf as crlf


def build(dir):
    crlf.build_with(dir, crlf.SCHEMA_STALE_LF.replace("\n", "\r\n").encode("utf-8"))
