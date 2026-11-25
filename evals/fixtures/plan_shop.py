"""Shared demo-shop code for the pr-plan fixtures (not a fixture itself)."""
from __future__ import annotations

FILES = {
    "README.md": "# demo-shop\n\nSmall order service: catalog, orders, notifications.\n\nRun tests with `python -m unittest discover -s tests`.\n",
    "shop/__init__.py": "",
    "shop/catalog/__init__.py": "",
    "shop/catalog/products.py": '''"""Product catalog and stock levels."""
from __future__ import annotations

_STOCK = {}


def set_stock(sku, quantity):
    _STOCK[sku] = quantity


def get_stock(sku):
    return _STOCK.get(sku, 0)


def reserve(sku, quantity):
    """Take `quantity` units out of stock. Raises ValueError if short."""
    if get_stock(sku) < quantity:
        raise ValueError("not enough stock for %s" % sku)
    _STOCK[sku] -= quantity
''',
    "shop/orders/__init__.py": "",
    "shop/orders/models.py": '''"""Order records."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Order:
    id: int
    customer_email: str
    lines: dict = field(default_factory=dict)  # sku -> quantity
    total_cents: int = 0
    status: str = "placed"  # placed | shipped | delivered
    payment_ref: str = ""
''',
    "shop/orders/placement.py": '''"""Order placement: the existing flow every new order feature follows."""
from __future__ import annotations

from shop.catalog import products
from shop.notifications import emails
from shop.orders.models import Order

_ORDERS = {}
_NEXT_ID = [1]


def place_order(customer_email, lines, total_cents, payment_ref):
    for sku, quantity in lines.items():
        products.reserve(sku, quantity)
    order = Order(_NEXT_ID[0], customer_email, dict(lines), total_cents,
                  "placed", payment_ref)
    _NEXT_ID[0] += 1
    _ORDERS[order.id] = order
    emails.send_template(customer_email, "order_placed", {"order_id": order.id})
    return order


def get_order(order_id):
    return _ORDERS[order_id]
''',
    "shop/orders/payments.py": '''"""Thin wrapper over the payment provider client."""
from __future__ import annotations


def charge(customer_email, amount_cents):
    """Charge a customer and return a payment reference."""
    return "pay_%s_%d" % (customer_email.split("@")[0], amount_cents)
''',
    "shop/notifications/__init__.py": "",
    "shop/notifications/emails.py": '''"""Customer emails, rendered from templates and handed to an outbox."""
from __future__ import annotations

TEMPLATES = {
    "order_placed": "Thanks! Your order #{order_id} is confirmed.",
}
OUTBOX = []


def send_template(to, name, context):
    OUTBOX.append((to, TEMPLATES[name].format(**context)))
''',
    "tests/__init__.py": "",
    "tests/test_placement.py": '''import unittest

from shop.catalog import products
from shop.notifications import emails
from shop.orders import placement


class PlacementTest(unittest.TestCase):
    def test_place_order_reserves_stock_and_emails(self):
        products.set_stock("mug", 5)
        emails.OUTBOX.clear()
        order = placement.place_order("a@example.com", {"mug": 2}, 1800, "pay_1")
        self.assertEqual(products.get_stock("mug"), 3)
        self.assertEqual(order.status, "placed")
        self.assertEqual(len(emails.OUTBOX), 1)


if __name__ == "__main__":
    unittest.main()
''',
}
