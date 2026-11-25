(Saved by the controller: the run returned its report as its final message instead of writing this file.)

The ticket is too thin to plan. Its only acceptance criterion is "It should be better", which names no behaviour, no part of the system and no definition of done.

**What's missing:**

1. What is wrong with checkout today? Is there a symptom, a user report, a support ticket or a metric (conversion, drop-off, error rate, latency) behind this?
2. What measurable outcome means done? For example a number, a behaviour a tester could check, or an error that no longer happens.
3. Which part of checkout does this cover? In the code, `shop/orders/checkout.py` `checkout()` computes the total, calls `payments.charge`, then calls `placement.place_order`. That reserves stock, creates the order and sends the `order_placed` email. Is the problem in one of these, or in something not in this repo (a UI, cart, shipping or address step)?
4. Which error and edge cases matter? Examples are payment failure, a stock reservation failing after the customer has been charged, an empty cart, repeated submits, or an invalid email.
5. What is out of scope? For example payment provider changes, new payment methods, the catalog, or the notification emails.
6. Who decides when it is right (product owner, designer, the ticket author), and what will they look at to accept it?

Can you answer these, or take them back to the ticket author? I'll plan once the criteria are testable.

(Nothing was edited, branched or committed. I read only the checkout, placement and payments files to make the questions concrete.)
