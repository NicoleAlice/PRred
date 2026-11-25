---
name: pr-setup
description: Use when the dev asks to set up pr-ready for a repo, or to create, refresh or update its PR-readiness profile (`.pr-ready/profile.md`), or to record the repo's git host, local CI commands, generated files, risk paths, or its contribution and AI-usage policy. Also use when another pr-ready skill finds no profile and the dev agrees to create one.
---

# pr-setup

Build the per-project profile `.pr-ready/profile.md` that the other pr-ready skills read: the host, the project's rules and AI policy with quotes, the base branch, the commands CI runs, generated files, budget, risk paths and known traps. Every value comes from a file or a script output you read. Show the complete draft, wait for approval, then save. On a re-run, keep every section the dev edited by hand.

Scripts and references live at `../../scripts/` and `../../references/` relative to this skill's base directory. Run scripts with `python3`, else `python`, else `py -3`; a command that exists but fails (for example the Windows Store alias that prints "Python was not found") counts as not working, so try the next one. If none works, stop and tell the dev to install Python 3.9+, and never redo a script's work by hand. Below, `<py>` is the interpreter that worked and `<scripts>` the scripts folder.

## Non-negotiable

- **Write nothing before approval.** Do not create `.pr-ready/`, `profile.md` or `.profile.generated.md` in the repo until the dev approves the complete draft that is already in your reply. An approval given before the draft was shown (for example inside the request) counts only once the draft is in your reply. The scratch copy outside the repo for the Step 4 parse check is not a write to the repo.
- **No invented values.** A command, glob or policy value with no source in a file you read is not written. Use `none found` for Commands, `none` for empty lists, `unclear` for policy fields.
- **Commit nothing, stage nothing, take no remote action.** Do not run the CI commands either; `pr-prove` runs them.

## Step 1: Detect and read

1. Go to the repo root (`git rev-parse --show-toplevel`) and run `<py> <scripts>/detect_platform.py --json` from there. On exit 2, show its stderr and stop.
2. Its JSON has: `host`, `remote_url`, `default_base`, `clis`, `stack_tools`, `policy_files`, `pr_templates`, `ci_files`, `agent_rules`, `commit_samples`, `ticket_keys`.
3. Read in full every path listed in `policy_files`, `pr_templates`, `ci_files` and `agent_rules`. Also read `references/profile-template.md` (the format) and `references/rule-precedence.md` (what the policy fields mean).
4. If `.pr-ready/profile.md` exists, this is a **re-run**: read it and `.pr-ready/.profile.generated.md` (if present) too. Never read secret files (`.env*`, key files, CI variable values).

## Step 2: Build the generated draft

Use the template's title, its `##` headings with their exact names and order, and its bullet keys. Leave out the template's explanatory paragraphs. Fill each section as below.

### Platform

- `host:` the `host` value from the JSON, verbatim (`github`, `gitlab`, `bitbucket`, `azure-devops`, `none`). If it is `unknown`, write `host: unknown` and ask the dev at the gate which host it is.
- `tracker:` a tracker connector available in this session, by name; else, if `ticket_keys` is non-empty, `unclear (keys seen: <first keys>)`; else `none`.
- `stack tool:` `gh stack`, `graphite` or `sapling` if `stack_tools` marks it true; else `plain branches`.

If the host's CLI (`gh`, `glab`, `az`, `bb`) is false in `clis`, say in your notes that remote steps will follow `references/platforms/none.md`.

### Project rules

- `contributing:` the CONTRIBUTING path(s) from `policy_files`, else `none`.
- `pr template:` every path in `pr_templates` (GitLab ones live under `.gitlab/merge_request_templates/`), else `none`.
- `commit format:` a format only when most `commit_samples` follow it, written `<format> (observed in history)`; else `unclear`.
- `agent rules:` the `agent_rules` paths, else `none`.
- The three policy fields. For each one, search the policy files, templates and agent rules for a sentence that settles it:
  - Found: write the value, then an indented quote line with the exact sentence, its file and section:
    ```
    - ai_description: forbidden
      > "Do not submit pull request descriptions written by AI tools" (CONTRIBUTING.md, section Tooling)
    ```
    Quote the source's words exactly; if the sentence wraps across lines in the file, join it with single spaces.
  - Not found: write `unclear` and no quote line. Silence is not a value: a policy that says nothing about disclosure is `ai_disclosure: unclear`, not `none`. A sentence about one field does not settle another.
  - Allowed values (anything else breaks the parser):
    - `ai_description`: `allowed` | `forbidden` | `unclear`
    - `ai_disclosure`: `none` | `required-in-description` | `required-in-trailer` | `forbidden-trailer` | `unclear`
    - `prior_approval`: `required` | `not-required` | `unclear`

### Base branch

`- base: <default_base>` without an `origin/` prefix. If `default_base` is null, write `- base: unclear` and ask the dev at the gate.

### Commands

Take commands **only from the files in `ci_files`**, copied verbatim (no added flags, no rewording):

- `setup:` the dependency install or restore steps (`pip install ...`, `npm ci`, `dotnet restore`, `bundle install` and the like), in order, joined with ` && `.
- `reproduce CI:` the job's other runnable steps in order, joined with ` && `. Install and restore steps go in `setup:`, never here. Skip CI-only steps too: checkout, cache, artifact upload, deploy, login or anything that needs a secret.
- `tests:` the step that runs the test suite.
- `build:` the step that builds.
- `generated check:` a step that regenerates files and diffs them.

Any of these with no CI step behind it is `none found`. With no CI files, all five are `none found`. Never fill a gap from ecosystem habit (`pytest`, `npm test`, `make test`, `python -c "import ..."`, `compileall`, "sanity checks"). A command that appears only in a README or CONTRIBUTING goes in your notes as a suggestion, not in the profile.

### Generated files

Only globs with evidence: `.gitattributes` entries marked `linguist-generated`, outputs a CI step regenerates, or tracked files whose header says they are generated (`git grep -l -I -E "Code generated .*DO NOT EDIT|@generated"`). Each bullet starts with the glob in backticks, then the evidence: `` - `src/gen/**` (header "DO NOT EDIT") ``. No evidence: `- none`.

### Budget

`- max_lines: 500`, unless a policy file states a size limit; then use it and quote it on an indented line.

### Risk paths

The built-in defaults (`DEFAULT_RISK_PATHS` in `../../scripts/classify_risk.py`) always apply; list only project-specific extras: tracked paths holding auth, secrets handling, migrations or public contracts that the defaults miss, each as a backtick glob plus a short reason. None: `- none`.

### Known traps

The table header `| Symptom | Cause | What to do |` and `|---|---|---|`. Add a row only for a trap a file documents; otherwise one row `| none yet | | |`.

This result is the **generated draft**. Keep it exactly; Step 5 saves it to `.pr-ready/.profile.generated.md`.

## Step 3: Re-run merge (only when `profile.md` exists)

Split three texts into sections at each `## ` heading (the title and anything before the first `##` form a preamble): the current `profile.md`, the old `.profile.generated.md`, and the new generated draft. Compare sections ignoring trailing whitespace and CR/LF differences.

For each section of the new generated draft:

| Current `profile.md` section | Result | Label |
|---|---|---|
| Same as the old generated section | New generated section | `updated` if it changed, else `unchanged` |
| Differs from the old generated section, and the new generated section is unchanged from the old | Current `profile.md` section, verbatim | `kept (dev edited)` |
| Differs, and the new generated section also changed | Current section; show the new one beside it and ask the dev at the gate which to keep | `kept (dev edited), conflict` |
| Missing from `profile.md` | New generated section (other skills need every heading) | `restored` |

When more than one row could apply, the more specific row wins (row 3 over row 2). Sections that exist only in `profile.md` stay where they are, labelled `kept (dev added)`. If `.profile.generated.md` is missing, you cannot tell edits from stale output: keep every current section that differs from the new draft, label it `kept (no baseline)`, and list them at the gate.

The merged text is the draft you show and save as `profile.md`. The new generated draft, unmerged, is what `.profile.generated.md` gets, so it never contains the dev's edits.

## Step 4: Show the draft and stop (save gate)

First check that the draft parses. Write it as `.pr-ready/profile.md` inside a new temporary folder outside the repo (`<tmp>`; writing there is not an edit to the repo), then run
`<py> -c "import sys, json; sys.path.insert(0, sys.argv[1]); from prlib.profile import read_profile; print(json.dumps(read_profile(sys.argv[2])))" <scripts> <tmp>`
If `warnings` is non-empty or a `policy` value differs from the draft, fix the draft before showing it. If no temporary folder can be written, say so; the check in Step 5 then catches format errors after saving.

Your reply contains, in this order:

1. **Sources read:** the paths from Step 1 and the detect summary (host, base, CLIs).
2. **The complete draft** in one fenced `markdown` block: every section and every line, exactly as it will be saved. Never a summary or excerpt.
3. **Re-run only, sections:** one line per section with its label from Step 3. Name each kept section and why, for example: "Known traps: kept, because profile.md differs from .pr-ready/.profile.generated.md (your hand-written row)".
4. **Notes:** each `unclear` field and what text would settle it; commands seen outside CI and not written; a missing host CLI.
5. **The gate question:** "Save this to `.pr-ready/profile.md`? Approve, or tell me what to change."

Then stop and wait for the dev's answer. If the dev asks for changes, apply them to the merged draft only, show the complete draft again and ask again.

## Step 5: Save (after approval only)

1. Create `.pr-ready/` if needed. Write `profile.md` with the approved draft and `.profile.generated.md` with the generated draft from Step 2, both UTF-8 with LF line endings.
2. Check that the profile parses: from the repo root run
   `<py> -c "import sys, json; sys.path.insert(0, sys.argv[1]); from prlib.profile import read_profile; print(json.dumps(read_profile('.')))" <scripts>`
   Pass `<scripts>` as the argument, never inside the Python string. The `policy` values must match the draft and `warnings` must be empty; otherwise fix the format, show the corrected draft, ask again, and re-save once it is approved.
3. Append to the evidence log: `<py> <scripts>/evidence.py add --kind note --text "pr-setup saved .pr-ready/profile.md; kept: <sections or none>; updated: <sections or none>"`. If it exits 2 (for example no commits yet), say so and go on.
4. Do not stage or commit. Tell the dev that `profile.md` and `.profile.generated.md` can be committed together to share the profile with the team, and that the choice is theirs.

Final report, in this order: draft shown, the dev's approval, the files written, the sections kept and why, and the `unclear` fields left for the dev.

## Gates used

From `references/human-gates.md`:

- **Before any edit:** the save gate in Step 4. Saving the profile is an edit; it needs approval of the complete draft, and a changed draft needs a new approval.
- **Any remote action:** none is taken. Do not push, fetch, or call `gh`, `glab`, `az` or `bb` beyond what `detect_platform.py` probes.
- **Never:** read, write or run credentials (reference CI secrets by name only); call deployed environments; put real customer data in the profile.

Rule precedence (`references/rule-precedence.md`): the project's own policy wins. Record it faithfully with its quote; do not soften `forbidden` or upgrade `unclear` to suit pr-ready's defaults.
