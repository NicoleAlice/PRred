# Human gates

These hold in every skill and at every level. A skill's own instructions never override them. When a gate applies, stop and wait for the dev's answer in this conversation. Silence, an earlier "go ahead" for a different step, or your own judgment is not approval.

## Stop and ask

- **Before any edit:** show the plan and stop and ask: "Approve this plan?" Edit no file until the dev says yes. A changed plan needs a new approval.
- **New-behaviour tests:** stop and ask the dev what "correct" means (the expected output or assertion). You write the mechanics; you never choose an assertion and then confirm your own code meets it.
- **Auth, authorization, secrets, caller input:** tell the dev a person must read this code line by line. List each file and line range, then stop and ask for confirmation that it was read.
- **Any remote action:** push, open a PR/MR, change a base, update a branch, trigger CI. Show the exact command and stop and ask: "Run this?" One confirmation covers one command, not the next one.
- **Lowering the risk level:** you may propose raising it; lowering needs the dev.
- **Installing dependencies:** the profile's `setup:` step (or any install) changes the environment and needs the network. Show the exact command and stop and ask before running it; without a yes, record it as `unverified`.
- **Same test failing the same way twice:** stop. Reframe the problem or ask the dev to read the error. Do not make a third attempt.

## Never

- Read, write, rotate or run credentials. A person sets them; you reference them by name.
- Call deployed environments. The first real run against a shared environment is a person's.
- Close and reopen a PR (to restart CI or for any other reason).
- Force-push a branch someone has reviewed.
- Put real customer data or production values in tests, prompts or PR text. Use synthetic fixtures.
