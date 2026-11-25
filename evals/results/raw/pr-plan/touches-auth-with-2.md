Plan for PORTAL-77, "remember me" on login. Nothing has been edited, branched or committed.

**Read**
- Ticket: pasted in the request, used verbatim. All six criteria are testable, so the ticket is not thin.
- Profile: no `.pr-ready/profile.md`, so I used the defaults. Budget is 500 lines, default risk paths apply, and `pr-setup` is worth running later.
- Files read in full:
  - `src/auth/login.py`
  - `src/auth/tokens.py`
  - `src/api/profile.py`
  - `tests/test_tokens.py`
  - `README.md`
- Sibling: the new code follows the shape of `src/auth/login.py` (`login`, built on `tokens.issue`) and the tests follow `tests/test_tokens.py` (`unittest`, a fixed `now=` instead of real time). Nothing like `refresh` exists yet.
- Base: `main`. There is no `origin` remote, so `origin/HEAD` does not resolve. I assume local `main`, with no fetch.
- Open PRs: skipped. There is no host remote, so no CLI query was possible.
- Commits on the base touching the same files: none. The repo has one commit, `82f5d1b`, and the branch has no extra changes.
- The scripts did not run. No code exists yet, so Step 5 matches paths by hand.

**Rigor: `risky`**
- `src/auth/tokens.py` and `src/auth/login.py` match `**/auth*/**`.
- Independently of the paths, the work handles authentication, tokens and a public contract (the return value of `login`, the new `refresh` call, and the token format that `get_profile` relies on). That would raise it to `risky` anyway.
- **A person must read the auth, authorization, secrets and caller-input changes line by line, not rely on tests or an agent review.**
  - PR 1: all of `src/auth/tokens.py` and the `check` call in `src/api/profile.py`.
  - PR 2: all of `src/auth/login.py`.
  - The exact line ranges are listed once the code exists.
- `risky` also adds an end-to-end run (login, then refresh, then profile) and a contract diff, because the return of `login` and the new `refresh` change the public contract.

**PRs** (stacked, one at a time; PR 1 on `main`, PR 2 on PR 1's branch)

1. **Add a token kind so access and refresh tokens cannot be swapped**
   - Base: `main`.
   - Files:
     - `src/auth/tokens.py`
     - `tests/test_tokens.py`
     - `tests/test_profile.py` (new)
   - Change: the signed payload carries a `kind` (`access` or `refresh`). `issue` takes `kind="access"` and `check` takes `kind="access"`. `check` rejects a token of the wrong kind, and a tampered kind fails the signature.
   - Size: ~90 lines. Basis: `tokens.py` ~25, tests ~65.
   - Proves: a reviewer can see from this PR alone that an access token is not accepted where a refresh token is expected (and the reverse), and that `get_profile` still rejects tampered, expired and wrong-kind tokens. The `get_profile` test covers the "access only" side, not the refresh side.
   - Criteria: 5, and the tampering half of 4. Criterion 6 is covered for these rules.
   - Level: `risky` (`src/auth/tokens.py` matches `**/auth*/**`).

2. **Add remember-me login and refresh**
   - Base: PR 1's branch.
   - Files:
     - `src/auth/login.py`
     - `tests/test_login.py` (new)
   - Change: `login(email, password, remember_me=False)` and a new `refresh(refresh_token)`. `refresh` calls `tokens.check(..., kind="refresh")` and issues a 900-second access token. The refresh token lives 30 days (2,592,000 seconds). Without the flag, `login` returns exactly what it returns today.
   - Size: ~140 lines. Basis: `login.py` ~35, `test_login.py` ~105.
   - Proves: the flag defaults to off and leaves behaviour unchanged. With the flag a 30-day refresh token comes back. `refresh` returns a 15-minute access token for a valid token and refuses expired, tampered, access-kind and malformed tokens.
   - Criteria: 1, 2, 3, 4 (expired and tampered), 6.
   - Level: `risky` (`src/auth/login.py` matches `**/auth*/**`).

**Weak points**
- Ordering: PR 1 changes the signed payload format. Tokens issued before the deploy have the old three-part shape and will be rejected, so everyone is logged out once. Access tokens last 15 minutes, so the effect is small, but it is a visible behaviour change.
- The return type of `login` is not in the ticket (open question 1). Today it returns a bare string. "Unchanged" without the flag means a string, and with the flag the shape has to change, so the return type depends on the flag. That is awkward for callers. It is the main public-contract risk.
- `tokens.check` has an existing bug in the failure path (`src/auth/tokens.py`).
  - `hmac.compare_digest` raises `TypeError` when the signature part contains non-ASCII characters.
  - So a tampered token can raise instead of returning `None`, which would break criterion 4.
  - PR 1 should fix this with a test, so it is a small addition to the scope.
- A hard-coded signing secret sits in `src/auth/tokens.py` (not copied here). It is acceptable for dev only. A 30-day refresh token raises the stakes of a leaked secret, and the ticket does not say where production gets it. I will not change it in this plan; it is flagged for the person doing the line-by-line read.
- `USERS` in `src/auth/login.py` holds plaintext passwords compared with `!=`. This is outside the ticket and I will not touch it. It is a weakness the reviewer should know about.
- Refresh tokens are stateless: no revocation, no rotation, no logout. A stolen refresh token works for 30 days. The ticket does not ask for revocation, so this is a gap to confirm, not scope I am adding.
- No ticket requirement covers whether a refresh token's subject is still a valid user at refresh time (a user removed from `USERS`). I plan to leave that out unless you say otherwise.
- Time is injected through `now=` in `tokens`, so tests can be deterministic. `login` and `refresh` need the same `now` parameter. This is a small interface addition on a public function.
- No overlap with open PRs could be checked (no remote).

**Rejected alternatives**
- One PR for everything: ~230 lines, within budget. Rejected because it mixes a change to the signed token format, which the whole app depends on, with a new API shape. A reviewer who accepts the token change but not the `login` return shape would have to reject both.
- Separate refresh-token secret or a separate module for refresh tokens: a cleaner split of keys, but a new module and a new config key to announce, for a ticket that does not ask for it. Rejected for scope.
- Mark the kind by a different TTL or a prefix on the subject instead of a signed field: easier to forge or confuse, and not covered by the signature. Rejected.
- Split by layer (tests first, then code): no PR would prove a behaviour on its own. Rejected.

**Conventions to announce**
- The signed token payload gains a `kind` field, and `tokens.check` now rejects tokens of another kind by default. This is a new token format, so the team should hear about it before PR 1.
- A new public call, `refresh`, and a new `remember_me` argument on `login`.

**Open questions**
1. What should `login` return when `remember_me` is true? Today it returns a bare token string. Options include a pair, a dict, or a small result object. Whichever you pick, the default (no flag) must stay a plain string to keep the unchanged behaviour in criterion 2.
2. Does this project need an approved issue or discussion before this PR? If yes, link it. (There is no profile and no `CONTRIBUTING.md`, so I cannot tell.)
3. Is it acceptable that tokens issued before the deploy stop working (one forced re-login)?
4. Should `refresh` re-check that the user still exists?
5. Base: no `origin/HEAD` resolves. Is local `main` the right base?

**Gate**
- This is the point where the dev answers. No `dev answers:` lines were supplied for this run, so there is nothing to continue from, and I stop here.
- Question to the dev: Approve this plan? Approve, or tell me what to change. Also answer open questions 1 to 5 above, especially question 1 (the `login` return shape) and question 2 (prior approval).
- Because the plan was not approved, nothing was recorded in the evidence log (Step 8 only runs after approval) and no files, branches or commits were changed.
