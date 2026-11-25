---
name: pr-cold-review
description: Use when the dev wants a fresh pair of eyes on a branch or diff before a person reviews it, asks for a once-over, a second opinion or a cold review, or asks "anything wrong with this before I open the PR?" or what a reviewer would refuse. It reads the code for wrong premises, false comments, leaked secrets and pipeline steps that do not do what they say. Not for running tests or mutations (pr-prove) or writing the PR description (pr-write).
---

# pr-cold-review

Get the change read by a reviewer who has none of your context, then check what it says. You build the prompt from `references/cold-review-prompt.md`, hand it to a fresh read-only subagent, verify every finding at its citation by reading the code, and report what holds up and what does not. You review; you do not fix. A reviewer who shares your context checks the diff. Only a cold one checks the premises.

Scripts and references live at `../../scripts/` and `../../references/` relative to this skill's base directory. Run scripts with `python3`, else `python`, else `py -3`. A command that exists but fails (for example the Windows Store alias that prints "Python was not found") counts as not working, so try the next one. If none works, stop and tell the dev to install Python 3.9+, and never redo a script's work by hand. Below, `<py>` is the interpreter that worked and `<scripts>` the scripts folder.

## Non-negotiable

- **No edits.** Do not change, create or delete any file in the repo, and do not commit, amend, stash, switch branches or create one. The only write is the evidence log, through `evidence.py`. A fix is a suggestion in the report. Edits happen only when the dev asks for them after the report, as a new task with its own plan approval.
- **No remote actions.** Do not push, fetch, open or comment on PRs, trigger CI or call a deployed environment.
- **Keep your conclusions out of the prompt.** No hypothesis, suspected issue, earlier review result or hint about where to look. An agent handed a hypothesis tends to confirm it.
- **No finding without a citation.** A citation is `path:line` or `path:start-end`, the only two forms used below. Every finding you report has one, with lines you read yourself and a quote of them. If you cannot place it on a line, it is not a finding. The one exception is a rejected entry whose location does not resolve, which uses the no-location form in Step 5.
- **No padding.** A clean diff is reported as clean. Do not add nitpicks to look thorough.

## Step 1: Scope

1. Go to the repo root (`git rev-parse --show-toplevel`) and note its absolute path. Run `git status --porcelain` and keep the output, to compare at the end. Uncommitted changes are not part of the review; say so if there are any.
2. Read `.pr-ready/profile.md` if it exists (base, `Project rules`, agent rules, `Known traps`). No profile: use the defaults and suggest `pr-setup`.
3. Resolve the base: the profile's `base`, else the target of `origin/HEAD`, else local `main`, else `master`; none resolves: ask the dev. Do not fetch.
4. Run `<py> <scripts>/count_lines.py --json` for the changed files (`files`, with the excluded ones marked) and `<py> <scripts>/classify_risk.py --json` for the `level` and its `reasons`. Note the branch (`git branch --show-current`) and `git log --oneline <base>..HEAD`.

Do not read the diff closely yet and form no opinion of it: you would carry it into the prompt.

## Step 2: Build the prompt

Copy the block in `references/cold-review-prompt.md` verbatim and fill its placeholders:

- **`<branch>` and `<path>`:** the branch name and the repo root's absolute path. Add the base after the branch: "against base `<base>` (`git diff <base>...HEAD`)".
- **Read for context:** the files the change relies on, chosen by name, imports and calls, not by judging the code: the callers and callees of changed functions (`git grep -l <name>`), the tests next to changed files, the CI or pipeline files that run them, the README or docs that describe the changed behaviour, and the project's agent or contribution rules. List paths only, with no comment on why.
- **The rule the change must keep**, from the first source that states one: the ticket or the approved plan (`evidence.py show`, a `pr-plan approved:` note), then the profile (`Project rules`, agent rules, `Known traps`), then the dev's request. From the request, take the rule alone ("no request writes to disk"), never the dev's suspicion or hypothesis ("I think the cache leaks"). If none states one, write "none stated: existing behaviour and its tests stay as they are, and no secret reaches output" and put "Is there a rule this change must keep?" in the report's questions. Do not invent a stricter rule.

After the block, add exactly these lines:

```
Also read-only: no commits, no branch changes, no running code or tests.
Read files and use read-only git commands (diff, log, show, grep) only.
Cite every finding as path:line or path:start-end and quote the line.
```

Nothing else goes in: not what you saw in Step 1 beyond names and paths, not the dev's worries, not what earlier reviews found.

## Step 3: Dispatch the cold reviewer

- **A subagent tool is available:** dispatch one fresh subagent with the prompt as its whole task. Read-only: no edits, no network, no commits. Do not continue an earlier agent; it is not cold. Wait for its answer.
- **No subagent tool:** run a second pass yourself and label the whole result **"not cold (no subagent available)"**. For each category, read only the diff (`git diff <base>...HEAD`) and the context files before answering, and do not reuse anything concluded earlier in the conversation. Then go on to Step 4 as if a reviewer had answered.

If the reviewer's answer has a finding with no citation, try to place it yourself in Step 4; if you cannot, reject it as "location does not exist" (no-location form, Step 5).

## Step 4: Verify every finding

A finding is a claim, not a fact. For each one:

1. **Resolve the citation.** Open the file with line numbers (a file read with line numbers, or `grep -n`; `wc -l` for its length). Never count lines by eye. Confirm that:
   - the path exists on the branch;
   - the line, or every line of a range, is within the file's length;
   - the quoted text appears at that line, or within 2 lines of it.

   If the text is within 2 lines, or `grep -n` finds it elsewhere in the same file, correct the citation to the line you read and say "line corrected from <n>". If none of that works, reject the finding as "location does not exist" (no-location form, Step 5) and stop there.
2. Check the claim against the code, not against comments: follow the call, search for the premise (for a claim that something "is validated upstream", `git grep -n` for the validation and read the callers), read the test that is said to cover it, read the pipeline job that is said to need a variable.
3. Mark it:
   - **accepted:** the code shows it. Keep the category number, the line and a one-line consequence (for example "a `name` containing `..` reads outside `reports/`").
   - **rejected:** the code contradicts it, with the reason and the citation that refutes it.
   - **unverified:** reading cannot settle it (for example runtime behaviour on a deployed platform). It is not reported as a finding.

Category fixes: a secret or token visible to a step, job or log that does not need it is category 2, whichever category the reviewer used. A comment stating something the code does not do is category 5; when the false comment hides a defect, report the defect in its own category too, citing the line of the code.

Anything you notice while verifying that the reviewer did not raise goes in a separate list, "found while verifying (not cold)", with the same evidence. Do not mix it into the reviewer's findings.

**Only lines you read.** No citation goes into the report or the evidence unless you read that line in this session. That includes accepted findings, the refuting line of a rejected one, unverified ones, "found while verifying" items and Minor remarks.

## Step 5: Record evidence

From the repo root, add one entry:

```
<py> <scripts>/evidence.py add --kind review --stdin <<'EOF'
cold review: <cold | not cold (no subagent available)>, base <base>
rule: <the rule as sent>
accepted: <n>; rejected: <n>; unverified: <n>; found while verifying: <n>
- accepted [cat <n>] <citation> <one-line finding>
- rejected: <citation> <claim> (<reason>)
- rejected: <path or "no location"> (location does not exist) <claim>
- unverified: <citation> <claim> (<what would settle it>)
- found while verifying [cat <n>] <citation> <one-line finding>
EOF
```

One line for each item in every list: accepted, rejected, unverified and found while verifying. A clean review records "accepted: 0" and the categories checked. If `evidence.py` exits 2, show its stderr in the report and say the review was not recorded.

## Step 6: Check the tree

Run `git status --porcelain` and `git log --oneline <base>..HEAD`. Both must match what Step 1 saw (the evidence folder is git-ignored). If something you caused shows up, undo it and say so.

## Step 7: Report

In this order:

1. **Verdict**, one line: "Not ready: <n> findings to fix" or "Clean: no finding in any category". Add "(not cold: no subagent available)" when Step 3 fell back.
2. **Reviewed:** the branch, the base, the commits, the files changed, the context files sent, the rule sent, and that the prompt held no conclusions.
3. **Findings**, ranked by severity. For each:
   - **[category <n>] `<citation>`** and the line quoted in a code span;
   - **why it matters:** the consequence, concretely;
   - **suggested fix**, as text (for example "check that `name` has no path separator or `..` before the join, and add a test for it"). You do not apply it.
4. **Categories 1 to 6:** each with its accepted findings by citation, or "no finding".
5. **Rejected:** each rejected claim with its reason and the refuting citation, or the no-location form. Then the unverified ones with what would settle them.
6. **Found while verifying (not cold),** if any.
7. **Minor (optional),** only if real, each with a citation and a quote, and labelled optional. A clean diff usually has none; leave the section out rather than fill it.
8. **Gates:** at `risky`, list each auth, authorization, secrets or caller-input file from `classify_risk.py` with its line range and ask the dev to confirm a person read them line by line. A cold review is not that read. When the dev confirms, record `<py> <scripts>/evidence.py add --kind note --text "pr-ready: line-by-line read confirmed by the dev: <ranges>"`, the same text `pr-ready` and `pr-prove` use.
9. **Questions for the dev** (the missing rule, an unresolved base).
10. **Next:** "After you fix anything, rerun `pr-prove` so the tests and mutations cover the fix, then run this review again if the fix changed more than the cited lines." Also the evidence file (`evidence.py path`) and that the tree and log are unchanged.

## Step 8: Re-check every citation

Before sending the report, go through every citation in it once more. Skip the no-location rejected entries: they cite no line. For every other citation, check that the path exists, that the lines are within the file's length and that the quoted text is on them. Fix any citation that does not resolve, or take it out together with its finding. Then send the report and stop.

## Gates used

From `references/human-gates.md`:

- **Before any edit:** none are made. Fixes are suggestions; applying them is a new task that needs the dev's request and an approved plan.
- **Auth, authorization, secrets, caller input:** at `risky`, a person reads them line by line (Step 7 item 8).
- **Remote actions:** none.
- **Never:** read, print or copy a credential's value (name the variable, never its value), call deployed environments, or put real customer data in the prompt or report.

Rule precedence (`references/rule-precedence.md`): the project's policy wins over the profile and over pr-ready. When it does, say so in one line and name the source.
