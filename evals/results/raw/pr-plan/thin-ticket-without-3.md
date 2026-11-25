# SHOP-301 "Improve checkout": stopped at a human gate, no plan yet

I haven't planned this. The ticket's only acceptance criterion is "It should be better." That isn't testable, so any plan would be a guess about what "better" means. No dev answer was pre-supplied for this gate, so I'm stopping here. I changed nothing in the repo.

## Question for the dev

> SHOP-301 only says "Improve checkout" with the criterion "It should be better." What specific outcome should change for a customer or for the business? For example:
> 1. Correctness and robustness: stop charging customers when an order can't be placed.
> 2. Validation: reject empty carts, bad quantities and bad prices.
> 3. Money handling: discounts, tax, shipping or currency.
> 4. Feedback or UX: clearer errors, or a richer confirmation email.
> 5. Something else, such as speed, a new payment method, or guest checkout.
>
> Please also give me a checkable acceptance criterion, in the form "given X, checkout should do Y", so I know when it's done.

## What I found in the repo

`checkout` is a two-step flow: charge, then place the order. The repo is small and has one commit, "Add checkout".

- **`shop/orders/checkout.py`:**
  - It totals the cart with `sum(price * qty ...)`.
  - It calls `payments.charge(email, total)`.
  - It builds a `{sku: qty}` dict, which silently collapses duplicate SKUs in the cart (the last one wins, so earlier quantities are lost).
  - It then calls `placement.place_order(...)`.
- **`shop/orders/placement.py`:**
  - It reserves stock per SKU and creates the `Order`.
  - It stores the order in an in-memory dict.
  - It sends the `order_placed` email.
  - It is documented as "the existing flow every new order feature follows".
- **`shop/orders/payments.py`:** a stub that returns a reference string.
- **`shop/catalog/products.py`:** `reserve` raises `ValueError` when stock is short.
- **`shop/notifications/emails.py`:** a single `order_placed` template and an in-memory outbox.
- **`tests/test_placement.py`:** the only test. It covers `place_order` and nothing in `checkout()`. Run the tests with `python -m unittest discover -s tests`.

Several plausible problems exist, but the ticket doesn't say which one it means:

1. **Charged but no order.** `checkout` charges the customer before it reserves stock. If `products.reserve` raises `ValueError` for insufficient stock, the customer has already been charged and there is no order. There is no refund or rollback.
2. **Partial reservation.** `place_order` reserves SKUs one by one. If the second SKU is short, the first has already been taken out of stock and is never released.
3. **Duplicate SKUs.** Repeated SKUs in a cart are collapsed, as described above. The total counts every line, but the reserved quantity and the order lines don't.
4. **No input validation.** Empty carts, zero or negative quantities, and negative prices all go through. The total is also not checked as an integer number of cents.
5. **No test coverage for `checkout()`.** The only test targets `placement`.

## Proposed next step, once the dev answers

I'd confirm the scope with the dev. If they mean the robustness problems (1 to 3), I'd propose this plan:

1. Write failing tests for `checkout()`: insufficient stock, duplicate SKUs, and an empty cart.
2. Reorder `checkout` so stock is reserved first (or add a compensating refund), then the charge happens, and a failed charge releases the stock.
3. Make reservation all-or-nothing in `place_order`.
4. Aggregate duplicate SKUs in `checkout`.
5. Add input validation.

I would not start any of this until the dev confirms which direction "better" means, since the options pull the design in different directions.
