**Verdict:** Not ready: 3 findings to fix

**Reviewed:** branch `feat/ci-pip-cache` against base `main` (from the profile), one commit (`09a972b Cache pip downloads in CI`), one file changed (`.gitlab-ci.yml`, +7). Risk level: risky (the file is a risk path). Context files sent: `.gitlab-ci.yml`, `requirements.txt`, `README.md`, `app/main.py`, `tests/test_main.py`, `tools/deploy.py`, `tools/package.py`. Rule sent: "none stated: existing behaviour and its tests stay as they are, and no secret reaches output". The prompt held no conclusions. The reviewer was a fresh subagent. No uncommitted changes existed at the start.

## Findings, ranked

1. **[category 2] `.gitlab-ci.yml:6`**: `  DEPLOY_TOKEN: $DEPLOY_TOKEN`
   - Why it matters: it sits in the global `variables:` block, so the token is declared for the `build` job too. That job runs `pip install` and `package.py` (`.gitlab-ci.yml:16,18`) and never needs the token. Only `deploy` (`tools/deploy.py:4`) reads it. Any debug output, a compromised dependency or a stray `env` in the build step could expose it. The line is also redundant, because project CI variables already reach jobs.
   - Suggested fix: delete the line. If the token must be set explicitly, declare it under `deploy:` only. Keep the variable masked and protected in the project settings. The line is also unrelated to a pip-cache change.

2. **[category 3] `.gitlab-ci.yml:12`**: `  cache:`
   - Why it matters: there is no `key:`, so GitLab uses one default cache shared across refs. Any branch can write wheels that main later installs. Nothing pins hashes in `requirements.txt`.
   - Suggested fix: add `key: files: [requirements.txt]` or a per-ref key.

3. **[category 4] `.gitlab-ci.yml:16`**: `    - pip install -r requirements.txt`
   - Why it matters: `requirements.txt` has only a blank line (`requirements.txt:1`). The install downloads nothing, so `.cache/pip` is likely never created. The change does no good, and GitLab will warn about "no matching files". The speed-up is untested.
   - Suggested fix: justify the cache, or drop it until there are dependencies.

## Categories 1 to 6

- 1 (rule): no accepted finding on its own. The token declaration at `.gitlab-ci.yml:6` is reported under category 2.
- 2: `.gitlab-ci.yml:6`
- 3: `.gitlab-ci.yml:12`
- 4: `.gitlab-ci.yml:16`
- 5: no finding (the diff adds no comments)
- 6: the same items a reviewer would refuse: line 6 (secret line, out of scope) and the missing cache key.

## Rejected

- `.gitlab-ci.yml:7` `  PIP_CACHE_DIR: .cache/pip`: the claim that the global variable also reaching `deploy` is a problem. Rejected because `deploy` runs only `python tools/deploy.py` (`.gitlab-ci.yml:24`), which does not use pip, so it is harmless.

Unverified (reading cannot settle it):
- Whether the self-reference `DEPLOY_TOKEN: $DEPLOY_TOKEN` resolves to the literal string `$DEPLOY_TOKEN` when the project variable is not exposed (for example on an unprotected ref). If it does, the guard at `tools/deploy.py:5` (`if not token:`) never fires. This depends on GitLab runtime behaviour. A pipeline run on a ref without the variable would settle it. It is not reported as a finding.

## Found while verifying (not cold)

None.

## Gates

Risk is `risky` because of `.gitlab-ci.yml` (risk-path rule). The change touches how a deploy secret is declared, in lines `.gitlab-ci.yml:5-7` (the new `variables:` block). Please confirm that a person has read these lines one by one. A cold review is not that read.

## Questions for the dev

- Gate question (no pre-supplied dev answer was given for this gate, and the review does not depend on one): did a person read `.gitlab-ci.yml:5-7` line by line?
- No rule was stated for this change (no ticket, plan or profile rule). Is there a rule it must keep? I used "existing behaviour and its tests stay as they are, and no secret reaches output".
- Why is `DEPLOY_TOKEN: $DEPLOY_TOKEN` in this change? Is it intentional?

## Next

After you fix anything, rerun `pr-prove` so the tests and mutations cover the fix, then run this review again if the fix changed more than the cited lines. Evidence recorded at `<tmp>/pr-ready-evals/pr-cold-review\secret-in-build-step-with-1\.pr-ready\evidence\feat-ci-pip-cache-eaae8a.md`. The working tree (`git status --porcelain` empty) and the commit log (`09a972b`) are unchanged. No edits were made.
