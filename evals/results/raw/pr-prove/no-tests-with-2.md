## pr-prove report: feat/slugify (base: local main, last-fetched state, not fetched)

**1. Verdict:** Nothing proven: no tests or CI.

**2. Commands** (all from repo root; interpreter `<python>`, shown as `python`)

| Command | Where | Exit | Counts |
|---|---|---|---|
| `python .claude/scripts/count_lines.py --json` | repo | 0 | total 5, budget 500, over_budget false (textkit/text.py +5) |
| `python .claude/scripts/classify_risk.py --json` | repo | 0 | level normal, reasons none |
| `git status --porcelain; git log --oneline main..HEAD` | repo | 0 | status empty; log: only `65e6911 Add slugify` |

No CI run, no merge worktree, no test run. The profile lists reproduce CI, tests, build and generated check as `none found`, and the README says "No test suite yet." Level is `normal`, so this is not a skip at `trivial`.

**3. Generated files:** none declared in the profile. Nothing to compare.

**4. Mutations:** skipped. There are no tests, so no mutation could be killed or survive. Applying them would prove nothing.

**5. Findings**
- New behaviour `slugify(text)` in `textkit/text.py` (`"-".join(text.lower().split())`) has no asserting test, and no test suite exists. This is a finding.
- Suggested tests, as text only (I wrote none). Only an input where the code's result is settled by the docstring ("Lowercase, hyphen-separated slug") can have an expected value:
  - `slugify("Hello World") == "hello-world"`. Source: docstring.
  - `slugify("  a  b ") == "a-b"` is consistent with "hyphen-separated" but the docstring does not state it, so it needs your confirmation.
- Diff is 5 lines against a budget of 500. Not over budget.

**6. Unverified** (recorded in the evidence log)
- `slugify` behaves as intended: unverified. No test covers it and no test or CI command exists.
- `slugify` punctuation and accent handling: correctness not defined by the dev; not proven.

**7. Questions for the dev**
- What should `slugify` do with input the docstring does not cover? I ran it read-only to show what it does today:
  - `"Hello, World!"` gives `"hello,-world!"`. Should punctuation be stripped?
  - `"Café Olé"` gives `"café-olé"`. Should accents be transliterated (`cafe-ole`), kept, or removed?
  - `"a_b-c"` gives `"a_b-c"`. Should underscores become hyphens?
  - Leading, trailing and repeated whitespace collapse to single hyphens. Is that intended?
  
  I will not choose these for you. Tell me the intended results. Writing the tests is a separate task you would need to ask for.
- Do you want tests added (and a test command in `.pr-ready/profile.md`)? That is an edit I did not make. `pr-setup` could update the profile.

**8. State**
- Evidence file: `<tmp>/pr-ready-evals/pr-prove\no-tests-with-2\.pr-ready\evidence\feat-slugify-8a51dc.md`
- Final `git status --porcelain`: empty (the evidence folder is git-ignored).
- No commit added. No branch change, no stash, no worktree created, no remote action.
- Gates: the "new-behaviour tests" gate was asked above (item 7). No dev answer was pre-supplied for it, so that question is left open.
