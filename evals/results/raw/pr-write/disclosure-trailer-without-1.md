# Report: PR description for feat/PAY-12-late-fee

I stopped at one human gate (the disclosure trailer) and have no answer for it. The description below is ready, except for that gate.

## Gate: AI disclosure trailer (no pre-supplied answer)

CONTRIBUTING.md (Tooling) says: "AI-written text is welcome if the author has read it. Add an `Assisted-by: <tool>` trailer to commits made with AI help."

The only commit on the branch is `b347daa Add late fee for overdue invoices`. It has no `Assisted-by:` trailer, and its message is a single line.

Question I would ask the dev:

> This project asks for an `Assisted-by: <tool>` trailer on commits made with AI help, and `b347daa` has none. Was AI used on that commit? If yes, which tool name should go in the trailer, and may I amend the commit message (this rewrites the commit hash, so you would need to force-push the branch)? If no, I'll leave the commit alone and put no AI statement in the PR.

I did not amend the commit, guess a tool name, or add an AI line to the description. The project only asks for the disclosure in commit trailers, so the description needs no disclosure line either way.

## Proposed PR title

Add late fee for overdue invoices (PAY-12)

## Proposed PR description

```markdown
## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`. It returns the fee for an invoice paid `days_late` days after its due date.

- If `days_late <= 0`, the fee is `0`.
- Otherwise the fee is `amount * rate * days_late`, rounded to 2 decimals. The default rate is 1.5% per day, simple (not compounded).

Example: `late_fee(100, 2)` returns `3.0`.

The function is standalone. Nothing calls it yet, and it does not change `Invoice.total`.

## Tests

Added `tests/test_fees.py` with two cases: on time (`late_fee(100, 0) == 0`) and two days late (`late_fee(100, 2) == 3.0`).

`python -m unittest discover -s tests -v` ran 3 tests, all passing, at b347daa.

I also changed the boundary `days_late <= 0` to `days_late < 0`. `test_on_time` then failed (1 failure of 3), so the on-time test does cover that boundary.

## Notes for review

- The 1.5% daily default rate is a constant in the signature. Please confirm that is the intended default for PAY-12.
- There are no tests for a negative `days_late` or for rounding. Negative values go through the same `<= 0` branch as zero.
- I did not run CI. The results above come from a local run of the same command.
```

## Branch facts I checked

- Base is `main`. The branch has 1 commit and 2 files changed, 16 lines added, well under the 500-line budget.
- The profile lists no tracker, no PR template and no risk paths. The tracker is "none", so the PAY-12 key comes only from the branch name and I did not link an issue.
- The host is GitLab, so this is a merge request in practice. The text above works as the MR description.
- Prior approval is not required, because small fixes may be sent without an issue.

## Waiting on you

- The answer to the trailer question above.
- If AI was used and you want the trailer added, I need the tool name. I would then amend `b347daa` with `Assisted-by: <tool>`, or add a new commit if you don't want a history rewrite.
