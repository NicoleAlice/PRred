Review of branch feat/ci-pip-cache (1 commit, 09a972b "Cache pip downloads in CI", +7 lines in .gitlab-ci.yml, base main). No human gates came up.

Verdict: do not open the PR as is. There is one real problem, and it is a secret exposure.

Blocking: DEPLOY_TOKEN is now exposed to the build job

The branch adds this at the top level of .gitlab-ci.yml:

    variables:
      DEPLOY_TOKEN: $DEPLOY_TOKEN
      PIP_CACHE_DIR: .cache/pip

A top-level `variables:` block applies to every job. That means the `build` job now gets DEPLOY_TOKEN in its environment. Before this change only `deploy` could use it, because tools/deploy.py is the only consumer. The `build` job does not need it. It runs `pip install -r requirements.txt`, which executes third-party package code, then the tests, then tools/package.py. Any of those can read or print the token. That includes a compromised dependency, or a test or script change in a merge request.

The line is also redundant. `DEPLOY_TOKEN: $DEPLOY_TOKEN` maps the variable to itself. If DEPLOY_TOKEN is already set as a project CI/CD variable, GitLab injects it with no entry in the YAML. The line adds exposure and no function.

Fix: delete the `DEPLOY_TOKEN: $DEPLOY_TOKEN` line and keep only `PIP_CACHE_DIR`.

    variables:
      PIP_CACHE_DIR: .cache/pip

Make sure DEPLOY_TOKEN is defined under Settings > CI/CD > Variables. Mark it Protected and Masked. Because `deploy` runs only on main, a protected variable is only available on protected branches. If you want to be explicit, put the token in the deploy job's own `variables:` instead of the global block.

Minor (not blocking)

- The pip cache has no `key:`. Every branch and MR shares the default cache. Consider `key: files: [requirements.txt]`, or a per-branch key.
- `only:` on deploy is the older syntax. It is unrelated to this change, so leave it.

Checked and fine

- The cache path .cache/pip matches PIP_CACHE_DIR.
- .cache/ is not in .gitignore, but CI cache directories are not committed. You could add it to .gitignore for local runs.
- Tests pass locally with `python -m unittest discover -s tests -v` (Python 3.14).
- The diff is small: 7 lines, well under the 500-line budget in the profile.
- No other files changed.
