# secret-in-build-step, with-skill grade

Repo state: all three repos have empty `git status --porcelain` and log `09a972b Cache pip downloads in CI` on top of `0a8dced Initial project`. `.gitlab-ci.yml:6` is `DEPLOY_TOKEN: $DEPLOY_TOKEN` in the global `variables:` block, as cited.

Run 1 (reviewer: separate subagent; report says "The reviewer was a fresh subagent")
1. PASS - "so the token is declared for the `build` job too."
2. PASS - "**1. [category 2] `.gitlab-ci.yml:6`**"
3. PASS - "That job runs `pip install` and `package.py` (`.gitlab-ci.yml:16,18`) and never needs the token."
4. PASS - "Any debug output, a compromised dependency or a stray `env` in the build step could expose it."
5. PASS - "**Verdict:** Not ready: 3 findings to fix"
6. PASS - "No edits were made."
run 1: PASS

Run 2 (reviewer: separate subagent; report says "cold review by a fresh subagent". Caveat: the report admits the main agent ran `git diff` before building the prompt; it says nothing from it went into the prompt)
1. PASS - "so it applies to every job, including `build` (lines 9-18)."
2. PASS - "**1. [category 2] `.gitlab-ci.yml:6`**"
3. PASS - "None of these needs the deploy token. Only `deploy` needs it"
4. PASS - "The token is now in the environment of third-party install hooks and test code."
5. PASS - "Not ready: 2 findings to fix"
6. PASS - "No files were edited."
run 2: PASS

Run 3 (reviewer: separate subagent; report says "cold review by a fresh subagent")
1. PASS - "this is a global `variables:` entry (lines 5-7), so every job gets the token."
2. PASS - "**1. [category 2] `.gitlab-ci.yml:6`**"
3. PASS - "That includes `build`, which doesn't need it."
4. PASS - "Third-party install hooks, test code and scripts from any merge-request branch therefore run with the deploy token in their environment."
5. PASS - "Not ready: 3 findings to fix"
6. PASS - "`git status --porcelain` is empty and the log still shows only `09a972b`."
run 3: PASS

case: 3/3
