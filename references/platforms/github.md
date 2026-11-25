# Platform: GitHub (`gh`)

Every remote action here (push, open PR, retarget, update branch, trigger CI) needs the dev's confirmation first: show the exact command and stop and ask. Keep the description in a file (`F` below) and never close and reopen a PR.

## Commands

| Task | Command |
|---|---|
| Fetch an issue | `gh issue view <number> --comments` (add `--repo <owner>/<repo>` outside the repo) |
| Open a draft PR, body from a file | `gh pr create --draft --base <base> --title "<title>" --body-file F` |
| Retarget a PR | `gh pr edit <number> --base <new-base>` |
| Update the branch with its base | `gh pr update-branch <number>` |

Without `gh`, or without a login, fall back to `none.md`: the dev opens the PR from your text outputs. Never handle tokens yourself.

## Stack behaviours

A stack is merged from the bottom, with merge commits for parents.

| Behaviour | What to do |
|---|---|
| CI on a PR whose base is another branch | Whether checks run depends on the workflow's `branches:` filters and your host settings: check in your host settings. Reproduce CI locally for every PR in the stack regardless. |
| Parent branch deleted after merge | Whether the child PR retargets automatically depends on the repository's branch-deletion settings: check in your host settings. Verify the base after every merge; retarget with `gh pr edit` if needed (confirm first). |
| Editing the base while PRs are stacked on it | Check in your host settings. Re-read the diff after any base change. |
| Description loss | Editing or retargeting a PR may drop or alter the description: check in your host settings. Keep the description in a file, compare after each edit, and restore with `gh pr edit <number> --body-file F` (confirm first). |
