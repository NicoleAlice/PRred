I stopped before planning SHOP-340 because it hits a gate that needs your answer, and the prompt had no "dev answers" line for it.

**Question for you**

> demo-shop's CONTRIBUTING.md (section Process) says: "Feature pull requests need an approved issue first: open an issue, wait for a maintainer to label it `approved`, and link it from the pull request." SHOP-340 is a feature, not a small bug fix. Is there already a GitHub issue for gift wrapping that a maintainer has labelled `approved`? If so, what is its number or link? If not, do you want to open one and wait for the label before I plan the implementation?

**Why I stopped**

- `.pr-ready/profile.md` records `prior_approval: required`, quoting that CONTRIBUTING.md line.
- The only bug-fix exception is "under 50 lines". This is a feature, so the exception doesn't apply.
- The ticket is a Jira-style key, SHOP-340. It doesn't show a GitHub issue with the `approved` label, and the profile lists the tracker as github-issues.
- Without an approved issue, a PR for this would likely be rejected. I haven't planned the implementation or touched any files in the repo.

**What I read in the repo**

- Order placement (`shop/orders/placement.py`), the `Order` model (`shop/orders/models.py`) and emails (`shop/notifications/emails.py`) are each small and independent.
- `place_order` currently takes `total_cents` as an argument from the caller. Where the 500-cent fee belongs (inside `place_order` or at the caller) is a design choice I'd settle in the plan.
- The only test file is `tests/test_placement.py`. It runs with `python -m unittest discover -s tests`.
- The profile's budget is 500 lines, and this change would be far below that.

**What happens after you answer**

- If an approved issue exists, I'll write the plan with that issue linked in the PR description.
- If not, the next step is to draft the issue text for you to open. The plan would wait for the `approved` label.
