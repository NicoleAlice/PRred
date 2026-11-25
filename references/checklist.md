# Checklist before asking for review

`pr-ready` walks this list. For each item, the tagged skill produces the evidence; an item that does not apply at the PR's level is skipped and reported as skipped, not as passed. Levels: `trivial`, `normal`, `risky` (see `rule-precedence.md` and `human-gates.md`: only the dev may lower a level).

- `trivial`: only non-executable files change (`*.md`, `*.txt`, `*.rst`, `*.adoc`, images, `LICENSE*`).
- `normal`: any other change that is not `risky`.
- `risky`: a changed path matches a risk path (built-in or the profile's), or the work handles authentication, authorization, secrets, tokens, caller input or a public contract.

| # | Item | Skill | Levels |
|---|---|---|---|
| 1 | The PR does one task, from one ticket, and its title needs no "and". | pr-plan | trivial, normal, risky |
| 2 | Hand-written lines are within the budget (default 500), measured after building. | pr-prove | trivial, normal, risky |
| 3 | I read the whole diff, and nothing outside the task moved. | pr-write | trivial, normal, risky |
| 4 | I can explain every line, and every new comment says something the code cannot. | pr-write | trivial, normal, risky |
| 5 | Every claim in the code, comments and description was checked against the code or a run. | pr-prove | normal, risky |
| 6 | CI passed on the merge commit, with its counts written down. | pr-prove | normal, risky |
| 7 | Committed generated files match what the build generates, and a contract change has its diff result in the PR. | pr-prove | normal, risky |
| 8 | The build has no new unique warnings compared with the base. | pr-prove | normal, risky |
| 9 | Any new package exists, is the one meant, and its shipped licence was read. | pr-prove | normal, risky |
| 10 | Each new test failed under at least one mutation, and the PR lists them. | pr-prove | normal, risky |
| 11 | Paths a user takes were run end to end, on a local stack when they reach a deployed platform. | pr-prove | risky |
| 12 | A cold review ran, and its findings were checked and fixed or answered. | pr-cold-review | normal, risky |
| 13 | A new convention was announced to the team before the PR. | pr-plan | normal, risky |
| 14 | The description matches the final diff, names the weakest point, and asks the reviewer nothing. | pr-write | trivial, normal, risky |
| 15 | No secret, customer value or local path appears in the code, the commits or the description. | pr-write | trivial, normal, risky |
