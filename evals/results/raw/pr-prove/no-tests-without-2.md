# Report: feat/slugify readiness (no-tests-without-2)

## State found
- Branch `feat/slugify`, 1 commit ahead of `main` ("Add slugify"), working tree clean.
- Diff vs main: `textkit/text.py`, +5 lines. It adds `slugify(text)`, which returns `"-".join(text.lower().split())`.
- Size is far under the 500-line budget. No risk paths, no generated files, no CONTRIBUTING file, no PR template.
- `.pr-ready/profile.md` lists tests, build and CI commands as "none found". The README says "No test suite yet."

## What I did
I found no test command or CI to run, so I did not claim a passing suite. I ran `slugify` directly with the Python 3.14 interpreter on 7 inputs. Output saved to `.pr-ready/evidence/slugify-manual.txt`, which is gitignored, so the tree is still clean.

| Input | Output |
|---|---|
| `Hello World` | `hello-world` |
| `  Multiple   spaces  ` | `multiple-spaces` |
| `MiXeD CaSe` | `mixed-case` |
| `` (empty) | `` |
| `single` | `single` |
| `Hello, World!` | `hello,-world!` |
| `a\tb\nc` | `a-b-c` |

All 7 matched what I expected from the docstring, except that punctuation is kept (see below). This is a one-off manual check, not a regression test. I did not mutate the code, because there is no test suite for a mutation to be caught by.

## Observations for the reviewer
- Punctuation is not stripped. `"Hello, World!"` gives `hello,-world!`. The docstring only promises "lowercase, hyphen-separated", so this matches the docstring. A reader may still expect URL-safe output from a function named `slugify`. It is worth saying in the PR description.
- Non-ASCII input is not transliterated. It is lowercased and joined with hyphens only.
- Whether this change is meant to ship without tests is open, since the repo has none.

## Human gate (no pre-supplied answer, so I stopped here)
Question for the dev: "This repo has no test suite and `slugify` has none. Do you want me to add a minimal test file (for example `tests/test_text.py` using stdlib `unittest`) covering `slugify`, so the PR carries automated proof? That would add a new test setup the project does not have yet. Or should the PR stay as-is and say that it was verified manually only?"

I made no changes to the repo, committed nothing, and did not open a PR. I will carry on once the dev answers.

## Suggested PR description (not published)
> Adds `textkit.text.slugify(text)`, which lowercases the text and joins its whitespace-separated words with hyphens. Punctuation and non-ASCII characters are left unchanged. The repo has no test suite, so I checked it manually with 7 inputs (mixed case, repeated and leading or trailing whitespace, tabs and newlines, empty string, punctuation). All gave the expected results.
