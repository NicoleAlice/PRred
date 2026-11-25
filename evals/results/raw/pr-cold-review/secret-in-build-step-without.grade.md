## Run 1
1. PASS - "A top-level `variables:` block applies to every job. That means the `build` job now gets DEPLOY_TOKEN in its environment."
2. FAIL - "The branch adds this at the top level of .gitlab-ci.yml:" (quoted line, but no line number given; actual line is 6)
3. PASS - "The `build` job does not need it."
4. PASS - "There is one real problem, and it is a secret exposure."
5. PASS - "Verdict: do not open the PR as is."
6. PASS - "Review of branch feat/ci-pip-cache (1 commit, 09a972b "Cache pip downloads in CI")"
run 1: FAIL

## Run 2
1. PASS - "It is declared globally, so every job gets it, including the `build` job."
2. FAIL - "The diff adds a global `variables:` block:" (quoted block, no line number given; actual line is 6)
3. PASS - "Only `deploy` needs it, and that job runs on `main` only."
4. PASS - "It widens who can see the secret."
5. PASS - "Don't open the PR as is."
6. PASS - "The working tree is clean."
run 2: FAIL

## Run 3
1. PASS - "Top-level `variables:` apply to every job."
2. FAIL - "## Problem: the commit also adds `DEPLOY_TOKEN` to the build job" (code block quoted, no line number given; actual line is 6)
3. PASS - "Only `deploy` needs the token, since `tools/deploy.py` reads it from the environment."
4. PASS - "The token is exposed to the wrong job."
5. PASS - "Do not open the PR as is."
6. PASS - "Scope: one commit (09a972b "Cache pip downloads in CI") against main."
run 3: FAIL

case: 0/3
