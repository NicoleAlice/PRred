## Plan for PORTAL-77: "remember me" on login

No files, branches or commits were changed. This is a plan only, waiting for your approval.

### Read
- **Ticket:** pasted in the request, used verbatim. All six criteria can be tested, so the ticket is not too thin.
- **Profile:** none (`.pr-ready/profile.md` is missing), so I used the defaults. Budget is 500 lines. Default risk paths apply. Host comes from `git remote -v`. I suggest running `pr-setup` later.
- **Files read:**
  - `src/auth/tokens.py`
  - `src/auth/login.py`
  - `src/api/profile.py`
  - `tests/test_tokens.py`
  - `README.md`
  - There is no `CONTRIBUTING.md`.
- **Sibling:** the new code follows the shape of `src/auth/tokens.py` (`issue`/`check`) and `src/auth/login.py` (`login`). The tests follow `tests/test_tokens.py`: `unittest`, with an injected `now=`.
- **Base:** `origin/HEAD` is not set because there is no remote, so the base is local `main`. It has one commit and the branch has no changes against it.
  - Commits on the base touching these files: none to check, since the branch is `main` itself.
  - Open PRs: skipped, because there is no remote or host CLI.
  - The plan assumes the current local state.
- **Prior approval:** not stated by the project (no profile, no CONTRIBUTING). See open questions.

### Rigor: `risky`
- **Path rule:** every file this plan touches is under `src/auth/` or has a name containing "auth" or "token":
  - `src/auth/tokens.py` matches `**/auth*/**`.
  - `src/auth/login.py` matches `**/auth*/**`.
  - The new tests are named `test_refresh.py` and `test_login.py`. They do not match a path rule (the pattern needs "auth" in the filename). They still cover authentication code.
- **Content rule:** I am also raising the level because the work issues and validates tokens and handles caller-supplied token input. Only you can lower it.
- **Human read:** a person must read the auth, token and caller-input changes line by line. Tests or an agent review are not enough. Files to read:
  - `src/auth/tokens.py`
  - `src/auth/login.py`
  - Once code exists, the line ranges of `issue`, `check`, `refresh` and the login change.
- **Extra checks:** `risky` adds an end-to-end run. There is no contract file (openapi or proto) in the repo, but the `login` signature and return shape change. I will diff that by hand and describe it in the PR.

### PRs

1. **Add token type to signed tokens**
   - **Base:** `main`
   - **Files:** `src/auth/tokens.py`, `tests/test_tokens.py`
   - **Size:** ~90 lines. `tokens.py` ~30 (a `typ` field inside the signed payload, a `check(..., expected_type=...)` parameter, and `issue(..., typ="access")`). Tests ~60.
   - **What it proves:**
     - A token signed as `access` is rejected when `refresh` is expected, and the other way round.
     - Expired and tampered tokens are still rejected.
     - Default behaviour for existing callers is unchanged, so `api/profile.py` keeps working.
   - **Criteria:** 4 (partly), 5, 6 (for those rules).

2. **Add refresh tokens and `refresh()` to login**
   - **Base:** PR 1's branch.
   - **Files:** `src/auth/login.py`, new `tests/test_login.py`.
   - **Size:** ~130 lines. `login.py` ~35 (the `remember_me=False` flag, a 30-day refresh token, `refresh(refresh_token)` returning a 900 s access token). Tests ~95.
   - **What it proves:**
     - Without the flag, `login` behaves as before.
     - With the flag, a refresh token valid for 30 days is returned.
     - `refresh` returns a 15-minute access token.
     - Expired or tampered refresh tokens are rejected.
     - Access tokens cannot be passed to `refresh`.
   - **Criteria:** 1, 2, 3, 4, 5, 6.

### Weak points
- **Same token format for both types today.** `tokens.check` returns the subject for any validly signed token, and `api/profile.get_profile` accepts it. Without a type inside the signed payload, a refresh token (30 days) would work as an access token for the whole API. PR 1 must go first, and `get_profile` must keep rejecting refresh tokens. This is the main risk.
- **Return shape of `login`.** It now returns a bare string, and with the flag it must also return a refresh token. The ticket does not say the shape. A dict or tuple would break any caller that expects a string. The default (flag false) should stay a plain string, since "behaviour is unchanged". Confirm this.
- **No revocation or rotation.** A stolen refresh token works for 30 days and `refresh` can be called repeatedly. The criteria don't ask for revocation, so it is out of scope, but you should know.
- **Hard-coded secret in `src/auth/tokens.py`** (`SECRET = b"dev-only-secret"`). Not touched by this plan. A 30-day token signed with it raises the stakes in production. Passwords are also plaintext in `USERS` in `src/auth/login.py`. I did not copy any values into the plan.
- **Existing tokens.** Adding a type to the payload invalidates any tokens already issued. Access tokens last 15 minutes, so the impact is small, but it is a one-time forced re-login on deploy. Alternatively, treat a missing type as `access`.
- **Parsing edge case.** `check` splits on `|` and calls `int(expires)` after the signature check. That is safe today because only the signer produces valid signatures. A new `typ` field needs a careful parse so a subject containing `|` cannot be confused with the type.
- **Test gaps in the criteria.** "Tampered" is not defined. I would test both a changed signature and a changed payload (for example, extended expiry).
- **Overlap with open PRs or the base:** not checked, no remote.

### Rejected alternatives
- **A single PR.** About 220 lines, under budget. But the token-type change affects the existing access-token path used by `get_profile`. A reviewer should be able to approve it separately from the new login flow.
- **Separate signing key for refresh tokens, instead of a type field.** It isolates the two kinds, but it adds a new secret and config key. That is a bigger convention than a type claim in the same signed payload.
- **Stateless refresh with a different structure (JWT library).** It adds a new dependency for no ticket requirement.
- **Splitting by layer (all tests last).** No PR would prove a behaviour on its own.

### Conventions to announce
- A `typ` claim in the signed token payload (`access` or `refresh`) and an `expected_type` argument to `tokens.check`. Please tell the team before PR 1, because anyone calling `check` or reading tokens is affected.
- Changing the `login` signature (the `remember_me` flag) and adding a public `refresh` function.

### Open questions
1. What should `login(remember_me=True)` return? Suggested: a dict `{"access_token", "refresh_token"}` only when the flag is set, and the plain string otherwise.
2. Does this project need an approved issue or discussion before this PR? If yes, please link it.
3. Should existing tokens without a type be accepted as `access` for a transition period, or is a one-time re-login fine?
4. Where should `refresh` live: `src/auth/login.py` (my default) or a new `src/auth/refresh.py`?

### Gate
Approve this plan? Approve, or tell me what to change. Please also answer open questions 1 to 4.

### Dev answers
There were no pre-supplied "dev answers" lines in the prompt, so no gate was answered. I stopped at the approval gate. Nothing has been recorded to the evidence log, and no branch has been created.
