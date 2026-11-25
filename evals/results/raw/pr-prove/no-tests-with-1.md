I ran pr-prove on `feat/slugify`. The branch has no tests, no CI and no build command, so I could not prove it works, and it is not ready for review as it stands.

## 1. Verdict
**Nothing proven: no tests or CI.** There are 2 findings and 2 unverified items. The change itself is small: `slugify` was added to `textkit/text.py`.

## 2. Commands
I used Python 3.14 (`<python>`) as `python`.

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 5, budget 500, over_budget false |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, small true, no reasons |
| `git status --porcelain; git log --oneline main..HEAD` | repo | 0 | status empty; log shows only `65e6911 Add slugify` |

I did not create a merge worktree and ran no test or CI command. The profile lists reproduce CI, tests, build and generated check all as "none found", and the README says "No test suite yet".

## 3. Generated files
The profile lists none, so there is nothing to compare. I recorded this as skipped, not as passed.

## 4. Mutations
Skipped: there are no tests, so a mutation could not be caught by anything. The rule says to skip when no tests exist.

## 5. Findings
1. **New behaviour with no test.** `slugify` in `textkit/text.py` has no test. It is `"-".join(text.lower().split())`, and nothing in the project asserts what it returns.
2. **Project has no test or CI command at all.** Nothing could be run on the merge result.

Not findings: the diff is 5 of 500 budgeted lines, and the risk level is `normal`.

Suggested fix, as text only (I wrote no tests): add a test runner, then assertions. The docstring ("Lowercase, hyphen-separated slug") settles only simple cases. Based on that docstring, you could assert `slugify("Hello World") == "hello-world"`.

## 6. Unverified
- No CI or test command exists for this project.
- `slugify` behaves as intended: unverified, no test covers it.
- `slugify` correctness for inputs beyond the simple case: not defined by you, not proven (see section 7).

## 7. Questions for the dev
The docstring does not say what `slugify` should return for punctuation, underscores, non-ASCII, repeated hyphens or empty input. I did not pick an answer. I ran the function read-only, and it currently returns:

| Input | Output |
|---|---|
| `"Hello, World!"` | `"hello,-world!"` (punctuation kept) |
| `"a-b - c"` | `"a-b---c"` (hyphens not collapsed) |
| `"snake_case"` | `"snake_case"` (underscore kept) |
| `"Café Olé"` | `"café-olé"` (accents kept) |
| `""` | `""` |
| `"  a   b "` | `"a-b"` |

Which of these are correct, and which should change? For example, should `"Hello, World!"` give `"hello-world"`, and should accents be stripped?

Gate answers: no dev answers were supplied, and none were needed beyond these questions. I wrote no tests or code.

## 8. State
- Evidence log: `<tmp>/pr-ready-evals/pr-prove\no-tests-with-1\.pr-ready\evidence\feat-slugify-3bb19a.md`
- `git status --porcelain` is empty.
- No commit was added: `main..HEAD` is still only `65e6911 Add slugify`.
- No worktrees were created, so none needed removing.
