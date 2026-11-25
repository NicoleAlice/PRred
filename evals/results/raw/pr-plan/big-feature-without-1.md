# SHOP-212 plan: order cancellation with refunds, stock restore, emails

I read the whole repo (it is small) and changed nothing. No "dev answers" lines were supplied, and I hit no human gate that needs one. The open questions are at the end, each with the default I would use if you don't answer.

## What exists today

- `shop/orders/models.py`: `Order` dataclass with `id, customer_email, lines{sku: qty}, total_cents, status (placed|shipped|delivered), payment_ref`. It has no refund fields.
- `shop/orders/placement.py`: in-memory `_ORDERS`, `place_order()`, `get_order()`. Placement calls `products.reserve()` for each line, stores the order, then sends the `order_placed` email.
- `shop/orders/payments.py`: only `charge()`. There is no refund function.
- `shop/catalog/products.py`: `_STOCK` dict with `set_stock`, `get_stock`, `reserve`. There is no way to put stock back, and no record of why stock changed.
- `shop/notifications/emails.py`: `TEMPLATES` dict, `OUTBOX` list, `send_template(to, name, context)`.
- `tests/test_placement.py`: one `unittest` test. Run tests with `python -m unittest discover -s tests`.

## Design decisions

1. **New module `shop/orders/cancellation.py`** with `cancel_order(order_id)`. It follows the pattern of `placement.py`. It reads orders through `placement.get_order`, so the order store stays in one place.
2. **Status.** Add `cancelled` to the status comment in `Order`. Only `placed` can be cancelled. `shipped` and `delivered` raise a dedicated `OrderNotCancellable(ValueError)` whose message names the status (AC1). An already-`cancelled` order is an idempotent no-op that returns the order (AC3). It does not raise, it does not refund and it sends no email.
3. **Refund.** Add `payments.refund(payment_ref, amount_cents)` that returns a refund reference, in the same stub style as `charge()`. It raises `PaymentError` on failure. A full refund means `order.total_cents` against `order.payment_ref` (AC2).
4. **Refund record.** Add `refund_ref: str = ""` and `refunded_cents: int = 0` to `Order` (AC3).
5. **Double-cancel safety.** Check the status first. After a successful refund, record the refund fields and set the status to `cancelled` in the same step. A second call then returns early on the `cancelled` status. As a second guard, skip the refund when `refund_ref` is already set.
6. **Refund failure.**
   - The refund call raises, so the order is left in a state that can be retried. It stays `placed` with no refund recorded.
   - Stock is not restored, because the cancel did not complete.
   - The customer gets the `cancellation_refund_failed` email telling them support will follow up (AC5).
   - `cancel_order` returns without raising. I would rather return a result than raise after emailing the customer. See open question 1.
   - A retry is possible because the order is still `placed`.
7. **Stock restore (AC4).** Add `products.restock(sku, quantity, reason)`. On success, call it for every line.
8. **Stock history for support (AC6).**
   - Add an append-only `_STOCK_LOG` in `products.py`, with entries `(sku, delta, reason, ref)`.
   - Add `stock_history(sku=None)` as the read API.
   - `reserve()` gains a `reason` parameter (default `"placement"`) and an optional `ref` (the order id), and it logs every change. `restock` logs `"cancellation"`.
   - Placement passes the order id as `ref`. The order id isn't known until the Order is built, so `place_order` has to be reordered slightly: allocate the id first, then reserve. Keep that edit small and covered by the existing test.
   - Reasons are module constants (`PLACEMENT`, `CANCELLATION`), not free strings.
   - The existing `reserve(sku, qty)` call signature keeps working because the new parameters have defaults.
9. **Emails (AC5).** Add two templates, `order_cancelled` ("Your order #{order_id} was cancelled. We refunded {refund_amount}.") and `order_cancel_refund_failed` ("We could not refund order #{order_id} automatically. Our support team will follow up."). Format the amount from cents in the caller, for example `"%.2f" % (cents / 100)`, because the template only does `str.format`.

## Implementation order (small, reviewable steps; each ends with the test suite green)

1. **Catalog.** Add `restock`, `_STOCK_LOG`, `stock_history`, and the `reason`/`ref` parameters on `reserve`. Update `place_order` to pass the reason. Add catalog tests, including one that checks placement shows up in the history.
2. **Payments and model.** Add `payments.refund` and `PaymentError`, plus the `Order` refund fields and the `cancelled` status.
3. **Emails.** Add the two templates.
4. **Cancellation flow.** Write `cancellation.py` with the rules in design decisions 2, 5, 6 and 7. Write the tests below at the same time, red first.
5. **README.** Add a short "Cancelling an order" note.

## Tests (AC7), in `tests/test_cancellation.py`, plus catalog tests

Test setup: clear the `OUTBOX` and `_ORDERS`, and reset the stock and the log. For failure paths, patch `payments.refund` with `unittest.mock`.

| Rule | Test |
|---|---|
| AC1 | cancelling a `placed` order works; `shipped` and `delivered` each raise `OrderNotCancellable` with the status in the message, and change no stock, refund or email |
| AC2 | `payments.refund` is called once with the order's `payment_ref` and `total_cents` |
| AC3 | `refund_ref` and `refunded_cents` are recorded; a second `cancel_order` makes no second refund call, no second email and no second restock |
| AC4 | a multi-line order gets every line's quantity back; stock equals the pre-order level |
| AC5 | one `order_cancelled` email with the amount; on refund failure, exactly one `order_cancel_refund_failed` email and no `order_cancelled` email |
| AC5 failure state | after a refund failure the order is still `placed`, there is no refund record, and stock is not restored; a retry that succeeds then completes the cancel |
| AC6 | `stock_history` shows the placement entry, then the cancellation entry, with reason and order ref, for the right sku |
| Unknown order id | `cancel_order` for a missing id raises `KeyError`, the same as `get_order` |

I will also run each test against a deliberately broken implementation (for example, drop the status check, drop the already-cancelled guard, skip the restock) to confirm that the test fails when it should.

## Risks and notes

- All state is in-process module globals, so tests must reset them. A small `setUp` helper handles this.
- Refund then restock is not atomic in a real system. With in-memory state the order of steps is enough. A real database would need a transaction, and the plan notes that for later.
- Changing `reserve`'s signature touches the one existing flow. Keeping defaults means no existing caller changes. Only `place_order` is edited, to pass the reason and order id.
- This is one feature with a natural split by layer, but it is small enough (about 5 source files and 2 test files) for a single PR if you want one. If you prefer smaller PRs, the split is step 1 (catalog history and restock) followed by steps 2 to 5.

## Open questions for you (defaults noted)

1. On a refund failure, should `cancel_order` return a result and stay quiet, or also raise so the caller sees the failure? Default: return a result object with `status="refund_failed"`, and no raise.
2. If the refund fails, should the order stay `placed` (retryable) or move to a `cancel_failed` state for support to handle? Default: stay `placed`.
3. Do you want to ship this as one PR or as two? Default: one PR.
