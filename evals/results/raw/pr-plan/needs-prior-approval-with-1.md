I stopped before planning SHOP-340 because the project requires prior approval for feature changes like this one.

The rule: "Feature pull requests need an approved issue first" (CONTRIBUTING.md, section Process). The full text there reads: "Bug fixes under 50 lines may be sent directly. Feature pull requests need an approved issue first: open an issue, wait for a maintainer to label it `approved`, and link it from the pull request." The profile (`.pr-ready/profile.md`) records this as `prior_approval: required`.

What I checked and did not find:
- The ticket text (SHOP-340) has no linked issue, discussion, `approved` label or approval reference.
- Your request names no issue or approval link either.
- The exemption does not apply. Gift wrapping is a new feature, not a bug fix under 50 lines.

What to do next: open the issue the rule names and wait for a maintainer to label it `approved`. If an approved issue already exists, share its link. Then run `pr-plan` again.

I made no PR split, sizes or implementation steps, and I changed nothing in the repo.
