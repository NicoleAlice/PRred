SHOP-301 is too thin to plan: its only acceptance criterion, "It should be better.", names no behaviour, no part of the system and no definition of done.

**What's missing:**

1. What is wrong with checkout today? Is there a symptom, a user report, a bug or a metric behind "Improve checkout"?
2. What measurable outcome means done? For example a latency target, a lower failure rate or a specific behaviour that must change.
3. Which part of checkout does this cover? Today `shop/orders/checkout.py::checkout` computes the total, charges via `payments.charge`, then calls `placement.place_order`, which reserves stock, stores the order and sends the "order_placed" email. Is the change in one of those steps, or in the flow as a whole?
4. Which error and edge cases matter? Examples: a payment that fails, stock that can't be reserved after the customer has been charged, an empty cart, a repeated submission.
5. What is out of scope?
6. Who decides when it is right, and how will they check it?

Can you answer these, or take them back to the ticket author? I'll plan once the criteria are testable.
