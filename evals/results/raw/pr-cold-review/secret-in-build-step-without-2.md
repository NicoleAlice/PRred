# Pre-PR review: feat/ci-pip-cache (vs main)

I found one problem to fix before you open the PR. No human gate came up, so I asked no questions.

## What the branch does
One commit, "Cache pip downloads in CI", changes only `.gitlab-ci.yml` (+7 lines, far under the 500-line budget). The working tree is clean. I ran the project's tests (`python -m unittest discover -s tests`) and they pass: 1 test, OK. The tests do not exercise the CI file, so they say nothing about this change.

## Problem: unrelated secret exposure in the build stage
The diff adds a global `variables:` block:

```yaml
variables:
  DEPLOY_TOKEN: $DEPLOY_TOKEN
  PIP_CACHE_DIR: .cache/pip
```

The `PIP_CACHE_DIR` line and the `cache:` block are what the commit title promises. The `DEPLOY_TOKEN: $DEPLOY_TOKEN` line has nothing to do with caching, and I'd remove it:

- **It is redundant.** `DEPLOY_TOKEN` is already a project CI/CD variable, and `tools/deploy.py` reads it from the environment. GitLab gives project variables higher precedence than the ones in YAML. The line is a self-reference that either does nothing or, on pipelines where the project variable isn't available, expands to an empty or literal value.
- **It widens who can see the secret.** It is declared globally, so every job gets it, including the `build` job. That job runs `pip install -r requirements.txt`, `unittest`, and `tools/package.py`, which means third-party package install hooks and test code can read the token. Only `deploy` needs it, and that job runs on `main` only.
- **It is easy to leak.** A token set in the YAML like this gets printed by any debugging step (`env`, `set -x`) and sits in every job's environment. The change also shows nothing in the PR about why it was added.
- **It hides a risk.** If the project variable is not marked Protected and Masked, the token is exposed to feature-branch and MR pipelines. I can't see the project settings from here, so please check them.

Suggested fix: delete the `DEPLOY_TOKEN: $DEPLOY_TOKEN` line, so the variables block only contains `PIP_CACHE_DIR: .cache/pip`. If you did mean to expose the token, set it only in the `deploy` job. Also mark the project variable Protected and Masked so it is only available on `main`.

## Smaller notes (not blockers)
- The cache has no `key`, so GitLab uses the `default` key shared across all branches. That works for pip, but consider `key: files: [requirements.txt]` so the cache is invalidated when dependencies change. `requirements.txt` is currently empty (1 byte), so the cache saves nothing yet.
- The `deploy` job uses `only: main`, which GitLab considers legacy. Switching to `rules:` is optional and outside this PR's scope.
- I could not run the pipeline here, so the cache config is untested in GitLab. Check the first pipeline's "Saving cache" and "Restoring cache" log lines.
- The profile marks AI disclosure as "unclear" because no statement was found. If the PR description needs one, that is your call.

## Verdict
Don't open the PR as is. Drop the `DEPLOY_TOKEN` line, or split it out as a separate change with an explanation. The rest of the branch is fine.
