(Saved by the controller: the run returned its report as its final message instead of writing this file.)

**The ticket is too thin to plan.** SHOP-301's only acceptance criterion is "It should be better." That names no observable behaviour, no part of the system and no definition of done.

I stopped at the thin-ticket check, so there is no PR split, no sizes and no implementation steps. I made no edits and took no remote actions. There is no `.pr-ready/profile.md`, so defaults would apply once the ticket is plannable.

**What's missing:**

1. What is wrong with checkout today? Is there a bug report, a customer complaint, a support ticket or a metric (conversion, drop-off, error rate, latency)?
2. What measurable outcome means done? For example, "the order confirmation arrives within N seconds" or "failed payments show a specific message".
3. Which part of checkout does this cover? `shop/orders/checkout.py` `checkout()` does four things in sequence:
   - It totals the cart.
   - It charges the payment.
   - It reserves stock and creates the order.
   - It sends the "order_placed" email.

   Is the problem in one of these, in the UI or API in front of it, or in something that doesn't exist yet?
4. What should happen in error and edge cases? Examples are:
   - the payment succeeds but stock reservation fails
   - an empty cart
   - a repeated submit of the same cart
   - an invalid email
5. What is explicitly out of scope, such as new payment methods, a redesign of the flow or notifications?
6. Who decides when "better" is achieved: the ticket author, product or the dev? Is there an approver for the acceptance?

Can you answer these, or take them back to the ticket author? I'll plan once the criteria are testable.
