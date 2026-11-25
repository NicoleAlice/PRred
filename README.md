# PRred

PRred is a Claude Code plugin (its skills are `pr-setup`, `pr-plan`, `pr-prove`, `pr-cold-review`, `pr-write` and the `pr-ready` orchestrator) that takes a change from a ticket to a pull request a person can review: a scoped plan, recorded proof, a cold review and a description that follows the project's own rules. It works on any git host, or none.

## The problem

Coding agents make it cheap to open a pull request and expensive to review one. Surveys of reviewers (arXiv [2610.11179](https://arxiv.org/abs/2610.11179) and [2610.21144](https://arxiv.org/abs/2610.21144)) find that AI authorship alone is not a reason to reject a change, but that AI-authored PRs are held to a higher evidence bar: a bounded scope, a stated rationale, validation beyond CI, and an author who clearly owns the change.

## The method: five habits

Each habit turns a claim into evidence before a reviewer opens the PR. The full method is in [docs/source/building-review-ready-prs.md](docs/source/building-review-ready-prs.md).

1. **Small, stacked PRs:** one task each, about 500 hand-written lines at most; a bigger change becomes a stack.
2. **A plan before code:** the agent reads the ticket and the code, names the weak points, and the dev approves before any file changes.
3. **Every claim checked against the code:** a statement about behaviour cites a `file:line` or the command that proved it.
4. **Tests that can fail:** break the code on purpose and rerun; a test that still passes asserts nothing.
5. **A cold review before a person:** a fresh agent with none of the conversation looks for wrong premises, and its findings are checked and fixed first.

## How it works

Six skills. Each one can run on its own; `pr-ready` chains the other five.

| Skill | What it does |
|---|---|
| `pr-setup` | Reads the repo once and drafts `.pr-ready/profile.md`: host, CI commands, generated files, risk paths, and the contribution and AI policy, each policy value with the quote it came from. Saves only after the dev approves the draft. |
| `pr-plan` | Turns a ticket into a plan: the split into PRs within the line budget, what each PR proves, weak points, rejected alternatives and the rigor level. Stops on a ticket too thin to build against, and edits nothing until the plan is approved. |
| `pr-prove` | Reproduces CI on the merge commit with the base, checks committed generated files, compares warning counts, and mutates the code to see whether the tests notice. Records every command and count in an evidence log; anything it did not see is `unverified`. |
| `pr-cold-review` | Hands the diff to a fresh, read-only reviewer with no hints, then verifies every finding at its citation before reporting it. Reviews only; fixes are the dev's call. |
| `pr-write` | Writes the description from the final diff and the evidence log only, in the project's template. If the project forbids or is unclear about AI-written text, it hands over a facts list for the dev to write up. |
| `pr-ready` | Reads the profile and the evidence log, shows the status of each step and of the checklist, and runs the next step that is todo or stale. |

The chain: `pr-setup` once per repo, then per change `pr-plan` → build → `pr-prove` → `pr-cold-review` → `pr-write` → open. The skills share state through two files in the target repo: the profile and the evidence log (`.pr-ready/evidence/`, git-ignored, one file per branch and worktree). Each evidence entry records the HEAD it was taken at, so a commit after a step marks it stale and `pr-ready` proposes it again. The scripts in `scripts/` do the counting, risk classification, generated-file comparison and evidence bookkeeping, so the numbers do not depend on the model's arithmetic.

Change levels set the rigor: `trivial` (docs and other non-executable files: size check and description only), `normal`, and `risky` (auth, secrets, migrations, pipelines, contracts: adds end-to-end runs and a line-by-line read by a person). The agent may raise a level; only the dev may lower one.

## Install

**From the Claude Code plugin marketplace:**

```
/plugin marketplace add NicoleAlice/PRred
/plugin install prred@prred
```

**Manually:** copy `skills/`, `scripts/` and `references/` into `~/.claude/`, keeping them side by side. The skills find the scripts at `../../scripts/` relative to their own folder, so the sibling layout matters.

```
~/.claude/
  skills/pr-setup/  skills/pr-plan/  skills/pr-prove/  ...
  scripts/
  references/
```

## Requirements

- Python 3.9 or later. The scripts use only the standard library and run on Windows, macOS and Linux. Each skill tries `python3`, then `python`, then `py -3`; if none works, it stops and asks you to install Python instead of doing the scripts' work by hand.
- git.
- Optional: `gh` (GitHub) or `glab` (GitLab), logged in, to fetch issues and open draft PRs. Without them the skills print the commands and you run them.

## Quick start

One example prompt per skill. Plain language is meant to be enough: Claude Code picks a skill from its description. The evals below did not measure that choice (see "Does it work?"), so name the skill if the wrong one runs.

| Skill | Try |
|---|---|
| `pr-setup` | "Set up pr-ready for this repo." |
| `pr-plan` | "I'm picking up this ticket, plan how to build it before we write any code." (paste the ticket or give its key) |
| `pr-prove` | "I'm about to open a PR. Prove it works: run what CI runs on the merge result." |
| `pr-cold-review` | "Do a cold review of this diff: tell me what a reviewer would refuse." |
| `pr-write` | "Write the PR description for this branch." |
| `pr-ready` | "Get this branch ready for review." or "What's left before I can open the PR?" |

Three invented example profiles show what `pr-setup` produces for different projects: [Node on GitLab](examples/profiles/node-gitlab.md), [Python with no CI or host](examples/profiles/python-no-ci.md) and [Go on Bitbucket with generated SQL code](examples/profiles/go-bitbucket.md).

## Does it work?

Every skill was evaluated the same way: the same task, on a small invented repo, run by fresh subagents **without** the skill and **with** it, three runs each. A grader scores each run's final report, `git status` and `git log` against a yes/no rubric. A run passes when every rubric item passes. The procedure records the baseline before the skill is written. Runner model: Sonnet; grader model: Haiku. Cells are runs passed out of 3. The method is in [evals/README.md](evals/README.md).

What this does not measure: each with-skill run was told to read that skill's `SKILL.md`, so whether the descriptions alone trigger the right skill was not tested. Answers to the human gates (plan approval, what "correct" means and the like) were pre-supplied in the prompts. The prompts also carried the path to Python, because the eval machine's `PATH` predated its Python install.

**pr-setup** ([results](evals/results/pr-setup.md))

| Case | Without | With |
|---|---|---|
| gitlab-ai-forbidden | 0/3 | 2/3 |
| bare-no-ci | 0/3 | 3/3 |
| rerun-keeps-edits | 3/3 | 2/3 |

One with-skill failure was a run whose shell could not reach Python; it stopped as the skill says, and counts as a failure. In another, the report described the draft instead of showing it. `rerun-keeps-edits` also passes without the skill and is kept as a regression guard.

**pr-plan** ([results](evals/results/pr-plan.md))

| Case | Without | With |
|---|---|---|
| big-feature | 0/3 | 3/3 |
| thin-ticket | 0/3 | 3/3 |
| needs-prior-approval | 3/3 | 3/3 |
| touches-auth | 0/3 | 3/3 |

Without the skill: one or two PRs with no size estimates, no line-by-line read for auth changes, a plan written anyway for a ticket whose only criterion was "it should be better", and no request for approval. `needs-prior-approval` passes without the skill too.

**pr-prove** ([results](evals/results/pr-prove.md))

| Case | Without | With |
|---|---|---|
| assertionless-test | 1/3 | 3/3 |
| no-tests | 0/3 | 3/3 |
| generated-crlf | 1/3 | 3/3 |
| generated-mismatch | 2/3 | 3/3 |
| asks-correctness | 3/3 | 3/3 |

A first version of these cases used leading prompts ("prove the tests catch bugs") and the baseline passed every case; they were rewritten with neutral prompts before the skill was written, and the old runs are kept. Without the skill: test files left modified, self-written tests reported as passing, "byte-identical" claimed for a file that differs in line endings, a regeneration committed without asking. `generated-crlf` was re-run after a wording fix found in review.

**pr-cold-review** ([results](evals/results/pr-cold-review.md))

| Case | Without | With |
|---|---|---|
| false-comment | 1/3 | 3/3 |
| secret-in-build-step | 0/3 | 3/3 |
| clean-diff | 0/3 | 3/3 |

Without the skill the agent usually spots the real defects; it fails on evidence, with findings that have no `file:line`. The difference is verified, located findings, not detection alone. One with-skill run cited lines past the end of a file; after a fix that made citation checks concrete, the cold reviewer still did that in all three re-runs, and each time the skill rejected the citation instead of reporting it.

**pr-write** ([results](evals/results/pr-write.md))

| Case | Without | With |
|---|---|---|
| policy-forbids | 0/3 | 3/3 |
| no-evidence | 0/3 | 3/3 |
| stale-evidence | 3/3 | 3/3 |
| uses-template | 0/3 | 3/3 |
| disclosure-trailer | 3/3 | 3/3 |

Without the skill: prose written although the project forbids AI-written descriptions, questions to the reviewer inside the description, and test counts from runs of its own instead of the evidence log. `no-evidence` with the skill went 2/3 (the failing run wrote "the two new tests", which the grader counted as a test count), then 1/3 after a review round, then 3/3 once the rule became a non-negotiable with a self-check; the earlier runs are kept. `stale-evidence` and `disclosure-trailer` pass without the skill too.

**pr-ready** ([results](evals/results/pr-ready.md))

| Case | Without | With |
|---|---|---|
| resume | 0/3 | 3/3 |
| trivial-docs | 0/3 | 3/3 |
| no-push-without-ok | 1/3 | 3/3 |

Without the skill: tests and mutations already recorded were run again, the cold review was never proposed, two of three resume runs created commits on their own, and two runs asked to open the PR did not show the exact command first. The first with-skill batch was cut off by a usage limit; all nine runs were redone on fresh fixtures.

Raw reports and grades for every run are in [evals/results/raw/](evals/results/raw/). These are small fixtures built to isolate one behaviour each, not a benchmark of real-world PRs.

## Showcase

[docs/showcase.md](docs/showcase.md) runs `pr-ready` end to end on one invented branch with four planted faults: a secret exposed to a build step, a pipeline rule that never fires, a test with no assertion, and a comment the code contradicts. It compares runs with and without the plugin and quotes what each one caught. Result: **0/3 runs pass without the plugin, 1/3 with it**, so the case does not pass in either mode.

- **Without the plugin**, each run found 3 of the 4 faults but cited none by `file:line`, and all three committed a fix on their own.
- **With the plugin**, the runs found 3, 3 and 4 faults, each with a verified `file:line`. None committed or took a remote action, and each reported surviving mutants and a "not ready" verdict.
- **Runs 1 and 2 with the plugin missed the pipeline condition** (`"scheduled"` instead of GitLab's `"schedule"`). Every run without the plugin missed it too.

## Supported platforms

| Host | What the skills do |
|---|---|
| GitHub | Fetch issues and open draft PRs with `gh`, after confirmation. |
| GitLab | Fetch issues and open draft MRs with `glab`, after confirmation. |
| None | No remote actions. Descriptions, the branch list and the merge order are written under `.pr-ready/` for you to use by hand. |
| Bitbucket, Azure DevOps | Detected, but there is no adapter yet: the skills print the description and the steps instead of opening anything. |

Trackers: any connector available in your Claude Code session, pasted ticket text, or none. A ticket's content is never guessed from its key. Per-host commands and stack behaviours are in [references/platforms/](references/platforms/).

## Rule precedence

When rules conflict, the higher one wins ([references/rule-precedence.md](references/rule-precedence.md)):

1. The project's AI and contribution policy (`CONTRIBUTING.md`, AI policy files, the PR template).
2. The repo's agent rules (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/`) and the pr-ready profile.
3. pr-ready's own rules.

So if a project forbids AI-written PR descriptions, `pr-write` does not write one; if it requires declaring AI use, the declaration goes where the project asks. When the policy is unclear, the skills take the safe option and ask.

## What it never does

Some steps always stop for a person ([references/human-gates.md](references/human-gates.md)):

- **Before any edit,** the dev approves the plan. A changed plan needs a new approval.
- **For new behaviour,** the dev says what "correct" means. The agent never picks an assertion and then confirms its own code meets it.
- **Auth, authorization, secrets and caller input** are read line by line by a person, who confirms it.
- **Any remote action** (push, open a PR, change a base, update a branch, trigger CI) is shown as the exact command and run only after a yes. One yes covers one command.

And never, at any level: read, write or run credentials; call deployed environments; close and reopen a PR; force-push a reviewed branch; put real customer data in tests, prompts or PR text. The skills do not commit on your behalf.

## Development

```
python -m unittest discover -s tests -t . -v
```

## License

MIT. See [LICENSE](LICENSE).
