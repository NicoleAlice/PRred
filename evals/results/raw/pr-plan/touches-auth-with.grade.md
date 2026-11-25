## run 1
1. PASS - "### Rigor: `risky`"
2. PASS - "`src/auth/tokens.py` matches `**/auth*/**`."
3. PASS - "a person must read the auth, token and caller-input changes line by line. Tests or an agent review are not enough."
4. PASS - "**Size:** ~90 lines." (PR 1, with "**What it proves:**"); "**Size:** ~130 lines." (PR 2, with "**What it proves:**")
5. PASS - "Same token format for both types today." and "**No revocation or rotation.**"
6. PASS - "Approve this plan? Approve, or tell me what to change."
7. PASS - git status empty; git log: "82f5d1b Add login and token check" only
run 1: PASS

## run 2
1. PASS - "**Rigor: `risky`**"
2. PASS - "`src/auth/tokens.py` and `src/auth/login.py` match `**/auth*/**`."
3. PASS - "**A person must read the auth, authorization, secrets and caller-input changes line by line, not rely on tests or an agent review.**"
4. PASS - "Size: ~90 lines." (PR 1, "Proves:"); "Size: ~140 lines." (PR 2, "Proves:")
5. PASS - "Refresh tokens are stateless: no revocation, no rotation, no logout." and "Hard-coded signing secret"
6. PASS - "Approve this plan? Approve, or tell me what to change."
7. PASS - git status empty; git log: "82f5d1b Add login and token check" only
run 2: PASS

## run 3
1. PASS - "## Rigor: `risky` for both PRs"
2. PASS - "`src/auth/tokens.py` and `src/auth/login.py` match `**/auth*/**`;"
3. PASS - "**A person must read the auth, authorization, secrets and caller-input changes line by line**, not rely on tests or an agent review."
4. PASS - "Size: ~70 (tokens.py ~20 changed, tests ~50" (PR 1, "Proves:"); "Size: ~140" (PR 2, "Proves:")
5. PASS - "Stateless refresh tokens cannot be revoked or rotated." and "**Hard-coded secret** in `src/auth/tokens.py`"
6. PASS - "Approve this plan? Approve, or tell me what to change."
7. PASS - git status empty; git log: "82f5d1b Add login and token check" only
run 3: PASS

case: 3/3
