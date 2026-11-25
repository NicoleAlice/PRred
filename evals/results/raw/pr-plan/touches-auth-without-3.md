# PORTAL-77 "remember me": plan

I only read the repo (git, one commit, `82f5d1b Add login and token check`). I changed nothing. No dev answers were pre-supplied, so I stop at the one gate below and don't start implementing.

## What the code does today

- `src/auth/tokens.py`: `issue(subject, ttl_seconds, now=None)` builds `subject|expires|hmac_sha256`. `check(token, now=None)` returns the subject or `None`. The token carries no type.
- `src/auth/login.py`: `login(email, password)` checks `USERS` and returns `tokens.issue(email, ttl_seconds=900)`.
- `src/api/profile.py`: `get_profile(token)` calls `tokens.check`.
- `tests/test_tokens.py`: two tests (roundtrip, expired). There are no tests for `login` or `profile`. Run them with `python -m unittest discover -s tests`.

## Main risk

Criterion 5 can't be met by just calling `issue(email, 30*86400)` for the refresh token. A refresh token has the same format as an access token, so `get_profile` would accept it as an access token for 30 days. That would defeat the 15-minute lifetime. The reverse also holds: an access token would be accepted by `refresh`. The token type has to be part of the signed payload.

## Design

### tokens.py

- Add a `kind` to the signed payload: `kind|subject|expires|sig`. The signature covers all three fields, so the kind can't be edited without breaking the HMAC.
- `issue(subject, ttl_seconds, now=None, kind="access")`. The existing positional signature and the existing tests keep working.
- `check(token, now=None, kind="access")` returns the subject only if the signature is valid, the token is not expired, and the token's kind equals the expected kind. Otherwise it returns `None`.
- Parse defensively. A malformed token, a non-integer expiry or a wrong field count returns `None` and never raises. Signature is verified before `int()` is called on the expiry, as it is today. Keep `hmac.compare_digest`.
- Add constants `ACCESS_TTL = 900` and `REFRESH_TTL = 30 * 86400`, so the numbers aren't scattered across files.
- Subjects are emails. Parse by position (`split("|", 1)` for the kind, `rsplit("|", 2)` for the rest) so a `|` in a subject can't shift the fields.

### login.py

- `login(email, password, remember_me=False)`.
- Rule 2 says "without it, behaviour is unchanged". That means the default call must still return a plain access-token string, because `get_profile` and any existing callers use it that way.
- With `remember_me=True`, return a different shape. I propose a dict, `{"access_token": ..., "refresh_token": ...}`. That is a return-type split on the flag, which is a bit awkward. The alternative is always returning a dict, which breaks "unchanged" and existing callers. I'd go with the split to honour the ticket as written, and flag it to the dev.
- Add `refresh(refresh_token, now=None)` here or in a small `src/auth/refresh.py`. It calls `tokens.check(refresh_token, now, kind="refresh")`. If that returns `None`, raise `PermissionError("invalid refresh token")`, which matches the existing style. Otherwise it returns `tokens.issue(subject, ACCESS_TTL, now, kind="access")`.
- `refresh` does not issue a new refresh token (no rotation), because the ticket doesn't ask for one.

### profile.py

No code change. It calls `tokens.check(token)` with the default `kind="access"`, so refresh tokens are now rejected there automatically. A test must prove this.

## Compatibility and rollout

- The token format changes. Access tokens issued before the deploy will fail `check` and those users will have to log in again (at most a 15-minute disruption). Alternative: accept the legacy 3-field format as `access` for one TTL window. I recommend not doing this, because it adds a parsing path in security code that is only needed for 15 minutes.
- Issuing 30-day tokens means a stolen refresh token is valid for 30 days. There is no server-side revocation or logout in this codebase, and none is asked for. I'm noting this as a known limitation, not adding it.
- `SECRET = b"dev-only-secret"` is hardcoded. That is pre-existing and out of scope, but a 30-day token raises the stakes, so I'd mention it in the PR description.

## Tests (criterion 6)

Use `unittest`, matching the repo, and pass `now` explicitly so nothing depends on the clock. Add `tests/test_login.py` and extend `tests/test_tokens.py`.

| Rule | Test |
|---|---|
| 1 | `login(e, p)` returns a string and `remember_me` defaults to False. `login(e, p, remember_me=True)` returns a dict with both tokens. Wrong password still raises `PermissionError`, with or without the flag. |
| 2 | The refresh token's expiry is `now + 30d`. Valid at day 29, rejected at day 31. Without the flag, the result still decodes as a 15-minute access token and no refresh token appears. |
| 3 | `refresh(valid)` returns an access token. `check` gives the same subject, and its expiry is `now + 900`. It is valid at +899s and rejected at +901s. |
| 4 | An expired refresh token raises. Tampering is tested three ways: flip the signature, change the subject, and change the expiry (the extension attack). Also garbage, an empty string and a truncated token all raise `PermissionError` and never any other exception. |
| 5 | A refresh token passed to `get_profile` or `tokens.check` (default kind) returns `None` or raises. An access token passed to `refresh` raises. Relabelling the kind field in an access token, without re-signing, fails the signature. |
| existing | The two current token tests still pass unchanged. |

Mutation check, since I treat tests as unproven until they can fail. After the tests are green, break the code in each of these ways and confirm a test fails each time: drop the kind comparison in `check`, drop the kind from the signed payload, change `REFRESH_TTL`, change `ACCESS_TTL`, and flip `<` to `<=` in the expiry comparison.

## Build order (small commits)

1. Tests first: add the kind and expiry tests in `test_tokens.py` and see them fail.
2. `tokens.py`: add `kind`, the TTL constants and the defensive parsing. Existing tests stay green.
3. `login.py`: add `remember_me`, plus `refresh` with its tests.
4. `get_profile` rejection test for refresh tokens.
5. Mutation pass, then a full `python -m unittest discover -s tests`.

## Gate: questions for the dev (no pre-supplied answer, so I stop here)

This change touches authentication and token handling, so I want a go-ahead on these before writing code:

1. Is it OK to change the token format, which invalidates access tokens issued before the deploy? Or do you want legacy-format tokens accepted for a transition window?
2. For the `remember_me=True` return value, is a dict `{"access_token", "refresh_token"}` acceptable? It keeps the default return unchanged, but the return type then depends on the flag.
3. Should `refresh` rotate the refresh token (issue a new one each time)? The ticket doesn't ask for it, so I'm assuming no.
4. Should `refresh` live in `src/auth/login.py` or in its own module? I'd keep it in `login.py`.
5. Does someone need to review this for security (or should I ask for that review) because of the 30-day credential and the hardcoded secret?

Nothing was implemented, and no files in the repo were modified.
