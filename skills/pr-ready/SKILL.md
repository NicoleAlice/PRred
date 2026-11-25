---
name: pr-ready
description: Use when the dev wants the whole flow from ticket or finished code to a review-ready PR, asks to get a branch ready for review, asks what is left before opening the PR, or wants to resume pr-ready where it stopped. It reads the profile and the evidence log, shows the checklist status and runs the next pr-ready skill. Not for a single step the dev names (setting up the profile, planning a ticket, proving the tests, a cold review, writing the description): use that skill directly.
---

# pr-ready

Orchestrate the other five skills. You read the profile and the evidence log, work out which steps are done, stale, still to do or not applicable at this PR's level, show that status, and hand over to the first step that is not done by loading that skill. You do not redo a step the evidence shows as done and fresh, and you do not repeat any sibling skill's steps here: the sibling's own SKILL.md does that work.

Scripts and references live at `../../scripts/` and `../../references/` relative to this skill's base directory; sibling skills at `../<name>/SKILL.md`. Run scripts with `python3`, else `python`, else `py -3`; a command that exists but fails (for example the Windows Store alias that prints "Python was not found") counts as not working, so try the next one. If none works, stop and tell the dev to install Python 3.9+, and never redo a script's work by hand. Below, `<py>` is the interpreter that worked and `<scripts>` the scripts folder.

## Non-negotiable

- **No commits, no pushes.** pr-ready never commits, amends, stashes or pushes, and never creates a branch without the dev's yes (Step 6). Code changes happen only in the build step, only after an approved plan, and only when the dev asks for them. A missing or weak test is a finding for the dev, not something you write.
- **Status comes from the evidence, not from new runs.** Do not run tests, builds or mutations to fill in the status. Only a sibling skill runs them, and only when its step is todo or stale.
- **Every gate stops the run** (`references/human-gates.md`): plan approval, what "correct" means, the line-by-line read at `risky`, and every remote action. Stop at the gate and wait for the dev's answer. An earlier yes covers only the step it was given for.

## Step 1: Read the state

From the repo root (`git rev-parse --show-toplevel`):

1. Note `git status --porcelain` and `git log --oneline -1`, to compare at the end.
2. Read `.pr-ready/profile.md` if it exists (host, base, policy, commands). No profile: setup is todo.
3. Resolve the base: the profile's `base`, else the target of `origin/HEAD`, else local `main`, else `master`; none: ask the dev. Do not fetch. Run `git log --oneline <base>..HEAD`.
4. Run `<py> <scripts>/evidence.py show --json`. Keep the top-level `head` and each entry's `kind`, `head`, `stale` and `text`. Exit 2: show its stderr and treat the log as empty.
5. Run `<py> <scripts>/classify_risk.py --json` (`level`, `reasons`) and `<py> <scripts>/count_lines.py --json` (`files`, `total`, `budget`).
6. Check the upstream: `git rev-parse --abbrev-ref --symbolic-full-name @{u}` (an error means the branch was never pushed).

## Step 2: The level

Propose the level from `classify_risk.py`. A higher level in a plan note or a `note` from `pr-prove`, or one the dev gave, wins. You may raise it (say why: auth, secrets, caller input, a public contract); only the dev may lower it.

The level is confirmed when the dev confirmed it in this conversation or in the approved plan note. Otherwise show it as "proposed" with its reasons and ask in the report (Step 5): "Level `<level>`: confirm it, or raise it?"

At `trivial` (only non-executable files such as `*.md`, `*.txt`, images, `LICENSE*`), mutations and the cold review are **n/a: docs/non-executable only (`<files>`), there is no behaviour to mutate or review**. Say so in those words in the report. Prove at `trivial` is only the size check, and the description step still applies.

## Step 3: Step status

Derive each step's status from the profile, the branch and the evidence entries. An entry is fresh when `"stale": false`.

| Step | done when | stale when | Skill |
|---|---|---|---|
| setup | `.pr-ready/profile.md` exists | | `pr-setup` |
| plan | a `note` whose text starts, ignoring case, with `pr-plan approved`, `plan approved` or `plan: scope agreed by the dev` (fresh or not: building the plan moves HEAD); no other note counts | | `pr-plan` |
| build | the branch has commits on top of the base | | the dev, or you when the dev asks |
| prove | at `normal`/`risky`: fresh `command` and fresh `mutation` entries, or **done, not proven** (below); at `trivial`: a fresh `command` entry whose text contains `count_lines.py` (pr-prove Step 2) | those entries exist only with `"stale": true` | `pr-prove` |
| cold review | a fresh `review` entry | the `review` entries are all stale | `pr-cold-review` |
| write | a fresh `note` starting "pr-write:", or a `.pr-ready/pr-description*.md` file other than `pr-description-facts.md` and `pr-description-order.md` exists and no `pr-write:` note does | the `pr-write:` notes are all stale | `pr-write` |
| open | the dev says the PR is open | | the open gate (Step 6) |

- A step with no entry is **todo**. A step the level excludes is **n/a**, with the reason. At `trivial`, pr-prove runs only its Step 2 (`count_lines.py` and `classify_risk.py` as `command` entries, plus a `note` that CI, generated files, warnings and mutations were skipped at `trivial`): prove is done with the fresh `count_lines.py` command entry, items 5 to 11 and mutations are n/a, and the cold review is n/a.
- A **stale** step names its evidence: "stale: `<kind>` entry recorded at HEAD `<entry head>`, HEAD is now `<head>`". The commits since then changed the code it covered (`git log --oneline <entry head>..HEAD`).
- A fresh `unverified` entry keeps its checklist item todo, with the entry's text as the reason.
- **Done, not proven:** pr-prove ran but could not run mutations (no tests, or a red suite). It then records a fresh `note` whose text starts with `pr-prove: mutations skipped`, followed by the reason. When that note exists together with fresh `command` and/or `unverified` entries, the steps table shows prove as "done, not proven" and cites the note. Its checklist items (2, 5 to 11) stay **todo**, each citing the `unverified` entries as the reason (item 10 cites the note). Next moves on to the cold review: do not propose `pr-prove` again until HEAD moves.
- After the review led to fixes (new commits), prove is stale first: rerun `pr-prove`. Then the review is stale too: ask the dev whether the fix changed more than the cited lines; if yes, rerun `pr-cold-review`, else the dev may accept the earlier review.
- No profile and the dev declines `pr-setup`: setup is n/a ("defaults, no profile") and the other steps run on defaults.

## Step 4: Checklist status

Render `references/checklist.md` for the level, one row per item: `| # | Item (short) | Status | Why |`. Items outside the level are n/a with "not run at `<level>`". The others take their step's status: items 1 and 13 from plan, 2 and 5 to 11 from prove (item 10 from the `mutation` entries alone, item 11 only at `risky`), 12 from cold review, 3, 4, 14 and 15 from write.

**At `risky`**, add a row "A person read the auth, authorization, secrets and caller-input hunks line by line". List each such file from `classify_risk.py`'s `reasons`, and any file you raised the level for, with its hunks as `file:start-end` from `git diff -U0 <base>...HEAD -- <file>` (each `@@ -a,b +c,d @@` header gives `c` to `c+d-1`; read the numbers, never count by eye). The row stays **todo** until the dev confirms in this conversation that a person read them. Then record `<py> <scripts>/evidence.py add --kind note --text "pr-ready: line-by-line read confirmed by the dev: <ranges>"` (`pr-prove` and `pr-cold-review` record the same text). A fresh `note` whose text starts with `pr-ready: line-by-line read confirmed` marks it done, whichever skill recorded it. Tests, the cold review and your own reading do not count.

## Step 5: Report, then hand over

Your reply starts with:

1. **Branch:** branch, base, commits, files changed, hand-written lines against the budget.
2. **Level:** the level, its reasons, and "confirmed" or "proposed".
3. **Steps:** a compact table `| Step | Status | Evidence |` for setup, plan, build, prove, cold review, write, open. The Evidence column cites the entry (kind and HEAD) or the file, or the n/a reason.
4. **Checklist:** the Step 4 table.
5. **Next:** the first step that is todo or stale, in the order of the steps table, with one line on why. A done and fresh step is never proposed again: if tests or mutations come up, say "already done at HEAD `<head>`, not stale". Then list the steps left after it, so the dev sees the whole way to the PR.

Then:

- **The dev asked what is left** (a status question): end with the offer, "Shall I run `<skill>` now?", plus any level question, and stop.
- **The dev asked to move forward** ("get this branch ready", "take me to the PR") and the level is confirmed: load `../<skill>/SKILL.md` and follow it from its first step. Its gates are yours: when it stops for an answer, you stop. When it finishes, come back here, redo Step 1 and Step 3 only, and show the updated steps table and the next step.
- **The dev asked to open the PR:** go to Step 6 after the report, and ask any level question there too. If a step before open is todo or stale, say which and ask: "Run `<skill>` first, or open as it is?" Then stop.
- **The level is not confirmed:** ask the level question together with "Next is `<skill>`: run it?", and stop.
- **The next step is plan and the branch already has commits:** offer `pr-plan`, or the dev may say the scope was agreed; then record `evidence.py add --kind note --text "plan: scope agreed by the dev, no pr-plan run: <their words>"` and move on.
- **The next step is build:** the dev builds, or asks you to; you edit only what the approved plan names and commit nothing. Then prove.

## Step 6: Remote actions and stacks (gates)

**Opening the PR** (the dev asks to open it, or every step up to open is done). Use `references/platforms/<host>.md`. Run nothing yet. Show the exact command lines, filled in:

1. If Step 1 found no upstream: `git push -u origin <branch>`.
2. The adapter's draft create command with the base, the title and the body file `.pr-ready/pr-description.md` (in a stack, `.pr-ready/pr-description-<n>.md` for PR `n`; never `pr-description-order.md`). For example GitLab: `glab mr create --draft --target-branch <base> --title "<title>" --description "$(cat .pr-ready/pr-description.md)"`; GitHub: `gh pr create --draft --base <base> --title "<title>" --body-file .pr-ready/pr-description.md`. The title is the one `pr-write` gave; else the branch's first commit subject, and say so. Never use a facts list (`pr-description-facts.md`) as the body. No description file: write is todo, so run `pr-write` first.

Then ask: "Run this?" for the first command only. Run it only after an explicit yes in this conversation, then show the next one and ask again. One yes covers one command. No yes: run nothing and stop. If the host CLI is missing or not logged in, still show the commands, say the CLI is unavailable, and let the dev run them. Host `none`, or no adapter for the host: run nothing and print the steps from `references/platforms/none.md` (the description file, and for a stack the branch list with bases and the merge order with its reminders, in `.pr-ready/pr-description-order.md`).

Other remote actions (change a base, update a branch, trigger CI) take the same gate with the adapter's command. Never close and reopen a PR, and never force-push a reviewed branch.

**Multi-PR plans.** The approved plan note lists the PRs in order. Work on one PR at a time: its steps table runs to open before the next starts. To start PR n+1, show `git switch -c <branch n+1> <branch n>` and run it only after the dev's yes (branches come from the previous PR's branch, with plain git). Its PR base is branch n, through the adapter's `--base` / `--target-branch`, behind the same "Run this?" gate. Follow the adapter's stack behaviours after each merge.

## Step 7: Check the tree

Before you end, and after a sibling skill returns: run `git status --porcelain` and `git log --oneline -1`. Only paths under `.pr-ready/` may be new, and the last commit is the one Step 1 saw unless the dev made or asked for a commit. If anything else changed, report it, and don't revert anything without the dev's yes. End with the evidence file (`evidence.py path`) and "no commit or push was made".

## Gates used

From `references/human-gates.md`, all through the sibling skills and Step 6:

- **Before any edit:** plan approval in `pr-plan`; the build edits only after it, and only when the dev asks.
- **New-behaviour tests:** the dev says what "correct" means (`pr-prove`).
- **Auth, authorization, secrets, caller input:** at `risky`, the line-by-line read row stays todo until the dev confirms (Step 4).
- **Any remote action:** the exact command and "Run this?", one command per yes (Step 6).
- **Lowering the risk level:** only the dev.
- **Never:** handle credentials, call deployed environments, close and reopen a PR, force-push a reviewed branch, or put real customer data anywhere.

Rule precedence (`references/rule-precedence.md`): the project's policy wins over the profile and over pr-ready. When it does, say so in one line and name the source.
