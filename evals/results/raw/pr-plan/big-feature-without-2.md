# SHOP-212 plan: order cancellation with refunds, stock restore, customer emails

I read the repo (one commit, "Add catalog, order placement and emails") and changed nothing. This is a plan only, with no code written yet.

## What exists today

- `shop/orders/placement.py`: `place_order` reserves stock, builds an `Order`, stores it in the in-memory `_ORDERS`, and sends the `order_placed` email. `get_order` reads from `_ORDERS`.
- `shop/orders/models.py`: `Order` has `status` (`placed | shipped | delivered`) and `payment_ref`. It has no refund fields and no `cancelled` status.
- `shop/orders/payments.py`: only `charge()`. There is no refund call.
- `shop/catalog/products.py`: `_STOCK`, `set_stock`, `get_stock` and `reserve`. There is no way to put stock back and no record of why stock changed.
- `shop/notifications/emails.py`: `TEMPLATES` is a dict, and `send_template(to, name, context)` appends to `OUTBOX`.
- `tests/test_placement.py`: one `unittest` test. Run with `python -m unittest discover -s tests`.

## Decisions I'm proposing (each is easy to change)

1. **New status `cancelled`.** The `Order.status` comment is updated to `placed | cancelled | shipped | delivered`.
2. **New refund fields on `Order`:** `refund_ref: str = ""` and `refund_cents: int = 0`. A non-empty `refund_ref` means "already refunded". This is the idempotency marker for AC3.
3. **Refunds go through `payments.refund(payment_ref, amount_cents)`.** It returns a refund reference like `ref_...` and raises `payments.RefundError` on failure. It follows the style of the existing `charge` stub. The amount is the order's `total_cents`, which is a full refund (AC2).
4. **Stock history lives in the catalog (AC6).** `products.py` gets a movement log, `_MOVEMENTS`, holding `(sku, delta, reason, order_id)` entries.
   - `reserve(sku, quantity, reason="placement", order_id=None)` records `-quantity`. The new arguments are optional, so existing callers keep working.
   - New `restock(sku, quantity, reason, order_id)` adds stock and records `+quantity`.
   - New `stock_history(sku)` returns the entries for support staff.
   - Reasons are plain constants, `PLACEMENT` and `CANCELLATION`.
5. **New module `shop/orders/cancellation.py`** with `cancel_order(order_id)`. It follows the placement pattern: module-level function, `get_order`, then catalog and emails.
6. **Two new email templates:** `order_cancelled` (includes the refund amount) and `order_cancel_refund_failed` (support will follow up). Amounts are formatted from cents, e.g. `18.00`.
7. **Error type:** `cancellation.CancellationError(ValueError)` with a clear message such as `"order 3 is shipped and can no longer be cancelled"`. Callers that already catch `ValueError`, like `reserve`, keep working.

## Order of operations inside `cancel_order(order_id)`

1. Load the order. If it is already `cancelled` and `refund_ref` is set, return it unchanged. No second refund, no second email, no second restock (AC3).
2. If the status is not `placed` (`shipped`, `delivered`), raise `CancellationError` before any side effect (AC1).
3. Call `payments.refund(order.payment_ref, order.total_cents)`.
   - **Success:** set `refund_ref` and `refund_cents`, set `status = "cancelled"`, restock every line with reason `cancellation`, then send `order_cancelled` with the refund amount (AC2, 3, 4, 5).
   - **`RefundError`:** send `order_cancel_refund_failed` and do not record a refund. Whether the order and stock change in this case is open question 1 below.
4. Charge and refund are never called twice for the same order, because a recorded `refund_ref` short-circuits step 1.

## Task breakdown (TDD, one commit each)

1. **Model:** add the `cancelled` status, `refund_ref` and `refund_cents`.
2. **Payments:** add `refund()` and `RefundError`. Tests: returns a reference derived from the payment ref, and a failure raises.
3. **Catalog:** add `restock()`, the movement log and `stock_history()`. Make `reserve` record movements with a default reason. Tests: restock adds stock, history shows placement then cancellation, and `reserve` still raises when short. Update `place_order` to pass `reason=PLACEMENT, order_id=...`. That needs the order id before reserving, so it is a small reorder in `place_order`.
4. **Emails:** add the two templates and an amount formatter. Tests cover the rendered text.
5. **Cancellation:** `cancel_order` as above.
6. **Tests in `tests/test_cancellation.py`**, one or more per acceptance criterion:
   - AC1: `placed` cancels. `shipped` and `delivered` raise `CancellationError` with a clear message, and nothing is refunded, restocked or emailed.
   - AC2: `refund` is called with the order's `payment_ref` and the full `total_cents`.
   - AC3: `refund_ref` and `refund_cents` are stored. A second `cancel_order` does not refund again, which I check by counting calls with a patched `payments.refund`.
   - AC4: a multi-line order returns each SKU's quantity to stock.
   - AC5: the success email contains the refund amount. When the refund fails, the failure email is sent instead, and the success email is not.
   - AC6: `stock_history("mug")` shows `placement` followed by `cancellation` with the order id.
   - AC7: every failure path above has a test. I would also add a refund-failure test that checks the order is not marked refunded, and a test for an unknown order id.
7. **README:** one line on cancellation, if you want it.

I would check the whole thing with `python -m unittest discover -s tests` and, as a sanity check, break the code on purpose (skip the idempotency check, skip the restock, swap the email template) to confirm the tests fail.

## Size and PR shape

This is about 6 files touched plus 1 new module and 1 new test file. I'd ship it as one PR. If you'd rather keep review small, the natural split is two PRs. PR 1 is the catalog stock history, `restock` and `place_order` passing a reason (AC6, no behavior change for customers). PR 2 is payments `refund`, the model fields, emails and `cancel_order` (AC1 to AC5).

## Open questions for the dev (human gate, no pre-supplied answer, so I'm stopping here)

1. **Refund failure: what happens to the order and the stock?** My default: the order is NOT cancelled, stock is NOT restored, the support email is sent, and the order stays `placed` so it can be retried. The alternative is to mark it `cancelled` (or a new `refund_failed`) and restock, which leaves support to refund by hand. The ticket only says "a refund failure sends a different email telling them support will follow up", so it does not decide this.
2. **Should a failed refund raise to the caller, or return quietly?** My default: return the unchanged order and let the email carry the news. The alternative is to raise `RefundError` after sending the email.
3. **Is the one-PR shape OK, or do you want the two-PR split above?**
4. **Is `cancelled` as a new status value OK?** I'm assuming nothing else switches on status values.

Reply with answers to 1 to 4, or "go with your defaults", and I'll start with task 1.
