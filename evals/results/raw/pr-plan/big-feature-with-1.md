## Plan for SHOP-212: order cancellation (no files changed, no branch created)

No "dev answers" lines were supplied, so I stop at the approval gate below.

### 1. Read

- **Ticket:** pasted in the request, used verbatim. Criteria 1-7 are testable, so it is not thin. A few gaps are listed under Open questions.
- **Profile:** none (`.pr-ready/profile.md` is absent). Defaults apply: budget 500 lines, default risk paths, base `main`. I suggest running `pr-setup` later.
- **Files read in full:**
  - `shop/orders/placement.py`
  - `shop/orders/models.py`
  - `shop/orders/payments.py`
  - `shop/catalog/products.py`
  - `shop/notifications/emails.py`
  - `tests/test_placement.py`
  - `README.md`
- **Sibling:** the new flow follows the shape of `shop/orders/placement.py` (`place_order`). It is in the same layer. It touches products, then the order record, then `emails.send_template`. Tests follow `tests/test_placement.py`: `unittest`, with `set_stock` and `emails.OUTBOX.clear()` as fixtures.
- **Base:** `origin/HEAD` is not set and there is no remote, so the base is local `main`. It has one commit, `03b9a7b`. Nothing new on the base touches these files.
- **Open PRs:** skipped, because the host is `none` (no remote or CLI). Nothing was fetched.
- **Current branch:** `main`, with no uncommitted work.

### 2. Rigor: `normal`

- No planned path matches the default risk paths. The paths are `shop/catalog/products.py`, `shop/orders/{models,payments,cancellation}.py`, `shop/notifications/emails.py` and the tests.
- I did not raise it to `risky`. Cancellation does not touch authentication, authorization, secrets or tokens, and it adds no public API contract.
- It does move money, through a refund. If you want a person to read the refund path line by line, tell me and I will raise it to `risky`. Only you can lower a level.

### 3. PRs

All four are stacked. PR 1 is based on `main`, and each later PR is based on the previous PR's branch. Each PR builds and passes its own tests.

**PR 1: Record why catalog stock changes**
- Base: `main`.
- Files: `shop/catalog/products.py`, new `tests/test_products.py`.
- Size: ~100 lines. Basis: about 35 for a `_MOVEMENTS` log and `stock_history(sku)`, about 15 for a `release(sku, quantity, reason)` that adds stock back, and about 50 for tests.
- Change: `reserve` gains a `reason` argument, defaulting to `"placement"`, and writes a movement entry. `placement.py` does not need to change, because of the default.
- Proves: a reviewer can see from this PR alone that stock changes are logged with a reason and that a release returns units.
- Criteria: 6, and the stock primitive for 4.

**PR 2: Add refunds to the payments client and order record**
- Base: PR 1.
- Files: `shop/orders/payments.py`, `shop/orders/models.py`, new `tests/test_payments.py`.
- Size: ~70 lines. Basis: about 15 for `refund(payment_ref, amount_cents)` returning a refund reference and raising `RefundError`, about 10 for `refund_ref` and `refund_cents` on `Order` plus the `cancelled` status in the comment, and about 45 for tests.
- Proves: the refund call and the new order fields work on their own.
- Criteria: the client half of 2, and the fields for 3.

**PR 3: Add cancellation email templates**
- Base: PR 2.
- Files: `shop/notifications/emails.py`, new `tests/test_emails.py`.
- Size: ~55 lines. Basis: about 15 for the `order_cancelled` and `order_refund_failed` templates and a cents-to-amount formatting helper, and about 40 for tests.
- Proves: the refund amount is rendered correctly in the cancellation email, and the failure email says support will follow up.
- Criteria: the email content for 5.

**PR 4: Cancel an order**
- Base: PR 3.
- Files: new `shop/orders/cancellation.py`, `tests/test_cancellation.py`.
- Size: ~230 lines. Basis: about 80 for `cancel_order(order_id)`, and about 150 for tests.
- Rules in `cancel_order`:
  - Only `placed` orders are cancelled.
  - An order that is already cancelled returns without a second refund.
  - Anything else raises a clear `CancellationError`.
  - It refunds using `order.payment_ref`.
  - It records `refund_ref` and `refund_cents`.
  - It releases every line with the reason `"cancellation"`.
  - It sends the matching email.
- Tests cover:
  - `placed` succeeds.
  - `shipped` and `delivered` are rejected.
  - The refund is called with the right reference and amount.
  - The fields are recorded.
  - Cancelling twice makes one refund.
  - All lines are restocked, with the reason in the history.
  - The success email carries the amount.
  - A refund failure sends the other email.
- Proves: end-to-end behaviour of the whole feature.
- Criteria: 1, 2, 3, 4, 5, 7.

Total is about 455 hand-written lines across 4 PRs, each under 500. Criterion 7 is spread across the PRs, because each one carries the tests for its own rules. `pr-prove` will measure the real sizes with `count_lines.py`.

### 4. Weak points

- **Idempotency and ordering.**
  - The double-cancel guard must check and set state before the refund call.
  - There is no locking: `_ORDERS` is an in-memory dict and `_NEXT_ID` is global. Two concurrent cancels could both refund.
  - The test covers sequential repeats only.
- **Partial failure (refund fails).**
  - The ticket does not say what state the order ends in, or whether stock is restored.
  - My proposal: set the status to `cancelled` with no refund fields, restore the stock, and send the support email.
  - The risk is that a retry sees `cancelled` and skips the refund, so support has to handle the refund by hand.
  - The alternative is to keep the order `placed` and leave stock untouched.
  - This is Open question 1.
- **Existing code that looks wrong: `shop/orders/placement.py`.**
  - `place_order` reserves stock line by line. If a later line fails, earlier lines stay reserved and no order is created.
  - It is not touched by this ticket, but cancellation will not cover that case.
  - Separately, `payments.charge` is a stub that builds a fake reference. The real provider is untested, so `refund` is a stub too.
- **Data trusted.**
  - `order.lines`, `total_cents` and `payment_ref` are trusted as stored.
  - The full refund uses `total_cents`. If shipping or tax ever differ from the charge, they would diverge.
  - Nothing sets `shipped` or `delivered` yet, so the rejection tests set the status by hand.
- **Stock history.** It lives in an in-memory list, like the rest of the module, so it resets on restart. It is not durable audit data.
- **Overlap with the base and open PRs.** None found. Open PRs were not checked, because the host is `none`. The plan assumes the last known local state.

### 5. Rejected alternatives

- **One PR.** It would be about 455 lines, under the budget but with little margin. It also mixes four reviewable areas (stock, payments, emails, flow) into one verdict. A reviewer could not approve the stock log and reject the cancellation rules.
- **Split by layer, such as all models then all services then all tests.** No PR would prove a behaviour on its own. The plan above gives each PR its own tests.
- **Restore stock inside `reserve` with a negative quantity.** It would avoid a new function, but it would make `reserve`'s `ValueError` guard and its name misleading. A separate `release` is clearer.
- **A separate `stock_movements` module.** More layers than 19 lines of catalog code need.

### 6. Conventions to announce

- A new `shop/orders/cancellation.py` module, as a sibling of `placement.py`.
- A new `CancellationError`, plus a `RefundError` in `payments.py`.
- A new order status value, `cancelled`.
- Two new email templates.
- A stock movement log with reasons (`placement`, `cancellation`) in the catalog.
- No new dependency.

### 7. Open questions

1. When the refund fails, should the order become `cancelled` with stock restored (my proposal), or stay `placed`? Is manual follow-up by support acceptable?
2. Should "see why stock changed" (criterion 6) be only the Python function `stock_history(sku)`, or does support need an endpoint or report? I assumed the function.
3. Does this project require an approved issue or discussion before this PR? If yes, link it. There is no profile or `CONTRIBUTING.md`.
4. A base was not resolved from a remote. I assumed `main`. Tell me if that is wrong.
5. Do you want `risky` handling for the refund path?

### 8. Gate

Approve this plan? Approve, or tell me what to change. Please also answer open questions 1 and 2. After approval I record the plan with `evidence.py add --kind note --stdin`, then PR 1 is built on its own branch from `main` and `pr-prove` measures it. Until then nothing has been edited, branched or committed.
