"""Shared pieces for the pr-write fixtures: a tiny invented project on a feature branch."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .lib import _git, make_repo

EVIDENCE_PY = Path(__file__).resolve().parents[2] / "scripts" / "evidence.py"
BRANCH = "feat/PAY-12-late-fee"

BASE_FILES = {
    "README.md": "# ledgerlite\n\nA tiny invoice library.\n",
    ".gitignore": "__pycache__/\n*.pyc\n",
    "ledgerlite/__init__.py": "",
    "ledgerlite/invoice.py": (
        "def total(lines):\n"
        "    return sum(qty * price for qty, price in lines)\n"
    ),
    "tests/__init__.py": "",
    "tests/test_invoice.py": (
        "import unittest\n\n"
        "from ledgerlite.invoice import total\n\n\n"
        "class TotalTest(unittest.TestCase):\n"
        "    def test_total(self):\n"
        "        self.assertEqual(total([(2, 5)]), 10)\n"
    ),
}

FEATURE_FILES = {
    "ledgerlite/fees.py": (
        "def late_fee(amount, days_late, rate=0.015):\n"
        "    \"\"\"Fee for an invoice paid days_late days after the due date.\"\"\"\n"
        "    if days_late <= 0:\n"
        "        return 0\n"
        "    return round(amount * rate * days_late, 2)\n"
    ),
    "tests/test_fees.py": (
        "import unittest\n\n"
        "from ledgerlite.fees import late_fee\n\n\n"
        "class LateFeeTest(unittest.TestCase):\n"
        "    def test_on_time(self):\n"
        "        self.assertEqual(late_fee(100, 0), 0)\n\n"
        "    def test_late(self):\n"
        "        self.assertEqual(late_fee(100, 2), 3.0)\n"
    ),
}

FOLLOWUP_FILES = {
    "ledgerlite/fees.py": (
        "def late_fee(amount, days_late, rate=0.015, cap=0.2):\n"
        "    \"\"\"Fee for an invoice paid days_late days after the due date, capped.\"\"\"\n"
        "    if days_late <= 0:\n"
        "        return 0\n"
        "    return round(min(amount * rate * days_late, amount * cap), 2)\n"
    ),
}

DESC_QUOTES = {
    "allowed": '"AI-written text is welcome if the author has read it" (CONTRIBUTING.md, section Tooling)',
    "forbidden": '"Pull request descriptions must be written by a human" (CONTRIBUTING.md, section Tooling)',
    "unclear": '"no statement found" (CONTRIBUTING.md)',
}
NONE_QUOTE = '"Contributors need not mention the tools they used" (CONTRIBUTING.md, section Tooling)'

PROFILE = """# pr-ready profile

## Platform

- host: gitlab
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: CONTRIBUTING.md
- pr template: {template}
- commit format: free-form (observed in history)
- agent rules: none
- ai_description: {ai_description}
  > {description_quote}
- ai_disclosure: {ai_disclosure}
  > {disclosure_quote}
- prior_approval: not-required
  > "Small fixes may be sent without an issue" (CONTRIBUTING.md, section Process)

## Base branch

- base: main

## Commands

- reproduce CI: `python -m unittest discover -s tests -v`
- tests: `python -m unittest discover -s tests -v`
- build: none found
- generated check: none found

## Generated files

- none

## Budget

- max_lines: 500

## Risk paths

- none
"""


def profile(ai_description="allowed", description_quote=None,
            ai_disclosure="none", disclosure_quote=None, template="none"):
    return PROFILE.format(
        template=template, ai_description=ai_description,
        description_quote=description_quote or DESC_QUOTES[ai_description],
        ai_disclosure=ai_disclosure,
        disclosure_quote=disclosure_quote or NONE_QUOTE)


def contributing(tooling):
    return ("# Contributing to ledgerlite\n\n## Process\n\n"
            "Small fixes may be sent without an issue.\n\n## Tooling\n\n%s\n" % tooling)


def add_evidence(dir, kind, text):
    r = subprocess.run([sys.executable, str(EVIDENCE_PY), "add", "--kind", kind,
                        "--text", text], cwd=str(dir), capture_output=True,
                       text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError("evidence add failed: %s" % r.stderr.strip())


def fresh_evidence(dir):
    add_evidence(dir, "command",
                 "`python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK")
    add_evidence(dir, "mutation",
                 "Changed `days_late <= 0` to `days_late < 0` in late_fee: "
                 "test_on_time failed (1 failure of 3)")


def build_branch(dir, tooling, prof, extra=None):
    files = dict(BASE_FILES)
    files["CONTRIBUTING.md"] = contributing(tooling)
    files[".pr-ready/profile.md"] = prof
    files.update(extra or {})
    make_repo(dir, [
        {"files": files, "commit": "Add invoice total"},
        {"branch": BRANCH, "files": FEATURE_FILES,
         "commit": "Add late fee for overdue invoices"},
    ])


def add_followup_commit(dir):
    for rel, content in FOLLOWUP_FILES.items():
        with open(str(Path(dir) / rel), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
    _git(["add", "-A"], dir)
    _git(["commit", "-m", "Cap the late fee at 20 percent of the amount"], dir)
