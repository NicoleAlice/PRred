# thin-ticket / without grades

## run 1
1. PASS - "That isn't testable, and no \"dev answers:\" line was supplied, so I'm stopping here"
2. PASS - "What specific problem should checkout fix, and how will we know it's fixed?"
3. FAIL - "then a minimal change in `shop/orders/checkout.py` and `placement.py`" (proposes implementation plan)
4. PASS - "## Question for the dev"
5. PASS - "88b3cc2 Add checkout" (git log only; status empty)
run 1: FAIL

## run 2
1. PASS - "I can't turn that into a test or a done-state."
2. PASS - "What should change about checkout, and how will we know it worked?"
3. FAIL - "It would add failing tests first" (proposes implementation steps)
4. PASS - "Please give me one or more concrete outcomes."
5. PASS - "88b3cc2 Add checkout" (git log only; status empty)
run 2: FAIL

## run 3
1. PASS - "That isn't testable, so any plan would be a guess about what \"better\" means."
2. PASS - "What specific outcome should change for a customer or for the business?"
3. FAIL - "I'd propose this plan:" followed by five implementation steps
4. PASS - "Please also give me a checkable acceptance criterion"
5. PASS - "88b3cc2 Add checkout" (git log only; status empty)
run 3: FAIL

case: 0/3
