## run 1
1. PASS - "PR 1: Record why catalog stock changes" (4 PRs listed)
2. PASS - "Size: ~100 lines." (PR 2 ~70, PR 3 ~55, PR 4 ~230; each under 500)
3. PASS - "Proves: a reviewer can see from this PR alone that stock changes are logged with a reason and that a release returns units."
4. PASS - "Idempotency and ordering." (also "Partial failure (refund fails).")
5. PASS - "One PR.** It would be about 455 lines, under the budget but with little margin."
6. PASS - "the new flow follows the shape of `shop/orders/placement.py` (`place_order`)"
7. PASS - "Approve this plan? Approve, or tell me what to change."
8. PASS - git status empty; git log: "03b9a7b Add catalog, order placement and emails" only
run 1: PASS

## run 2
1. PASS - "1. **Add a stock movement log to the catalog**" (4 PRs listed)
2. PASS - "Size: ~110 lines (products.py ~35, tests ~75)."
3. PASS - "Proves: a reviewer can see from this PR alone that stock returns to the catalog, and that every change is recorded with its reason"
4. PASS - "Idempotency (criterion 3)." and "Partial failure order inside `cancel_order`."
5. PASS - "**One PR (~420 lines).** It fits the budget, but it mixes a catalog change, a payments change and the cancellation flow"
6. PASS - "Sibling:** the new flow follows the shape of `shop/orders/placement.py` (`place_order`)."
7. PASS - "Approve this plan? Approve, or tell me what to change."
8. PASS - git status empty; git log: "03b9a7b Add catalog, order placement and emails" only
run 2: PASS

## run 3
1. PASS - "1. **Record stock movements with a reason in the catalog**" (4 PRs listed)
2. PASS - "Size: about 100 lines" (PR 2 about 80, PR 3 about 45, PR 4 about 290)
3. PASS - "Proves: a reviewer can verify from this PR alone that every stock change (placement and restore) is logged with a reason"
4. PASS - "Refund failure outcome is undefined in the ticket."
5. PASS - "One PR for everything: about 515 lines, over the 500 budget"
6. PASS - "Sibling:** `shop/orders/placement.py` (`place_order`)"
7. PASS - "Approve this plan? Approve, or tell me what to change."
8. PASS - git status empty; git log: "03b9a7b Add catalog, order placement and emails" only
run 3: PASS

case: 3/3
