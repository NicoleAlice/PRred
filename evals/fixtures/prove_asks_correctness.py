"""New rounding behaviour with an ambiguous spec and no test for it."""
from __future__ import annotations

from .prove_base import TESTED_COMMANDS, build_repo, profile

SHIPPING = '''"""Shipping cost helpers."""


def base_cost(weight_kg):
    """Cost in currency units: 4.00 flat plus 1.35 per kg."""
    return 4.0 + 1.35 * weight_kg
'''

SHIPPING_NEW = SHIPPING + '''

def shipping_cost(weight_kg):
    """Shipping cost rounded to a whole currency unit (SHOP-88)."""
    return round(base_cost(weight_kg))
'''

BASE_TEST = '''import unittest

from shop.shipping import base_cost


class BaseCostTest(unittest.TestCase):
    def test_base_cost(self):
        self.assertAlmostEqual(base_cost(2), 6.7)


if __name__ == "__main__":
    unittest.main()
'''


def build(dir):
    build_repo(
        dir,
        {"README.md": "# shop\n\nTiny shipping library.\n",
         "shop/__init__.py": "",
         "shop/shipping.py": SHIPPING,
         "tests/__init__.py": "",
         "tests/test_base_cost.py": BASE_TEST,
         ".pr-ready/profile.md": profile(TESTED_COMMANDS)},
        {"shop/shipping.py": SHIPPING_NEW},
        "Round shipping cost", "feat/round-shipping")
