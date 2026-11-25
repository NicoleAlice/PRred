# Platform: none (no host, or no CLI)

Take no remote action: no push, no PR, no base change, no CI trigger. The dev does the remote steps by hand from your outputs. Write every output as a plain text file under `.pr-ready/` (never the repo root, so nothing is committed by accident) so the dev can paste it.

The ticket: the dev pastes its text; do not guess its content.

## Outputs

1. **The description:** the file `pr-write` saved, in the `pr-format.md` section order: `.pr-ready/pr-description.md` for a single PR, `.pr-ready/pr-description-<n>.md` for PR `n` of a stack. When the policy requires a facts list instead (see `rule-precedence.md`), it is `.pr-ready/pr-description-facts.md`. One line per paragraph.
2. **The ordered branch list** (a stack only): one line per PR, bottom of the stack first: `<n>. <branch> -> base <base-branch>`. The first PR's base is the project's base branch; each later PR's base is the previous PR's branch.
3. **The merge order** (a stack only): the same list as a numbered sequence, with the reminders below.

Write the branch list and the merge order together to `.pr-ready/pr-description-order.md`, so the `pr-description*.md` line in `.pr-ready/.gitignore` covers it. If that ignore file is tracked and lacks the line, print them instead of saving, as `pr-write` does.

## Reminders to include with the merge order

- Merge from the bottom, one PR at a time. Before each merge, test the next PR on top of what its base will be after the merge.
- Use merge commits for stacked parents: a squashed parent makes its commits reappear as changes in every PR stacked on it.
- After each merge, check what the next PR targets and retarget it by hand if the host did not.
- Never close and reopen a PR, and never force-push a reviewed branch.
