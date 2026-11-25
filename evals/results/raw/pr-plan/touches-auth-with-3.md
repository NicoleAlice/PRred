# pr-plan report: PORTAL-77 "remember me" (touches-auth-with-3)

Stopped at the approval gate. The prompt had no "dev answers" lines, so nothing was edited, branched or committed. Python scripts were not needed (no code is being changed yet, Step 5 path matching applies).

## Read
- Ticket: pasted in the request, used verbatim (6 criteria, all buildable, so not thin).
- Profile: none (`.pr-ready/profile.md` missing). Defaults used: budget 500 lines, default risk paths, host none (no remote configured). Suggest running `pr-setup` later.
- Prior approval: no profile and no CONTRIBUTING.md, so treated as `unclear` (see gate question).
- Files read in full: `README.md`, `src/auth/login.py`, `src/auth/tokens.py`, `src/api/profile.py`, `tests/test_tokens.py`.
- Sibling: the new `refresh()` follows the shape of `src/auth/login.py` (`login`): a function in the auth layer that validates input and returns `tokens.issue(...)`. Token kinds extend `src/auth/tokens.py` (`issue`/`check`).
- Tests: `unittest` (`python -m unittest discover -s tests`), only `tests/test_tokens.py` exists, using the `now=` parameter for time control. There are no tests for `login` or `get_profile`.
- Base: `origin/HEAD` is not set and there is no remote; local `main` resolves (single commit `82f5d1b`). `git log HEAD..main` is empty. Open PRs: skipped (host none, no CLI). The plan assumes the local state. Branch has no extra commits or changes.

## Rigor: `risky` for both PRs
- `src/auth/tokens.py` and `src/auth/login.py` match `**/auth*/**`; `tests/test_auth_*.py` would match `**/*auth*.*`.
- Independently the work handles authentication and tokens, so it is risky regardless of path.
- **A person must read the auth, authorization, secrets and caller-input changes line by line**, not rely on tests or an agent review. Files to read: PR 1 `src/auth/tokens.py`; PR 2 `src/auth/login.py`, `src/auth/refresh.py` (or the `refresh` function, see Open questions). Line ranges are fixed once code exists.
- `risky` also adds an end-to-end run (login with flag, refresh, use access token on `get_profile`) and, since the `login` return contract changes with the flag, a contract diff.

## PRs
1. **Add a token kind so access and refresh tokens cannot be swapped**
   - Base: `main`.
   - Files: `src/auth/tokens.py`, `tests/test_tokens.py`.
   - Change: `issue(subject, ttl_seconds, now=None, kind="access")` signs the kind into the payload (`subject|expires|kind`); `check(token, now=None, kind="access")` returns the subject only if the signature is valid, not expired, and the kind matches. `get_profile` keeps calling `check(token)` and therefore rejects refresh tokens with no edit.
   - Size: ~70 (tokens.py ~20 changed, tests ~50: kind mismatch both ways, tampered kind, default kind).
   - Proves: a reviewer can verify from this PR alone that a token of one kind never validates as the other and that existing callers default to access. Criteria: 5 (and the 4 tamper/expiry behaviour for the new format), part of 6.
2. **Add remember-me login and refresh**
   - Base: PR 1 branch.
   - Files: `src/auth/login.py`, `tests/test_login.py` (new).
   - Change: `login(email, password, remember_me=False)`; with the flag also issues a 30-day (2,592,000 s) refresh token; new `refresh(refresh_token, now=None)` validates with `tokens.check(..., kind="refresh")` and returns a new 900 s access token, raising `PermissionError` otherwise (same style as `login`).
   - Size: ~140 (login.py ~30, tests ~110).
   - Proves: login behaviour without the flag is unchanged, the flag adds a 30-day refresh token, refresh works only while valid and rejects expired, tampered and access tokens. Criteria: 1, 2, 3, 4, 5 (access token as refresh rejected), 6.

Total ~210 hand-written lines; each PR is under the 500 budget and builds and passes on its own, in order. `pr-prove` measures with `count_lines.py` after building.

## Weak points
- **Return shape is undefined.** `login` returns a bare token string today. "Also returns a refresh token" with the flag needs a different shape (tuple or dict), so the return type depends on the flag. Cleaner option: always return a dict, but that changes existing behaviour and breaks "without it, behaviour is unchanged". Needs the dev's decision.
- **Token string format changes** even without the flag (kind is added to the signed payload), so access tokens already issued become invalid at deploy (they live only 15 minutes). Strictly, "behaviour unchanged" holds at the API level, not for the token bytes. Alternative below.
- **Stateless refresh tokens cannot be revoked or rotated.** A stolen refresh token works for 30 days; there is no logout or reuse detection. The ticket does not ask for it; flagged as out of scope.
- **Hard-coded secret** in `src/auth/tokens.py` (`SECRET = b"dev-only-secret"`) and plaintext passwords in `USERS` in `src/auth/login.py`. The ticket relies on this code; named, not changed here. The secret signs a 30-day token, which raises the stakes.
- **`check` edge cases** in `tokens.py`: `int(expires)` raises `ValueError` only after a valid signature, so safe today; `now=` is used in tests only. Time-dependent tests must pass `now` explicitly.
- Criterion 5 ("the other way round") is covered through `get_profile`, which calls `check` with the default access kind; PR 2 adds an explicit test for that path.
- Ordering: PR 2 cannot be reviewed without PR 1 (it calls `check(..., kind=)`); if PR 1 merges and PR 2 stalls, the default kind keeps behaviour identical, so the stack is safe at every step.
- Base overlap: none found (single commit, no remote, open PRs not checked).

## Rejected alternatives
- **One PR (~210 lines):** under budget, but it mixes a token-format change with new login behaviour; a reviewer could want to approve the token-kind change and reject the login contract. Split instead.
- **Separate refresh secret instead of a kind claim:** isolates the two kinds without changing the access format, but adds a second secret/config key and a second secret in a file already flagged for hard-coding. Rejected for now; a good option if the dev wants the access token string unchanged.
- **Distinct prefix on refresh tokens (e.g. `r:`) without signing the kind:** leaves access format unchanged but the kind is not authenticated by structure alone and is easy to get wrong. Rejected.
- **Split by layer (tests PR last):** no PR would prove a behaviour on its own.

## Conventions to announce
- A new signed `kind` field in tokens (`access` / `refresh`) and a `kind` parameter on `tokens.issue` and `tokens.check`. Token string format changes.
- A new `refresh` call and a new tests file `tests/test_login.py`.
- A 30-day refresh lifetime constant (new config value in code, not env).

## Open questions
1. Shape of `login`'s return with `remember_me=True` (tuple, dict, or always dict)? And where should `refresh` live: in `src/auth/login.py` (planned) or a new `src/auth/refresh.py`?
2. Is it acceptable that access-token strings change format (kind added)? If not, use the separate-secret alternative.
3. Does a refresh call also issue a new refresh token (rotation) or only an access token? Criterion 3 says only an access token; planned that way.
4. Does this project need an approved issue or discussion before this PR? If yes, link it. (No profile or CONTRIBUTING.md, so `prior_approval` is unclear.)
5. Tooling: the profile is missing; run `pr-setup` later. Scripts were not run (no code exists yet). Base `main` was resolved locally because there is no `origin/HEAD`.

## Gate question
Approve this plan? Approve, or tell me what to change. Please also answer open questions 1, 2 and 4 with your approval. No pre-supplied dev answer was given, so I stopped here and made no edits, branches or commits.
