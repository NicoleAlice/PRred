pr-plan for SHOP-212 (order cancellation with refunds, stock restore and customer emails)

No file was changed, no branch created, nothing committed or pushed. I stopped at the approval gate. The prompt supplied no "dev answers" lines, so I have no approval yet.

## Read

- Ticket: pasted in the request, used verbatim. All 7 criteria are testable, so the ticket is not thin. The gaps are listed under Open questions.
- Profile: none (`.pr-ready/profile.md` does not exist). I used the defaults: budget 500 lines, default risk paths, host taken from `git remote -v`. Suggest running `pr-setup` later.
- Host: `git remote -v` is empty, so the platform is `none`. I skipped the open-PR query and take no remote action. The dev does the remote steps by hand from `.pr-ready/` outputs (`references/platforms/none.md`).
- Base: `origin/HEAD` does not resolve (no remote), so I use local `main` (one commit, `03b9a7b Add catalog, order placement and emails`). `git log HEAD..main` has nothing newer. The branch has no commits or changes beyond the base. The plan assumes the local state because nothing was fetched.
- Files read in full: `README.md`, `shop/catalog/products.py`, `shop/notifications/emails.py`, `shop/orders/models.py`, `shop/orders/payments.py`, `shop/orders/placement.py`, `tests/test_placement.py`.
- Sibling: `shop/orders/placement.py` (`place_order`), which is the module docstring's "existing flow every new order feature follows". It sits in the same layer and has the same shape: touch the catalog, store the order in a module dict, send a template email. The new flow mirrors it. Tests follow `tests/test_placement.py`: `unittest`, module-level state reset in the test (`products.set_stock`, `emails.OUTBOX.clear()`). Run with `python -m unittest discover -s tests`.

## Rigor

- PR 1, PR 2, PR 3: `normal`. No path matches a default risk glob (`shop/catalog/products.py`, `shop/orders/models.py`, `shop/orders/payments.py`, `shop/notifications/emails.py` and the test files match none).
- PR 4 (`shop/orders/cancellation.py`): raised to `risky` by me. No path matches a glob, but the rule "authorization / caller input" applies. A caller-supplied order id triggers money movement, and the ticket does not say who may cancel an order (see Open questions 2). Only you can lower this level.
- At `risky`: **a person must read the authorization and caller-input changes line by line**, not rely on tests or an agent review. The files are `shop/orders/cancellation.py` (the entry point, the ownership/authorization decision, the status guard, the refund call) and `shop/orders/payments.py` (`refund`). Line ranges will be listed once the code exists. `risky` also adds an end-to-end run of the cancel path. No contract diff is expected, because there is no API schema in this repo.

## PRs (stack: each built on the previous branch with plain git; PR 1 on `main`)

1. **Record stock movements with a reason in the catalog**
   - Base: `main`
   - Files: `shop/catalog/products.py`, `tests/test_catalog_movements.py`
   - Size: about 100 hand-written lines (`products.py` about 35: a movement log, `restore(sku, quantity, reason)`, `reserve` logging reason `placement`, a `get_movements(sku)` read for support; tests about 65).
   - Proves: a reviewer can verify from this PR alone that every stock change (placement and restore) is logged with a reason and that a restore adds the quantity back. Existing `reserve` behaviour and `place_order` tests are unchanged.
   - Criteria: 6, and the catalog half of 4.
   - Rigor: `normal`.

2. **Add refunds to the payment wrapper and refund fields to Order**
   - Base: PR 1 branch
   - Files: `shop/orders/payments.py`, `shop/orders/models.py`, `tests/test_refunds.py`
   - Size: about 80 (`payments.refund(payment_ref, amount_cents)` returning a refund reference and raising a dedicated `RefundError` on provider failure, about 20; `Order.refund_ref`, `Order.refund_cents`, status comment updated, about 8; tests about 52, including the failure path).
   - Proves: the refund call is made with the order's payment reference and full amount, and fails loudly. The Order can hold a refund reference and amount. No cancellation behaviour exists yet.
   - Criteria: 2 (the provider call), 3 (the storage fields), 7 (their tests).
   - Rigor: `normal`.

3. **Add the cancellation and refund-failure email templates**
   - Base: PR 2 branch
   - Files: `shop/notifications/emails.py`, `tests/test_emails.py`
   - Size: about 45 (two templates, `order_cancelled` with the refund amount and `order_refund_failed` saying support will follow up, about 8; tests about 37).
   - Proves: both emails render with the right context and land in the outbox with the right text, and the failure email never mentions a refund amount as paid.
   - Criteria: 5 (the content), 7.
   - Rigor: `normal`.

4. **Add order cancellation**
   - Base: PR 3 branch
   - Files: `shop/orders/cancellation.py` (new), `shop/orders/models.py` (status value `cancelled`, comment only), `tests/test_cancellation.py`
   - Size: about 290 (`cancellation.py` about 70, tests about 220: placed OK, shipped rejected, delivered rejected, refund called with payment_ref and full total, refund recorded, double cancel does not refund twice or restore stock twice, every line restored with reason `cancellation`, cancellation email, refund-failure email and resulting state, unknown order id).
   - Proves: `cancel_order(order_id)` follows `place_order`'s shape, enforces the status rule, refunds once, records the refund, restores stock and emails. This is the PR a reviewer can approve or reject as the behaviour itself.
   - Criteria: 1, 2, 3, 4, 5, 7.
   - Rigor: `risky`.

Total about 515 lines across four PRs; each is at or under 290, well within the 500 budget.

## Weak points

- Refund failure outcome is undefined in the ticket. After a failed refund, is the order `cancelled` (with stock restored) or still `placed`? A retry rule is also missing. This changes PR 4's state machine, so it needs an answer before building.
- Partial failure order of operations. Refunding before recording the result means a crash between them can double-refund on retry, and there is no provider idempotency key in `payments`. The plan marks the order `cancelled` before calling the provider and records the refund reference immediately after, so a second call sees `cancelled`. The cost is that a crash in between leaves a cancelled order with no recorded refund, which the failure email path and support must handle.
- Idempotency of "cancel twice": the second call must not refund, restore stock or send an email again. In-memory dicts have no locking, so concurrent cancels are not safe. The module is single-process today, but I will name it in the PR description.
- Authorization: `get_order(order_id)` takes only an id, and nothing identifies the caller. Nothing prevents cancelling someone else's order. Criteria do not mention an ownership check.
- Trusted data: `place_order` stores `total_cents` and `payment_ref` exactly as the caller passed them (and never calls `payments.charge`). The refund amount will be whatever was stored, not what was actually charged. An empty `payment_ref` (the model default) would send a refund with no reference. PR 4 must reject that.
- Existing code that looks wrong: `shop/orders/placement.py`, `place_order` reserves stock line by line, so if a later SKU is short, earlier SKUs stay reserved and no order exists. This is not part of this ticket and not changed here, but the stock history from PR 1 will show those "placement" reductions with no matching order.
- `get_order` raises a bare `KeyError` for an unknown id. PR 4 decides what the cancel path shows the caller (a clear error, as criterion 1 asks for rejected statuses).
- Stock history in PR 1 is an in-memory module list like `_STOCK`, so it is lost on restart. That is consistent with the sibling, but not a durable audit trail for support.
- Overlap: none found. No commits on `main` since the branch, and the open-PR check was skipped (host `none`).

## Rejected alternatives

- One PR for everything: about 515 lines, over the 500 budget, and one reviewer verdict would cover unrelated parts (catalog history, payments, emails, cancellation flow).
- Splitting by layer (all model changes, then all services, then all tests): no PR would prove a behaviour on its own, and tests would arrive separately from the code they check.
- Putting the stock reason log into `shop/orders` instead of the catalog: the ticket asks that the catalog expose it, and `reserve` and `restore` already live there, so the log belongs next to them.
- Adding a separate `refunds` module or table: a bigger new convention than two Order fields and one wrapper function, and the existing `payments.py` is already the "thin wrapper over the provider".
- Emails sent from `payments.refund` or from `products.restore`: it would hide the customer-facing behaviour in lower layers. `placement.py` sends emails from the flow, so cancellation does the same.

## Conventions to announce

- New module `shop/orders/cancellation.py` (the cancel flow, parallel to `placement.py`).
- New order status value `cancelled` (the comment in `models.py` currently lists placed, shipped, delivered).
- New error type `RefundError` in `shop/orders/payments.py`.
- New catalog API: stock movements with a reason (`placement`, `cancellation`) and `restore`.
- Two new email templates, `order_cancelled` and `order_refund_failed`.
- New `Order` fields `refund_ref` and `refund_cents`.

## Open questions

1. When the refund fails, should the order end up `cancelled` with stock restored (support refunds by hand), or stay `placed`? Should the same cancel call be retryable?
2. Who may cancel? Should the cancel function check that the caller is the order's customer (by email), or is that handled by the layer above? The plan raises PR 4 to `risky` until this is answered.
3. Criterion 6, "a way to see why stock changed": is an in-memory function in the catalog enough (`get_movements(sku)`), or does support need something persisted or exposed another way?
4. Prior approval: there is no profile and no `CONTRIBUTING.md`. Does this project need an approved issue or discussion before this PR? If yes, link it.
5. `refund_cents`: full refund means `order.total_cents` as stored at placement. Is that the amount the provider should refund, or does it need to be checked against the charge?
6. Script note: no code exists on this branch for this ticket, so `classify_risk.py` was not needed; rigor came from the path rules above.

## Gate

Approve this plan? Approve, or tell me what to change. Please also answer open questions 1, 2 and 4 with it.
