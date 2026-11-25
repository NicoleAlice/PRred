I stopped before planning SHOP-340 because this repo requires an approved issue before a feature PR, and I don't know whether one exists. I changed nothing in the repo.

## What I checked

- `CONTRIBUTING.md`, section Process: "Bug fixes under 50 lines may be sent directly. Feature pull requests need an approved issue first: open an issue, wait for a maintainer to label it `approved`, and link it from the pull request."
- `.pr-ready/profile.md` records the same rule as `prior_approval: required`.
- SHOP-340 is a feature: it adds a new order option and fee, and it is more than 50 lines once tests are included. The bug-fix exception doesn't apply.
- The ticket and your message don't mention a GitHub issue carrying the `approved` label. The prompt has no `dev answers:` line for this gate.

## Question for you

Does SHOP-340 have a GitHub issue that a maintainer has labelled `approved`? If so, what is its number or link? I'll need it to link from the PR.

- If it does, tell me the issue and I'll plan the build.
- If it doesn't, the next step is to open an issue for the gift wrap option and wait for a maintainer to add the `approved` label. I shouldn't start a feature branch or PR until then.

## Where the work would go

This is what I found in the code, not a plan. I'll write the plan once the gate is cleared.

- The `Order` dataclass (`shop/orders/models.py`) would get a `gift_wrap` flag, default false.
- `place_order` (`shop/orders/placement.py`) is where the 500-cent fee and the email context would be handled.
- The `order_placed` template (`shop/notifications/emails.py`) is where the confirmation text would change.
- The existing test file is `tests/test_placement.py`. The test command is `python -m unittest discover -s tests`.
- The diff should be small, well under the 500-line budget in the profile.
