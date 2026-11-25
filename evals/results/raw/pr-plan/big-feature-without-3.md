# Plan: SHOP-212 order cancellation (refunds, stock restore, emails)

I read the repo (one commit, "Add catalog, order placement and emails") and changed nothing. No "dev answers" lines were supplied, so there was no pre-supplied answer for any gate. The questions below would be asked, and each has the default I would plan with.

## What exists today
- `shop/orders/models.py`: `Order` has `status` (placed | shipped | delivered) and `payment_ref`. It has no refund fields and no cancelled status.
- `shop/orders/payments.py`: only `charge()`. There is no refund call.
- `shop/orders/placement.py`: `place_order` reserves stock, stores the order in `_ORDERS`, and sends the `order_placed` email. It is the pattern to follow.
- `shop/catalog/products.py`: `set_stock`, `get_stock` and `reserve`. There is no restock function and no record of why stock changed.
- `shop/notifications/emails.py`: a `TEMPLATES` dict, `send_template` and an `OUTBOX` list.
- `tests/test_placement.py`: a single unittest. Run the tests with `python -m unittest discover -s tests`.

## Questions for the dev (gates)
1. **Refund failure state.** If the provider refund fails, should the order become `cancelled` with no refund recorded, or stay `placed`? Is stock restored? Can support retry later?
   - Default: the order becomes `cancelled`, stock is restored, and the refund fields stay empty. The "support will follow up" email is sent. A retry is possible because `refund_ref` is empty. Retrying is out of scope.
2. **Second cancel of an already-cancelled order.** Should it raise an error or do nothing?
   - Default: it raises `OrderNotCancellable`. No refund, no stock change and no email happen. This is safe and explicit.
3. **Stock-change history shape** (AC6). Is an in-memory log in the catalog module enough for support staff, matching the existing in-memory style?
   - Default: yes. Each entry holds sku, delta, reason (`placement` or `cancellation`) and order_id, exposed through `stock_history(sku=None)`.
4. **PR split.** Is one PR acceptable, or should it be stacked? The change touches 5 modules plus tests, roughly 150 to 250 lines.
   - Default: split it as below.

## Design
- **Model.**
  - Add `refund_ref: str = ""` and `refund_cents: int = 0` to `Order`.
  - Add `cancelled` to the status comment and use it as the status value.
- **Payments.** Add `refund(payment_ref, amount_cents)`, which returns a refund reference such as `"ref_<payment_ref>_<amount>"`. It mirrors the stubbed `charge`. It raises `PaymentError` on failure.
- **Catalog.**
  - Add a module-level `_HISTORY` list.
  - Add `restock(sku, quantity, reason="cancellation", order_id=None)` and `stock_history(sku=None)`.
  - Extend `reserve` with optional `reason="placement"` and `order_id=None` arguments. Existing callers keep working. `placement.place_order` passes the order id, which means allocating the id before reserving.
- **Emails.** Add two templates to `TEMPLATES`:
  - `order_cancelled`: "Your order #{order_id} was cancelled. We refunded {refund_amount}."
  - `order_cancelled_refund_failed`: "Your order #{order_id} was cancelled, but the refund failed. Support will follow up."
  - The refund amount is formatted from cents in one small helper, for example `"$18.00"`.
- **New module `shop/orders/cancellation.py`** with `cancel_order(order_id)`, in this order:
  1. Look up the order with `get_order`.
  2. If the status is not `placed` (shipped, delivered or already cancelled), raise `OrderNotCancellable("order #N is <status>; only placed orders can be cancelled")`.
  3. Set `status = "cancelled"` before any external call. This makes a second call hit the guard, so there is no double refund (AC3).
  4. Restock every line through `products.restock`, which writes the history entries (AC4 and AC6).
  5. Call `payments.refund(order.payment_ref, order.total_cents)`.
     - On success: set `refund_ref` and `refund_cents`, then send `order_cancelled` with the amount.
     - On `PaymentError`: leave the refund fields empty, send `order_cancelled_refund_failed`, and do not re-raise.
  6. Return the order.

## Proposed PR slices (stacked, each reviewable alone and green)
1. **Catalog stock history and restock** (AC4 infrastructure and AC6).
   - Changes: `products.restock`, `stock_history`, and the `reason` and `order_id` arguments on `reserve`. `placement.py` passes the order id.
   - Tests: restock adds quantity, history records both placement and cancellation reasons, and the existing placement test still passes.
2. **Refund primitive, order fields and email templates** (AC2, AC3 fields, AC5 templates).
   - Changes: `payments.refund` and `PaymentError`, the `Order` fields, and the two templates with the amount helper.
   - Tests: the refund reference, the failure raising `PaymentError`, and the rendered email text including the amount.
3. **`cancel_order` flow and tests** (AC1, AC2, AC3, AC4, AC5, AC7). It depends on 1 and 2.
   - Tests, one per rule:
     - A placed order is cancelled.
     - A shipped order is rejected with a clear message and nothing else changes.
     - A delivered order is rejected with a clear message and nothing else changes.
     - The refund is called with the order's `payment_ref` and the full total.
     - The refund reference and amount are recorded on the order.
     - Cancelling twice makes one refund call and one email (patch `payments.refund` and count calls).
     - Every line is restocked, with a multi-line order.
     - The success email goes to the customer and contains the amount.
     - A refund failure sends the failure email, records no refund, and still restocks.
     - The stock history shows the placement and cancellation entries.

If the dev prefers a single PR, the same order works as three commits.

## Verification before declaring done
- Run `python -m unittest discover -s tests` after each slice.
- Mutation-check the new tests. For example: remove the status guard, move the status assignment after the refund, skip restocking, swap the email templates, and drop `payment_ref`. Each mutation should make at least one test fail.

## Risks and notes
- `_ORDERS`, `_STOCK`, `OUTBOX` and the history are module-level state, so each test must reset them (`setUp` with `clear()`). Reset `_NEXT_ID` too if ids matter.
- The refund is a stub like `charge`. Real provider semantics (idempotency keys, retries) are out of scope and noted as follow-up.
- Setting the status to `cancelled` before the external call means a crash mid-flow leaves a cancelled order with no refund. That is acceptable at this in-memory scale, and it is the reason to keep the refund fields as the retry signal.
