---
name: pr-write
description: Use when the dev is ready to open a PR or MR and wants its description, title or merge request text written, asks to write up what changed and where reviewers should look, or needs the facts for a description they will write themselves. It writes from the diff and the recorded evidence only. Not for running tests or mutations (pr-prove) or reviewing the code (pr-cold-review).
---

# pr-write

Write the PR description from what is verified: the final diff, the profile's policy, the project's template and the evidence log. The diff says how; the description says what changed, why, and where to look. You write; you do not prove. Every test count comes from the evidence log, never from a run of your own. When the project forbids or is unclear about AI-written descriptions, you hand the dev a facts list instead, and they write the prose.

Scripts and references live at `../../scripts/` and `../../references/` relative to this skill's base directory. Run scripts with `python3`, else `python`, else `py -3`; a command that exists but fails (for example the Windows Store alias that prints "Python was not found") counts as not working, so try the next one. If none works, stop and tell the dev to install Python 3.9+, and never redo a script's work by hand. Below, `<py>` is the interpreter that worked and `<scripts>` the scripts folder.

## Non-negotiable

- **Evidence only from the log.** Test counts, mutation results and command outcomes come only from entries in `evidence.py show --json` with `"stale": false`. Do not run tests, builds or mutations yourself, not even "just to check". No usable entry means the evidence is missing, and the description says so.
- **No usable evidence → never put a number next to "test" or "tests"**, in the description or in your report: no "two tests", "2 tests", "both tests", "3 tests added". Refer to tests by file or name only (e.g. "tests in `tests/test_fees.py`: `test_on_time`, `test_late`").
- **The project's policy wins.** `ai_description` and `ai_disclosure` decide what you write and where AI use is declared (`references/rule-precedence.md`). When a policy overrides a pr-ready rule, say so in one line and name the source.
- **No questions to the reviewer.** The description states answers. An open question goes to the dev, in your report, never in the description.
- **No commit, no remote action without confirmation.** The draft lives in a git-ignored file under `.pr-ready/`. Do not commit, amend, stash or switch branches. Push and open the PR/MR only after the dev confirms the exact command (Step 7).

## Step 1: Read the branch

1. Go to the repo root (`git rev-parse --show-toplevel`). Note `git status --porcelain` and `git log --oneline -1` to compare at the end.
2. Read `.pr-ready/profile.md`: `Platform` (host, tracker), `Project rules` (`pr template`, `commit format`, `ai_description`, `ai_disclosure`, each with its quote), `Base branch`. No profile: run `<py> <scripts>/detect_platform.py --json` for `host` and `pr_templates`, treat both policy fields as `unclear`, and suggest `pr-setup`. A profile with no `pr template` value: take `pr_templates` from `detect_platform.py` too.
3. Resolve the base: the profile's `base`, else the target of `origin/HEAD`, else local `main`, else `master`; none: ask the dev. Do not fetch.
4. Read the final diff (`git diff <merge-base>...HEAD`), `git log --oneline <base>..HEAD`, and every changed file in full. Run `<py> <scripts>/count_lines.py --json` for the files and the hand-written total.
5. Get the ticket: pasted text, or fetched read-only through the tracker connector or the host CLI (`references/platforms/<host>.md`). No connector and no adapter file for the host: ask the dev to paste the ticket. A key in the branch name with no tracker and no pasted text gives the key only; never guess its content.

## Step 2: Sort the evidence

Run `<py> <scripts>/evidence.py show --json` from the repo root. Compare each entry's `head` with the top-level `head`:

- **Usable:** `"stale": false`. These are the only source for the Tests section and for any "verified" claim.
- **Stale:** `"stale": true`. Do not quote their counts or results anywhere, not even "for reference". Say in the report: "The recorded evidence is from commit `<entry head>`, older than HEAD `<head>`, so it is not used." The Tests section says the evidence for this HEAD is missing.
- **Missing:** no entries, or only stale ones. Say so in the report and point to `pr-prove`: "Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again."

Unverified means the usable `unverified` entries, copied as they are, plus any new behaviour in the diff that no usable entry covers. It goes to `## Unverified` in a facts list. In a description's Tests section: with some usable evidence, the recorded results followed by "not verified: <text>" lines; with no usable evidence, only the evidence-missing line (Step 4) followed by the new test names by file, and no "not verified:" lines. `evidence.py` exits 2: show its stderr and treat the evidence as missing.

## Step 3: Choose the output

From `ai_description`:

- **`allowed`:** write the description (Step 4).
- **`forbidden`, `unclear`, or no profile:** write only the facts list (Step 5). Say in one line which policy applies, with its quote.

From `ai_disclosure`:

- **`required-in-trailer`:** give the dev the exact trailer line for their commit, in the project's format from the quote (for example `Assisted-by: <tool>`). The description body gets no AI mention and no generated-by footer. You do not amend; the dev adds the trailer to the commits made with AI help.
- **`required-in-description`:** add one short disclosure line at the end of the body, in the project's wording if it gives one.
- **`forbidden-trailer`:** never suggest a trailer.
- **`none`:** no AI mention and no generated-by footer in the body.
- **`unclear`, or no profile:** add nothing, and ask the dev whether and how the project wants AI use declared.

## Step 4: Write the description

**Open questions first.** List what you cannot settle from the diff, the ticket or the evidence (an unstated expected value, a missing ticket link). If the description cannot be written without the answer (several templates and no way to pick, no base), ask the dev and stop. Otherwise write what is verified, state the gap as a fact in Focus or Out of Scope ("the 1.5% default rate is not stated in any ticket or doc"), and put the question to the dev in your report.

**Sections.** Use the template when there is one: its headings, in its order, at its heading level, and no other headings at that level. Keep its checkboxes and fixed text; drop its HTML comments. Map the method's sections into it (`references/pr-format.md`): What, Why and Impact into the summary-like heading, Tests into the testing-like heading, Focus and Out of Scope into the risk- or notes-like heading. Content with no fitting heading goes under the nearest one; never add a heading of your own. The ticket link stays on the first line of the body, above the template's first heading. No template: use the `pr-format.md` sections in order: Ticket, What, Why, Impact, Focus, Out of Scope (only if it has an entry), Tests.

**Title:** the commit-subject shape (`commit format` from the profile), naming what shipped in the ticket's words. It goes in your report and the open command, not in the body.

**Writing rules:**

- One line per paragraph. No hard wraps inside a sentence.
- **Tests** comes only from usable entries: each command line as recorded, its counts copied exactly, and each mutation with the test that failed. With no usable entry, the section has only the evidence-missing line, "Evidence missing for `<head>`: no recorded run for this commit. Run `pr-prove` before review.", followed by the new test names by file, as Step 2 sets out. Then no part of the body gives a count of tests (not even tests added in the diff) or says "passes", "tested" or "verified"; name new test files or functions from the diff, without a number. With usable evidence, a count of tests added may appear in What or Impact only as a diff fact ("adds two tests in `tests/test_fees.py`"), never with "passes", "tested" or "verified".
- **Focus** names the weakest point: the least-tested or least-certain part of the change, and what was checked about it (a mutation, a read, nothing). Never "none".
- **Impact** lists what else the change reaches (callers, contracts, config, pipelines, the parent branch if stacked), or says it reaches nothing beyond the files named, when the diff shows that.
- No question to the reviewer, no "please confirm", no "let me know". If two readings exist, state what the code does.
- No claim the diff or a usable entry does not support. No list of what was not run; the one exception is the required "not verified: ..." lines from Step 2 in Tests.

## Step 5: The facts list (policy forbids or is unclear)

Output exactly the facts-list block from `references/pr-format.md`, with exactly its headings, in its order: `## What changed`, `## Why (from ticket)`, `## Commands and counts`, `## Mutations`, `## Weakest point`, `## Unverified`. Bullet facts only: no sentence of explanation, no advice, no draft prose, no summary before or after it. A heading with no fact keeps `- none`. `Commands and counts` and `Mutations` come only from usable entries; with none, `Commands and counts` says `- none: evidence missing for <head>; run pr-prove` and `Unverified` holds what Step 2 defines: the usable `unverified` entries plus any behaviour no usable entry covers. No template mapping applies.

Around the block, your report adds only: the one-line policy statement, the evidence status (Step 2), the saved path or the printed-only notice (Step 7), the disclosure line from Step 3 if any, the comprehension-check hunks (Step 6, as `file:start-end` and "explain this in your own words", with no comment on what they do), and the ask: "Write the description in your own words from these facts." No other sentence about the change, anywhere in the report.

## Step 6: Check against the diff

1. **Claims:** list every claim in the draft (each behaviour, number, file, impact, test result). Map each to a hunk (`file:line`) or a usable evidence entry. Remove or correct any claim with no mapping. Re-read the draft against the final diff, not the plan: text from an earlier plan that the diff no longer matches goes.
2. **Test counts:** with no usable evidence, scan the draft and your report for a digit or number word ("one", "two", "three", "both", "several") within 3 words of "test" or "tests", and remove it, rewriting with file or test names only. Digits inside a test identifier (`test_2fa`, `test_v2_parser`) are exempt.
3. **Policy:** recheck Step 3 (no AI mention in the body unless `required-in-description`; no trailer under `forbidden-trailer`) and that the body has no question to the reviewer.
4. **Comprehension check (offer it, optional):** list 3 to 5 hunks a reviewer would question (a default value, a boundary, a rounding, a new branch, a removed check), each as `file:start-end` with line numbers read from the file (`grep -n` or a numbered read, never by eye), and ask the dev to explain each in their own words. It does not block: with no answer, the draft stands. A hunk the dev cannot explain goes back to review (`pr-cold-review` or `pr-prove`) or into Focus.

## Step 7: Save, then stop or open

1. Check whether `.pr-ready/.gitignore` is tracked: `git ls-files --error-unmatch .pr-ready/.gitignore` (exit 0 means tracked). Tracked: do not edit it; if it lacks the line `pr-description*.md`, print the draft instead of saving it, and tell the dev why (saving would leave an unignored file next to a tracked ignore file they own) and which line to add. Not tracked: create it, or append the line `pr-description*.md` if it is missing, keeping what is there and adding a newline first if the file does not end with one.
2. Only when `.pr-ready/.gitignore` is untracked, or tracked and already contains the line: save the body to `.pr-ready/pr-description.md` (a stack: `.pr-ready/pr-description-<n>.md`; a facts list: `.pr-ready/pr-description-facts.md`), UTF-8, one line per paragraph, and confirm `git check-ignore -q <path>` exits 0. Never commit it. Tracked without the line: save nothing; the draft is only printed in the report.
3. Record a note from the repo root: `<py> <scripts>/evidence.py add --kind note --text "pr-write: <description|facts list> <saved to <path> | printed (not saved: .pr-ready/.gitignore is tracked)>; template <path|none>; usable evidence <n>, stale <n>"`.
4. Run `git status --porcelain` and `git log --oneline -1`. Only untracked or ignored paths under `.pr-ready/` may be new, and there is no new commit. Undo anything else you caused and say so.
5. **A facts list is never a PR/MR body.** After a facts list, save or print it and stop. Open a PR only later, with a body the dev wrote and supplied (a file path or pasted text), and then through the gate below.
6. Opening the PR/MR (a description, or the dev's own body): on host `none`, with no adapter in `references/platforms/` for the host, or with no CLI or login, print the text and stop; the dev opens it by hand. Otherwise show the exact commands, each behind its own "Run this?" and the dev's answer: first the push if the branch has no upstream, `git push -u origin <branch>`; then the adapter's draft create command with the body from the saved file. No confirmation in this conversation: run nothing and stop.

## Step 8: Report

For a facts list, the report is what Step 5 allows, nothing more. For a description, in this order:

1. **Policy:** the `ai_description` and `ai_disclosure` values with their quotes, and the output chosen.
2. **Evidence:** usable entries used; stale entries ignored, with their commit and HEAD; or "evidence missing: run `pr-prove`".
3. **Title** (for a description) and the **draft** or the facts list, as saved.
4. **Disclosure:** the trailer line for the dev's commit, or the question about declaring AI use, if Step 3 gave one.
5. **Questions for you (the dev, not in the description)** from Step 4, and the comprehension-check hunks.
6. **State:** the saved path or the printed-only notice (Step 7), the open command shown (or "not opened: host `none`" / "awaiting confirmation"), and that the tree has no new commit.

## Gates used

From `references/human-gates.md`:

- **Any remote action:** push and open PR/MR only after the dev confirms each exact command (Step 7). Never close and reopen a PR, and never force-push a reviewed branch.
- **Before any edit:** the only writes are the draft, `.pr-ready/.gitignore` and the evidence note, all under `.pr-ready/` and never committed.
- **Never:** handle credentials, call deployed environments, or put real customer data in the description.

Rule precedence (`references/rule-precedence.md`): the project's policy wins over the profile and over pr-ready. When it does, say so in one line and name the source.
