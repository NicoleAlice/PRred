# Report: feat/slugify readiness

## Verdict

I can't call this branch "ready for review" on automated evidence, because the project has none. I did check the behavior by hand. It does what the docstring says, with two limits you should know about.

## What the branch changes

`feat/slugify` is one commit (`65e6911 Add slugify`) on top of `main`. It touches one file and adds 5 lines, far under the 500-line budget.

```python
def slugify(text):
    """Lowercase, hyphen-separated slug."""
    return "-".join(text.lower().split())
```

## What I could and couldn't run

- **Tests:** none exist. `.pr-ready/profile.md` says "tests: none found", "build: none found", "reproduce CI: none found", and the README says "No test suite yet." I did not claim a test run, because there is nothing to run.
- **Contribution rules:** none found (no contributing guide, no PR template, no agent rules).
- **Risk paths and generated files:** none.
- **Working tree:** clean.

## Manual check I wrote and ran

I wrote a throwaway script, `.pr-ready/evidence/check_slugify.py`. That folder is gitignored, so I added nothing to the branch or the diff. I ran it with Python 3.14.

7 of 9 cases passed:
- `"Hello World"` gives `hello-world`.
- `"  Many   spaces here "` gives `many-spaces-here`.
- `"ALLCAPS"` gives `allcaps`.
- `""` and `"   "` both give `""`.
- Tabs and newlines become a single hyphen.
- `"Already-hyphenated Word"` gives `already-hyphenated-word`.

2 cases failed. Both go beyond what the docstring promises:
- `"Hello, World!"` gives `hello,-world!`. Punctuation is kept.
- `"Café Münster"` gives `café-münster`. Accents are kept. I expected `cafe-munster`.

I also checked that the script catches regressions. I changed the joiner from `-` to `_` and, separately, removed `.lower()`. The script failed both times. I restored the file afterwards, and `git status` is clean.

## Points for you to decide

1. **Punctuation and accents.** The docstring only says "lowercase, hyphen-separated", and the code matches that. A reviewer might expect a slug to be URL-safe, though. If so, strip punctuation and normalize accents before this ships. If not, a docstring note such as "whitespace only; punctuation and accents are kept" would stop anyone assuming more than it does.
2. **No tests.** I did not add a test suite, since the project has none and starting one is your call. I'd suggest adding a small `tests/test_text.py` covering the cases above. Tell me if you want it.
3. **PR description.** There is no PR template. `ai_description` and `ai_disclosure` are "unclear" in the profile, meaning no policy statement was found. If you disclose AI help, say so in the PR text.

No human gate came up that needed a pre-supplied answer, and I made no commits.
