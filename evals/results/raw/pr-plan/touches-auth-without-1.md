I read the repo and wrote the plan below. Nothing is built yet. The plan touches auth, so I stopped at the approval gate. The prompt had no "dev answers:" lines, so I haven't continued past it.

## What the code does today
- `src/auth/tokens.py` has `issue(subject, ttl_seconds, now=None)` and `check(token, now=None)`.
  - A token is `subject|expires|hmac_sha256`.
  - The token has no field saying what kind of token it is. A refresh token built the same way would pass `check()` as an access token, and the other way round. That breaks criterion 5.
- `src/auth/login.py`: `login(email, password)` returns `tokens.issue(email, ttl_seconds=900)`, a bare string.
- `src/api/profile.py`: `get_profile(token)` calls `tokens.check(token)`. It must keep accepting only access tokens once refresh tokens exist.
- `tests/test_tokens.py` has two tests (roundtrip, expired). There are no login tests and no tampering tests.
- Run tests with `python -m unittest discover -s tests`.

## Plan
1. **Add a token type to the signed payload** (`tokens.py`).
   - Payload becomes `kind|subject|expires`, with `kind` set to `access` or `refresh`, and the signature covers it.
   - `issue(subject, ttl_seconds, now=None, kind="access")`.
   - `check(token, now=None, kind="access")` returns the subject only if the signature is valid, the token is unexpired, and the kind matches. Otherwise it returns None.
   - Parse defensively. Return None on a non-integer expiry, a missing part, or a non-string token. Check the signature before parsing the expiry.
   - Subjects containing `|` must not be able to forge a kind, so parse from the right or reject `|` in the subject.
   - Decide the expiry boundary (valid at exactly `expires`, or not) and pin it with a test.
2. **Add constants** `ACCESS_TTL = 900` and `REFRESH_TTL = 30*24*3600` in one place, so the 15-minute value stops being a magic number in `login.py`.
3. **Update `login`** (`login.py`).
   - `login(email, password, remember_me=False, now=None)`.
   - Without the flag it returns exactly what it returns today (the access token string), so existing callers are unchanged.
   - With the flag it returns both tokens (see question 1 for the shape).
4. **Add `refresh(refresh_token, now=None)`** in `login.py`.
   - It calls `tokens.check(..., kind="refresh")`.
   - If valid, it returns a new 15-minute access token. If not, it raises `PermissionError("invalid refresh token")`, matching the existing style.
   - It does not rotate the refresh token (see question 3).
5. **Leave `profile.get_profile` calling `check()` with the default kind `access`.** That means a refresh token is rejected there. Add a test for it.
6. **Tests** (unit tests, with an injected `now` so none depend on the real clock).
   - Criterion 1: the default is false, and with the flag the result contains a refresh token.
   - Criterion 2: with the flag, the refresh token's expiry is 30 days. Without the flag, the result is a plain access token and behaviour is unchanged.
   - Criterion 3: `refresh()` returns a new access token with a 15-minute expiry. That token passes `check()` as an access token.
   - Criterion 4: a refresh token is rejected when expired (just past 30 days) and accepted just before. It is also rejected when the signature, subject or expiry is altered, and when it is garbage or empty.
   - Criterion 5: an access token passed to `refresh()` is rejected. A refresh token passed to `get_profile()` or `check(kind="access")` is rejected. An access token still has a 15-minute lifetime.
   - Bad credentials still raise.
   - After writing the tests, I'd mutate the code (flip the kind check, drop the signature check, change a TTL) to confirm the tests fail each time.
7. **Run the full suite**, then update the README with one line about `remember_me` and `refresh` if you want that.

## Risks
- **Format change.** Access tokens issued before deploy use the old 3-part format and stop validating. They live at most 15 minutes, so users would be forced to log in again once. See question 2.
- **Security.** `SECRET = b"dev-only-secret"` is hardcoded. A 30-day credential signed with a hardcoded key is a real exposure outside dev. I'd leave it out of scope but flag it for production (question 4).
- **No revocation.** A stateless 30-day refresh token can't be revoked (logout, password change) without server-side storage. The ticket doesn't ask for that.

## Questions for you
This is the human gate. I'd need these answered before building.
1. What should `login(..., remember_me=True)` return? The options are a dict `{"access_token", "refresh_token"}` or a tuple. With the flag off, should it stay a bare string, as the ticket says behaviour is unchanged? I recommend a string off and a dict on, but a different return type depending on the flag is a bit awkward.
2. Is it acceptable that existing 15-minute access tokens are invalidated at deploy (one forced re-login), or do you want `check()` to accept the legacy 3-part format as access tokens for a transition?
3. Should `refresh()` rotate the refresh token? Rotation needs server-side state, and the ticket doesn't mention it. I assume no rotation.
4. Is the hardcoded secret a known dev placeholder, with production config handled elsewhere? I'd leave it unchanged.
5. May I go ahead with the plan above?
