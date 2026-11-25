## Report to the developer (pr-write, branch feat/PAY-12-late-fee)

**Gates:** none came up that needed a pre-supplied answer. Nothing was pushed or opened.

### 1. Policy
- ai_description: allowed. Quote: "AI-written text is welcome if the author has read it" (CONTRIBUTING.md, Tooling). Output chosen: full description.
- ai_disclosure: none. Quote: "Contributors need not mention the tools they used" (CONTRIBUTING.md, Tooling). The body has no AI mention and no footer.
- Template: none.

### 2. Evidence
Evidence missing. `evidence.py show --json` returned no entries for HEAD `5027869`. Run `pr-prove` to record evidence for this HEAD, then run `pr-write` again. I ran no tests myself. The Tests section says the evidence is missing and gives no counts and no "passes".

### 3. Title
`Add late fee for overdue invoices`

(This is the commit subject. Commit format is free-form. The ticket text is not available, so I used the commit's words.)

### Draft (saved to `.pr-ready/pr-description.md`)

```
## Ticket

PAY-12 (key from the branch name; no tracker connected, ticket text not available)

## What

Adds `late_fee(amount, days_late, rate=0.015)` in `ledgerlite/fees.py`: the fee is `amount * rate * days_late` rounded to 2 decimals, and 0 when `days_late` is 0 or negative.

## Why

Overdue invoices had no late fee calculation (PAY-12, "Add late fee for overdue invoices").

## Impact

Reaches nothing beyond the two files named: `late_fee` is a new function in a new module, and nothing in the diff calls it or changes `ledgerlite/invoice.py`.

## Focus

The default `rate=0.015` (1.5% per day, simple not compounding) is the least certain part: it is not stated in any ticket or doc available here, and it was read in the diff only, not checked against a requirement. The rounding uses Python's `round(..., 2)` on a float product.

## Tests

Evidence missing for `5027869`: no recorded run for this commit. Run `pr-prove` before review.

New tests are in `tests/test_fees.py`: `test_on_time` and `test_late`.
```

### 4. Disclosure
None needed (ai_disclosure: none). No trailer.

### 5. Questions for you (not in the description)
- What is the intended rate? Is 1.5% per day, simple (not compounding), what PAY-12 asks for? It is not in the repo. I left it in Focus as a stated gap.
- Paste the PAY-12 text, or connect a tracker, so Why can use the ticket's own words. The host in the profile is `gitlab`, but `detect_platform.py` found no remote, and `glab` is not installed.
- Comprehension check, explain each in your own words:
  - `ledgerlite/fees.py:1-1` (default `rate=0.015`)
  - `ledgerlite/fees.py:3-4` (`days_late <= 0` returns 0)
  - `ledgerlite/fees.py:5-5` (`round(amount * rate * days_late, 2)`)
  - `tests/test_fees.py:11-11` (the `3.0` expectation for `late_fee(100, 2)`)

### 6. State
- Saved: `.pr-ready/pr-description.md`. Created `.pr-ready/.gitignore` with `pr-description*.md`. `git check-ignore` exits 0.
- Evidence note recorded in the evidence log.
- Not opened. No `glab` and no remote, so I am only printing the text. Open the MR by hand.
- The tree has no new commit (HEAD still `5027869`). The only new untracked path is `.pr-ready/.gitignore`. The ignored `.pr-ready/` files are the draft and the evidence log.
- Diff size: 16 hand-written lines, within the 500 budget.
