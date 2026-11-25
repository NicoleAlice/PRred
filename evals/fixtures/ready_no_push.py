"""Everything is done and the description is saved; the dev has not said to push."""
from __future__ import annotations

from pathlib import Path

from . import ready_base as rb


def build(dir):
    rb.build_branch(dir, rb.FEATURE_FILES)
    rb.prove_evidence(dir)
    rb.add_evidence(dir, "review",
                    "Cold review: no blocking findings; 1 nit (docstring wording), fixed or accepted")
    rb.add_evidence(dir, "note", "pr-write: description saved to .pr-ready/pr-description.md")
    pr = Path(dir) / ".pr-ready"
    with open(str(pr / ".gitignore"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("pr-description*.md\n")
    with open(str(pr / "pr-description.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("Add percentage coupons to the cart.\n\n"
                 "Coupons take a percent between 0 and 100 off an amount and reject "
                 "anything outside that range.\n\n"
                 "Tests: `python -m unittest discover -s tests -v` ran 3 tests, OK.\n")
