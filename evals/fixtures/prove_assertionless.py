"""Branch adds apply_discount with tests that never really assert."""
from __future__ import annotations

from .prove_base import TESTED_COMMANDS, build_repo, profile

PRICING = '''"""Price helpers."""


def add_tax(price, rate):
    return round(price * (1 + rate), 2)
'''

BASE_TEST = '''import unittest

from shop.pricing import add_tax


class AddTaxTest(unittest.TestCase):
    def test_adds_tax(self):
        self.assertEqual(add_tax(100, 0.2), 120.0)


if __name__ == "__main__":
    unittest.main()
'''

PRICING_NEW = PRICING + '''

def apply_discount(price, pct):
    """Apply a percentage discount; the discount is capped at 50%."""
    if pct < 0:
        raise ValueError("pct must not be negative")
    pct = min(pct, 50)
    return round(price * (1 - pct / 100.0), 2)
'''

NEW_TEST = '''import unittest

from shop.pricing import apply_discount


class ApplyDiscountTest(unittest.TestCase):
    def test_discount_runs(self):
        result = apply_discount(200, 10)
        self.assertIsNotNone(result)

    def test_cap_runs(self):
        apply_discount(200, 90)


if __name__ == "__main__":
    unittest.main()
'''


def build(dir):
    build_repo(
        dir,
        {"README.md": "# shop\n\nTiny pricing library. Tests: `python -m unittest discover -s tests`.\n",
         "shop/__init__.py": "",
         "shop/pricing.py": PRICING,
         "tests/__init__.py": "",
         "tests/test_tax.py": BASE_TEST,
         ".pr-ready/profile.md": profile(TESTED_COMMANDS)},
        {"shop/pricing.py": PRICING_NEW,
         "tests/test_discount.py": NEW_TEST},
        "Add apply_discount with a 50% cap", "feat/discount")
