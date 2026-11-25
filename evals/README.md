# pr-ready evals

Evals prove a skill changes behaviour: the same task is run by fresh subagents
**without** and **with** the skill, and a grader scores each run against a rubric.

## Files

- `evals/<skill>/cases.json`

  ```json
  {"cases": [{"id": "...", "fixture": "...", "prompt": "...",
              "rubric": ["yes/no observable statement"], "runs": 3}],
   "triggers": {"should": ["..."], "should_not": ["..."]}}
  ```

  An optional `"skill"` names the skill the `with` prompt points at, when it
  differs from the folder name (`evals/showcase/` runs `pr-ready`).
  Every rubric item must be a yes/no statement a grader can check from the run's
  final report, `git status --porcelain` and `git log --oneline`.
- `evals/fixtures/<name>.py` defines `build(dir)`; `fixtures/lib.py` provides
  `make_repo(dir, steps, remote=None)`, a deterministic repo builder (branch
  `main`, fixed author, fixed commit dates, `core.autocrlf=false`). A step is
  `{"files": {rel: str|bytes}, "delete": [rel], "commit": msg, "branch": name}`;
  only `commit` is required.
- `evals/results/<skill>.md` holds the summary; raw reports go to
  `evals/results/raw/<skill>/<case>-<mode>-<n>.md`.

## Procedure (the controller runs this)

For each case, each mode (`without`, `with`) and each run `n` in 1..`runs`:

1. Build a fresh fixture and get the runner prompt. Use a new `OUT_DIR` for
   every run: `<system temp>/pr-ready-evals/<skill>/<case>-<mode>-<n>`. Create
   `evals/results/raw/<skill>/` once before saving reports.

   ```
   python evals/setup.py SKILL CASE_ID {with,without} OUT_DIR
   ```

   `OUT_DIR` must not exist or be empty (otherwise exit 2). A failed setup can
   leave `OUT_DIR` non-empty: delete it before rerunning. In `with` mode the
   plugin's `skills/`, `scripts/` and `references/` are copied to
   `OUT_DIR/.claude/` (sibling layout, so `../../scripts` resolves; no
   `__pycache__`), and `.claude/` is added to `.git/info/exclude` so the copy
   is neither committed nor shown as an untracked change.
2. The stdout of `setup.py` is the **runner prompt**; give it verbatim to a
   fresh subagent. It already contains:
   - both modes: "Work only inside `<OUT_DIR>`; it is a git repository. Do not
     modify anything outside it."
   - `with` only: "Before starting, read `<OUT_DIR>/.claude/skills/<skill>/SKILL.md`
     and follow it; its scripts and references are at `<OUT_DIR>/.claude/scripts`
     and `<OUT_DIR>/.claude/references`." (A subagent runs inside the
     controller's session and does not auto-load skills from the fixture, so
     the prompt points at the file.) `without` mentions no skills.
   - then the case prompt.
3. Save the subagent's final report to
   `evals/results/raw/<skill>/<case>-<mode>-<n>.md`.
4. Dispatch a grader subagent with the case rubric, that final report, and the
   output of `git -C <OUT_DIR> status --porcelain` and
   `git -C <OUT_DIR> log --oneline`. It answers every rubric item
   `PASS` or `FAIL` with a quote from that evidence. Exact grader prompt:

   ```
   You are grading one eval run. Answer each rubric item with PASS or FAIL
   and a short verbatim quote from the evidence below that justifies it. If
   the evidence does not show the item, answer FAIL. Do not be lenient.

   RUBRIC:
   <numbered rubric items from cases.json>

   FINAL REPORT OF THE RUN:
   <contents of the saved report>

   git status --porcelain:
   <output>

   git log --oneline:
   <output>

   Reply with one line per item: "<n>. PASS|FAIL - \"<quote>\"".
   ```

## Pass rule and results

A **run** passes when every rubric item is `PASS` in that run. A **case**
passes in a mode when at least 2 of its 3 runs pass. Record the baseline
(`without`) before writing the skill, then iterate the skill until every case
passes `with`. Summarise in `evals/results/<skill>.md`, one cell per mode as
`k/3` (runs passed):

```
| case | without | with |
|------|---------|------|
| greet | 1/3 | 3/3 |
```

## Human gates

Case prompts may contain lines `dev answers: ...`. They are pre-supplied in the
case prompt, and `setup.py` adds to the runner prompt (both modes) one sentence
telling the subagent: at a human gate, write the question you would ask the
dev, then continue as if the dev gave the pre-supplied answer; if a gate comes
up with no pre-supplied answer, stop there and report the question.

## Trigger evals

Separate from the behaviour runs: for each phrase in `triggers.should` /
`triggers.should_not`, ask a fresh subagent, given only the list of skill names
and descriptions, which skill it would use. Every `should` phrase must select
this skill; no `should_not` phrase may.
