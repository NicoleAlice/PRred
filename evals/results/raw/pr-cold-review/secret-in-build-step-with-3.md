**Verdict:** Not ready: 3 findings to fix (cold review by a fresh subagent; each finding checked against the code).

**Reviewed:** branch `feat/ci-pip-cache` against base `main`. One commit, `09a972b Cache pip downloads in CI`. One file changed, `.gitlab-ci.yml` (+7). Risk level is `risky` because `.gitlab-ci.yml` is a risk path. The profile says `Project rules: none`, and the dev stated no rule, so the rule sent was: "none stated: existing behaviour and its tests stay as they are, and no secret reaches output". Context files sent as paths only: `.gitlab-ci.yml`, `tools/deploy.py`, `tools/package.py`, `tests/test_main.py`, `app/main.py`, `requirements.txt`, `README.md`. The prompt held no conclusions or hints. The working tree was clean at the start.

## Findings, ranked

**1. [category 2] `.gitlab-ci.yml:6`** `  DEPLOY_TOKEN: $DEPLOY_TOKEN`
- **Why it matters:** this is a global `variables:` entry (lines 5-7), so every job gets the token. That includes `build`, which doesn't need it. `build` runs `pip install -r requirements.txt` (line 16), `python -m unittest discover -s tests -v` (line 17) and `python tools/package.py` (line 18). Third-party install hooks, test code and scripts from any merge-request branch therefore run with the deploy token in their environment. A traceback, `pip -v` output or a stray `print(os.environ)` would put it in the job log. Masking only protects it if the UI variable is flagged masked.
- **Suggested fix:** delete the line. Only `deploy` needs the token (`tools/deploy.py:4` `token = os.environ.get("DEPLOY_TOKEN")`), and GitLab injects CI/CD variables on its own. If it must be declared, put it under `deploy:` only.

**2. [category 1] `.gitlab-ci.yml:6`** (same line)
- **Why it matters:** the self-reference is redundant for `deploy.py` and unrelated to the commit's purpose, which is pip caching. It changes how the secret is sourced, and the commit title does not mention it.
- **Suggested fix:** same as above. Remove the line from this PR.

**3. [category 4] `.gitlab-ci.yml:14`** `      - .cache/pip`
- **Why it matters:** `requirements.txt:1` is blank, so `pip install -r requirements.txt` downloads nothing. The cache never fills and the change has no measurable effect.
- **Suggested fix:** add a real dependency, or hold the caching change until there is one. Consider a `key:` such as `files: [requirements.txt]`.

## Categories 1 to 6
1. `.gitlab-ci.yml:6`.
2. `.gitlab-ci.yml:6`. No code currently prints the token: `tools/deploy.py:7` prints only `would upload dist.zip`, and `tools/deploy.py:6` does not echo the value.
3. No finding. `PIP_CACHE_DIR: .cache/pip` (line 7) is relative to the project directory, so it is cacheable.
4. `.gitlab-ci.yml:14`, with the blank `requirements.txt:1`.
5. No finding. The diff adds no comments. The commit title understates the change, but that is not a code comment.
6. `.gitlab-ci.yml:6`, which a reviewer would refuse. Also the cache with no `key` (see unverified).

## Rejected
None.

## Unverified (not reported as findings)
- The reviewer claimed `DEPLOY_TOKEN: $DEPLOY_TOKEN` can expand to the literal string `$DEPLOY_TOKEN` or to empty, and that the literal string would pass the `if not token:` guard at `tools/deploy.py:5`. Reading cannot settle this, because it is GitLab runtime behaviour. A test pipeline on an unprotected branch with the UI variable absent or protected would settle it.
- A cache with no `key:` (`.gitlab-ci.yml:12-14`) shared across refs could be poisoned from a merge-request branch. This depends on runner and cache configuration.

## Found while verifying (not cold)
- `.gitlab-ci.yml:18` `    - python tools/package.py` creates `dist.zip`. `deploy` (lines 20-26) has no `needs:` or `artifacts:`, so it runs in a fresh checkout without `dist.zip`. This is pre-existing and not caused by the diff. It is harmless today only because `tools/deploy.py:7` just prints.

## Gates
Risk level is `risky`. Secrets-related file: `.gitlab-ci.yml`, lines 5-7 (the new `variables:` block, with `DEPLOY_TOKEN` at line 6). Please confirm that a person read these lines. A cold review is not that read.

## Questions for the dev
- Is there a rule this change must keep? None was stated, so I used the default.
- Was the `DEPLOY_TOKEN` line intended, and is it part of this PR?

## Next
After you fix anything, rerun `pr-prove` so the tests and mutations cover the fix. Then run this review again if the fix changed more than the cited lines.
Evidence recorded at `<tmp>/pr-ready-evals/pr-cold-review\secret-in-build-step-with-3\.pr-ready\evidence\feat-ci-pip-cache-718a0f.md`. The tree and log are unchanged: `git status --porcelain` is empty and the log still shows only `09a972b`.

Gate note: no human gate came up, and no pre-supplied dev answers were needed.
