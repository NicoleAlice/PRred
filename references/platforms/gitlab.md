# Platform: GitLab (`glab`)

Every remote action here (push, open MR, retarget, update branch, trigger a pipeline) needs the dev's confirmation first: show the exact command and stop and ask. Keep the description in a file (`F` below) and never close and reopen an MR.

## Commands

| Task | Command |
|---|---|
| Fetch an issue | `glab issue view <number>` |
| Open a draft MR, body from a file | `glab mr create --draft --target-branch <base> --title "<title>" --description "$(cat F)"` |
| Retarget an MR | `glab mr update <number> --target-branch <new-base>` |
| Update the branch with its base (safe default) | `git fetch origin && git merge origin/<target>`, then push after the dev confirms. No history rewrite, so safe for reviewed branches. |
| Update the branch by rebase | `glab mr rebase <number>` rewrites the source branch history. Only for a branch nobody has reviewed yet, and only after the dev confirms. |

Without `glab`, or without a login, fall back to `none.md`. Never handle tokens yourself.

## Stack behaviours

A stack is merged from the bottom, with merge commits for parents.

| Behaviour | What to do |
|---|---|
| Pipelines on an MR whose target is another branch | Depends on the project's pipeline rules and merge request pipeline settings: check in your host settings. Reproduce CI locally for every MR in the stack regardless. |
| Parent branch deleted after merge | Whether child MRs retarget automatically: check in your host settings. Verify the target after every merge; retarget with `glab mr update` if needed (confirm first). |
| Editing the target while MRs are stacked on it | Check in your host settings. Re-read the diff after any target change. |
| Description loss | Whether editing or retargeting keeps the description: check in your host settings. Keep it in a file, compare after each edit, and restore with `glab mr update <number> --description "$(cat F)"` (confirm first). |
