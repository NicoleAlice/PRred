---
name: pr-plan
description: Use when the dev hands over a ticket, issue or feature request and wants a plan before any code is written, asks to break work into small reviewable PRs, or wants the risks, split and rigor level of a change agreed and approved first. Also use when another pr-ready skill needs an approved plan before editing.
---

# pr-plan

Turn a ticket into a plan the dev approves before any file changes: the split into PRs within the line budget, what each PR proves, the weak points, the alternatives you rejected, the rigor level and any new convention the team must hear about first. Read the ticket and the code around the change before proposing anything. Stop instead of planning when the ticket is too thin or the project requires an approval that is missing.

Scripts and references live at `../../scripts/` and `../../references/` relative to this skill's base directory. Run scripts with `python3`, else `python`, else `py -3`; a command that exists but fails (for example the Windows Store alias that prints "Python was not found") counts as not working, so try the next one. If none works, stop and tell the dev to install Python 3.9+, and never redo a script's work by hand. The one exception: if no code exists yet, the plan needs no script (Step 5 matches paths against the list below), so go on and say in the plan that the scripts could not run.

## Non-negotiable

- **No edits before approval.** No file written or changed, no branch created or switched, no commit, no stash, until the dev approves the complete plan that is already in your reply. An approval given before the plan was shown (for example inside the request) counts only once the plan is in your reply. A changed plan needs a new approval.
- **No remote actions.** Do not push, fetch, open or edit PRs, or trigger CI. Read-only queries through the host CLI are fine (Step 4).
- **No plan on a thin ticket or a missing required approval.** Step 2 and Step 3 end the run with questions, not with a tentative plan, not with "I would start by", not with implementation steps.

## Step 1: Get the ticket and the profile

1. Go to the repo root (`git rev-parse --show-toplevel`).
2. Read `.pr-ready/profile.md` if it exists. It gives the host and tracker (`Platform`), the policy fields (`Project rules`), the base, `max_lines` (`Budget`) and extra risk paths. No profile: use the defaults (host from `git remote -v`, budget 500, the default risk paths below), say so in the plan, and suggest running `pr-setup` later. Do not stop for it.
3. Get the ticket text:
   - pasted in the conversation: use it verbatim;
   - a key or URL, and a tracker connector or the host CLI from `references/platforms/<host>.md` is available: fetch it (read-only), including comments;
   - otherwise ask the dev to paste it. Never guess a ticket's content from its title or key.

## Step 2: Check the acceptance criteria (thin-ticket stop)

A criterion is buildable when you could write a test for it: it names an observable behaviour or output, the part of the system it applies to, and what counts as done. The ticket is too thin when no criterion is buildable, or the criteria do not say what to change (for example "it should be better", "improve X", "make it faster" with no number).

When it is too thin, your whole reply is:

1. One line: the ticket is too thin to plan, and why (quote the criterion).
2. **What's missing:** a numbered list of specific questions for this ticket. Cover what applies: what is wrong today (the symptom, a report, a metric), the measurable outcome that means done, which part of the code or flow it covers, error and edge cases, what is out of scope, who decides when it is right. You may read the code to make the questions concrete (for example "checkout has steps A, B and C: which one?"), but do not suggest answers or a design.
3. The ask: "Can you answer these, or take them back to the ticket author? I'll plan once the criteria are testable."

No PR split, no sizes, no implementation steps, no "a possible plan". Then stop.

A ticket with some buildable criteria and a few gaps is not thin: plan it, and list the gaps as open questions in the plan.

## Step 3: Check prior approval

Read `prior_approval` from the profile (`Project rules`), with its quoted sentence. If the project's `CONTRIBUTING.md` or policy states a rule the profile does not, the project wins (`references/rule-precedence.md`).

- `required`: look for a linked issue, discussion or approval reference in the ticket, the request and (read-only, through the host CLI) the issue itself if one is named. If the work is a kind the rule exempts (for example a small bug fix), say which exemption applies and continue. If no approval is found, your whole reply is:
  1. One line: you stopped before planning because the project requires prior approval for this kind of change.
  2. The rule, quoted with its source: `"<sentence>" (<file>, section <name>)`.
  3. What you checked and did not find (no linked issue, no approval label or reference in the ticket).
  4. What to do next: open the issue or discussion the rule names and wait for its approval, or share the link to an existing approval; then run `pr-plan` again.

  No PR split or sizes, not even as a draft. Then stop.
- `not-required`: continue.
- `unclear`, or no profile: continue, and put the question in the plan's gate: "Does this project need an approved issue or discussion before this PR? If yes, link it." Do not treat silence as `not-required`.

## Step 4: Read the code, the sibling and the base

1. Find the files the ticket touches (`git ls-files`, `git grep` for the names in the ticket) and read them in full.
2. Find a **sibling**: an existing file or function that already does something similar (the existing flow the new one mirrors: same layer, same shape). Read it and name it in the plan: "follows the shape of `<path>` (`<function>`)". If nothing similar exists, say so; the plan then sets a new convention (Step 6).
3. Read the tests next to those files, to know how the project tests and which fixtures exist.
4. Resolve the base: the target of `origin/HEAD` (`git symbolic-ref --short refs/remotes/origin/HEAD`), else local `main`, else `master`; the profile's `base` wins if set. If none resolves, ask the dev in the gate.
5. Base and open PRs, read-only, through `references/platforms/<host>.md`:
   - commits on the base since the last fetch that touch the same files: `git log --oneline HEAD..<base> -- <paths>`. Do not fetch; say when the plan assumes the last fetched state.
   - open PRs that touch the same files, through the host CLI's list command (for example `gh pr list`, `glab mr list`). Host `none`, no CLI or no login: skip, and say it was skipped.
   - anything relevant (overlap, a conflicting PR, a moved base) goes in Weak points.
6. If the current branch already has commits or changes against the base, note them: they are part of the work and count toward the first PR's size.

## Step 5: Rigor level

Name exactly one of `trivial`, `normal`, `risky`, written that way (`references/checklist.md` shows which checks each level runs).

- **Code already exists on this branch:** run `classify_risk.py --json` from the repo root and use its `level` and `reasons`.
- **No code yet:** match every path the plan will touch (new or changed, tests included) against the default risk paths below plus the profile's `Risk paths`, case-insensitively:

  `**/auth*/**`, `**/*auth*.*`, `**/*secret*`, `**/*credential*`, `**/migrations/**`, `**/*.sql`, `.github/workflows/**`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`, `**/openapi*`, `**/*.proto`, `**/Dockerfile`

  Any match: `risky`. Only non-executable files (`*.md`, `*.txt`, `*.rst`, `*.adoc`, images, `LICENSE*`): `trivial`. Otherwise `normal`.
- Raise to `risky` when the work handles authentication, authorization, secrets, tokens, caller input or a public contract, even outside those paths, and say why. You may raise a level; only the dev may lower it.
- Give the level per PR when they differ, and the reason as path plus rule (for example "`src/auth/tokens.py` matches `**/auth*/**`").
- At `risky`, state in the plan: **a person must read the auth, authorization, secrets and caller-input changes line by line**, not rely on tests or an agent review; list the files (and, once code exists, the line ranges) they will read. Also say that `risky` adds an end-to-end run and, where a contract changes, a contract diff.

## Step 6: Build the plan

**Split.** Every PR has an estimated size of at most the budget (`max_lines`, default 500), with no exception: if an estimate is over, split again.

- Size = **hand-written lines**, added plus removed, tests included, generated files excluded. Give a number or a narrow range and a one-line basis (for example "~260: new `cancellation.py` ~120, model fields ~20, tests ~120"). These are estimates; `pr-prove` measures after building with `count_lines.py`.
- Cut where a reviewer could approve one PR and reject the next: a shared piece first (model, library, contract), then one PR per feature area, then the code that wires them together. Each PR builds and passes its tests on its own, in order.
- Each PR does one task, and its title needs no "and" (checklist item 1).
- Order the PRs and give each one's base: the first on the project's base, each later one on the previous PR's branch (built one at a time with plain git; see `references/platforms/<host>.md` for stack behaviour).

**What each PR proves.** One or two sentences: what a reviewer can verify from that PR alone, and which acceptance criteria it covers (by number).

**Weak points.** What could go wrong with this plan, specifically: ordering between PRs, partial failure (a step fails after an earlier one has side effects), repeated calls and idempotency, data the change trusts, gaps or ambiguity left in the criteria, existing code the change relies on that looks wrong (name the file), overlap with the base or open PRs.

**Rejected alternatives.** At least one, each with the reason: for example a single PR (over budget, one reviewer verdict for unrelated parts), a split by layer (no PR proves a behaviour), a different design.

**Conventions to announce.** New patterns the team should hear about before the PR (a new module or layer, error type, status value, event, table, config key, dependency). Checklist item 13. Write `none` when the plan follows the sibling throughout.

## Step 7: Show the plan and stop (approval gate)

Your reply contains, in this order:

1. **Read:** the ticket source, the files read, the sibling, the base and what Step 4 found about it and open PRs (or that it was skipped), and the profile (or "no profile: defaults").
2. **Rigor:** the level, its reason, and at `risky` the line-by-line human read with the files.
3. **PRs:** a numbered list. For each: title, base, files, estimated size with its basis, what it proves, the criteria covered.
4. **Weak points.**
5. **Rejected alternatives.**
6. **Conventions to announce.**
7. **Open questions:** gaps in the criteria, the prior-approval question when Step 3 said so, a base that did not resolve, a script that could not run.
8. **The gate question,** last: "Approve this plan? Approve, or tell me what to change." Add any open question the dev must answer with it.

Then stop and wait for the dev's answer. If the dev asks for changes, show the complete changed plan and ask again.

## Step 8: Record it (after approval only)

Append the approved plan to the evidence log from the repo root, passing the plan text on stdin:

`evidence.py add --kind note --stdin`

Start the text with `pr-plan approved:` and include the PR list with sizes, the rigor level and the sibling. If it exits 2 (for example no commits yet), or no Python works, say the plan was not recorded and go on. Then hand over: the first PR is built on its own branch from the base, and `pr-prove` measures and proves it.

## Gates used

From `references/human-gates.md`:

- **Before any edit:** the approval gate in Step 7. Nothing is edited, branched or committed before it.
- **Auth, authorization, secrets, caller input:** at `risky`, the plan says a person reads those changes line by line; the read itself happens once code exists.
- **Lowering the risk level:** only the dev.
- **Any remote action:** none is taken; host queries are read-only.
- **Never:** read or handle credentials (a hard-coded secret in the code is a weak point to name, never a value to copy into the plan); call deployed environments; use real customer data in examples.

Rule precedence (`references/rule-precedence.md`): the project's policy wins over the profile and over pr-ready. When it does, say so in one line and name the source.
