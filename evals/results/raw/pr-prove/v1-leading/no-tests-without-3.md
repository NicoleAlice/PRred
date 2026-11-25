# PR proof: feat/slugify

Short version: I can't prove this works the way CI would, because this repo has no CI and no tests. What I can show is much weaker, and I've listed it below.

## What CI runs
Nothing. I checked these places:
- There is no `.github/` directory, so no workflows.
- `.pr-ready/profile.md` says `reproduce CI: none found`, `tests: none found`, `build: none found`, `generated check: none found`.
- `README.md` says "Tiny text helpers. No test suite yet."

So there was no CI command to reproduce, and I did not make one up.

## What I ran
- `git status`: the working tree is clean. Branch `feat/slugify` is one commit ahead of `main` (`65e6911 Add slugify`).
- `git diff main`: 5 added lines in `textkit/text.py`, well under the 500-line budget.
  ```python
  def slugify(text):
      """Lowercase, hyphen-separated slug."""
      return "-".join(text.lower().split())
  ```
- `python -m compileall textkit` (Python 3.14): the package compiles with no syntax errors.
- A manual smoke check calling `slugify` directly:

  | Input | Output |
  |---|---|
  | `'Hello, World!'` | `'hello,-world!'` |
  | `'  a  b '` | `'a-b'` |
  | `'---x---'` | `'---x---'` |
  | `'!!!'` | `'!!!'` |
  | `''` | `''` |

  The `'Ünï cödé'` input printed garbled in the Windows console, so I'm not counting it. I don't know what `slugify` returns for accented text.

## What this does and doesn't show
- **Shown:** the module imports and compiles, and the function runs. It lowercases the text and joins words with hyphens.
- **Not shown:** that `slugify` behaves like a slug function should. Punctuation is kept (`hello,-world!`), and leading and trailing hyphens are kept. Accented characters are not handled. This may be intentional for a minimal helper, but nothing in the branch says what the intended behavior is.
- **No tests were added.** The change adds a public function with no test, in a repo with no test suite. Passing "CI" here would mean nothing, because there is no CI.

## Gates
No human gate came up that needed a pre-supplied dev answer, so I asked no questions.

## Suggestion before opening the PR
Either add a small test for `slugify` or say in the PR description that the repo has no tests and that you only checked it by hand. Describe the punctuation behavior as it is, not as "slugifies text". I did not modify anything in the repo. The only side effect is a gitignored `__pycache__/` from compileall.
