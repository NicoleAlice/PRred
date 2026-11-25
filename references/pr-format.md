# PR description format

The diff says how; the description says what changed, why, and where to look. Open the PR as a draft where the host supports it. First check the profile policy (see `rule-precedence.md`): if `ai_description` is `forbidden` or `unclear`, or there is no profile, do not write the description; produce the facts list below.

## Sections

| Section | What goes in it |
|---|---|
| Title | The commit-subject shape, naming what shipped in the ticket's own words, not its purpose |
| Ticket | The link, first line |
| What | One or two sentences, in domain terms |
| Why | The problem behind it, or who asked |
| Impact | What else it reaches: contracts, config, pipelines, other services, the parent branch if stacked |
| Focus | The weakest point, named, with what you checked |
| Out of Scope | Only gaps a reviewer would read as a bug, each with its reason; omit the section otherwise |
| Tests | What you added and how you proved it: commands, counts, mutations and what each one broke |

## Writing rules

1. **Tests are evidence, not intent.** Only counts from entries in the evidence log that are not stale (recorded at the current HEAD). Never a list of what was not run.
2. **No questions to reviewers.** If two readings exist, state what the code does. Open questions go to the dev before the description is written, never into it.
3. **Read the description against the final diff before it goes up.** A plan that changed mid-way still has the old text.
4. **One line per paragraph.** Most hosts render a hard-wrapped line as a break, mid-sentence.
5. **AI attribution follows the project's policy.** Where the project says nothing, keep generated-by footers out of the body. If the project requires disclosure, put it where the project asks (description or trailer).

Keep the description in a file, never only in the host's text box.

## Facts-list format

Used when `ai_description` is `forbidden` or `unclear`, or when there is no profile. The dev writes the description in their own words from these facts. Bullet facts only: no sentences of explanation, no advice, no description prose. Every fact comes from the code, the ticket or a non-stale evidence-log entry. Use exactly these headings, in this order, and keep a heading with `- none` when it has no facts.

```
## What changed
- <file or area>: <fact>

## Why (from ticket)
- <ticket key or link>: <acceptance criterion or stated problem>

## Commands and counts
- `<command>`: <counts printed, from a non-stale evidence entry>

## Mutations
- <mutation>: <test that failed>

## Weakest point
- <the weakest point and what was checked>

## Unverified
- <claim not proved, and why>
```
