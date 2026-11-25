---
name: pr-prove
description: Use when the dev wants to know a branch actually works before review, says it is about to open a PR and asks whether it is good to go or ready, asks to run what CI runs on the merge result, to check that committed generated files are up to date, or to find out whether the tests would catch a bug. Also use when another pr-ready skill needs commands, counts and mutation results recorded as evidence.
---

# pr-prove

Turn "tests pass" into evidence. Reproduce CI on the merge commit with the base, record every command with its exit code and counts, check committed generated files against a fresh build, and break the code on purpose to see whether the tests notice. You prove what is there: weak or missing tests are findings, not something you fix. You never claim what you did not see.

Scripts and references live at `../../scripts/` and `../../references/` relative to this skill's base directory. Run scripts with `python3`, else `python`, else `py -3`; a command that exists but fails (for example the Windows Store alias that prints "Python was not found") counts as not working, so try the next one. If none works, stop and tell the dev to install Python 3.9+, and never redo a script's work by hand. Below, `<py>` is the interpreter that worked and `<scripts>` the scripts folder.

## Non-negotiable

- **Prove, don't change.** Do not write or edit tests, do not fix the code under review, do not copy a regenerated file over a committed one, and do not commit, amend, stash, switch branches or create one. The only writes allowed are: the evidence log (through `evidence.py`), the temporary worktree, one temporary mutation at a time (reverted at once), and output in git-ignored or temporary paths. An answer supplied with the request ("dev answers: yes") is not a request to edit anything. Edits happen only when the dev asks for them after seeing your report, and then as a new task.
- **Only what you saw.** Every number in the report comes from a command output in this session and is recorded in the evidence log. No tests or no CI means `unverified`, never "pass" or "verified". A test you did not run, a file you did not compare, a path you did not run end to end are `unverified`.
- **The dev decides what "correct" means.** You may propose and run mutations without asking. You may not choose the expected result of new behaviour and then report that the code meets it (Step 7).
- **No remote actions.** Do not push, fetch, open or edit PRs, trigger CI, or call a deployed environment.
- **Leave the tree as you found it.** At the end, `git status --porcelain` in the repo shows nothing new apart from git-ignored paths, `git log` shows no new commit, and the temporary worktree is removed.
- **Always clean up.** Whatever the outcome or stop reason (two strikes, interpreter failure, worktree failure, a merge conflict, missing dependencies, `unverified` exits, the dev interrupting), run Step 10 before ending. No stop skips it.
- **Never install unasked.** Installing changes the environment and needs the network. The profile's `setup:` command is the only install you may run, and only after the dev's explicit yes in this conversation (Step 3). Missing dependencies otherwise (no `node_modules`, no venv, a package not importable): record `unverified` and ask the dev how they want it run. Do not install anything else, and do not count it as a strike.

## Recording evidence

Record every check right after it runs, from the repo root (never from the temporary worktree, which would write to a different log):

```
<py> <scripts>/evidence.py add --kind <kind> --stdin <<'EOF'
cmd: <exact command line, as run>
where: <repo | merge worktree HEAD <sha7> + <base> <sha7>>
exit: <code>
counts: <what the output printed, e.g. "Ran 3 tests, OK">
EOF
```

Kinds: `command` for a run (scripts included), `mutation` for each mutation (Step 8), `unverified` for anything not proven, with the reason, and `note` for a decision (a skip, the level, a question asked). `evidence.py path` prints the log's path. If `evidence.py` exits 2, show its stderr in the report and say the evidence was not recorded.

## Step 1: Read the branch

1. Go to the repo root (`git rev-parse --show-toplevel`). Run `git status --porcelain`. If it lists any change to a tracked file or an untracked file that is not ignored, stop and ask the dev to commit or set it aside; you prove commits, and you never stash for them.
2. Read `.pr-ready/profile.md`: `Commands` (setup, reproduce CI, tests, build, generated check), `Generated files`, `Base branch`, `Budget`, `Risk paths`. No profile: take the commands from the CI files and the README, say so, and suggest `pr-setup`. A command marked `none found` does not exist; do not invent one.
3. Resolve the base: the profile's `base`, else the target of `origin/HEAD`, else local `main`, else `master`; none: ask the dev. Do not fetch; say the base is the local, last-fetched state.
4. Read the diff (`git diff <merge-base>...HEAD`) and every changed file and test in full. List the new behaviour (new functions, branches, outputs) and, for each, the tests that exercise it and what they assert.

## Step 2: Size and level

Run from the repo root and record both as `command` entries:

- `<py> <scripts>/count_lines.py --json`: hand-written `total` against `budget`. `over_budget: true` is a finding (checklist item 2).
- `<py> <scripts>/classify_risk.py --json`: the `level` and its `reasons`. The plan's level (in the evidence log) or the dev's wins if it is higher; only the dev may lower it. Record the level as a `note`.

At `trivial`, run only Step 2 and Step 10: record a `note` that CI, generated files, warnings and mutations were skipped at `trivial`, and report them as skipped, not passed.

## Step 3: Reproduce CI on the merge commit

1. Create the worktree inside the git-ignored evidence folder (the first `evidence.py add` created it, with a `.gitignore` of `*`; if it has none, use a temporary directory outside the repo instead). With no CI, tests or build command, skip the worktree and go to item 4. First run `git worktree prune`; if `.pr-ready/evidence/tmp/merge-<sha7>` already exists (a run that did not finish), remove it with `git worktree remove --force <wt>`, or delete the folder and prune again. Then:
   `git worktree add --detach .pr-ready/evidence/tmp/merge-<sha7> HEAD`
   then in it: `git -C <wt> merge --no-commit --no-ff <base>`. "Already up to date" is fine (the branch contains the base). If git refuses for lack of an identity, rerun with `git -c user.name=pr-ready -c user.email=pr-ready@invalid -C <wt> merge ...`; that sets nothing permanently. If the worktree cannot be created, record `unverified` for the merge-commit run, clean up (Step 10) and stop.
2. **Conflict:** record a `command` entry with the conflicting files, run `git -C <wt> merge --abort`, clean up (Step 10), and stop. Report that the branch does not merge cleanly with the base; nothing else is proven.
3. **Setup:** if the profile has a `setup:` command, do not run it on your own. Show it and ask: "Run the setup step `<command>` in the merge worktree? It installs dependencies, which changes the environment and needs the network." Run it only after an explicit yes (one given with the request counts), and record it as a `command`. Without a yes, record `unverified`: "setup step not run, the dev did not approve installing: `<command>`", and go on; a run that then fails on a missing dependency is handled by "Never install unasked".
   Then run the profile's `reproduce CI` command (else `tests`) inside the worktree, exactly as written. `reproduce CI` never includes install steps; if an older profile has one there, run only its other steps and say so. If its interpreter fails to start (for example `python` is the Store alias), run the same line with `<py>` and say so. Record the exact line, exit code and the counts it printed (tests run, failures, errors, skipped). Copy counts from the output; never compute them.
4. **No CI command and no tests command:** record `unverified` entries: "no CI or test command exists for this project", and one per new behaviour, for example "`slugify` behaves as intended: unverified, no test covers it". Do not write tests or ad-hoc scripts to stand in for them; a check you wrote yourself is not the project's evidence. Suggest tests as text in the report (Step 7). With no tests, record the mutations-skipped note (Step 8).
5. **A test fails:** read the failure. If it is a missing dependency (an import or module not found, a tool not installed), it is not a test failure: see "Never install". Otherwise you may rerun once to rule out flakiness. If it fails the same way twice, stop (two strikes): record it, do not attempt a third run or a fix, clean up (Step 10) and ask the dev to read the error or reframe the problem. A red suite also means no mutations: record the mutations-skipped note (Step 8) before you stop.

## Step 4: Generated files

For each path matching `Generated files` (`git ls-files -- ':(glob)<glob>'`), when the profile says how it is generated:

1. Regenerate it in the merge worktree with the profile's `build` or `generated check` command, run as written in a POSIX shell (Bash; Git Bash on Windows). Create the output folder first if needed (`mkdir -p <wt>/build` in Bash). The output must land in a git-ignored or temporary path. If the command writes over the tracked file, it only touches the worktree; save the committed copy first, byte for byte.
   **Bytes must not be re-encoded.** Windows PowerShell 5.1 rewrites `>` output as UTF-16 and changes line endings, which corrupts the comparison. Use Bash for redirects, or write files through Python, for example the committed copy:
   `<py> -c "import subprocess,sys; open(sys.argv[2],'wb').write(subprocess.check_output(['git','-C',sys.argv[1],'cat-file','blob',':'+sys.argv[3]]))" <wt> <wt>/../<name>.committed <path>`
   If neither Bash nor that works, record `unverified` for the file.
2. Compare: `<py> <scripts>/compare_generated.py <committed> <generated> --json`, and record it.
   - Exit 0, `"equal": true`: report "**equal (line-ending differences ignored)**": the files match apart from line endings (CRLF versus LF), if they differ in those at all. Never write "identical" or "byte-identical": the script does not check bytes. The file is not stale.
   - Exit 1: the committed file is **stale**, a finding. Give `first_diff_line` and name the difference from `git diff --no-index --ignore-cr-at-eol -- <committed> <generated>` (for example "the committed file lacks the `done` field"). Regenerating and committing is the dev's fix; you do neither.
   - Exit 2: record `unverified` with the stderr.
3. No way to regenerate (no command in the profile): record `unverified` for that file.

## Step 5: Warnings

When the profile's `build` command prints a build log (compiler or linter output, not output redirected into a generated file), run it in the merge worktree and in a second worktree at the base (`git worktree add --detach .pr-ready/evidence/tmp/base-<sha7> <base>`), saving each log under `.pr-ready/evidence/tmp/`. Then `<py> <scripts>/warning_delta.py <base.log> <merge.log> --root <wt-base> --root <wt-merge> --json`. Any entry in `added` is a finding: the branch adds new unique warnings. The script then exits 1, even when `delta` is zero or negative (a removed warning does not offset a new one); `delta` is information only. List each entry of `added`. No build log: record a `note` that the warning delta does not apply.

Then remove every worktree now (Step 10 item 1), before any mutation, so the repo's test runner does not collect their files.

## Step 6: Claims and dependencies

- **Claims** (checklist item 5): list each comment, docstring, log or error message the diff adds or changes that states a behaviour ("capped at 50%", "returns None when missing", "retries 3 times"). Check each against the code, or against a run you already recorded. A mismatch is a finding with `file:line`, the claim and what the code does. A claim you could not check is `unverified`.
- **New dependencies** (checklist item 9): for each package the diff adds to a manifest, confirm it exists and is the one meant (name, publisher, not a look-alike), and read the licence it ships, not only the registry field. Read from files already present or the registry page; never install it. Anything you could not read is `unverified`.

## Step 7: What "correct" means

For each new behaviour from Step 1, decide whether its expected result is settled by the ticket, a docstring or an existing test.

- **Settled** (for example "the discount is capped at 50%"): you may suggest an assertion as text, quoting the source of the expected value.
- **Ambiguous or unstated** (for example "rounded to a whole unit": half up, half to even, or always up?): do not pick one. Name the ambiguity with a concrete input on which the readings disagree, run it through the code read-only if useful to show what the code does today, and ask the dev which result is correct. Record a `note` with the question and an `unverified` entry: "<behaviour>: correctness not defined by the dev; not proven".

You never write the assertion into the repo, even after the answer; writing tests is an edit the dev asks for separately. A new behaviour with no asserting test is a finding either way.

## Step 8: Mutations

Skip at `trivial`. Skip when the suite is red or there are no tests, and record a `note` whose text starts with `pr-prove: mutations skipped`, followed by the reason, for example `pr-prove: mutations skipped: no tests exist` or `pr-prove: mutations skipped: suite red on the merge commit (<test>)`. `pr-ready` reads that note to mark prove "done, not proven". Otherwise follow [mutations.md](mutations.md): with the worktrees already removed, first run the tests command once in the repo's own working tree and confirm it is green there (record it); prefer the project's mutation tool when one is configured; else propose 2 or 3 mutations per new or changed test and at least one per new behaviour with no test, apply them **one at a time** in the repo's working tree, run the tests command, record, revert with `git checkout -- <file>`, delete any file the run created, and confirm `git status --porcelain` is empty before the next. A survivor is a finding that names the test that should have caught it. While any mutation survives, the tests are not adequate and the change is not proven.

## Step 9: At `risky`

- Give the person-reads-it gate from `references/human-gates.md`: list every auth, authorization, secrets or caller-input file with line ranges, and ask the dev to confirm a person read them line by line. Do not treat tests or your own reading as that. When the dev confirms, record `<py> <scripts>/evidence.py add --kind note --text "pr-ready: line-by-line read confirmed by the dev: <ranges>"`, the same text `pr-ready` and `pr-cold-review` use.
- Run each user path the change touches end to end, after Step 8, against a local stack (containers, local stand-ins, a mock identity provider) when it reaches a deployed platform. Never call a deployed environment. Delete what the run created; status must be empty afterwards. A path you could not run is `unverified`.
- A changed contract file (OpenAPI, proto, schema): run the project's contract diff tool on base and branch if one is configured, and record its output; otherwise record `unverified`: "contract diff not run: no tool configured".

## Step 10: Clean up and check

This step runs on every exit, including every stop above.

1. `git worktree remove --force <wt>` for each worktree you created, then `git worktree prune`. Delete `.pr-ready/evidence/tmp/`. If a mutation is still applied, revert it (`git checkout -- <file>`).
2. Run `git status --porcelain` and `git log --oneline <base>..HEAD`; record both. The status must show nothing (ignored paths do not appear) and the log only the branch's original commits. If either shows something you caused, undo it (`git checkout -- <file>` for a tracked file, delete your own untracked file) and say so in the report.

## Step 11: Report

In this order, with exact command lines:

1. **Verdict**, one line. "No findings" only when CI ran green on the merge commit, every generated file is equal, every mutation was killed and nothing is `unverified`. Otherwise "Not ready: <n> findings, <m> unverified" or "Nothing proven: no tests or CI". Never "verified", "proven" or "tests pass" without a recorded run behind it.
2. **Commands:** a table of command line, where it ran (repo, or merge worktree with both SHAs), exit code and counts. Scripts and git checks included.
3. **Generated files:** each file, the verdict in the words of Step 4, and for a stale file the difference.
4. **Mutations:** a table of `file:line`, the change, killed or survived, and the test that caught it (or "none"). Or why they were skipped.
5. **Findings:** survivors with the weak test named (`file::test`) and what it fails to assert, tests that assert nothing, uncovered behaviour, claims the code contradicts, dependency problems, stale files, new unique warnings, over budget. Each with a suggested fix as text: an assertion whose expected value comes from a stated source, or a question for the dev.
6. **Unverified:** every `unverified` entry, with the reason.
7. **Questions for the dev:** the Step 7 questions and any two-strikes stop.
8. **State:** the evidence file path (`evidence.py path`), the final `git status --porcelain` (empty or ignored only) and that no commit was added.

Then stop. `pr-write` builds the PR's Tests section from this log only.

## Gates used

From `references/human-gates.md`:

- **New-behaviour tests:** the dev says what "correct" means (Step 7). Mutations need no approval; assertions do.
- **Before any edit:** mutations are the only edits, each temporary and reverted at once (Step 8); they rely on the approved plan or on the dev asking to prove the branch. Permanent edits (new or changed tests, fixes, a regenerated file) need the dev's explicit request after the report, as a new task.
- **Same test failing the same way twice:** stop and ask (Step 3).
- **Installing dependencies:** the `setup:` step runs only after the dev's yes (Step 3).
- **Auth, authorization, secrets, caller input:** at `risky`, a person reads them line by line (Step 9).
- **Remote actions:** none. **Never:** handle credentials, call deployed environments, or put real customer data in a mutation, test input or report.

Rule precedence (`references/rule-precedence.md`): the project's policy wins over the profile and over pr-ready. When it does, say so in one line and name the source.
