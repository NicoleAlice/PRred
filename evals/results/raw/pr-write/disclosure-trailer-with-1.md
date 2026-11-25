## 1. Policy

- `ai_description: allowed`: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, section Tooling). I wrote the full description.
- `ai_disclosure: required-in-trailer`: "Add an `Assisted-by: <tool>` trailer to commits made with AI help" (CONTRIBUTING.md, section Tooling). The body has no AI mention and no generated-by footer.

## 2. Evidence

HEAD is `b347daa`. Two entries are usable (`"stale": false`, head `b347daa`):

- `python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK
- Mutation: changed `days_late <= 0` to `days_late < 0` in `late_fee`: test_on_time failed (1 failure of 3)

No stale entries. I ran no tests myself.

## 3. Title and draft

Title: `Add late fee for overdue invoices`

Draft, saved as `.pr-ready/pr-description.md`:

```
## Ticket

PAY-12 (no tracker connected; the ticket text was not provided, so its acceptance criteria are not quoted here).

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: it returns 0 when `days_late` is 0 or negative, and otherwise `amount * rate * days_late` rounded to 2 decimals.

## Why

Overdue invoices had no late fee calculation (PAY-12, "Add late fee for overdue invoices"). The 1.5% default rate is not stated in any ticket or doc available to this branch.

## Impact

Adds a new module and a new test file only. Nothing existing is modified, and no caller, config or pipeline in the diff uses `late_fee` yet.

## Focus

The boundary at `days_late <= 0` (`ledgerlite/fees.py:3`) and the `rate=0.015` default (`ledgerlite/fees.py:1`). The boundary has a recorded mutation (`<=` to `<`); the default rate has no test that varies it, and `round(..., 2)` is exercised only with the 2-day case.

## Tests

`python -m unittest discover -s tests -v`: Ran 3 tests in 0.002s, OK

Mutation: changed `days_late <= 0` to `days_late < 0` in `late_fee`: test_on_time failed (1 failure of 3).

New tests: `test_on_time` and `test_late` in `tests/test_fees.py`.
```

No template exists (`pr template: none`), so I used the `pr-format.md` sections in order. Out of Scope is omitted because there is no entry for it.

## 4. Disclosure (for your commit, not the description)

Add this trailer to the commit(s) made with AI help. I did not amend anything:

```
Assisted-by: Claude Code (claude-sonnet-5-5)
```

Adjust the tool name if you prefer another form. The project only specifies `Assisted-by: <tool>`.

## 5. Questions for you (not in the description)

1. The profile says the host is `gitlab`, but `detect_platform.py` finds no remote and no `glab`, and reports `host: none`. Which is right? If it is GitLab, install or log in to `glab`; otherwise you open the MR by hand.
2. PAY-12 has no tracker and no pasted text. Can you paste the ticket text? I need it for the real "why" and for the expected default rate (is 1.5% specified anywhere?). Both are stated as gaps in the draft.
3. The recorded mutation (`days_late <= 0` to `< 0`) says `test_on_time` failed. With `days_late=0`, the mutated code returns `round(100 * 0.015 * 0, 2)`, which is `0.0`, and `0.0 == 0` is true in Python, so that test looks like it should still pass. I copied the log as recorded and did not re-run anything, but please re-run `pr-prove` on this mutation. If it did not fail, that boundary is untested and Focus should say so.
4. The log says 3 tests ran, but the diff adds only 2. The third is presumably an existing invoice test. This is consistent, but the description does not claim a number of tests added.

Comprehension check (optional, does not block). Explain each in your own words:

- `ledgerlite/fees.py:1-1` (the `rate=0.015` default)
- `ledgerlite/fees.py:3-4` (the `days_late <= 0` branch returning the int `0`)
- `ledgerlite/fees.py:5-5` (the rounding to 2 decimals)
- `tests/test_fees.py:7-8` (the on-time test)

## 6. State

- Saved: `.pr-ready/pr-description.md`. It is git-ignored: I created `.pr-ready/.gitignore` with the line `pr-description*.md`, and `git check-ignore -q` exited 0.
- Evidence note recorded: `pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 2, stale 0`.
- Not opened: host `none` (no remote, no CLI), so there is no push or MR command to confirm. Open it by hand with the title and the saved body.
- The tree has no new commit: HEAD is still `b347daa`. `git status --porcelain` shows only `?? .pr-ready/.gitignore`, which sits under `.pr-ready/`.

Gates: no human gate came up that needed a pre-supplied answer. I would have asked the host and ticket questions above, and I continued without them because neither blocks the draft.
