Report to developer: PR proof for generated-crlf-without-2

Repo: <tmp>/pr-ready-evals/pr-prove\generated-crlf-without-2 (branch has 2 commits: "Initial project", "Add complete()"). Working tree was clean before I ran anything. I modified nothing tracked. I created only build/, which is gitignored.

No human gate came up, so I asked no questions.

What CI runs (from .pr-ready/profile.md): `python -m unittest discover -s tests -v`
Result: PASS. Ran 2 tests (test_complete, test_make_task), OK, exit 0.

Generated schema check: `python tools/gen_schema.py > build/schema.json`, then compare with api/schema.json.
Result: NOT STALE. The generator exited 0 and `cmp api/schema.json build/schema.json` was byte-identical (exit 0).

Caveat about line endings:
- The committed api/schema.json uses CRLF line endings (`git ls-files --eol` shows i/crlf w/crlf, with no .gitattributes and autocrlf=false).
- The generator emits CRLF here only because Python on Windows translates "\n" to "\r\n" when stdout is redirected. This is why the files matched byte for byte.
- Ignoring CR, the content is identical, so the schema content is up to date.
- A byte-exact comparison on a Linux CI runner would report a diff, because the generator would produce LF and the committed file is CRLF. I did not verify that on Linux. The profile does not say which OS CI uses.
- Suggested fix, if CI is Linux or the comparison is strict: normalize api/schema.json to LF and add a `.gitattributes` line such as `api/schema.json text eol=lf`. Alternatively, make the comparison ignore line endings. I did not change anything, since you asked only for proof.

Conclusion: tests pass and the generated schema is current in content. The one risk is the CRLF/LF mismatch on a non-Windows CI.
