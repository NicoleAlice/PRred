I stopped before planning SHOP-340 because this project requires prior approval for feature changes, and I found none.

**The rule:** "Feature pull requests need an approved issue first" (CONTRIBUTING.md, section Process). The same section says: "open an issue, wait for a maintainer to label it `approved`, and link it from the pull request." The profile (`.pr-ready/profile.md`) has `prior_approval: required`, and CONTRIBUTING.md says the same.

**Exemption:** the only exemption is "Bug fixes under 50 lines". A gift wrap option with a new flag, a fee and email text is a feature, so it does not apply.

**What I checked and did not find:**
- The ticket text (SHOP-340) has no linked issue, discussion or `approved` label.
- Your request has no approval reference either.
- No issue is named, so there was nothing to look up through the host CLI.

**What to do next:**
1. Open an issue for the gift wrap feature (or share the link if one exists), and wait for a maintainer to label it `approved`.
2. Run `pr-plan` again with the issue link, and I'll plan it then.

I have not made a PR split, sizes or implementation steps, and I have not changed any files, branches or commits.
