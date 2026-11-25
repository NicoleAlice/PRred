I stopped before planning SHOP-340 because this repo requires prior approval for feature PRs, and I don't know whether the ticket has it. I changed nothing in the repo.

**Why I stopped**

This is a feature, so the rule applies. `.pr-ready/profile.md` has `prior_approval: required`, citing CONTRIBUTING.md, section Process: "Feature pull requests need an approved issue first". CONTRIBUTING.md adds: "open an issue, wait for a maintainer to label it `approved`, and link it from the pull request."

Bug fixes under 50 lines are exempt. Gift wrapping is a new feature that touches the model, pricing and email, so the exemption doesn't apply.

The ticket doesn't say whether an approved issue exists, and the prompt contained no `dev answers:` line for this gate. I can't assume it's approved, so I'm not going further.

**Question for you**

> CONTRIBUTING.md says feature PRs need an issue that a maintainer has labelled `approved`, and the PR must link it. Does SHOP-340 have an approved GitHub issue? If so, what's its number or link? If not, should I draft the issue text for you to open, and hold off on planning until a maintainer approves it?

**What I'll do once you answer**

- If the issue is approved, I'll write the full plan and link the issue in the PR plan.
- If it isn't, I'll draft the issue and wait for the `approved` label before planning the PR.

**What I found in the repo**

- `shop/orders/models.py`: the `Order` dataclass has no `gift_wrap` field.
- `shop/orders/placement.py`: `place_order(customer_email, lines, total_cents, payment_ref)` takes the total from the caller. The 500-cent fee will need a decision on where it gets added.
- `shop/notifications/emails.py`: there is one template, `order_placed`, so the email text would change there.
- `tests/test_placement.py`: has one test. Run the suite with `python -m unittest discover -s tests`.
- Budget is `max_lines: 500`, which this change should stay well under.
