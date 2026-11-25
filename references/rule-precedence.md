# Rule precedence

When rules conflict, the higher one wins:

1. The target project's AI and contribution policy (`CONTRIBUTING.md`, `AI_POLICY*`, `AI*.md`, PR template, as recorded under `Project rules` in the profile).
2. The repo's agent rules (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/`) and the pr-ready profile.
3. pr-ready's own rules.

When a higher rule overrides a pr-ready rule, say so in one line and name the source.

## Five consequences

1. **Policy forbids AI-written descriptions** (`ai_description: forbidden`): `pr-write` does not write the description. It produces the facts list from `pr-format.md` (what changed, commands and counts, mutations, weakest point) for the dev to write in their own words.
2. **Policy requires declaring AI use** (`ai_disclosure: required-in-description` or `required-in-trailer`): include the declaration where the project asks, in the description or in the commit trailer. With `forbidden-trailer`, add no trailer.
3. **"No generated-by footer"** applies only when the project says nothing about AI. Any project statement overrides it.
4. **Unclear policy, or no profile** (`unclear` values, or no `.pr-ready/profile.md`): take the safe option. `pr-write` delivers the facts list, not a finished description, and asks the dev whether and how to declare AI use.
5. **Prior approval** (`prior_approval`): if it is `required`, `pr-plan` verifies that an issue or discussion approved the work before the PR; if there is none, it stops and tells the dev. If it is `unclear`, or there is no profile, `pr-plan` asks the dev whether such an approval exists.
