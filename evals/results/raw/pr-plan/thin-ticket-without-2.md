# SHOP-301 "Improve checkout": stopped at a human gate, no plan yet

I haven't planned this. The ticket's only acceptance criterion is "It should be better", and I can't turn that into a test or a done-state. Any plan I wrote would be a guess at what "better" means. No gate answer was pre-supplied, so I'm stopping here. I changed nothing in the repo.

## Question for the dev

> SHOP-301's only acceptance criterion is "It should be better", so I can't tell what done looks like. What should change about checkout, and how will we know it worked? Please give me one or more concrete outcomes. For example:
> 1. **Correctness:** don't charge the customer if stock is short, and refund or roll back if order placement fails.
> 2. **Speed:** a target, such as checkout latency under N ms.
> 3. **Validation:** reject empty carts, bad quantities or prices, and malformed emails with clear errors.
> 4. **UX or emails:** a richer confirmation email with line items and total.
> 5. **Something else**, such as discounts, tax or shipping.
>
> Is there a product owner or a linked design or bug report I can check? And what is explicitly out of scope?

## What I found in the code (read-only)

These are observations only, not a scope decision.

The flow lives in `shop/orders/checkout.py`:
- It computes the total, calls `payments.charge`, then calls `placement.place_order`.
- `place_order` reserves stock per SKU, creates the `Order`, and sends the `order_placed` email.

Possible candidates for "better", if the dev points at correctness:
- **Charge before reserve.** `checkout()` charges the customer first. If `products.reserve` then raises `ValueError` for short stock, the customer has been charged and there is no order. There is no refund or compensation path.
- **Partial reservation.** `place_order` reserves SKUs one at a time. If a later SKU fails, the earlier ones stay reserved, so stock leaks.
- **No input validation.** Nothing checks for an empty cart, negative or zero quantity or price, or duplicate SKUs. The line `lines = {sku: qty ...}` silently drops duplicate SKUs, while `total` still counts them.
- **Money handling.** The total is a plain sum of `price * qty`. Whether prices are in cents isn't documented, although `Order.total_cents` suggests they are.
- **Test coverage.** `tests/test_placement.py` covers only the happy path of `place_order`. `checkout()` and the payments module have no tests.

## Proposed next step once the dev answers

1. Turn the answer into 2 to 4 testable acceptance criteria and confirm them with the dev.
2. Write a short plan that follows the existing flow in `placement.py`. It would add failing tests first (`unittest`, run with `python -m unittest discover -s tests`), then make the change, with a separate step for any behaviour change to payments.
3. Keep the PR scoped to the agreed criteria.
