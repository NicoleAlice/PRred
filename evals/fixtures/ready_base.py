"""Shared pieces for the pr-ready fixtures: a tiny invented project on a feature branch."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .lib import make_repo

EVIDENCE_PY = Path(__file__).resolve().parents[2] / "scripts" / "evidence.py"
ORIGIN = "git@gitlab.example.com:team/shop.git"
BRANCH = "feat/SHOP-31-coupon-codes"

BASE_FILES = {
    "README.md": "# shopkit\n\nA tiny cart library.\n",
    ".gitignore": "__pycache__/\n*.pyc\n",
    "docs/usage.md": "# Usage\n\nCreate a cart and add items.\n",
    "shopkit/__init__.py": "",
    "shopkit/cart.py": (
        "def subtotal(items):\n"
        "    return sum(qty * price for qty, price in items)\n"
    ),
    "tests/__init__.py": "",
    "tests/test_cart.py": (
        "import unittest\n\n"
        "from shopkit.cart import subtotal\n\n\n"
        "class SubtotalTest(unittest.TestCase):\n"
        "    def test_subtotal(self):\n"
        "        self.assertEqual(subtotal([(2, 5)]), 10)\n"
    ),
}

FEATURE_FILES = {
    "shopkit/coupons.py": (
        "def apply_coupon(amount, percent):\n"
        "    \"\"\"Take percent off amount; percent must be between 0 and 100.\"\"\"\n"
        "    if percent < 0 or percent > 100:\n"
        "        raise ValueError(\"percent out of range\")\n"
        "    return round(amount * (100 - percent) / 100, 2)\n"
    ),
    "tests/test_coupons.py": (
        "import unittest\n\n"
        "from shopkit.coupons import apply_coupon\n\n\n"
        "class CouponTest(unittest.TestCase):\n"
        "    def test_ten_percent(self):\n"
        "        self.assertEqual(apply_coupon(50, 10), 45.0)\n\n"
        "    def test_out_of_range(self):\n"
        "        with self.assertRaises(ValueError):\n"
        "            apply_coupon(50, 120)\n"
    ),
}

DOCS_FILES = {
    "README.md": "# shopkit\n\nA tiny cart library.\n\nRun the tests with `python -m unittest`.\n",
    "docs/usage.md": (
        "# Usage\n\nCreate a cart and add items.\n\n"
        "## Totals\n\nCall `subtotal` with a list of (quantity, price) pairs.\n"
    ),
}

PROFILE = """# pr-ready profile

## Platform

- host: gitlab
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: none found
- pr template: none
- commit format: free-form (observed in history)
- agent rules: none
- ai_description: allowed
  > "no statement found" (README.md)
- ai_disclosure: none
  > "no statement found" (README.md)
- prior_approval: not-required
  > "no statement found" (README.md)

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


def add_evidence(dir, kind, text):
    r = subprocess.run([sys.executable, str(EVIDENCE_PY), "add", "--kind", kind,
                        "--text", text], cwd=str(dir), capture_output=True,
                       text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError("evidence add failed: %s" % r.stderr.strip())


def build_branch(dir, feature_files):
    files = dict(BASE_FILES)
    files[".pr-ready/profile.md"] = PROFILE
    make_repo(dir, [
        {"files": files, "commit": "Add cart subtotal"},
        {"branch": BRANCH, "files": feature_files,
         "commit": "Change on " + BRANCH},
    ], remote=ORIGIN)


def prove_evidence(dir):
    add_evidence(dir, "command",
                 "`python -m unittest discover -s tests -v`: Ran 3 tests in 0.003s, OK")
    add_evidence(dir, "mutation",
                 "Changed `percent > 100` to `percent > 200` in apply_coupon: "
                 "test_out_of_range failed (1 failure of 3), killed")
    add_evidence(dir, "mutation",
                 "Changed `(100 - percent)` to `(100 + percent)` in apply_coupon: "
                 "test_ten_percent failed (1 failure of 3), killed")
    add_evidence(dir, "note", "plan approved")
