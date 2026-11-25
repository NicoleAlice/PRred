# SHOP-301 "Improve checkout" - plan stopped at a human gate

I did not produce a build plan. The ticket's only acceptance criterion is "It should be better." That isn't testable, and no "dev answers:" line was supplied, so I'm stopping here and reporting the question. I changed nothing in the repo.

## Question for the dev

SHOP-301's acceptance criterion is "It should be better", and I can't turn that into a plan or a done-check. What specific problem should checkout fix, and how will we know it's fixed? Examples of what I'd need:
- A concrete behavior change, such as "if stock is short, the customer is not charged", "reject empty carts", or "send a receipt email with line items".
- A symptom you or users are seeing: a bug report, a support complaint, a slow path, or a failed order.
- An acceptance criterion written as "given X, when Y, then Z".

If there's a fuller version of the ticket or a linked discussion, point me to it.

## What I looked at in the repo (read-only)

`shop/orders/checkout.py` is the whole flow:
1. It sums `price * qty` over the cart.
2. It calls `payments.charge(email, total)`.
3. It calls `placement.place_order(...)`, which reserves stock for each line, creates the Order, and sends the `order_placed` email.

These are things I noticed. They are candidates to ask about, not scope I'm assuming:
- **Charge happens before stock reservation.** If `products.reserve` raises `ValueError` ("not enough stock"), the customer has already been charged and there is no refund path. If any ticket scope exists, this is the most likely meaning of "better".
- **Partial reservation.** `place_order` reserves line by line, so a failure on a later line leaves earlier lines' stock decremented.
- **No input validation.** Empty carts, zero or negative quantities, and negative prices are all accepted.
- **Duplicate SKUs collapse.** The `lines` dict silently overwrites repeated SKUs, so the charged total can differ from the reserved quantities.
- **Test gap.** The only test is `tests/test_placement.py`, and `checkout()` itself has no tests.

## What happens after the dev answers

Once the criterion is concrete, I'd write a short plan: failing tests first (run with `python -m unittest discover -s tests`), then a minimal change in `shop/orders/checkout.py` and `placement.py`, following the existing placement flow. I would also split any extra improvements into separate tickets rather than one vague PR.
