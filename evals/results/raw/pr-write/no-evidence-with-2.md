(Saved by the controller: the run returned its report as its final message instead of writing this file.)

# pr-write report (branch feat/PAY-12-late-fee)

**Gates:** No "dev answers" lines were supplied and none were needed. The one gate was the ticket text. The question I would ask: "Can you paste the PAY-12 ticket text? The tracker is none and I only have the key from the branch name."

**1. Policy**
- `ai_description: allowed`. The quote is "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). I wrote a full description, not a facts list.
- `ai_disclosure: none`. The quote is "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). The body has no AI mention, no footer and no trailer.
- No PR template exists (`pr template: none`), so I used the `pr-format.md` sections in order. There is no Out of Scope section because there was no entry for it.

**2. Evidence**
- Evidence is missing. `evidence.py show --json` returned no entries for HEAD `5027869`.
- Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again.
- The Tests section says so, and the body has no test counts and no "passes", "tested" or "verified".

**3. Title**

`Add late fee for overdue invoices (PAY-12)`

The profile's commit format is free-form. The title is not in the body.

**Draft** (saved at `.pr-ready/pr-description.md`):

```
Ticket: PAY-12

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: it returns 0 when `days_late` is 0 or negative, otherwise `amount * rate * days_late` rounded to two decimals, so the fee grows linearly per day late. Adds `tests/test_fees.py` with `test_on_time` and `test_late`.

## Why

PAY-12 asks for a late fee on overdue invoices (commit "Add late fee for overdue invoices"). The ticket text was not available when this was written, so the stated problem and acceptance criteria are not repeated here.

## Impact

Nothing else is reached: `late_fee` is a new function in a new module, and no existing code in `ledgerlite/` imports or calls it yet. No config, contract or pipeline changes.

## Focus

The weakest point is the default `rate=0.015`, applied per day late: it is not stated in any ticket or doc available here, so it is checked against nothing. The rounding (`round(..., 2)`) and the `days_late <= 0` boundary were checked by reading only; the only late case in the tests is `late_fee(100, 2) == 3.0`.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.

New tests are in `tests/test_fees.py`: `test_on_time`, `test_late`.
```

**4. Disclosure:** Nothing to add. The policy is `none`.

**5. Questions for you (not in the description)**
- Is `PAY-12` the right ticket, and what does it say? I gave the key only and did not guess its content.
- What should the default rate of 0.015 mean? The code applies 1.5% of the amount per day late (linear, not compounding). No ticket or doc states this.
- Should the on-time case return the int `0` or `0.0`? The code returns int `0` for `days_late <= 0`, and the test compares it with `0`.

Comprehension-check hunks. Please explain each in your own words:
- `ledgerlite/fees.py:1-1`, the default `rate=0.015`
- `ledgerlite/fees.py:3-4`, the `days_late <= 0` early return of `0`
- `ledgerlite/fees.py:5-5`, `round(amount * rate * days_late, 2)`
- `tests/test_fees.py:10-11`, the expected `3.0` for `late_fee(100, 2)`

**6. State**
- Saved to `.pr-ready/pr-description.md`. `.pr-ready/.gitignore` was untracked, so I created it with the line `pr-description*.md`. `git check-ignore` exits 0 for the draft.
- I recorded an evidence note: "pr-write: description saved to .pr-ready/pr-description.md; template none; usable evidence 0, stale 0".
- Not opened, awaiting confirmation. The host is gitlab and `glab` is the adapter. I have not checked whether `glab` is installed or logged in. The branch has no upstream that I checked. Each command needs your "Run this?" before I run it.
  1. `git push -u origin feat/PAY-12-late-fee`
  2. `glab mr create --draft --target-branch main --title "Add late fee for overdue invoices (PAY-12)" --description "$(cat .pr-ready/pr-description.md)"`
- There is no new commit (HEAD is still `5027869`). `git status --porcelain` shows only `?? .pr-ready/.gitignore`. The evidence note went into the ignored evidence file. I ran no tests, builds or mutations.
