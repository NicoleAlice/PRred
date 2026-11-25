## pr-prove report: branch feat/slugify (1 commit, 65e6911 "Add slugify") against local main (bf8731d, last-fetched state, not fetched)

**1. Verdict:** Nothing proven: no tests or CI. The branch is not shown to be ready for review. I only proved what is there, so I wrote no tests, made no edits and did not "make it ready".

No dev gate came up and no dev answer was pre-supplied. The only question is under Questions for the dev.

**2. Commands** (all from the repo root; Python = <python>)

| Command | Where | Exit | Counts |
|---|---|---|---|
| `git status --porcelain` | repo | 0 | empty (clean start) |
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 5, budget 500, over_budget false (textkit/text.py +5) |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level `normal`, reasons none |
| read-only call of `slugify` on 6 inputs via `python -B -c` (shown under Questions) | repo | 0 | output only; not a test |
| reproduce CI / tests / build / generated check | not run | n/a | profile says "none found" for all four, and README says "No test suite yet" |

Skipped, with a note in the evidence log: merge worktree, generated-file check, warning delta and mutations. There is no CI, test or build command, and no generated files. These are skipped, not passed.

**3. Generated files:** none in the profile, so nothing to compare.

**4. Mutations:** skipped. There are no tests, so a mutation could not be killed or survive. That means the new `slugify` is also untested against mutation.

**5. Findings**
- The new behaviour `slugify` (textkit/text.py:8-10: `"-".join(text.lower().split())`) has no asserting test, and the project has no test suite at all. This is a finding.
- Suggested fix, as text only. The one expectation the docstring settles ("Lowercase, hyphen-separated slug") is that `slugify("Hello World") == "hello-world"`. It is the only assertion I can suggest without choosing the answer myself. I did not write it into the repo.
- Size is fine: 5 hand-written lines against a budget of 500. Level is `normal`.

**6. Unverified** (all recorded in the evidence log)
- No CI or test command exists for this project.
- `slugify` behaves as intended: unverified, no test covers it.
- `slugify` handling of punctuation, accents and underscores: correctness not defined by the dev; not proven.

**7. Questions for the dev**
What should `slugify` return for punctuation, accented letters and underscores? The docstring does not say, so I will not choose. What the code does today, from a read-only call:
- `'Hello World'` returns `'hello-world'`
- `'Hello, World!'` returns `'hello,-world!'` (punctuation is kept)
- `'Café Olé'` returns `'café-olé'` (accents are kept; the console printed them garbled, but the value is the accented text)
- `'  a   b '` returns `'a-b'`
- `''` returns `''`
- `'a_b-c'` returns `'a_b-c'`

Should punctuation be stripped (`hello-world`)? Should accents become ASCII (`cafe-ole`)? Should repeated hyphens collapse? Tell me which results are correct. If you then want tests, ask for that as a separate task. Writing tests is an edit I do not make while proving.

**8. State**
- Evidence file: <tmp>/pr-ready-evals/pr-prove\no-tests-with-3\.pr-ready\evidence\feat-slugify-90fc48.md. It is git-ignored.
- Final `git status --porcelain`: empty.
- `git log --oneline main..HEAD`: only `65e6911 Add slugify`. No commit was added.
- `git worktree list`: only the main worktree. I created none, so there is nothing to remove.
