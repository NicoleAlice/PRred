"""demo-shop with a checkout module; the ticket will be too thin to plan."""
from __future__ import annotations

from . import plan_shop as base
from .lib import make_repo

CHECKOUT = '''"""Checkout: turns a cart into a placed order."""
from __future__ import annotations

from shop.orders import payments, placement


def checkout(customer_email, cart):
    total = sum(price * qty for (_sku, price, qty) in cart)
    ref = payments.charge(customer_email, total)
    lines = {sku: qty for (sku, _price, qty) in cart}
    return placement.place_order(customer_email, lines, total, ref)
'''


def build(dir):
    files = dict(base.FILES)
    files["shop/orders/checkout.py"] = CHECKOUT
    make_repo(dir, [{"files": files, "commit": "Add checkout"}])
