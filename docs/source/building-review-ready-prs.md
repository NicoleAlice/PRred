# Building review-ready PRs with an agent (source method)

Nov 18, 2026 · Nicole Danni. The method behind `pr-ready`, written generically. It contains no material from any employer's repository: no project names, file names, commands, tickets, PR numbers or incidents. Keep it that way.

## The short version

Five habits do most of the work. Each one turns a claim into evidence before a reviewer opens the PR.

1. **Small, stacked PRs.** One task each, about 500 hand-written lines at most. A bigger change becomes a stack of PRs that merge one after another.
2. **A plan before code.** The agent reads the ticket and the code around the change, proposes a plan with its weak points, and you approve it before any file changes.
3. **Every claim checked against the code.** A statement about behaviour cites the file and line, or the command that proved it.
4. **Tests that can fail.** Break the code on purpose and rerun: a test that still passes asserts nothing. Run every path a user takes, end to end.
5. **A cold review before a person.** A fresh agent that sees only the code and the docs looks for untested premises. Its findings are fixed before anyone is asked to review.

## Before any code

Start from the ticket and its acceptance criteria. If they are too thin to build against, fix the ticket before prompting.

- **Make the agent read first.** The ticket, the files it will touch, and a sibling that already does something similar. Name the sibling: "follow the shape of `<sibling file>`" carries conventions no prompt spells out.
- **Ask for a plan, then approve it.** The plan names its weak points and the alternatives it rejected. A wrong plan costs minutes; a wrong 800-line diff costs an afternoon.
- **Budget about 500 hand-written lines per PR.** Generated files don't count. Measure after building; over budget, split again.
- **Split where a reviewer could approve one part and reject the next.** For example: a shared library first, then one PR per feature area, then the code that uses them.
- **Re-check the base branch and the open PRs before building.** The base moves, and a stack built on an old base needs rework.

## While writing

The code should read as if the person who wrote the file next to it wrote it too.

- **Match the surrounding code** over any general best practice: naming, error handling, test layout. When the repo has agent rules for a topic, the agent follows them.
- **Verify every premise in the code, not from memory.** A method, a config key, an error message, which pipeline deploys where. Ask for `file:line` on each claim. An inferred behaviour is the first thing a reviewer tests.
- **Search before writing a helper.** The agent only knows the code it has read; ask it to find an existing one and reuse it.
- **Comments carry only what the code cannot:** why, a constraint from outside the file, a deliberate omission, a trap. No comment that restates a name, no ticket key in code.
- **Commits** follow the project's format, have a body that says why, and hold one logical change each.

**A new convention goes to the team before the PR does.** A new shared project, a new top-level folder, a first use of some mechanism: each is a team decision, so announce it and link the PR, rather than letting it land inside a feature.

## Proving it works

"All tests pass" is a claim. The PR carries the command that ran and the counts it printed.

### Reproduce CI locally

Run what CI runs, the way CI runs it, and test the PR's merge commit with its base, not the branch alone. A merge that fails locally fails in CI too. If the toolchain can't run on the developer's machine, run it in a container with the same versions CI pins.

### Keep generated files honest

- When generated files are committed, check that they equal what the build generates. Compare ignoring line endings: a Windows checkout differs from a Linux build only in CR/LF.
- A change to a source of generated code (an API contract, a schema) regenerates everything downstream, and each must be checked.

### Make the tests prove something

- **Mutations.** Change one thing a test should catch (drop a field, reword an expected message, remove a check), rerun, expect red. List each mutation and what failed in the PR. A mutation that survives is a finding.
- **Read the survivors too.** When some requests still pass under conditions that should reject them, know why before calling it fine.

**You decide what correct means; the agent writes the mechanics.** Never let it choose an assertion and then confirm its own code meets it. And two strikes: when the same test fails the same way twice, stop and reframe the problem, or read the error yourself, instead of asking for a third attempt.

### Run the real path end to end

For anything that calls a deployed platform, run it against a local stack in containers first: the database, local stand-ins for cloud services, a mock identity provider, and the application built from the branch. For edge behaviour, point the suite at a small stub that answers as a load balancer, a WAF or a throttle would.

## Cold review

Before a person sees the PR, a fresh agent reviews it with none of the conversation. A reviewer who shares your context checks the diff; only a cold one checks the premises.

Give it the worktree, the files to read for context, and the rules the change must keep. Not your conclusions: an agent handed your hypothesis tends to confirm it. Then ask:

```
Cold review, read-only: no edits, no network calls. The change is the diff on
branch <branch> in <path>.
Read for context: <the docs and code the change relies on>.
The rule the change must keep: <e.g. no request writes to the database or
calls an external service>.
Answer with file:line evidence, ranked by severity:
1. Anything that breaks the rule above.
2. Any way a secret or token could reach a log, a test result, a summary or
an exception.
3. Pipeline expressions or steps that do not behave as written.
4. Premises that are untested or wrong.
5. Comments that say something the code does not.
6. Anything a reviewer would refuse.
Say "no finding" for a category you checked and found clean.
```

Then check every finding against the code before acting on it. Typical findings a local run misses: a comment that names the wrong pipeline, a safety comment resting on a false premise, a request that logs a noisy warning on every scheduled run, a secret visible to a step that doesn't need it, and a missing setting that leaves a scheduled job green while it tests nothing. Fix them, then rerun the tests and the mutations before the PR goes up.

## Writing the PR

The diff says how; the description says what changed, why, and where to look. Open the PR as a draft where the host supports it.

| Section | What goes in it |
|---|---|
| Title | The commit-subject shape, naming what shipped in the ticket's own words, not its purpose |
| Ticket | The link, first line |
| What | One or two sentences, in domain terms |
| Why | The problem behind it, or who asked |
| Impact | What else it reaches: contracts, config, pipelines, other services, the parent branch if stacked |
| Focus | The weakest point, named, with what you checked |
| Out of Scope | Only gaps a reviewer would read as a bug, each with its reason; omit the section otherwise |
| Tests | What you added and how you proved it: commands, counts, mutations and what each one broke |

- **Tests are evidence, not intent.** Only counts you saw in this session. Never a list of what was not run.
- **No questions to reviewers.** If two options exist, test both and state the answer.
- **Read the description against the final diff before it goes up.** A plan that changed mid-way still has the old text.
- **One line per paragraph.** Most hosts render a hard-wrapped line as a break, mid-sentence.
- **AI attribution follows the project's policy.** Where the project says nothing, keep generated-by footers out of the body.

## Stacked PRs

Merge a stack from the bottom, one PR at a time. Before each merge, test the next PR on top of what its base will be after the merge. Use merge commits for stacked parents: a squashed parent makes its commits reappear as changes in every PR stacked on it.

Every host behaves differently with stacks: whether a PR based on another branch gets CI, whether the next PR retargets automatically when its parent's branch is deleted, whether changing a base is allowed while another PR stacks on it, and whether editing a PR can drop its description. The platform adapters record these per host. Two rules hold everywhere: keep each description in a file, and never close and reopen a PR to restart CI or force-push a branch someone has reviewed.

## Security habits

Generated code gets more scrutiny, not less: insecure code usually works.

- A secret never goes in a chat, a prompt or a message. Copy it from where it lives straight into where it is used, or share it through a password vault.
- The agent never writes, rotates or reads a credential. A person sets it; the agent references it by name.
- A secret reaches only the step that uses it. Build in one step and pass the secret only to the step that needs it.
- A missing setting fails loudly. A scheduled job that turns green while testing nothing is worse than a red one.
- Synthetic fixtures only. No customer data or production values in prompts, tests or PR text.
- The agent makes no calls to deployed environments. The first real run against a shared environment is a person's.
- Anything touching authentication, authorization, secrets or caller input is read line by line by a person, however routine it looks.

## Generic traps

| Trap | What you see | What to do |
|---|---|---|
| A contract change breaks a consumer | Nothing, until a client fails | Run a contract diff tool (e.g. `oasdiff` for OpenAPI) on base and branch and paste the result in the PR. |
| A new package's licence | The registry's licence field says one thing, the package ships an EULA or a fee | Read the licence inside the package before adding it; check who maintains it. |
| Analyzers or lint rules that ride in with a package | New warnings in code that never referenced it | Compare the build's unique warning count with the base's; it must not grow. |
| A stacked PR gets no CI on some hosts | No checks while its base is another branch | Reproduce CI locally for every PR in the stack. |
| Copying a worktree on Windows | "Path not found" on long file names | Copy to a short root, or use `\\?\`-prefixed paths. |

## Checklist before asking for review

- The PR does one task, from one ticket, and its title needs no "and".
- Hand-written lines are about 500 or fewer, measured after building.
- I read the whole diff, and nothing outside the task moved.
- I can explain every line, and every new comment says something the code cannot.
- Every claim in the code, comments and description was checked against the code or a run.
- CI passed on the merge commit, with its counts written down.
- Committed generated files match what the build generates, and a contract change has its diff result in the PR.
- The build's unique warning count is the same as the base's.
- Any new package exists, is the one meant, and its shipped licence was read.
- Each new test failed under at least one mutation, and the PR lists them.
- Paths a user takes were run end to end, on a local stack when they reach a deployed platform.
- A cold review ran, and its findings were checked and fixed or answered.
- A new convention was announced to the team before the PR.
- The description matches the final diff, names the weakest point, and asks the reviewer nothing.
- No secret, customer value or local path appears in the code, the commits or the description.

## Prompts to copy

**Starting a task**
```
Read <ticket> and its acceptance criteria, the files under <path>, and
<sibling file> as the shape to follow.
Propose a plan: the PRs it splits into (about 500 hand-written lines each),
what each one proves, its weak points and the alternatives you rejected.
Write no code until I approve.
```

**When it says something works**
```
Are you sure? Show the file:line or the command and its output for each
claim. Anything you inferred, test it or mark it as unverified.
```

**Before calling the tests done**
```
Reproduce CI on the merge commit with the base and give me the counts.
Then break the code in <n> ways each new test should catch, rerun, and
list what failed under each mutation.
```

**Before the PR goes up**
```
Read the whole diff. Remove any comment that restates the code, revert
anything outside the task, and check the description against the final diff.
```

**After a stacked PR merges**
```
<parent PR> is merged. Check what <next PR> now targets, test it on top of
the new base, and ask me before updating its branch on the remote.
```
