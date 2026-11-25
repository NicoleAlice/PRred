I stopped before planning because this project requires prior approval for feature changes, and I found none for SHOP-340.

**The rule:** "Feature pull requests need an approved issue first" (CONTRIBUTING.md, section Process). The full text there reads: "Bug fixes under 50 lines may be sent directly. Feature pull requests need an approved issue first: open an issue, wait for a maintainer to label it `approved`, and link it from the pull request." The profile (`.pr-ready/profile.md`) records the same rule as `prior_approval: required`.

**What I checked and did not find:**
- The ticket text you pasted (SHOP-340) has no linked GitHub issue, discussion, `approved` label or other approval reference.
- Your request names no issue or approval either.
- The exemption does not apply. Gift wrapping is a new feature, not a bug fix under 50 lines.

**What to do next:** open a GitHub issue for the gift wrapping option, wait for a maintainer to label it `approved`, and then run `pr-plan` again with the issue link. If an approved issue already exists, share its link and I'll plan from there.

I have not produced a PR split, sizes or implementation steps. I changed no files and took no remote action.
