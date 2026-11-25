Once-over of feat/truncate (vs main), in clean-diff-without-2

Verdict: looks ready to send to a teammate. I found no blocking issues.

What I did
- Read the full diff (main...feat/truncate): one commit, "Add truncate", 2 files, +35 lines. That is well under the 500-line budget in .pr-ready/profile.md.
- Ran the project's test command, `python -m unittest discover -s tests -v`. All 6 tests pass (1 existing, 5 new).
- The working tree is clean. No stray files, and nothing generated or in a risk path is touched.
- No human gate came up, so I asked the dev nothing.

The change
- textkit/text.py adds `truncate(s, limit)`. It raises ValueError if limit < 3. It returns s unchanged if len(s) <= limit. Otherwise it returns `s[:limit-3] + "..."`, so the result is never longer than limit.
- tests/test_truncate.py adds 5 tests: short string, exact length, long string cut with an ellipsis, result never exceeds the limit, and limit below 3 rejected.

Review notes
- Correctness: the boundaries are right. At len == limit the string is unchanged. At limit == 3 a long string becomes "...". At limit < 3 it raises, because the ellipsis would not fit.
- Tests: the boundary cases are covered, and I traced two likely off-by-one mistakes through them. If `<=` became `<`, the exact-length test would fail. If the `< 3` guard became `< 2`, the limit-2 test would fail. I did not run actual mutations.
- Nits, not blockers:
  - There is no test for limit == 3, the smallest allowed value, which should give "...". The same goes for an empty string.
  - Non-integer or negative limits are not handled explicitly. Negative values do hit the ValueError, so that case is fine.
  - The docstring says "at most `limit` characters", which matches the behaviour.
- Process: the commit message is free-form, which fits the repo history. No issue is needed (prior_approval: not-required). The repo has no AI-disclosure policy (the profile says "unclear"), so there is nothing to add there.

Suggested next step: send it to the reviewer as is. Optionally add a limit == 3 test first.
