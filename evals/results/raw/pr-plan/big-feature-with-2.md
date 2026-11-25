# Plan for SHOP-212: order cancellation (nothing edited, branched or committed)

## Read

- **Ticket:** pasted in the request, used verbatim. The criteria are buildable, so this is not a thin ticket (gaps are listed as open questions).
- **Profile:** none (`.pr-ready/` does not exist). Defaults apply: budget 500 hand-written lines per PR, default risk paths, host from `git remote -v`. There is no remote, so the platform is `none`. I suggest running `pr-setup` later.
- **Files read in full:**
  - `shop/orders/placement.py`
  - `shop/orders/models.py`
  - `shop/orders/payments.py`
  - `shop/catalog/products.py`
  - `shop/notifications/emails.py`
  - `tests/test_placement.py`
  - `README.md`
- **Sibling:** the new flow follows the shape of `shop/orders/placement.py` (`place_order`). It is the same layer, mutates `products` stock, sends a template through `emails.send_template`, and keeps an in-module registry. Its test is `tests/test_placement.py`, which uses `unittest`, sets stock with `products.set_stock`, and clears `emails.OUTBOX`.
- **Base:** `origin/HEAD` does not resolve (no remote), so I use local `main` (`03b9a7b`). The branch has no commits or changes against it. Nothing on the base since HEAD touches these files.
- **Open PRs:** skipped (host `none`, no CLI).
- **No `CONTRIBUTING.md`** and no policy file.

## Rigor: `normal`

No planned path matches the default risk paths. The planned paths are:
- `shop/catalog/products.py`
- `shop/orders/models.py`
- `shop/orders/payments.py`
- `shop/orders/cancellation.py`
- `shop/notifications/emails.py`
- `tests/*`

I did not raise the level to `risky`. There is no authentication, authorization, secret, token or public contract involved. The money movement goes through the provider wrapper, and the refund reference and amount are stored on the order. If you want refund code to get the `risky` treatment (line-by-line human read plus an end-to-end run), tell me. Only you can lower a level, but anyone may raise it.

## PRs (stacked, built one at a time with plain git)

1. **Add a stock movement log to the catalog**
   - Base: `main`.
   - Files:
     - `shop/catalog/products.py`: add `restock(sku, quantity, reason)`, a `_MOVEMENTS` log, `get_movements(sku)`, and a `reason` param on `reserve` defaulting to `"placement"`.
     - `tests/test_products.py` (new).
   - Size: ~110 lines (products.py ~35, tests ~75).
   - Proves: a reviewer can see from this PR alone that stock returns to the catalog, and that every change is recorded with its reason, quantity and sku, so support can tell placement from cancellation. Existing placement behaviour is unchanged.
   - Covers: criteria 4 (catalog side) and 6, plus unit tests for both.

2. **Add refund support for orders**
   - Base: PR 1's branch (no code dependency on it, but kept in the stack for one linear merge order).
   - Files:
     - `shop/orders/payments.py`: `refund(payment_ref, amount_cents)` returning a refund reference, plus a `PaymentError` raised when the provider fails.
     - `shop/orders/models.py`: `refund_ref`, `refund_cents`, and a `cancelled` status in the status comment.
     - `tests/test_payments.py` (new).
   - Size: ~70 lines (payments ~20, models ~5, tests ~45).
   - Proves: the refund call uses the order's payment reference and returns a reference. The provider failure path raises a typed error, and the order can hold a refund record.
   - Covers: criterion 2 (primitive) and the data side of 3, with tests.

3. **Add order cancellation**
   - Base: PR 2's branch.
   - Files:
     - `shop/orders/cancellation.py` (new): `cancel_order(order_id)`, built like `place_order`.
     - `shop/notifications/emails.py`: templates `order_cancelled` (with refund amount) and `order_cancel_refund_failed` (support will follow up).
     - `tests/test_cancellation.py` (new).
   - Size: ~240 lines (cancellation ~65, emails ~6, tests ~170).
   - Proves: the whole rule set in one place. Only `placed` orders cancel. A full refund is issued once, with the reference and amount recorded. Every line is restocked with reason `"cancellation"`. The right email goes out on success and on refund failure.
   - Covers: criteria 1, 2, 3, 4, 5 and 7. The tests cover the rejection of `shipped` and `delivered`, the double cancel, the refund failure and the stock movement reason.

Estimated total ~420 lines, over three PRs, each within 500 and each passing the tests on its own in order.

## Weak points

- **Partial failure order inside `cancel_order`.** The refund is an external side effect and the stock and status changes are local. I plan: check status, then refund, then (only on success) record the refund and set `cancelled`, then restock, then email. If the refund raises, the order stays `placed` and nothing is restocked. If the process dies after the refund but before the status write, a retry would refund twice. In this in-memory code that window is small, but a real provider needs an idempotency key. I would pass one derived from the order id, which needs your confirmation (see open questions).
- **Idempotency (criterion 3).** "Cancelling twice does not refund twice" is guaranteed by the `cancelled` status check before the refund. The second call's behaviour (raise, or return the order) is not specified.
- **Trusted amount.** The refund amount is `order.total_cents`, which `place_order` stores exactly as the caller passed it. It is never checked against the lines or the charge. If placement was given a wrong total, the refund repeats the error.
- **Existing code that looks wrong: `shop/orders/placement.py`.** `place_order` reserves line by line with no rollback, so if the second SKU is short, the first has already been taken out of stock and no order exists. This is outside the ticket. It affects the movement log: a failed placement leaves "placement" movements with no order. I will not change it in these PRs. I will name it in PR 1's description, or you can ask for a separate ticket.
- **Module-level global state.** Stock, orders, the outbox and the new movement log are module globals that are never reset. The new tests must set their own stock and clear `OUTBOX` and the log (as `test_placement.py` does), or they will depend on test order.
- **`payments.charge` is not called by `place_order`** (the reference is passed in), so no real reference format exists to test against. The refund tests use fabricated references such as `pay_1`.
- **Amount in the email.** Totals are in cents. The template must format them as currency, and the format is not specified.
- **No overlap check possible** with open PRs (skipped). The base has no newer commits on these files.

## Rejected alternatives

- **One PR (~420 lines).** It fits the budget, but it mixes a catalog change, a payments change and the cancellation flow, so a reviewer could not approve the stock log and reject the refund wiring. A single reviewer verdict for unrelated parts.
- **Split by layer** (all models, then all services, then all tests). No PR would prove a behaviour on its own, and tests would land apart from the code they check.
- **Log stock changes inside `place_order` and `cancel_order` instead of in the catalog.** It spreads the audit rule across callers, so any future caller of `reserve` would silently skip it. Keeping it in `products.py` puts it in one place.
- **Delete or flag the order on cancel instead of a `cancelled` status.** It loses the record that support needs, and it makes "cancelling twice" harder to detect.

## Conventions to announce

- A new module `shop/orders/cancellation.py`, following `placement.py`.
- A new order status value, `cancelled`, plus new order fields `refund_ref` and `refund_cents`.
- A new error type, `PaymentError`, in `shop/orders/payments.py`.
- A new catalog stock movement log (`restock`, `get_movements`) and a `reason` argument on `reserve`.
- Two new email templates.

## Open questions

1. **Refund failure, order state:** when the refund fails, should the order stay `placed` (customer can retry), or become `cancelled` with no refund recorded, with stock restored? The ticket only says a different email is sent. This changes the tests and the idempotency rule. My plan assumes it stays `placed`, nothing is restocked, and the failure email is sent.
2. **Second cancel:** should cancelling an already `cancelled` order raise a clear error, or quietly return the order with no new refund and no new email?
3. **"A way to see why stock changed":** is a read function in the catalog (`get_movements(sku)`) enough, or does support need something else (a CLI, an endpoint)? I assume the function.
4. **Prior approval:** does this project need an approved issue or discussion before this PR? If yes, please link it. There is no profile, and I found no `CONTRIBUTING.md` and no approval reference in the ticket.
5. **Provider idempotency:** does the real provider accept an idempotency key on refunds? If yes, I will pass one derived from the order id.
6. **Email amount format:** how should the refund amount appear (for example `18.00 EUR`)? The currency is not in the code.
7. **Rigor:** do you want `risky` for the refund code?
8. **Base and scripts:** no remote, so base is local `main`. I did not run `classify_risk.py` because no code exists on the branch yet; the level comes from the path match above.

**Approve this plan? Approve, or tell me what to change.** Please answer open questions 1 to 4 with it.

---

## Gate record (pre-supplied answers)

No `dev answers:` lines were supplied in the prompt. The approval gate has no pre-supplied answer, so I stopped here as required. No files were changed, no branch was created, nothing was committed, and nothing was recorded with `evidence.py`. That step comes only after approval.

The question I would ask the dev at the gate: "Approve this plan? Approve, or tell me what to change."
