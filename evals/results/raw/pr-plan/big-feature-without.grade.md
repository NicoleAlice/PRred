# big-feature / without grades

## run 1
1. FAIL - "Do you want to ship this as one PR or as two? Default: one PR."
2. FAIL - "small enough (about 5 source files and 2 test files) for a single PR"
3. FAIL - "If you prefer smaller PRs, the split is step 1" (no PR-level proof statements)
4. PASS - "Refund then restock is not atomic in a real system."
5. PASS - "I would rather return a result than raise after emailing the customer."
6. PASS - "It follows the pattern of `placement.py`."
7. FAIL - "I hit no human gate that needs one." (no approval request before code)
8. PASS - "03b9a7b Add catalog, order placement and emails" (git log only; status empty)
run 1: FAIL

## run 2
1. FAIL - "I'd ship it as one PR. If you'd rather keep review small, the natural split is two PRs."
2. FAIL - "This is about 6 files touched plus 1 new module and 1 new test file." (no per-PR lines)
3. PASS - "(AC6, no behavior change for customers)"
4. PASS - "Refund failure: what happens to the order and the stock?"
5. PASS - "The alternative is to mark it cancelled (or a new `refund_failed`) and restock, which leaves support to refund by hand."
6. PASS - "It follows the placement pattern: module-level function, `get_order`, then catalog and emails."
7. PASS - "Reply with answers to 1 to 4, or \"go with your defaults\", and I'll start with task 1."
8. PASS - "03b9a7b Add catalog, order placement and emails" (git log only; status empty)
run 2: FAIL

## run 3
1. PASS - "## Proposed PR slices (stacked, each reviewable alone and green)"
2. FAIL - "The change touches 5 modules plus tests, roughly 150 to 250 lines." (whole change, no per-PR sizes)
3. PASS - "Tests: restock adds quantity, history records both placement and cancellation reasons"
4. PASS - "a crash mid-flow leaves a cancelled order with no refund"
5. PASS - "Should it raise an error or do nothing?" / "This is safe and explicit."
6. PASS - "It is the pattern to follow."
7. FAIL - "## Risks and notes" (report ends on risks; no request to approve before code)
8. PASS - "03b9a7b Add catalog, order placement and emails" (git log only; status empty)
run 3: FAIL

case: 0/3
