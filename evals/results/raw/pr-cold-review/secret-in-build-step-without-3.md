# Pre-PR review: feat/ci-pip-cache

Scope: one commit (09a972b "Cache pip downloads in CI") against main. It changes only `.gitlab-ci.yml`, with 7 lines added. The unit tests pass locally (1 test, OK). I could not run the pipeline itself.

## Problem: the commit also adds `DEPLOY_TOKEN` to the build job

```yaml
variables:
  DEPLOY_TOKEN: $DEPLOY_TOKEN     # <- not part of "cache pip"
  PIP_CACHE_DIR: .cache/pip
```

The commit message and the PR purpose are about caching pip downloads. The `DEPLOY_TOKEN` line has nothing to do with that. It should come out before you open the PR.

Why it matters:

1. **The token is exposed to the wrong job.** Top-level `variables:` apply to every job. Only `deploy` needs the token, since `tools/deploy.py` reads it from the environment. The `build` job doesn't use it, but it runs `pip install -r requirements.txt`. That executes third-party package code, and `python tools/package.py` runs repo code, both with the token in their environment. Only the deploy job needs a deploy credential.
2. **It does nothing useful.** A CI/CD variable defined in the GitLab project settings is already injected into jobs. Re-declaring it as `DEPLOY_TOKEN: $DEPLOY_TOKEN` is a self-reference. At best it is a no-op. At worst it behaves differently from what you expect, for example when a variable is scoped to protected branches or to the `main` environment. It also makes the token look like it is managed in the YAML.
3. **It widens the review surface.** A "cache" PR that touches a secret is easy to approve without a second look.

Fix: delete the `DEPLOY_TOKEN: $DEPLOY_TOKEN` line. The `deploy` job will still get the project-level variable. If you want it explicit, put it under the `deploy` job's own `variables:` and keep the actual value in GitLab settings. Mark it masked and protected, because `deploy` only runs on `main`.

## Minor notes (optional)

- `PIP_CACHE_DIR: .cache/pip` is global, so it also applies to `deploy`. That is harmless, but you could scope it to `build`.
- `cache:` has no `key:`. The default shares one cache across all branches and jobs. This is fine for pip, but consider `key: files: [requirements.txt]` so the cache invalidates when dependencies change.
- `.cache/` is not in `.gitignore`. It matters only if someone runs with that dir locally. Optional.
- `requirements.txt` is effectively empty (1 byte), so the cache saves nothing yet. It is still correct for later.

## Verdict

Do not open the PR as is. Remove the `DEPLOY_TOKEN` line and keep the rest, which is a sound pip cache change. Then the PR matches its description.
